import tkinter as tk
from tkinter import ttk
from ins import ins_n6705c
from tkinter import Menu, Text
from tkinter import messagebox
import time
import devicei2c


class OUTPUT_VOL_UI:
    def __init__(self, content_frame, controller):
        self.content_frame = content_frame
        # self.controller = controller
        self.controller = ins_n6705c.PowerSupplyController(self)  # 将self作为UI的引用传递

    def create_output_voltage_module(self):
        ttk.Label(self.content_frame, text="Output Voltage", font=("Arial", 20)).pack(pady=20)
        ttk.Label(self.content_frame, text="This is the Output Voltage module.").pack(pady=10)

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
        self.channel_label = ttk.Label(frame_channel, text="Select Channel:")
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

        ttk.Label(frame_vbit_config, text="Select V/I", anchor="w").grid(row=0, column=0, pady=5)
        ttk.Combobox(frame_vbit_config, values=["V", "I"]).grid(row=0, column=1, pady=5)

        ttk.Label(frame_vbit_config, text="IIC weight", anchor="w").grid(row=0, column=2, pady=5)
        ttk.Entry(frame_vbit_config, textvariable=self.iic_weight).grid(row=0, column=3, pady=5)
        # ttk.Combobox(input_frame, values=["8", "10"]).grid(row=1, column=1, pady=5)

        ttk.Label(frame_vbit_config, text="Device Addr(x)", anchor="w").grid(row=0, column=4, pady=5)
        ttk.Entry(frame_vbit_config, textvariable=self.device_addr_var).grid(row=0, column=5, pady=5)

        ttk.Label(frame_vbit_config, text="Reg Addr(x)", anchor="w").grid(row=1, column=0, pady=5)
        ttk.Entry(frame_vbit_config, textvariable=self.reg_addr_var).grid(row=1, column=1, pady=5)

        ttk.Label(frame_vbit_config, text="LSB", anchor="w").grid(row=1, column=2, pady=5)
        ttk.Entry(frame_vbit_config, textvariable=self.lsb_var).grid(row=1, column=3, pady=5)

        ttk.Label(frame_vbit_config, text="MSB", anchor="w").grid(row=1, column=4, pady=5)
        ttk.Entry(frame_vbit_config, textvariable=self.msb_var).grid(row=1, column=5, pady=5)

        ttk.Label(frame_vbit_config, text="Min value", anchor="w").grid(row=2, column=0, pady=5)
        ttk.Entry(frame_vbit_config, textvariable=self.min_value_var).grid(row=2, column=1, pady=5)

        ttk.Label(frame_vbit_config, text="Max value", anchor="w").grid(row=2, column=2, pady=5)
        ttk.Entry(frame_vbit_config, textvariable=self.max_value_var).grid(row=2, column=3, pady=5)

        ttk.Button(frame_vbit_config, text="Start", command=self.run_output_voltage_test2).grid(row=3, columnspan=2,
                                                                                                pady=10)

        ttk.Button(self.content_frame, text="Check IIC Reg ADDR Weight", command=self.check_iic_weight).pack(
            side="left", pady=10)

        ttk.Button(self.content_frame, text="Run Test", command=self.run_output_voltage_test).pack(pady=10)

        # 创建输入区域
        input_frame = ttk.Frame(self.content_frame)
        input_frame.pack(pady=10)

        # 创建结果区域
        ttk.Label(self.content_frame, text="Test Result:").pack()
        self.test_result_text = Text(self.content_frame, height=15, width=50)
        self.test_result_text.pack()

    def connect(self):
        resource_name = self.instr_var.get()
        print(resource_name)
        self.controller.connect(resource_name)

    def disconnect(self):
        self.controller.disconnect()

    def set_voltage(self):
        voltage = self.voltage_entry.get()
        channel = self.channel_var.get()[-1]
        self.controller.set_voltage(channel, voltage)

    def set_current_limit(self):
        current = self.current_entry.get()
        channel = self.channel_var.get()[-1]
        self.controller.set_current_limit(channel, current)

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

    def help_vbit(self):
        messagebox.showinfo("Help", f"""OUTPUT Value TEST:
        1. Choose the correct N6705C
        2. Click the "Check IIC Reg ADDR Weight" button to check the iic addres bit width
        3. Set the value 
        4. Click the start button to start 
        5. Wait a moment and get the result from OUTPUT""")

    def check_iic_weight(self):
        deviceI2C = devicei2c.DeviceI2C()
        self_pmu_addr = 0x27
        reg_addr = 0x00
        pmu_addr = 0x17
        self_pmu_reg_8b = deviceI2C.read_register_value_8bit(self_pmu_addr, reg_addr)
        self_pmu_reg_10b = deviceI2C.read_register_value_10bit(self_pmu_addr, reg_addr)
        pmu_reg_8b = deviceI2C.read_register_value_8bit(pmu_addr, reg_addr)
        pmu_reg_10b = deviceI2C.read_register_value_10bit(pmu_addr, reg_addr)

        messagebox.showinfo("Des", f"""self_pmu 8bit is 0x{self_pmu_reg_8b:x}
self_pmu 10bit is 0x{self_pmu_reg_10b:x}
pmu 8bit is 0x{pmu_reg_8b:x}
pmu 10bit is 0x{pmu_reg_10b:x}
Please choose the write weight of your test""")

    def run_output_voltage_test(self):

        iic_weight = 8
        device_addr = 0x27
        reg_addr = 0x0128
        lsb = 10
        msb = 14
        vol_channel = 2

        deviceI2C = devicei2c.DeviceI2C()
        self.controller.get_voltage(vol_channel)
        default_reg_value = deviceI2C.read_register_value_bit(device_addr, reg_addr, iic_weight)
        # print(f"default_reg_value= 0x{default_reg_value:x}")
        voltage = self.controller.get_voltage(vol_channel)
        counter = msb - lsb + 1
        output = []
        offset = [0x3, 0x7, 0xf, 0x1f, 0x3f, 0x7f, 0xff, 0x1ff, 0x3ff, 0x7ff, 0xfff, 0x1fff, 0x3fff, 0x7fff, 0xffff]
        data_base = default_reg_value & (~(offset[msb - lsb - 1] << lsb))
        min_value = 0x1250
        max_value = 0x5E50
        for i in range(0, pow(2, counter), 1):
            time1 = time.time()
            write_reg = data_base | i << lsb
            time2 = time.time()
            print(time2 - time1)

            if write_reg <= min_value:
                write_reg2 = min_value
            elif write_reg >= max_value:
                write_reg2 = max_value
            else:
                write_reg2 = write_reg
            deviceI2C.write_register_value_bit(device_addr, reg_addr, write_reg2, iic_weight)
            time1 = time.time()
            print(time1 - time2)
            # output.append(i)
            time.sleep(0.003)
            time2 = time.time()
            print(time2 - time1)
            voltage = str(float(self.controller.get_voltage(vol_channel)))
            current = str(float(self.controller.get_current(vol_channel)))
            time1 = time.time()
            print(time1 - time2)
            output.append((i, voltage, current))
        result = []
        for item in output:
            # 将集合转换为列表，并确保元素顺序一致
            item_list = list(item)
            # item_list.sort(key=lambda x: isinstance(x, str))  # 字符串排在后面
            result.append(f"{item_list[0]},   {item_list[1]},   {item_list[2]}")
        result.append(f"derlta,  voltage,   current")
        self.test_result_text.delete("1.0", tk.END)
        self.test_result_text.insert(tk.END, "\n".join(result))

    def run_output_voltage_test2(self):
        # 获取输入数据并在测试结果区域显示
        iic_weight = self.iic_weight.get()
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

        deviceI2C = devicei2c.DeviceI2C()
        self.controller.get_voltage(vol_channel)
        default_reg_value = deviceI2C.read_register_value_bit(device_addr, reg_addr, iic_weight)
        # print(f"default_reg_value= 0x{default_reg_value:x}")
        voltage = self.controller.get_voltage(vol_channel)
        counter = msb - lsb + 1
        output = []
        offset = [0x3, 0x7, 0xf, 0x1f, 0x3f, 0x7f, 0xff, 0x1ff, 0x3ff, 0x7ff, 0xfff, 0x1fff, 0x3fff, 0x7fff, 0xffff]
        data_base = default_reg_value & (~(offset[msb - lsb - 1] << lsb))
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
            voltage = str(float(self.controller.get_voltage(vol_channel)))
            current = str(float(self.controller.get_current(vol_channel)))

            output.append((i, voltage, current))
        result = []
        for item in output:
            # 将集合转换为列表，并确保元素顺序一致
            item_list = list(item)
            # item_list.sort(key=lambda x: isinstance(x, str))  # 字符串排在后面
            result.append(f"{item_list[0]},   {item_list[1]},   {item_list[2]}")
        result.append(f"derlta,  voltage,   current")
        self.test_result_text.delete("1.0", tk.END)
        self.test_result_text.insert(tk.END, "\n".join(result))
