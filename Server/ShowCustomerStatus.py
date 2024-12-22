from datetime import datetime
import socket
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import time

class ServerManagementSystem(tk.Tk):
    def __init__(self):
        super().__init__()
    
        self.title("餐厅管理系统服务器端")
        
        # 获取屏幕宽高
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # 窗口的宽高
        window_width = 600
        window_height = 400
        
        # 计算居中位置
        x = (screen_width // 2) - (window_width // 2)
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
        columns = ("用户", "状态", "订单详情", "预计完成时间")
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)  # 设置更大的高度
        self.tree.pack(expand=True, fill='both')  # 使其填充整个主框架
    
        # 设置列标题和宽度
        self.tree.heading("用户", text="用户")
        self.tree.heading("状态", text="状态")
        self.tree.heading("订单详情", text="订单详情")
        self.tree.heading("预计完成时间", text="预计完成时间")
    
        self.tree.column("用户", width=100, anchor="center")
        self.tree.column("状态", width=100, anchor="center")
        self.tree.column("订单详情", width=250, anchor="center")
        self.tree.column("预计完成时间", width=150, anchor="center")
    
        # 存储用户订单状态
        self.user_orders = {}
    
        # 启动服务器线程
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.daemon = True
        self.server_thread.start()
    
        # 定期更新用户状态
        self.update_user_status()



    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('127.0.0.1', 9999))
        self.server_socket.listen(100)

        while True:
            client_socket, addr = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.daemon = True
            client_thread.start()

    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                if data.startswith("user:"):
                    user = data.split(":")[1]
                    # 更新用户订单状态
                    self.user_orders[user] = {
                        "status": "点餐中",
                        "order_details": None,
                        "estimated_finish_time": None
                    }

                else:
                    order_data = json.loads(data)
                    self.process_order(user, order_data)
        except Exception as e:
            print(f"处理客户端时出错: {e}")
        finally:
            client_socket.close()

    def process_order(self, user, order_data):
        # user = order_data["user"]
        order_id = order_data["order_id"]
        order_time = order_data["order_time"]
        dining_mode = order_data["dining_mode"]
        total_price = order_data["total_price"]
        total_cost = order_data["total_cost"]
        total_profit = order_data["total_profit"]
        estimated_finish_time = order_data["estimated_finish_time"]
        address = order_data.get("address", "堂食")
        order_details = order_data["order_details"]

        # 将订单信息写入文件
        with open('Server_Bills.txt', 'a', encoding='utf-8') as file:
            file.write(f"{order_id}\n")
            file.write(f"{order_time}\n")
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
        self.user_orders[user] = {
            "status": "已下单",
            "order_details": order_details,
            "estimated_finish_time": estimated_finish_time
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
                self.tree.insert('', 'end', values=(user, status, "", ""))
                continue
            else:
                order_details = ', '.join([f"{detail['dish_name']} x {detail['quantity']}" for detail in order["order_details"]])
                estimated_finish_time = order["estimated_finish_time"]
                self.tree.insert('', 'end', values=(user, status, order_details, estimated_finish_time))

        self.after(1000, self.update_user_status)

if __name__ == "__main__":
    app = ServerManagementSystem()
    app.mainloop()