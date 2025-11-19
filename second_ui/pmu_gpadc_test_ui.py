import tkinter as tk
from tkinter import ttk
from ins import ins_n6705c
from tkinter import Menu, Text
from tkinter import messagebox
import time
import devicei2c
from drv import vt6002

class PMU_GPADC_TEST_UI:
    def __init__(self, content_frame, controller):
        self.test_result_text = None
        self.content_frame = content_frame
        # self.controller = controller
        self.controller = ins_n6705c.PowerSupplyController(self)  # 将self作为UI的引用传递


    def create_pmu_gpadc_module(self):
        ttk.Label(self.content_frame, text="GPADC TEST", font=("Arial", 20)).pack(pady=20)
        ttk.Label(self.content_frame, text="This is the GPADC TEST module.").pack(pady=10)

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
        self.vbat_channel_label = ttk.Label(frame_channel, text="Select Vbat Channel:")
        self.vbat_channel_label.pack(side="left", padx=5, pady=5)
        self.vbat_channel_var = tk.StringVar(self.content_frame)
        self.vbat_channel_var.set("CH1")  # 默认通道为CH1
        self.channel_menu = ttk.OptionMenu(frame_channel, self.vbat_channel_var, "CH1", "CH1", "CH2", "CH3", "CH4")
        self.channel_menu.pack(side="left", padx=5, pady=5)
        self.channel_on_button = ttk.Button(frame_channel, text="SET", command=self.set_voltagemode)
        self.channel_on_button.pack(side="left", padx=5, pady=5)

        self.adc_source_channel_label = ttk.Label(frame_channel, text="Select Ext Source Channel:")
        self.adc_source_channel_label.pack(side="left", padx=5, pady=5)
        self.source_channel_var = tk.StringVar(self.content_frame)
        self.source_channel_var.set("CH2")  # 默认通道为CH1
        self.channel_menu = ttk.OptionMenu(frame_channel, self.source_channel_var, "CH1", "CH1", "CH2", "CH3", "CH4")
        self.channel_menu.pack(side="left", padx=5, pady=5)

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

        ttk.Label(frame_vbit_config, text="Start", anchor="w").grid(row=1, column=2, pady=5)
        ttk.Entry(frame_vbit_config, textvariable=self.lsb_var).grid(row=1, column=3, pady=5)

        ttk.Label(frame_vbit_config, text="End", anchor="w").grid(row=1, column=4, pady=5)
        ttk.Entry(frame_vbit_config, textvariable=self.msb_var).grid(row=1, column=5, pady=5)

        ttk.Label(frame_vbit_config, text="Min value", anchor="w").grid(row=2, column=0, pady=5)
        ttk.Entry(frame_vbit_config, textvariable=self.min_value_var).grid(row=2, column=1, pady=5)

        ttk.Label(frame_vbit_config, text="Max value", anchor="w").grid(row=2, column=2, pady=5)
        ttk.Entry(frame_vbit_config, textvariable=self.max_value_var).grid(row=2, column=3, pady=5)

        ttk.Button(frame_vbit_config, text="Start", command=self.run_pmu_gpadc_test).grid(row=3, columnspan=2, pady=10)

        ttk.Button(self.content_frame, text="Check IIC Reg ADDR Weight", command=self.check_iic_weight).pack(
            side="left", pady=10)

        ttk.Button(self.content_frame, text="Vbat_TEST", command=self.vbat_channel_test).pack(pady=10)

        ttk.Button(self.content_frame, text="Ex_GPADC0 TEST", command=self.external_gpadc0_channel_test).pack(pady=10)

        ttk.Button(self.content_frame, text="GPADC2_Temp", command=self.gpadc_test_vbatAndExternal).pack(pady=10)

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

    def test_function(self):
        device_addr = 0x27
        iic_weight = 10
        reg_addr = 0x57
        vbat_channel = 1
        deviceI2C = devicei2c.DeviceI2C()
        get_reg_cnt = 1000
        start_vol = 0.1
        self.controller.set_voltage(vbat_channel, start_vol)
        end_vol = 1.5
        end_vol = end_vol +0.005
        step_vol = 0.1
        start_cnt = start_vol
        while start_cnt <= end_vol:
            self.controller.set_voltage(vbat_channel, start_cnt)
            time.sleep(2)
            reg_sum = 0x0
            reg_max = 0x0
            reg_min = 0xffff
            cnt = get_reg_cnt
            while cnt:
                deviceI2C.write_register_value_bit(device_addr, 0x004f, 0x24, iic_weight)
                time.sleep(0.001)
                temp = deviceI2C.read_register_value_bit(device_addr, reg_addr, iic_weight)
                reg_sum += temp
                if reg_max < temp:
                    reg_max = temp
                if reg_min > temp:
                    reg_min = temp
                cnt = cnt - 1
                # print(f"{cnt} counts: temp={temp}; sum={reg_sum}; max={reg_max}; min={reg_min}")
            reg_sum = reg_sum - reg_max - reg_min
            avrage = reg_sum / (get_reg_cnt - 2)
            print(f"{get_reg_cnt} counts: voltage={start_cnt:.3f}V; avrage={avrage:.3f}; max={reg_max}; min={reg_min}")
            start_cnt = start_cnt + step_vol
        self.controller.set_voltage(vbat_channel, start_vol)


    def vbat_channel_test(self):
        device_addr = 0x27
        iic_weight = 10
        reg_addr = 0x57
        vbat_channel = 1
        deviceI2C = devicei2c.DeviceI2C()
        get_reg_cnt = 1000
        start_vol = 3.1
        self.controller.set_voltage(vbat_channel, start_vol)
        end_vol = 4.5
        end_vol = end_vol +0.005
        step_vol = 0.1
        start_cnt = start_vol
        while start_cnt <= end_vol:
            self.controller.set_voltage(vbat_channel, start_cnt)
            time.sleep(2)
            reg_sum = 0x0
            reg_max = 0x0
            reg_min = 0xffff
            cnt = get_reg_cnt
            while cnt:
                deviceI2C.write_register_value_bit(device_addr, 0x004f, 0x24, iic_weight)
                time.sleep(0.001)
                temp = deviceI2C.read_register_value_bit(device_addr, reg_addr, iic_weight)
                reg_sum += temp
                if reg_max < temp:
                    reg_max = temp
                if reg_min > temp:
                    reg_min = temp
                cnt = cnt - 1
                # print(f"{cnt} counts: temp={temp}; sum={reg_sum}; max={reg_max}; min={reg_min}")
            reg_sum = reg_sum - reg_max - reg_min
            avrage = reg_sum / (get_reg_cnt - 2)
            print(f"{get_reg_cnt} counts: voltage={start_cnt:.3f}V; avrage={avrage:.3f}; max={reg_max}; min={reg_min}")
            start_cnt = start_cnt + step_vol
        self.controller.set_voltage(vbat_channel, start_vol)

    def external_gpadc0_channel_test(self):
        device_addr = 0x27
        iic_weight = 10
        reg_addr = 0x58
        vbat_channel = 2
        deviceI2C = devicei2c.DeviceI2C()
        get_reg_cnt = 1000
        start_vol = 0.1
        self.controller.set_voltage(vbat_channel, start_vol)
        end_vol = 1.5
        end_vol = end_vol +0.005
        step_vol = 0.1
        start_cnt = start_vol
        while start_cnt <= end_vol:
            self.controller.set_voltage(vbat_channel, start_cnt)
            time.sleep(2)
            reg_sum = 0x0
            reg_max = 0x0
            reg_min = 0xffff
            cnt = get_reg_cnt
            while cnt:
                deviceI2C.write_register_value_bit(device_addr, 0x004f, 0x24, iic_weight)
                time.sleep(0.001)
                temp = deviceI2C.read_register_value_bit(device_addr, reg_addr, iic_weight)
                reg_sum += temp
                if reg_max < temp:
                    reg_max = temp
                if reg_min > temp:
                    reg_min = temp
                cnt = cnt - 1
                # print(f"{cnt} counts: temp={temp}; sum={reg_sum}; max={reg_max}; min={reg_min}")
            reg_sum = reg_sum - reg_max - reg_min
            avrage = reg_sum / (get_reg_cnt - 2)
            print(f"{get_reg_cnt} counts: voltage={start_cnt:.3f}V; avrage={avrage:.3f}; max={reg_max}; min={reg_min}")
            start_cnt = start_cnt + step_vol
        self.controller.set_voltage(vbat_channel, start_vol)


    def gpadc_reg_read(self, device_addr=0x27, reg_addr=0x57, iic_weight=10, get_reg_cnt=1000):
        device_addr = 0x27
        iic_weight = 10
        deviceI2C = devicei2c.DeviceI2C()
        get_reg_cnt = 1000
        time.sleep(1)
        reg_sum = 0x0
        reg_max = 0x0
        reg_min = 0xffff
        cnt = get_reg_cnt
        while cnt:
            deviceI2C.write_register_value_bit(device_addr, 0x004f, 0x24, iic_weight)
            time.sleep(0.001)
            temp = deviceI2C.read_register_value_bit(device_addr, reg_addr, iic_weight)
            reg_sum += temp
            if reg_max < temp:
                reg_max = temp
            if reg_min > temp:
                reg_min = temp
            cnt = cnt - 1
            # print(f"{cnt} counts: temp={temp}; sum={reg_sum}; max={reg_max}; min={reg_min}")
        reg_sum = reg_sum - reg_max - reg_min
        avrage = reg_sum / (get_reg_cnt - 2)
        print(f"{get_reg_cnt} counts: avrage={avrage:.3f}; max={reg_max}; min={reg_min}")
        return avrage, reg_max, reg_min

    def gpadc_temperature_test(self):
        vt6002_ac = vt6002.VT6002("COM9")  # 根据实际串口号修改
        device_addr = 0x27
        iic_weight = 8
        reg_addr = 0x56
        deviceI2C = devicei2c.DeviceI2C()
        get_reg_cnt = 1000

        vbat_channel = 1
        vbat_v1 = 3.2
        vbat_v2 = 4.2
        ext_v1 = 0.4
        ext_v2 = 1.2

        start_temp = -30.0
        end_temp = 80.0
        end_temp = end_temp + 0.01
        step_temp = 10
        current_temp = start_temp
        vt6002_ac.set_temperature(current_temp)
        while current_temp <= end_temp:
            reg_sum = 0
            reg_max = 0x0
            reg_min = 0xffff

            vt6002_ac.set_temperature(current_temp)
            current_temp_get = vt6002_ac.get_current_temp()
            while (current_temp_get < current_temp - 0.3) | (current_temp_get > current_temp + 0.3):
                time.sleep(1)
                current_temp_get = vt6002_ac.get_current_temp()
            time.sleep(60)
            cnt = get_reg_cnt
            while cnt:
                self.controller.set_voltage(vbat_channel, vbat_v1)
                deviceI2C.write_register_value_bit(device_addr, 0x004f, 0x24, iic_weight)
                time.sleep(0.001)
                temp = deviceI2C.read_register_value_bit(device_addr, reg_addr, iic_weight)
                reg_sum += temp
                if reg_max < temp:
                    reg_max = temp
                if reg_min > temp:
                    reg_min = temp
                cnt = cnt - 1
                # print(f"{cnt} counts: temp={temp}; sum={reg_sum}; max={reg_max}; min={reg_min}")
            reg_sum = reg_sum - reg_max - reg_min
            average = reg_sum / (get_reg_cnt - 2)
            print(f"Temperature is {current_temp:.3f}, {get_reg_cnt} counts: avrage={average:.3f}; max={reg_max}; min={reg_min}")
            current_temp = current_temp + step_temp

    def gpadc_test_vbatAndExternal(self):
        vt6002_ac = vt6002.VT6002("COM9")  # 根据实际串口号修改
        device_addr = 0x27
        iic_weight = 8
        reg_addr = 0x56
        chan1_addr = 0x57
        chan2_addr = 0x58
        chan3_addr = 0x59
        deviceI2C = devicei2c.DeviceI2C()
        get_reg_cnt = 1000

        vbat_channel = 1
        vbat_v1 = 3.2
        vbat_v2 = 4.2
        ext_v1 = 0.4
        ext_v2 = 1.2

        start_temp = -30.0
        end_temp = 80.0
        end_temp = end_temp + 0.01
        step_temp = 10
        current_temp = start_temp
        vt6002_ac.set_temperature(current_temp)

        temp_1 = self.gpadc_reg_read(reg_addr=0x57)
        print(temp_1)
        while current_temp <= end_temp:
            reg_sum = 0
            reg_max = 0x0
            reg_min = 0xffff

            vt6002_ac.set_temperature(current_temp)
            current_temp_get = vt6002_ac.get_current_temp()
            while (current_temp_get < current_temp - 0.3) | (current_temp_get > current_temp + 0.3):
                time.sleep(1)
                current_temp_get = vt6002_ac.get_current_temp()
            time.sleep(60)
            cnt = get_reg_cnt
            self.controller.set_voltage(vbat_channel, vbat_v1)
            time.sleep(0.1)
            self.gpadc_reg_read(reg_addr=0x57)


            while cnt:
                self.controller.set_voltage(vbat_channel, vbat_v1)
                deviceI2C.write_register_value_bit(device_addr, 0x004f, 0x24, iic_weight)
                time.sleep(0.001)
                temp = deviceI2C.read_register_value_bit(device_addr, chan1_addr, iic_weight)
                reg_sum += temp
                if reg_max < temp:
                    reg_max = temp
                if reg_min > temp:
                    reg_min = temp
                cnt = cnt - 1
                # print(f"{cnt} counts: temp={temp}; sum={reg_sum}; max={reg_max}; min={reg_min}")
            reg_sum = reg_sum - reg_max - reg_min
            average = reg_sum / (get_reg_cnt - 2)
            print(f"Temperature is {current_temp:.3f}, {get_reg_cnt} counts: avrage={average:.3f}; max={reg_max}; min={reg_min}")
            current_temp = current_temp + step_temp


    def run_pmu_gpadc_test(self):
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

        start_vol = 2.7
        end_vol = 3.1
        step_vol = 0.1
        start_cnt = start_vol

        vbat_channel = self.vbat_channel_var.get()
        if vbat_channel == 'CH1':
            vbat_channel = 1
        elif vbat_channel == 'CH2':
            vbat_channel = 2
        elif vbat_channel == 'CH3':
            vbat_channel = 3
        elif vbat_channel == 'CH4':
            vbat_channel = 4

        deviceI2C = devicei2c.DeviceI2C()

        get_reg_cnt = 1000
        while start_cnt < end_vol:
            self.controller.set_voltage(vbat_channel, start_cnt)
            time.sleep(0.005)
            reg_sum = 0x0
            reg_max = 0x0
            reg_min = 0xffff
            cnt = get_reg_cnt
            while cnt:
                deviceI2C.write_register_value_bit(device_addr, 0x004f, 0x24, iic_weight)
                time.sleep(0.001)
                temp = deviceI2C.read_register_value_bit(device_addr, reg_addr, iic_weight)
                reg_sum += temp
                if reg_max < temp:
                    reg_max = temp
                if reg_min > temp:
                    reg_min = temp
                cnt = cnt - 1
                # print(f"{cnt} counts: temp={temp}; sum={reg_sum}; max={reg_max}; min={reg_min}")
            reg_sum = reg_sum - reg_max - reg_min
            avrage = reg_sum / (get_reg_cnt - 2)
            print(f"{get_reg_cnt} counts: voltage={start_cnt}V; avrage={avrage}; max={reg_max}; min={reg_min}")
            start_cnt = start_cnt + step_vol

