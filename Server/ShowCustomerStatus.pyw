from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json, socket, threading, time, csv

class ServerManagementSystem(tk.Tk):
    def __init__(self):
        super().__init__()
    
        self.title("餐厅管理系统V3.0服务器端")
        
        # 获取屏幕宽度和高度
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # 窗口的宽高
        window_width = 750
        window_height = 400

        # 计算右侧屏幕居中的位置
        x = screen_width - window_width // 2 - (screen_width // 4)  # 调整这里的计算方式
        y = (screen_height // 2) - (window_height // 2)

        # 设置窗口大小和位置
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 创建主框架
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill='both')  # 让主框架填充整个可用空间
    
        # 设置样式
        style = ttk.Style()
        style.configure("Treeview", background="#faff72", rowheight=25)
        style.map("Treeview", background=[('selected', '#c9c9c9')])
    
        # 创建Treeview表格
        columns = ("用户", "状态", "订单详情", "预计完成时间", "预计送达时间")
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)  # 设置更大的高度
        self.tree.pack(expand=True, fill='both')  # 使其填充整个主框架
    
        # 设置列标题和宽度
        self.tree.heading("用户", text="用户")
        self.tree.heading("状态", text="状态")
        self.tree.heading("订单详情", text="订单详情")
        self.tree.heading("预计完成时间", text="预计完成时间")
        self.tree.heading("预计送达时间", text="预计送达时间")
    
        self.tree.column("用户", width=100, anchor="center")
        self.tree.column("状态", width=100, anchor="center")
        self.tree.column("订单详情", width=250, anchor="center")
        self.tree.column("预计完成时间", width=150, anchor="center")
        self.tree.column("预计送达时间", width=150, anchor="center")
    
        # 存储用户订单状态
        self.user_orders = {}
    
        # 启动服务器线程
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.daemon = True
        self.server_thread.start()
    
        # 定期更新用户状态
        self.update_user_status()

    def read_dishes_from_csv(file_path = 'Dishes.csv'):
        dishes = []
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                dishes.append(','.join(row))
        return '\n'.join(dishes)
    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server_socket.bind(('113.54.245.16', 9999))
        self.server_socket.bind(('192.168.0.197', 9999))
        self.server_socket.listen(100)

        while True:
            client_socket, addr = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.daemon = True
            client_thread.start()

    def handle_client(self, client_socket):
        try:
            def read_dishes_from_csv(file_path = 'Dishes.csv'):
                dishes = []
                with open(file_path, mode='r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        dishes.append(','.join(row))
                return '\n'.join(dishes)
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                if data.startswith("user:"):
                    user = data.split(":")[1]
                    client_socket.sendall(b"OK")
                    # 更新用户订单状态
                    if user not in self.user_orders.keys():
                        # client_socket.sendall(b"OK")
                        self.user_orders[user] = {
                            "status": "点餐中",
                            "order_details": None,
                            "estimated_finish_time": None,
                            "estimated_delivery_time": None
                        }
                elif data == "menu":
                    dishes = read_dishes_from_csv()
                    client_socket.sendall(dishes.encode('utf-8'))
                elif data == "time":
                    time_list = [datetime.strptime(order["estimated_finish_time"], "%Y-%m-%d %H:%M:%S").timestamp() for order in self.user_orders.values() if order["estimated_finish_time"] is not None]
                    latest_time = max(time_list) if time_list else datetime.now().timestamp()
                    client_socket.sendall(str(latest_time).encode('utf-8'))
                else:
                    order_data = json.loads(data)
                    self.process_order(user, order_data)
        except Exception as e:
            # print(f"处理客户端时出错: {e}")
            messagebox.showerror("错误", f"处理客户端时出错: {e}")
        finally:
            client_socket.close()

    def process_order(self, user, order_data):
        order_id = order_data["order_id"]
        order_time = order_data["order_time"]
        dining_mode = order_data["dining_mode"]
        total_price = order_data["total_price"]
        total_cost = order_data["total_cost"]
        total_profit = order_data["total_profit"]
        estimated_finish_time = order_data["estimated_finish_time"]
        estimated_delivery_time = order_data["estimated_delivery_time"]
        address = order_data.get("address", "堂食")
        order_details = order_data["order_details"]

        # 将订单信息写入文件
        with open('Bills.txt', 'a', encoding='utf-8') as file:
            file.write(f"订单编号: {order_id}\n")
            file.write(f"下单时间: {order_time}\n")
            file.write(f"用户: {user}\n")
            file.write(f"用餐方式: {dining_mode}\n")
            file.write(f"地址: {address}\n")
            for detail in order_details:
                file.write(f"菜名: {detail['dish_name']}, 售价: {detail['price']}元, 数量: {detail['quantity']}\n")
            file.write(f"总价: {total_price}元\n")
            file.write(f"总成本: {total_cost}元\n")
            file.write(f"总利润: {total_profit}元\n")
            file.write("=" * 40 + "\n")

        # 更新用户订单状态
        if self.user_orders[user]["status"] == "点餐中":
            self.user_orders[user] = {
                "status": "已下单",
                "order_details": order_details,
                "estimated_finish_time": estimated_finish_time,
                "estimated_delivery_time": estimated_delivery_time
            }
        else:
            initial_order_details = self.user_orders[user]["order_details"]
            added_order_details = order_details
            initial_numbers = [initial_detail['quantity'] for initial_detail in initial_order_details]
            added_numbers = [added_detail['quantity'] for added_detail in added_order_details]
            modified_numbers = [a + b for a, b in zip(initial_numbers, added_numbers)]
            for i, detail in enumerate(initial_order_details):
                detail['quantity'] = modified_numbers[i]
            order_details = initial_order_details
            self.user_orders[user] = {
                "status": "已下单",
                "order_details": order_details,
                "estimated_finish_time": estimated_finish_time,
                "estimated_delivery_time": estimated_delivery_time
            }

    def update_user_status(self):
        current_time = time.time()
        for user, order in self.user_orders.items():
            estimated_finish_time = order["estimated_finish_time"]
            if estimated_finish_time is None:
                continue
            else:
                estimated_finish_timestamp = datetime.strptime(estimated_finish_time, "%Y-%m-%d %H:%M:%S").timestamp()

            if estimated_finish_timestamp <= current_time:
                order["status"] = "已完成"

        # 更新Treeview表格
        for item in self.tree.get_children():
            self.tree.delete(item)

        for user, order in self.user_orders.items():
            status = order["status"]
            if order["order_details"] is None:
                self.tree.insert('', 'end', values=(user, status, "", "", ""))
                continue
            else:
                order_details = ', '.join([f"{detail['dish_name']} x {detail['quantity']}" for detail in order["order_details"]])
                estimated_finish_time = order["estimated_finish_time"]
                estimated_delivery_time = order["estimated_delivery_time"]
                self.tree.insert('', 'end', values=(user, status, order_details, estimated_finish_time, estimated_delivery_time))

        self.after(1000, self.update_user_status)

if __name__ == "__main__":
    app = ServerManagementSystem()
    app.mainloop()