import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv, os, threading

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
        self.management_button = ttk.Button(main_frame, text="管理模式", command=self.management_mode)

        # 将按钮放置在中间
        self.management_button.grid(row=2, column=0, padx=50, pady=20, sticky='ew')

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

    def management_mode(self):
        # 进入管理模式的逻辑实现
        login_window = tk.Toplevel(self)  # 创建一个新的窗口
        login_window.title("管理员登录")

        # 窗口居中设置
        window_width = 300
        window_height = 200
        screen_width = login_window.winfo_screenwidth()
        screen_height = login_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        login_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 确保登录窗口获得焦点
        login_window.focus_force()

        # 创建标签和输入框
        ttk.Label(login_window, text="用户名:").pack(pady=5)
        username_entry = ttk.Entry(login_window)
        username_entry.pack(pady=5)

        ttk.Label(login_window, text="密码:").pack(pady=5)
        password_entry = ttk.Entry(login_window, show="*")
        password_entry.pack(pady=5)

        attempts = 0  # 尝试次数计数

        def verify_credentials():
            nonlocal attempts  # 使用外部变量
            username = username_entry.get()
            password = password_entry.get()

            # 读取admininfo.csv文件
            try:
                with open('admininfo.csv', 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        admin_username, admin_password = line.strip().split(',')
                        if username == admin_username and password == admin_password:
                            # 登录成功后的操作
                            messagebox.showinfo("登录成功", "您已经成功登录")  # 弹出提示窗口
                            login_window.destroy()  # 关闭登录窗口
                        
                            # 使用多线程启动服务端程序
                            def start_server():
                                os.system("python ShowCustomerStatus.pyw")
                        
                            server_thread = threading.Thread(target=start_server)
                            server_thread.start()
                        
                            self.show_function_selection()  # 弹出功能选择窗口
                            return

                    attempts += 1
                    if attempts >= 3:
                        messagebox.showwarning("警告", "密码错误次数过多，自动退出")  # 错误次数达到上限
                        login_window.destroy()  # 关闭窗口
                    else:
                        messagebox.showwarning("登录失败", f"用户名或密码错误，您还有 {3 - attempts} 次机会")  # 弹出警告窗口
                        username_entry.delete(0, tk.END)  # 清空用户名输入框
                        password_entry.delete(0, tk.END)  # 清空密码输入框
                        messagebox.showinfo("提示", "请重新输入用户名和密码")  # 弹出提示窗口
                        login_window.lift()  # 将窗口提到前面
                        username_entry.focus()  # 聚焦到用户名输入框

            except FileNotFoundError:
                print("admininfo.csv文件未找到")  # 处理文件未找到的情况
                login_window.destroy()

        # 创建确认和退出按钮并左右放置
        button_frame = ttk.Frame(login_window)
        button_frame.pack(pady=10)

        confirm_button = ttk.Button(button_frame, text="确认", command=verify_credentials)
        confirm_button.pack(side=tk.LEFT, padx=(0, 10))  # 左侧对齐，右侧留空

        exit_button = ttk.Button(button_frame, text="退出", command=login_window.destroy)
        exit_button.pack(side=tk.LEFT)  # 左侧对齐

        # 绑定回车键和Esc键
        login_window.bind('<Return>', lambda event: verify_credentials())
        login_window.bind('<Escape>', lambda event: login_window.destroy())

    def show_function_selection(self):
        # 功能选择窗口
        self.function_window = tk.Toplevel(self)
        self.function_window.title("功能选择")

        # 窗口大小
        window_width = 300
        window_height = 200

        # 获取屏幕宽度的一半
        screen_width = self.function_window.winfo_screenwidth() // 2

        # 计算窗口左上角的x和y坐标，使窗口在左半个屏幕水平垂直居中
        x = (screen_width - window_width) // 2
        y = (self.function_window.winfo_screenheight() - window_height) // 2

        self.function_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 创建一个框架以居中按钮
        button_frame = tk.Frame(self.function_window)
        button_frame.pack(expand=True)

        # 创建功能按钮
        edit_menu_button = ttk.Button(button_frame, text="编辑菜单", command=self.edit_menu, style='TButton')
        edit_menu_button.pack(pady=10)

        # 新增编辑管理员信息按钮
        edit_admin_info_button = ttk.Button(button_frame, text="编辑管理员信息", command=self.edit_admin_info, style='TButton')
        edit_admin_info_button.pack(pady=10)

        income_expense_button = ttk.Button(button_frame, text="收入明细", command=self.show_profit, style='TButton')
        income_expense_button.pack(pady=10)

        set_chef_number_button = ttk.Button(button_frame, text="设置厨师数", command=self.set_chef_number, style='TButton')
        set_chef_number_button.pack(pady=10)
    def edit_menu(self):
        # 关闭功能选择窗口
        self.function_window.destroy()

        # 创建编辑窗口
        edit_window = tk.Toplevel(self)
        edit_window.title("编辑菜单")

        edit_window.focus_force()
        
        # 窗口居中设置
        window_width = 600
        window_height = 400
        screen_width = edit_window.winfo_screenwidth()
        screen_height = edit_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        edit_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 创建样式并设置Treeview的背景颜色
        style = ttk.Style()
        style.configure("Custom.Treeview", background="#faff72", foreground="black")
        style.map("Custom.Treeview", background=[('selected', '#ff8936')])  # 选中时的背景色
        
        # 创建Treeview表格
        columns = ("菜名", "售价/元", "成本/元", "制作时长/min")
        tree = ttk.Treeview(edit_window, columns=columns, show='headings', style="Custom.Treeview")
        tree.pack(expand=True, fill='both', side=tk.TOP)
        
        # 设置列标题和宽度
        tree.heading("菜名", text="菜名")
        tree.heading("售价/元", text="售价/元")
        tree.heading("成本/元", text="成本/元")
        tree.heading("制作时长/min", text="制作时长/min")
        
        # 设置列宽和对齐方式
        for col in columns:
            tree.column(col, anchor="center")  # 设置列的对齐方式为居中
        tree.column("菜名", width=150)
        tree.column("售价/元", width=100)
        tree.column("成本/元", width=100)
        tree.column("制作时长/min", width=100)
    
        # 加载数据
        def load_data():
            try:
                with open('Dishes.csv', newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        tree.insert('', 'end', values=row)
            except FileNotFoundError:
                messagebox.showwarning("警告", "Dishes.csv 文件未找到")
    
        load_data()

        # 保存数据到 Dishes.csv
        def save_data():
            try:
                with open('Dishes.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    for child in tree.get_children():
                        writer.writerow(tree.item(child, 'values'))  # 写入每一行的值
            except Exception as e:
                messagebox.showwarning("警告", f"保存信息时出错: {e}")
        
        # 删除选中行的函数
        def delete_selected_row():
            selected_item = tree.selection()  # 获取选中行
            if selected_item:
                for item in selected_item:
                    tree.delete(item)  # 删除选中的行
                save_data()  # 删除后保存数据
        
        # 新增空白行的函数
        def add_blank_row():
            tree.insert('', 'end', values=("", "", "", ""))  # 插入一行空白行
            save_data()  # 删除后保存数据
        
        # 创建按钮框架，设置在Treeview的下方并上下居中
        button_frame = ttk.Frame(edit_window)
        button_frame.pack(side=tk.TOP, pady=10)
        
        # 创建新增按钮
        add_button = ttk.Button(button_frame, text="新增", command=add_blank_row)
        add_button.pack(side=tk.LEFT, padx=5)  # 左侧对齐，右侧留空
        
        # 创建删除按钮
        delete_button = ttk.Button(button_frame, text="删除", command=delete_selected_row)
        delete_button.pack(side=tk.LEFT, padx=5)  # 左侧对齐，右侧留空
        
        # 创建退出按钮
        exit_button = ttk.Button(button_frame, text="退出编辑", command=lambda: self.exit_edit(edit_window))
        exit_button.pack(side=tk.LEFT, padx=5)  # 左侧对齐，右侧留空
    
        # 搜索框和确认按钮
        search_frame = ttk.Frame(edit_window)
        search_frame.pack(side=tk.BOTTOM, fill='x', pady=10)
        
        ttk.Label(search_frame, text="请输入菜名搜索:").pack(side=tk.LEFT, padx=(0, 5))
        search_entry = ttk.Entry(search_frame)
        search_entry.pack(side=tk.LEFT, expand=True, fill='x', padx=(0, 5))

        #绑定Insert键到新增按钮
        edit_window.bind('<Insert>', lambda event: add_button.invoke())
        
        # 绑定Delete键到删除按钮
        edit_window.bind('<Delete>', lambda event: delete_button.invoke())

        # 绑定Esc键到退出按钮
        # edit_window.bind('<Escape>', lambda event: exit_button.invoke())
        
        def show_search_result():
            dish_name = search_entry.get()
            items = tree.get_children()  # 获取所有行
            found_items = []  # 用于存储找到的菜品信息
            for item in items:
                values = tree.item(item, 'values')
                # 检查搜索的菜名是否在当前行的菜名中
                if (dish_name in values[0]) and (dish_name != ""):  # values[0] 是菜名
                    found_items.append(values)
            
            # 确认是否找到匹配的菜品
            if found_items:
                # 将搜索结果写入SearchDishes.csv
                try:
                    with open('SearchDishes.csv', 'w', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(["菜名", "售价/元", "成本/元", "制作时长/min"])  # 写入表头
                        writer.writerows(found_items)  # 写入找到的菜品信息
                except Exception as e:
                    messagebox.showwarning("警告", f"写入SearchDishes.csv时出错: {e}")
            
                # 创建新窗口以显示搜索结果
                result_window = tk.Toplevel(self)
                result_window.title("搜索结果")
            
                # 窗口居中设置
                window_width = 600
                window_height = 400
                screen_width = result_window.winfo_screenwidth()
                screen_height = result_window.winfo_screenheight()
                x = (screen_width - window_width) // 2
                y = (screen_height - window_height) // 2
                result_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            
                # 创建Treeview表格显示搜索结果
                search_columns = ("菜名", "售价/元", "成本/元", "制作时长/min")
                result_tree = ttk.Treeview(result_window, columns=search_columns, show='headings')
                result_tree.pack(expand=True, fill='both', side=tk.TOP)
            
                # 设置列标题和宽度
                for col in search_columns:
                    result_tree.heading(col, text=col)
                    result_tree.column(col, anchor="center", width=150)  # 设置列的宽度和对齐方式
                    
                # 插入找到的菜品信息到表格中
                for row in found_items:
                    result_tree.insert('', 'end', values=row)
            
                # 创建新搜索框和确认按钮
                search_frame = ttk.Frame(result_window)
                search_frame.pack(side=tk.BOTTOM, fill='x', pady=10)
            
                ttk.Label(search_frame, text="请输入菜名搜索:").pack(side=tk.LEFT, padx=(0, 5))
                new_search_entry = ttk.Entry(search_frame)
                new_search_entry.insert(0, dish_name)  # 将之前的搜索菜名填入新的搜索框
                new_search_entry.pack(side=tk.LEFT, expand=True, fill='x', padx=(0, 5))
            
                def new_show_search_result():
                    new_dish_name = new_search_entry.get()
                    new_found_items = []  # 用于存储新搜索的匹配项
                    for item in items:
                        values = tree.item(item, 'values')
                        if (new_dish_name in values[0]) and (new_dish_name != ""):
                            new_found_items.append(values)
            
                    # 清理结果树
                    for i in result_tree.get_children():
                        result_tree.delete(i)
            
                    if new_found_items:
                        for row in new_found_items:
                            result_tree.insert('', 'end', values=row)
                    else:
                        messagebox.showinfo("搜索结果", "未找到匹配的菜品")
            
                confirm_button = ttk.Button(search_frame, text="确认", command=new_show_search_result)
                confirm_button.pack(side=tk.LEFT)
            
            else:
                messagebox.showinfo("搜索结果", "未找到匹配的菜品")
        
            search_entry.delete(0, tk.END)  # 清空文本框
            edit_window.lift()  # 保持编辑窗口在最上面
            self.focus_set()  # 聚焦回功能选择窗口
            edit_window.focus_force()  # 强制编辑窗口获得焦点



            
        confirm_button = ttk.Button(search_frame, text="确认", command=show_search_result)
        confirm_button.pack(side=tk.LEFT)

        # 绑定回车键到确认按钮
        # edit_window.bind('<Return>', lambda event: confirm_button.invoke())
    
        # 绑定双击事件编辑单元格
        def edit_cell(event):
            item = tree.focus()
            column = tree.identify_column(event.x)
            col_index = int(column.replace('#', '')) - 1
            old_value = tree.item(item, 'values')[col_index]
            entry = ttk.Entry(edit_window)
            entry.insert(0, old_value)
            entry.bind('<Return>', lambda e: save_edit(item, col_index, entry.get()))
            entry.bind('<Escape>', lambda e: entry.destroy())
            entry.place(x=event.x, y=event.y)
            entry.focus_set()
        
            def save_edit(item, col_index, new_value):
                tree.item(item, values=[*tree.item(item, 'values')[:col_index], new_value, *tree.item(item, 'values')[col_index + 1:]])
                with open('Dishes.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    for child in tree.get_children():
                        writer.writerow(tree.item(child, 'values'))
                entry.destroy()
    
        tree.bind('<Double-1>', edit_cell)
    def exit_edit(self, edit_window):
        edit_window.destroy()  # 关闭编辑窗口
        self.show_function_selection()  # 重新显示功能选择窗口

    def edit_admin_info(self):
        # 关闭功能选择窗口
        self.function_window.destroy()

        # 创建编辑管理员信息窗口
        edit_admin_window = tk.Toplevel(self)
        edit_admin_window.title("编辑管理员信息")

        edit_admin_window.focus_force()

        # 窗口居中设置
        window_width = 400
        window_height = 300
        screen_width = edit_admin_window.winfo_screenwidth()
        screen_height = edit_admin_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        edit_admin_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 创建Treeview表格
        columns = ("用户名", "密码")
        tree = ttk.Treeview(edit_admin_window, columns=columns, show='headings')
        tree.pack(expand=True, fill='both', side=tk.TOP)

        # 设置列标题并自定义样式
        style = ttk.Style()
        style.configure("Custom.Treeview", background="#faff72", foreground="black")
        style.map("Custom.Treeview", background=[('selected', '#ff8936')])  # 选中时的背景色

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")  # 设置列的对齐方式为居中

        tree.configure(style="Custom.Treeview")  # 应用样式

        # 加载管理员信息
        def load_data():
            try:
                with open('admininfo.csv', newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        tree.insert('', 'end', values=row)
            except FileNotFoundError:
                messagebox.showwarning("警告", "admininfo.csv 文件未找到")

        load_data()

        # 新增空白行的函数
        def add_blank_row():
            tree.insert('', 'end', values=("", ""))  # 插入一行空白行

        # 删除选中行的函数
        def delete_selected_row():
            selected_item = tree.selection()  # 获取选中行
            if selected_item:
                for item in selected_item:
                    tree.delete(item)  # 删除选中的行

        # 更新管理员信息的函数
        def save_edit(item, col_index, new_value):
            tree.item(item, values=[*tree.item(item, 'values')[:col_index], new_value, *tree.item(item, 'values')[col_index + 1:]])

            # 更新admininfo.csv文件
            try:
                with open('admininfo.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    for child in tree.get_children():
                        writer.writerow(tree.item(child, 'values'))
            except Exception as e:
                messagebox.showwarning("警告", f"保存信息时出错: {e}")

        # 双击事件编辑单元格
        def edit_cell(event):
            item = tree.focus()
            column = tree.identify_column(event.x)
            col_index = int(column.replace('#', '')) - 1
            old_value = tree.item(item, 'values')[col_index]
            entry = ttk.Entry(edit_admin_window)
            entry.insert(0, old_value)
            entry.bind('<Return>', lambda e: [save_edit(item, col_index, entry.get()), entry.destroy()])  # 确保回车键调用save_edit函数
            entry.bind('<Escape>', lambda e: entry.destroy())
            entry.place(x=event.x, y=event.y)
            entry.focus_set()

        tree.bind('<Double-1>', edit_cell)

        # 创建按钮框架
        button_frame = ttk.Frame(edit_admin_window)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        # 创建新增按钮
        add_button = ttk.Button(button_frame, text="新增", command=add_blank_row)
        add_button.pack(side=tk.LEFT, padx=5)

        # 创建删除按钮
        delete_button = ttk.Button(button_frame, text="删除", command=delete_selected_row)
        delete_button.pack(side=tk.LEFT, padx=5)

        # 创建退出按钮
        exit_button = ttk.Button(button_frame, text="退出", command=lambda: [edit_admin_window.destroy(), self.show_function_selection()])
        exit_button.pack(side=tk.LEFT, padx=5)
    def show_profit(self):
        daily_profit = {}  # 用于存储每日总利润

        try:
            with open('Bills.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()
                current_date = ""
                for line in lines:
                    line = line.strip()
                    if line.startswith("下单时间:"):
                        # 提取日期部分
                        current_date = line.split()[1].split(" ")[0]  # 获取日期
                        if current_date not in daily_profit:
                            daily_profit[current_date] = 0  # 初始化日期的总利润为0
                    elif line.startswith("总利润:"):
                        # 提取利润
                        profit = float(line[5:-1])  # 取出利润并转换为浮点数
                        if current_date:
                            daily_profit[current_date] += profit  # 累加到对应日期的利润

        except FileNotFoundError:
            messagebox.showwarning("警告", "Bills.txt 文件未找到")
            return

        # 将每日利润写入Profit.csv文件
        self.write_profit_to_csv(daily_profit)

        # 绘制利润分析图
        if daily_profit:
            dates = list(daily_profit.keys())
            profits = list(daily_profit.values())

            # 创建新的窗口
            profit_window = tk.Toplevel(self)
            profit_window.title("每日利润分析")

            # 设置窗口大小
            window_width = 900  # 设置宽度
            window_height = 500  # 设置高度
            profit_window.geometry(f"{window_width}x{window_height}")

            # 计算屏幕中心位置
            screen_width = profit_window.winfo_screenwidth()
            screen_height = profit_window.winfo_screenheight()
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            profit_window.geometry(f"{window_width}x{window_height}+{x}+{y}")  # 重新设置窗口位置

            # 创建Figure
            fig = plt.Figure(figsize=(10, 5))
            ax = fig.add_subplot(111)  # 创建一个子图
            ax.plot(dates, profits, marker='o', linestyle='-', color='b')
            ax.set_title("每日利润趋势图", fontproperties='SimHei')  # 使用SimHei字体显示中文
            ax.set_xlabel("日期", fontproperties='SimHei')  # 使用SimHei字体显示中文
            ax.set_ylabel("总利润 (元)", fontproperties='SimHei')  # 使用SimHei字体显示中文

            # 自动格式化x轴日期
            ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: dates[int(x)] if int(x) < len(dates) else ''))
            ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))  # 限制x轴刻度为整数
            ax.grid()

            # 在窗口中展示图形
            canvas = FigureCanvasTkAgg(fig, profit_window)
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            canvas.draw()  # 绘制图形

    def write_profit_to_csv(self, daily_profit):
        try:
            with open('Profit.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["日期", "总利润"])  # 写入表头
                for date, profit in daily_profit.items():
                    writer.writerow([date, profit])  # 写入每一行数据
        except Exception as e:
            messagebox.showwarning("警告", f"写入Profit.csv时出错: {e}")
    def set_chef_number(self):
        # 关闭功能选择窗口
        self.function_window.destroy()
    
        # 创建设置厨师数量的窗口
        chef_number_window = tk.Toplevel(self)
        chef_number_window.title("设置厨师数量")
    
        chef_number_window.focus_force()
    
        # 窗口居中设置
        window_width = 400
        window_height = 300
        screen_width = chef_number_window.winfo_screenwidth()
        screen_height = chef_number_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        chef_number_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
        # 创建Treeview表格
        columns = ("级别", "数量")
        tree = ttk.Treeview(chef_number_window, columns=columns, show='headings')
        tree.pack(expand=True, fill='both')
    
        # 设置列标题并居中对齐
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        # 加载厨师数量数据
        def load_data():
            try:
                with open('Cooks.csv', newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    next(reader)  # 跳过表头
                    for row in reader:
                        tree.insert('', 'end', values=row)
            except FileNotFoundError:
                messagebox.showwarning("警告", "Cooks.csv 文件未找到")
    
        load_data()
    
        # 更新厨师数量
        def save_edit(item, col_index, new_value):
            tree.item(item, values=[*tree.item(item, 'values')[:col_index], new_value, *tree.item(item, 'values')[col_index + 1:]])
    
            # 更新Cooks.csv文件
            try:
                with open('Cooks.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(columns)  # 写入表头
                    for child in tree.get_children():
                        writer.writerow(tree.item(child, 'values'))
            except Exception as e:
                messagebox.showwarning("警告", f"保存信息时出错: {e}")
    
        # 双击事件编辑单元格
        def edit_cell(event):
            item = tree.focus()
            column = tree.identify_column(event.x)
            col_index = int(column.replace('#', '')) - 1
            old_value = tree.item(item, 'values')[col_index]
            entry = ttk.Entry(chef_number_window)
            entry.insert(0, old_value)
            entry.bind('<Return>', lambda e: [save_edit(item, col_index, entry.get()), entry.destroy()])
            entry.bind('<Escape>', lambda e: entry.destroy())
            entry.place(x=event.x, y=event.y)
            entry.focus_set()
    
        tree.bind('<Double-1>', edit_cell)
    
        # 创建退出按钮
        exit_button = ttk.Button(chef_number_window, text="退出", command=lambda: self.exit_edit(chef_number_window))
        exit_button.pack(pady=10)

if __name__ == "__main__":
    app = RestaurantManagementSystem()
    app.mainloop()