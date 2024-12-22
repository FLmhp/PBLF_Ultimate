import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime, timedelta
import time, csv, socket, json

from CookManagement import cook_dishes
from Map import get_dist_dura

class RestaurantManagementSystem(tk.Tk):
    def __init__(self):
        super().__init__()

        self.address = "四川省成都市建设北路二段四号"  # 餐厅地址

        self.title("餐厅管理系统V3.0")  # 设置窗口标题
        self.geometry("400x300")  # 设置窗口大小
        self.configure(bg="#fff143")  # 更改主窗口颜色

        # 窗口居中设置
        window_width = 400
        window_height = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")  # 重新设置窗口大小和位置

        # 创建样式并设置主框架的背景颜色
        style = ttk.Style()
        style.configure("MainFrame.TFrame", background="#f2be45")

        # 创建一个主框架
        main_frame = ttk.Frame(self, style="MainFrame.TFrame")
        main_frame.pack(expand=True)

        # 创建数字显示标签，放置在最上方
        self.number_label = ttk.Label(main_frame, font=("Arial", 16), background="#f2be45")
        self.number_label.grid(row=0, column=0, columnspan=2, pady=10)

        # 创建文本框显示“巨献”
        self.title_label = ttk.Label(main_frame, text="巨献", font=("Arial", 24), background="#f2be45")
        self.title_label.grid(row=1, column=0, columnspan=2, pady=10)

        # 创建按钮
        self.order_button = ttk.Button(main_frame, text="用户点餐模式", command=self.order_mode)

        # 修改按钮背景颜色
        self.order_button.configure(style="TButton")

        # 将按钮放置在中间
        self.order_button.grid(row=2, column=0, padx=50, pady=20, sticky='ew')

        # 初始化字符并开始显示
        self.characters = ['马瀚鹏', '李韦成', '宋宇阳', '裴科斌']  # 要显示的字符
        self.current_index = 0  # 当前显示字符的索引
        self.update_character()


    def update_character(self):
        # 显示字符，并自动滚动
        self.number_label.config(text=self.characters[self.current_index])
        self.current_index += 1
        if self.current_index >= len(self.characters):
            self.current_index = 0
        self.after(1000, self.update_character)  # 每隔1000毫秒（1秒）更新一次

    def order_mode(self):
        # 弹出输入窗口
        input_window = tk.Toplevel(self)
        input_window.title("输入服务器信息")
    
        # 设置窗口大小
        input_window.geometry("400x200")
    
        # 窗口居中设置
        window_width = 400
        window_height = 250
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        input_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
        ip_label = ttk.Label(input_window, text="IP地址:")
        ip_label.pack(pady=5)
        
        ip_entry = ttk.Entry(input_window)
        ip_entry.insert(0, "127.0.0.1")  # 设置默认IP地址
        ip_entry.pack(pady=5)
    
        port_label = ttk.Label(input_window, text="端口号:")
        port_label.pack(pady=5)
        
        port_entry = ttk.Entry(input_window)
        port_entry.insert(0, "9999")  # 设置默认端口号
        port_entry.pack(pady=5)
    
        user_label = ttk.Label(input_window, text="用户名:")
        user_label.pack(pady=5)
        
        user_entry = ttk.Entry(input_window)
        user_entry.pack(pady=5)
    
        def confirm_input(event=None):  # 允许绑定回车键
            global IP, PORT, user
            IP = ip_entry.get()
            PORT = port_entry.get()
            user = user_entry.get()
            if not IP or not PORT or not user:
                messagebox.showwarning("警告", "请填写所有信息!")
            else:
                input_window.destroy()
                self.create_order_window()
    
        confirm_button = ttk.Button(input_window, text="确认", command=confirm_input)
        confirm_button.pack(pady=10)
    
        # 绑定回车键进行确认
        input_window.bind('<Return>', confirm_input)


    def create_order_window(self):
        # 建立与服务器的连接
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((IP, int(PORT)))
            self.s.send(f"user:{user}".encode())  # 发送用户名
        except Exception as e:
            messagebox.showerror("错误", f"无法连接到服务器: {e}")
            return

        # 进入用户点餐模式的逻辑实现
        order_window = tk.Toplevel(self)
        order_window.title("用户点餐")

        # 窗口居中设置
        window_width = 900  # 增加宽度
        window_height = 400
        screen_width = order_window.winfo_screenwidth()
        screen_height = order_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        order_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 创建样式并设置Treeview的背景颜色
        style = ttk.Style()
        style.configure("Custom.Treeview", background="#faff72", foreground="black")
        style.map("Custom.Treeview", background=[('selected', '#ff8936')])  # 选中时的背景色

        # 创建Treeview表格
        columns = ("菜名", "售价/元", "制作时长/min", "数量", "总价/元")
        tree = ttk.Treeview(order_window, columns=columns, show='headings', style="Custom.Treeview")
        tree.pack(expand=True, fill='both')

        # 设置列标题和宽度
        tree.heading("菜名", text="菜名")
        tree.heading("售价/元", text="售价/元")
        tree.heading("制作时长/min", text="制作时长/min")
        tree.heading("数量", text="数量")
        tree.heading("总价/元", text="总价/元")

        tree.column("菜名", width=200, anchor="center")  # 菜名列宽度设置
        tree.column("售价/元", width=100, anchor="center")  # 售价列宽度设置
        tree.column("制作时长/min", width=120, anchor="center")  # 制作时长列宽度设置
        tree.column("数量", width=100, anchor="center")  # 数量列宽度设置
        tree.column("总价/元", width=120, anchor="center")  # 总价列宽度设置

        # 加载数据
        def load_data():
            try:
                with open('Dishes.csv', newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        # 初始化数量为0，移除成本
                        tree.insert('', 'end', values=row[:2] + [row[3], 0, 0])  # 将数量初始化为0，单价乘数量为0，忽略成本

            except FileNotFoundError:
                messagebox.showwarning("警告", "Dishes.csv 文件未找到")

        load_data()

        # 创建一个总价行（初始化为0）
        total_price = 0
        total_cook_time = 0
        total_row = tree.insert('', 'end', values=["", "", total_cook_time, "", total_price])

        # 更新总价和总时长的方法
        def update_total_price():
            nonlocal total_price  # 声明总价为非局部变量
            total_price = 0  # 重置总价
            cook_times = []  # 重置总时长

            for item in tree.get_children():
                if item != total_row:  # 忽略总价行
                    values = tree.item(item, 'values')
                    quantity = eval(values[3])  # 获取数量
                    price = eval(values[1])  # 获取售价
                    time = eval(values[2])  # 获取制作时长
                    if isinstance(quantity, int) and isinstance(price, (int, float)):
                        total = quantity * price
                        total_price += total
                        cook_times.extend([time] * quantity)  # 累加总时长
                        # 更新总价列
                        tree.item(item, values=list(values[:3]) + [quantity, total])  # 更新数量和总价

            total_cook_time = cook_dishes(cook_times)  # 调用cook_dishes计算总制作时长
            # 更新总价行
            tree.item(total_row, values=["", "", total_cook_time, "", total_price])  # 更新总价行

        # 创建确认和退出按钮框架
        button_frame = ttk.Frame(order_window)
        button_frame.pack(pady=10)

        confirm_button = ttk.Button(button_frame, text="确认", command=lambda: self.select_dining_mode(order_window, total_price)) 
        confirm_button.pack(side=tk.LEFT, padx=(0, 10))

        exit_button = ttk.Button(button_frame, text="退出", command=order_window.destroy)
        exit_button.pack(side=tk.LEFT)

        # 绑定鼠标滚轮事件以增加或减少数量
        def scroll_quantity(event):
            item = tree.focus()
            if item:
                values = tree.item(item, 'values')
                current_quantity = int(values[3])  # 获取当前数量
                if event.delta > 0:  # 向上滚动，增加数量
                    new_quantity = current_quantity + 1
                else:  # 向下滚动，减少数量
                    new_quantity = current_quantity - 1
                    if new_quantity < 0:  # 限制数量不能小于0
                        new_quantity = 0
                # 更新数量和总价
                tree.item(item, values=list(values[:3]) + [new_quantity, new_quantity * eval(values[1])])  
                update_total_price()  # 更新总价

        tree.bind('<MouseWheel>', scroll_quantity)  # 绑定鼠标滚轮事件

    def select_dining_mode(self, order_window, total_price):
        # 创建选择用餐方式的窗口
        dining_mode_window = tk.Toplevel(self)
        dining_mode_window.title("选择用餐方式")
    
        window_width = 300
        window_height = 200
        screen_width = dining_mode_window.winfo_screenwidth()
        screen_height = dining_mode_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        dining_mode_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
        # 创建一个框架以居中按钮
        button_frame = ttk.Frame(dining_mode_window)
        button_frame.pack(expand=True)  # 使用expand=True以使框架扩大并居中
    
        # 创建按钮选择堂食或外送
        dine_in_button = ttk.Button(button_frame, text="堂食", command=lambda: self.finalize_order("堂食", total_price, order_window, dining_mode_window))
        dine_in_button.pack(pady=10)
    
        takeout_button = ttk.Button(button_frame, text="外送", command=lambda: self.ask_for_address(total_price, order_window, dining_mode_window))
        takeout_button.pack(pady=10)

    def ask_for_address(self, total_price, order_window, dining_mode_window):
        # 创建输入地址的对话框
        address_window = tk.Toplevel(dining_mode_window)
        address_window.title("输入送餐地址")
        address_window.focus_force() # 强制聚焦到地址输入框

        window_width = 300
        window_height = 150
        screen_width = address_window.winfo_screenwidth()
        screen_height = address_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        address_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        ttk.Label(address_window, text="请输入送餐地址:").pack(pady=10)
        address_entry = ttk.Entry(address_window, width=40)
        address_entry.pack(pady=5)

        def confirm_address():
            address = address_entry.get()  # 获取用户输入的地址
            if address:
                self.finalize_order("外送", total_price, order_window, dining_mode_window, address)
                address_window.destroy()  # 关闭地址输入窗口
            else:
                messagebox.showwarning("警告", "地址不能为空！")  # 提示用户输入地址
                address_entry.delete(0, tk.END)  # 清空输入框
                address_entry.focus_set()  # 重新聚焦到输入框

        confirm_button = ttk.Button(address_window, text="确认", command=confirm_address)
        confirm_button.pack(pady=10)

        address_entry.bind('<Return>', lambda e: confirm_address())  # 绑定回车键

    def finalize_order(self, dining_mode, total_price, order_window, dining_mode_window, address=None):
        # 获取每道菜的制作时长，构建cook_times列表
        cook_times = []
        total_row_index = len(order_window.children['!treeview'].get_children()) - 1  # 总价行的索引
    
        # 遍历所有的子项
        order_details = []  # 用于存储订单信息
        total_cost = 0  # 总成本
        total_profit = 0  # 总利润
    
        for index, item in enumerate(order_window.children['!treeview'].get_children()):
            if index == total_row_index:  # 忽略最后一行（总价行）
                continue
            
            values = order_window.children['!treeview'].item(item, 'values')
            dish_name = values[0]  # 菜名
            price = float(values[1])  # 售价（以浮点数表示）
            quantity = int(values[3])  # 数量
            cooking_time = int(values[2])  # 获取制作时长
    
            cost = self.get_cost(dish_name)  # 获取菜品成本
            total_cost += cost * quantity  # 计算总成本
            total_profit += (price - cost) * quantity  # 计算总利润
    
            order_details.append({
                "dish_name": dish_name,
                "price": price,
                "quantity": quantity,
                "cooking_time": cooking_time
            })
    
            cook_times.extend([cooking_time] * quantity)  # 计算每道菜的总制作时长并加入列表
    
        total_cook_time = cook_dishes(cook_times)  # 计算总制作时长
        total_cook_time_dhm = self.convert_to_dhm(total_cook_time)  # 转换为天时分格式
    
        # 生成订单编号和下单时间
        order_id = f"订单编号: {self.generate_order_id()}"
        order_time = f"下单时间: {self.get_current_time()}"
    
        # 预计完成时间
        estimated_finish_time = datetime.now() + timedelta(minutes=total_cook_time)  # 计算预计完成时间
        estimated_finish_time_str = estimated_finish_time.strftime("%Y-%m-%d %H:%M:%S")  # 格式化为字符串
    
        # 将订单信息写入Bill.txt文件
        with open('Bills.txt', 'a', encoding='utf-8') as file:
            file.write(f"{order_id}\n")
            file.write(f"{order_time}\n")
            for detail in order_details:
                file.write(f"菜名: {detail['dish_name']}, 售价: {detail['price']}元, 数量: {detail['quantity']}\n")
            file.write(f"总价: {total_price}元\n")
            file.write(f"总成本: {total_cost}元\n")
            file.write(f"总利润: {total_profit}元\n")  # 写入总利润
            file.write("=" * 40 + "\n")  # 分隔符

        if dining_mode == "外送" and address:
            diliver_time = get_dist_dura(self.address, address)[1] / 60  # 计算配送时间
            diliver_time_str = self.convert_to_dhm(diliver_time)  # 转换为时分秒格式
            estimated_delivery_time = estimated_finish_time + timedelta(minutes=diliver_time)  # 计算预计送达时间
            estimated_delivery_time_str = estimated_delivery_time.strftime("%Y-%m-%d %H:%M:%S")  # 格式化为字符串
    
            messagebox.showinfo("订单确认", 
                f"您选择的用餐方式是: {dining_mode}\n总价: {total_price}元\n"
                f"预计完成时间: {estimated_finish_time_str}\n送餐地址: {address}\n"
                f"预计送达时间: {estimated_delivery_time_str}")
        else:
            messagebox.showinfo("订单确认", 
                f"您选择的用餐方式是: {dining_mode}\n总价: {total_price}元\n"
                f"预计完成时间: {estimated_finish_time_str}")
        
        # 准备发送的数据
        order_data = {
            "order_id": self.generate_order_id(),
            "order_time": self.get_current_time(),
            "dining_mode": dining_mode,
            "total_price": total_price,
            "total_cost": total_cost,
            "total_profit": total_profit,
            "estimated_finish_time": estimated_finish_time_str,
            "address": address if dining_mode == "外送" else None,
            "order_details": order_details
        }
        
        # 将订单数据序列化为JSON格式
        order_json = json.dumps(order_data, ensure_ascii=False)
    
        # 发送订单数据到服务器
        try:
            self.s.send(order_json.encode('utf-8'))
        except Exception as e:
            messagebox.showerror("错误", f"发送订单到服务器时出错: {e}")
    
        dining_mode_window.destroy()
        order_window.destroy()

    def get_cost(self, dish_name):
        # 从Dishes.csv文件中根据菜名获取对应成本
        try:
            with open('Dishes.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[0] == dish_name:  # 假设菜名在第一列，成本在第三列
                        return float(row[2])  # 返回成本，转换为浮点数
        except FileNotFoundError:
            messagebox.showwarning("警告", "Dishes.csv 文件未找到")
        return 0  # 如果未找到成本，返回0

    def generate_order_id(self):
        # 生成简单的订单编号逻辑，使用时间戳
        return str(int(time.time()))  # 使用当前时间作为简单的订单编号

    def get_current_time(self):
        # 获取当前时间
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def convert_to_dhm(self, minutes):
        # 计算总天数
        days = int(minutes // 1440)
        # 计算小时数
        hours = int((minutes % 1440) // 60)
        # 计算剩余分钟数
        remaining_minutes = int(minutes % 60)

        # 构建输出字符串
        parts = []
        if days > 0:
            parts.append(f"{days}天")
        if hours > 0:
            parts.append(f"{hours}小时")
        if remaining_minutes > 0:
            parts.append(f"{remaining_minutes}分钟")

        return ' '.join(parts) if parts else "0分钟"  # 如果所有部分为0时显示"0分钟"

if __name__ == "__main__":
    app = RestaurantManagementSystem()
    app.mainloop()