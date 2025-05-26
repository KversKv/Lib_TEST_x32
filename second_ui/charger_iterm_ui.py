import tkinter as tk
from tkinter import ttk
from ins import ins_n6705c
from tkinter import Menu, Text
from tkinter import messagebox
import time
import devicei2c
import csv

class CHARGER_ITERM_UI:
    def __init__(self, content_frame, controller):
        self.content_frame = content_frame
        # self.controller = controller
        self.controller = ins_n6705c.PowerSupplyController(self)  # 将self作为UI的引用传递

    def create_iterm_module(self):
        ttk.Label(self.content_frame, text="Iterm Test", font=("Arial", 20)).pack(pady=20)
        ttk.Label(self.content_frame, text="This is the Iterm current Test module.").pack(pady=10)

        # 仪器选择框架
        frame_instr = ttk.LabelFrame(self.content_frame, text="Instrument Selection", padding="10")
        # frame_instr.pack(side="left", padx=10, pady=10)(padx=10, pady=10, fill="both")
        frame_instr.pack(padx=10, pady=10, fill="both")

        self.instr_label = ttk.Label(frame_instr, text="Select Instrument:")
        self.instr_label.pack(side="left", padx=5, pady=5)

        self.instr_list = self.controller.rm.list_resources()  # 获取所有可用的VISA资源
        self.instr_var = tk.StringVar(self.content_frame)
        self.instr_var.set(self.instr_list[0] if self.instr_list else "No instruments found")
        self.instr_menu = ttk.OptionMenu(frame_instr, self.instr_var, self.instr_list[0], *self.instr_list)
        self.instr_menu.pack(side="left", padx=5, pady=5)

        self.status_label = ttk.Label(frame_instr, text="Status: Disconnected", foreground="red")
        self.status_label.pack(side="left", padx=5, pady=5)

        self.connect_button = ttk.Button(frame_instr, text="Connect", command=self.connect)
        self.connect_button.pack(side="left", padx=5, pady=5)
        self.disconnect_button = ttk.Button(frame_instr, text="Disconnect", command=self.disconnect)
        self.disconnect_button.pack(side="left", padx=5, pady=5)

        ttk.Button(frame_instr, text="Help", command=self.help_vbit).pack(
            pady=10)

        # 通道选择框架
        frame_channel = ttk.LabelFrame(self.content_frame, text="Channel Selection", padding="10")
        frame_channel.pack(padx=10, pady=10, fill="both")
        self.channel_label = ttk.Label(frame_channel, text="Select Vbat Channel:")
        self.channel_label.pack(side="left", padx=5, pady=5)
        self.channel_var = tk.StringVar(self.content_frame)
        self.channel_var.set("CH1")  # 默认通道为CH1
        self.channel_menu = ttk.OptionMenu(frame_channel, self.channel_var, "CH1", "CH1", "CH2", "CH3", "CH4")
        self.channel_menu.pack(side="left", padx=5, pady=5)
        self.channel_on_button = ttk.Button(frame_channel, text="SET", command=self.set_voltagemode)
        self.channel_on_button.pack(side="left", padx=5, pady=5)

        frame_vbit_config = ttk.LabelFrame(self.content_frame, text="Test Config", padding="10")
        frame_vbit_config.pack(padx=10, pady=10, fill="both")
        self.iic_weight = tk.StringVar()
        self.device_addr_var = tk.StringVar()
        self.reg_addr_var = tk.StringVar()
        self.lsb_var = tk.StringVar()
        self.msb_var = tk.StringVar()
        self.max_value_var = tk.StringVar()
        self.min_value_var = tk.StringVar()


        ttk.Label(frame_vbit_config, text="IIC weight", anchor="w").grid(row=0, column=0, pady=5)
        self.iic_weight.set("8")  # 默认通道为CH1
        ttk.Entry(frame_vbit_config, textvariable=self.iic_weight).grid(row=0, column=1, pady=5)
        # ttk.Combobox(input_frame, values=["8", "10"]).grid(row=1, column=1, pady=5)

        ttk.Label(frame_vbit_config, text="Device Addr(x)", anchor="w").grid(row=0, column=2, pady=5)
        self.device_addr_var.set("1A")  # 默认通道为CH1
        ttk.Entry(frame_vbit_config, textvariable=self.device_addr_var).grid(row=0, column=3, pady=5)

        ttk.Label(frame_vbit_config, text="Reg Addr(x)", anchor="w").grid(row=0, column=4, pady=5)
        self.reg_addr_var.set("5")  # 默认通道为CH1
        ttk.Entry(frame_vbit_config, textvariable=self.reg_addr_var).grid(row=0, column=5, pady=5)

        ttk.Label(frame_vbit_config, text="LSB", anchor="w").grid(row=1, column=0, pady=5)
        self.lsb_var.set("1")  # 默认通道为CH1
        ttk.Entry(frame_vbit_config, textvariable=self.lsb_var).grid(row=1, column=1, pady=5)

        ttk.Label(frame_vbit_config, text="MSB", anchor="w").grid(row=1, column=2, pady=5)
        self.msb_var.set("1")  # 默认通道为CH1
        ttk.Entry(frame_vbit_config, textvariable=self.msb_var).grid(row=1, column=3, pady=5)

        ttk.Label(frame_vbit_config, text="Min value", anchor="w").grid(row=2, column=0, pady=5)
        ttk.Entry(frame_vbit_config, textvariable=self.min_value_var).grid(row=2, column=1, pady=5)

        ttk.Label(frame_vbit_config, text="Max value", anchor="w").grid(row=2, column=2, pady=5)
        ttk.Entry(frame_vbit_config, textvariable=self.max_value_var).grid(row=2, column=3, pady=5)

        ttk.Button(frame_vbit_config, text="Start", command=self.run_iterm_test).grid(row=3, columnspan=2, pady=10)

        ttk.Button(self.content_frame, text="Check IIC Reg ADDR Weight", command=self.check_iic_weight).pack(
            side="left", pady=10)

        ttk.Button(self.content_frame, text="Run Test", command=self.run_test).pack(pady=10)

        # 创建输入区域
        input_frame = ttk.Frame(self.content_frame)
        input_frame.pack(pady=10)

        # 创建结果区域
        ttk.Label(self.content_frame, text="Test Result:").pack()
        self.test_result_text = Text(self.content_frame, height=15, width=50)
        self.test_result_text.pack()

    def connect(self):
        resource_name = self.instr_var.get()
        # print(resource_name)
        self.controller.connect(resource_name)

    def disconnect(self):
        self.controller.disconnect()
    #
    # def set_voltage(self):
    #     voltage = self.voltage_entry.get()
    #     channel = self.channel_var.get()[-1]
    #     self.controller.set_voltage(channel, voltage)
    #
    # def set_current_limit(self):
    #     current = self.current_entry.get()
    #     channel = self.channel_var.get()[-1]
    #     self.controller.set_current_limit(channel, current)

    def channel_on(self):
        channel = self.channel_var.get()[-1]
        self.controller.channel_on(channel)

    def channel_off(self):
        channel = self.channel_var.get()[-1]
        self.controller.channel_off(channel)

    def set_voltagemode(self):
        channel = self.channel_var.get()[-1]
        self.controller.set_voltagemode(channel)

    def update_values(self):
        channel = self.channel_var.get()[-1]
        self.controller.set_channel_range(channel)
        self.controller.update_values(channel)

    def update_status(self, status, color):
        self.status_label.config(text=f"Status: {status}", foreground=color)

    def remove_before_6_lines(self, input_filename='example.csv', output_filename='output.csv'):
        # 打开输入文件和输出文件
        with open(input_filename, 'r', newline='') as infile, open(output_filename, 'w', newline='') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            # 跳过前三行
            next(reader, None)  # 跳过第一行
            next(reader, None)  # 跳过第二行
            next(reader, None)  # 跳过第三行
            next(reader, None)  # 跳过第三行
            next(reader, None)  # 跳过第三行
            next(reader, None)  # 跳过第6行

            # 写入剩余的行到输出文件
            for row in reader:
                writer.writerow(row)

    def find_cutoff_by_sign_change(self,
                                   csv_file_path,
                                   time_col='Time_a',
                                   current_col='Active Instrument A Channel 2 Current Avg',
                                   voltage_col='Active Instrument A Channel 2 Voltage Avg',
                                   pre_cutoff_duration=5):
        """
        从CSV中读取数据(不使用pandas)，通过检测电流从负到正的符号变化
        来确定截止电流时间点，并在该点前 pre_cutoff_duration 秒内
        计算平均电流和平均电压。

        :param csv_file_path: CSV 文件路径
        :param time_col: 时间列的列名
        :param current_col: 电流列的列名
        :param voltage_col: 电压列的列名
        :param pre_cutoff_duration: 截止点前的时间窗口(单位: 秒)
        :return: (t_cutoff, avg_i, avg_v)
        """

        time_data = []
        current_data = []
        voltage_data = []

        # 1. 读取 CSV 文件
        with open(csv_file_path, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 将字符串转换为浮点数
                t = float(row[time_col])
                i = float(row[current_col])
                v = float(row[voltage_col])

                time_data.append(t)
                current_data.append(i)
                voltage_data.append(v)

        # 2. 按时间升序排序
        combined = sorted(zip(time_data, current_data, voltage_data), key=lambda x: x[0])

        # 3. 寻找电流由负值变为 >= 0 的点
        cutoff_index = None
        for idx in range(1, len(combined)):
            prev_i = combined[idx - 1][1]
            curr_i = combined[idx][1]
            if prev_i < 0 and curr_i >= 0:
                cutoff_index = idx
                break

        if cutoff_index is None:
            raise ValueError("未找到电流从负变正的时间点，请检查数据或调整逻辑。")

        t_cutoff = combined[cutoff_index][0]  # 截止时间

        # 4. 在 [t_cutoff - pre_cutoff_duration, t_cutoff] 区间计算平均电流、电压
        t_start = t_cutoff - pre_cutoff_duration
        window_i = []
        window_v = []

        for (t, i, v) in combined:
            if t >= t_start and t <= t_cutoff:
                window_i.append(i)
                window_v.append(v)

        if not window_i:
            raise ValueError("在截止点前的时间窗口里没有数据，请检查采样率或时间单位。")

        avg_i = sum(window_i) / len(window_i)
        avg_v = sum(window_v) / len(window_v)

        return t_cutoff, avg_i, avg_v


    def help_vbit(self):
        messagebox.showinfo("Help", f"""Charger voreg TEST:
        1. Choose the correct N6705C
        2. Confirm your charger is CC mode, and connect a 10 Ω resistor in series on Vbat
        3. Connect iic wires and measure channel on the other end of the resistor
        4. Click the "Check IIC Reg ADDR Weight" button to check the iic addres bit width
        5. Set the value 
        6. Click the start button to start 
        7. Wait a moment and get the result from OUTPUT""")

    def check_iic_weight(self):
        deviceI2C = devicei2c.DeviceI2C()
        self_charger_addr = 0x1A
        reg_addr = 0x01
        charger_addr = 0x17
        self_pmu_reg_8b = deviceI2C.read_register_value_8bit(self_charger_addr, reg_addr)
        self_pmu_reg_10b = deviceI2C.read_register_value_10bit(self_charger_addr, reg_addr)
        pmu_reg_8b = deviceI2C.read_register_value_8bit(charger_addr, reg_addr)
        pmu_reg_10b = deviceI2C.read_register_value_10bit(charger_addr, reg_addr)

        messagebox.showinfo("Des", f"""self_charger 8bit is 0x{self_pmu_reg_8b:x}
self_charger 10bit is 0x{self_pmu_reg_10b:x}
charger 8bit is 0x{pmu_reg_8b:x}
charger 10bit is 0x{pmu_reg_10b:x}
Please choose the write weight of your test""")

    def run_test(self):
        self.controller.export_file()
        time.sleep(4)
        self.controller.get_file()

    def run_iterm_test(self):
        # 获取输入数据并在测试结果区域显示
        iic_weight = self.iic_weight.get()
        print(iic_weight)
        iic_weight = int(iic_weight, 10)
        device_addr = self.device_addr_var.get()
        device_addr = int(device_addr, 16)
        reg_addr = self.reg_addr_var.get()
        reg_addr = int(reg_addr, 16)
        lsb = self.lsb_var.get()
        lsb = int(lsb, 10)
        msb = self.msb_var.get()
        msb = int(msb, 10)



        vol_channel = self.channel_var.get()
        if vol_channel == 'CH1':
            vol_channel = 1
        elif vol_channel == 'CH2':
            vol_channel = 2
        elif vol_channel == 'CH3':
            vol_channel = 3
        elif vol_channel == 'CH4':
            vol_channel = 4

        self.controller.set_voltage(vol_channel, 3.8)
        voltage = self.controller.get_voltage(vol_channel)
        print(voltage)


        deviceI2C = devicei2c.DeviceI2C()

        default_reg_value = deviceI2C.read_register_value_bit(device_addr, reg_addr, iic_weight)
        counter = msb - lsb + 1
        output = []
        offset = [0x1, 0x3, 0x7, 0xf, 0x1f, 0x3f, 0x7f, 0xff, 0x1ff, 0x3ff, 0x7ff, 0xfff, 0x1fff, 0x3fff, 0x7fff, 0xffff]
        data_base = default_reg_value & (~(offset[msb - lsb] << lsb))
        min_value = 0x0000
        max_value = 0xffff
        for i in range(0, pow(2, counter), 1):

            write_reg = data_base | i << lsb
            if write_reg <= min_value:
                write_reg2 = min_value
            elif write_reg >= max_value:
                write_reg2 = max_value
            else:
                write_reg2 = write_reg
            deviceI2C.write_register_value_bit(device_addr, reg_addr, write_reg2, iic_weight)
            # output.append(i)
            time.sleep(0.003)
            self.controller.dlog_config(1)
            self.controller.arb_set_staircafe(vol_channel, 4.1, 4.5)
            self.controller.BUS_TRG()
            time.sleep(14)
            self.controller.write_t(f"DIAG:FP:KEY 74")
            self.controller.export_file()
            time.sleep(2)
            self.controller.get_file()
            csv_path = "datalog1.csv"  # 替换为你的 CSV 文件路径
            self.remove_before_6_lines(csv_path, 'output.csv')
            csv_path = "output.csv"  # 替换为你的 CSV 文件路径
            cutoff_time, mean_i, mean_v = self.find_cutoff_by_sign_change(
                csv_file_path=csv_path,
                time_col='Sample',
                current_col='Curr avg 1',
                voltage_col='Volt avg 1',
                pre_cutoff_duration=300  # 如果单位是秒，则 0.5 表示 500ms
            )
            print(f"负->正 截止电流时间点: {cutoff_time:.4f}s")
            print(f"截止电流前 500ms 平均电流: {mean_i:.5f} A")
            print(f"截止电流前 500ms 平均电压: {mean_v:.5f} V")
            output.append((i, mean_i, mean_v))
            print(f"count{i} is finished")
        deviceI2C.write_register_value_bit(device_addr, reg_addr, default_reg_value, iic_weight)

        result = [f"reg,  ,iterm,   voltage"]

        for item in output:
            # 将集合转换为列表，并确保元素顺序一致
            item_list = list(item)
            result.append(f"{item_list[0]},   {item_list[1]}, {item_list[2]}")
        self.test_result_text.delete("1.0", tk.END)
        self.test_result_text.insert(tk.END, "\n".join(result))


    def run_iterm_test_back(self):
        # 获取输入数据并在测试结果区域显示
        iic_weight = self.iic_weight.get()
        print(iic_weight)
        iic_weight = int(iic_weight, 10)
        device_addr = self.device_addr_var.get()
        device_addr = int(device_addr, 16)
        reg_addr = self.reg_addr_var.get()
        reg_addr = int(reg_addr, 16)
        lsb = self.lsb_var.get()
        lsb = int(lsb, 10)
        msb = self.msb_var.get()
        msb = int(msb, 10)



        vol_channel = self.channel_var.get()
        if vol_channel == 'CH1':
            vol_channel = 1
        elif vol_channel == 'CH2':
            vol_channel = 2
        elif vol_channel == 'CH3':
            vol_channel = 3
        elif vol_channel == 'CH4':
            vol_channel = 4

        self.controller.set_voltage(vol_channel, 3.8)
        voltage = self.controller.get_voltage(vol_channel)
        print(voltage)


        deviceI2C = devicei2c.DeviceI2C()

        default_reg_value = deviceI2C.read_register_value_bit(device_addr, reg_addr, iic_weight)
        counter = msb - lsb + 1
        output = []
        offset = [0x1, 0x3, 0x7, 0xf, 0x1f, 0x3f, 0x7f, 0xff, 0x1ff, 0x3ff, 0x7ff, 0xfff, 0x1fff, 0x3fff, 0x7fff, 0xffff]
        data_base = default_reg_value & (~(offset[msb - lsb] << lsb))
        min_value = 0x0000
        max_value = 0xffff
        for i in range(0, pow(2, counter), 1):

            write_reg = data_base | i << lsb
            if write_reg <= min_value:
                write_reg2 = min_value
            elif write_reg >= max_value:
                write_reg2 = max_value
            else:
                write_reg2 = write_reg
            deviceI2C.write_register_value_bit(device_addr, reg_addr, write_reg2, iic_weight)
            # output.append(i)
            time.sleep(0.003)
            self.controller.dlog_config(1)
            self.controller.arb_set_staircafe(vol_channel, 4.1, 4.5)
            self.controller.BUS_TRG()
            time.sleep(67)
            self.controller.write_t(f"DIAG:FP:KEY 74")
            self.controller.export_file()
            time.sleep(4)
            start_t = time.time()
            self.controller.get_file()
            end_t = time.time()
            print(end_t - start_t)
            csv_path = "datalog1.csv"  # 替换为你的 CSV 文件路径
            self.remove_before_6_lines(csv_path, 'output.csv')
            csv_path = "output.csv"  # 替换为你的 CSV 文件路径
            cutoff_time, mean_i, mean_v = self.find_cutoff_by_sign_change(
                csv_file_path=csv_path,
                time_col='Sample',
                current_col='Curr avg 1',
                voltage_col='Volt avg 1',
                pre_cutoff_duration=50  # 如果单位是秒，则 0.5 表示 500ms
            )
            print(f"负->正 截止电流时间点: {cutoff_time:.4f}s")
            print(f"截止电流前 500ms 平均电流: {mean_i:.5f} A")
            print(f"截止电流前 500ms 平均电压: {mean_v:.5f} V")
            output.append((i, mean_i, mean_v))
            print(f"count{i} is finished")
        deviceI2C.write_register_value_bit(device_addr, reg_addr, default_reg_value, iic_weight)

        result = [f"reg,  ,iterm,   voltage"]

        for item in output:
            # 将集合转换为列表，并确保元素顺序一致
            item_list = list(item)
            result.append(f"{item_list[0]},   {item_list[1]}, {item_list[2]}")
        self.test_result_text.delete("1.0", tk.END)
        self.test_result_text.insert(tk.END, "\n".join(result))