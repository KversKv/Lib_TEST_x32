import tkinter as tk
from tkinter import ttk
from ins import ins_n6705c
from tkinter import Menu, Text
from tkinter import messagebox
import time

class DCDC_EFF_UI:
    def __init__(self, content_frame, controller):
        self.content_frame = content_frame
        # self.controller = controller
        self.controller = ins_n6705c.PowerSupplyController(self)  # 将self作为UI的引用传递

    def create_dcdc_effiency_module(self):
        ttk.Label(self.content_frame, text="DCDC Effiency Test", font=("Arial", 20)).pack(pady=20)
        ttk.Label(self.content_frame, text="This is the DCDC Effiency module.").pack(pady=10)

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

        self.channel_on_button = ttk.Button(frame_instr, text="Connect", command=self.connect)
        self.channel_on_button.pack(side="left", padx=5, pady=5)
        self.channel_off_button = ttk.Button(frame_instr, text="Disconnect", command=self.disconnect)
        self.channel_off_button.pack(side="left", padx=5, pady=5)
        ttk.Button(frame_instr, text="Help", command=self.help_eff).pack(
            pady=10)

        # 通道选择框架
        frame_channel = ttk.LabelFrame(self.content_frame, text="Channel Selection", padding="10")
        frame_channel.pack(padx=10, pady=10, fill="both")
        self.channel_label = ttk.Label(frame_channel, text="Select Vsys Channel:")
        self.channel_label.pack(side="left", padx=5, pady=5)
        self.dcdc_eff_vsys_channel_var = tk.StringVar(self.content_frame)
        self.dcdc_eff_vsys_channel_var.set("CH1")  # 默认通道为CH1
        self.channel_menu = ttk.OptionMenu(frame_channel, self.dcdc_eff_vsys_channel_var, "CH1", "CH1", "CH2", "CH3", "CH4")
        self.channel_menu.pack(side="left", padx=5, pady=5)

        self.channel_label = ttk.Label(frame_channel, text="Select voltage measure Channel:")
        self.channel_label.pack(side="left", padx=5, pady=10)
        self.dcdc_eff_measure_channel_var = tk.StringVar(self.content_frame)
        self.dcdc_eff_measure_channel_var.set("CH2")  # 默认通道为CH1
        self.channel_menu = ttk.OptionMenu(frame_channel, self.dcdc_eff_measure_channel_var, "CH2", "CH1", "CH2", "CH3", "CH4")
        self.channel_menu.pack(side="left", padx=5, pady=10)

        self.channel_label = ttk.Label(frame_channel, text="Select load current Channel:")
        self.channel_label.pack(side="left", padx=5, pady=15)
        self.dcdc_eff_iloed_channel_var = tk.StringVar(self.content_frame)
        self.dcdc_eff_iloed_channel_var.set("CH3")  # content_frame
        self.channel_menu = ttk.OptionMenu(frame_channel, self.dcdc_eff_iloed_channel_var, "CH3", "CH1", "CH2", "CH3", "CH4")
        self.channel_menu.pack(side="left", padx=5, pady=15)


        self.channel_on_button = ttk.Button(frame_channel, text="SET", command=self.set_dcdc_eff_mode)
        self.channel_on_button.pack(side="left", padx=5, pady=5)

        #frame dcdc effiency config
        frame_eff_config = ttk.LabelFrame(self.content_frame, text="Test Config", padding="10")
        frame_eff_config.pack(padx=10, pady=10, fill="both")
        self.start_Iload = tk.StringVar()
        ttk.Label(frame_eff_config, text="Start Iload(mA,ex:-0.1)", anchor="w").grid(row=1, column=0, pady=5)
        ttk.Entry(frame_eff_config, textvariable=self.start_Iload).grid(row=1, column=1, pady=5)
        self.end_Iload = tk.StringVar()
        ttk.Label(frame_eff_config, text="End Iload(mA,ex:-0.2)", anchor="w").grid(row=1, column=2, pady=5)
        ttk.Entry(frame_eff_config, textvariable=self.end_Iload).grid(row=1, column=3, pady=5)
        self.step_Iload = tk.StringVar()
        ttk.Label(frame_eff_config, text="Step Iload(mA,ex:-0.1)", anchor="w").grid(row=1, column=4, pady=5)
        ttk.Entry(frame_eff_config, textvariable=self.step_Iload).grid(row=1, column=5, pady=5)


        # self.channel_label = ttk.Label(frame_config, text="Select Vsys Channel:")
        # self.channel_label.pack(side="left", padx=5, pady=5)
        # self.dcdc_eff_vsys_channel_var = tk.StringVar(self.master)
        # self.dcdc_eff_vsys_channel_var.set("CH1")  # 默认通道为CH1
        # self.channel_menu = ttk.OptionMenu(frame_config, self.dcdc_eff_vsys_channel_var, "CH1", "CH1", "CH2", "CH3",
        #                                    "CH4")
        # self.channel_menu.pack(side="left", padx=5, pady=5)

        # 创建输入区域
        input_frame = ttk.Frame(self.content_frame)
        input_frame.pack(pady=10)

        ttk.Button(input_frame, text="Start", command=self.run_dcdc_eff_test1).grid(row=7, columnspan=2, pady=10)

        # 创建结果区域
        ttk.Label(self.content_frame, text="Test Result:").pack()
        self.test_result_text_eff = Text(self.content_frame, height=15, width=50)
        self.test_result_text_eff.pack()



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

    def set_dcdc_eff_mode(self):
        vsys_channel = self.dcdc_eff_vsys_channel_var.get()[-1]
        self.controller.set_channel_range(vsys_channel)
        self.controller.set_mode(vsys_channel, "PS2Q")
        measure_channel = self.dcdc_eff_measure_channel_var.get()[-1]
        self.controller.set_channel_range(measure_channel)
        self.controller.set_mode(measure_channel, "VMETer")
        iload_channel = self.dcdc_eff_iloed_channel_var.get()[-1]
        self.controller.set_channel_range(iload_channel)
        self.controller.set_mode(iload_channel, "CCLoad")

    def update_values(self):
        channel = self.channel_var.get()[-1]
        self.controller.set_channel_range(channel)
        self.controller.update_values(channel)

    def update_status(self, status, color):
        self.status_label.config(text=f"Status: {status}", foreground=color)


    def remove_max_min(self, lst):
        return [x for x in lst if x != max(lst) and x != min(lst)]

    def get_avr_voltage(self, channel, cnt):
        """获取通道电流"""
        voltage = []
        voltage.clear()
        for i in range(0, cnt, 1):
            voltage.append(float(self.controller.instr.query(f"MEAS:VOLT? (@{channel})")))
        print(len(voltage))
        voltage = self.remove_max_min(voltage)
        print(len(voltage))
        return sum(voltage)/len(voltage)

    def get_avr_current(self, channel, cnt):
        """获取通道电流"""
        current = []
        current.clear()
        for i in range(0, cnt, 1):
            current.append(float(self.controller.instr.query(f"MEAS:CURR? (@{channel})")))
        current = self.remove_max_min(current)
        return sum(current)/len(current)

    def run_dcdc_eff_test1(self):
        start_cc = self.start_Iload.get()
        start_cc = float(start_cc)
        stop_cc = self.end_Iload.get()
        stop_cc = float(stop_cc)
        stop_cc = stop_cc - 0.0005
        step_cc = self.step_Iload.get()
        step_cc = float(step_cc)
        # print(start_cc)
        # print(start_cc + " " + stop_cc + " " +step_cc )
        self.set_dcdc_eff_mode()
        vbat_channel = self.dcdc_eff_vsys_channel_var.get()[-1]
        v_measure_channel = self.dcdc_eff_measure_channel_var.get()[-1]
        cc_load_channel = self.dcdc_eff_iloed_channel_var.get()[-1]
        self.controller.set_voltage(vbat_channel, 3.8)
        #self.set_current_limit(1, 0.3)
        self.controller.set_current_limit(vbat_channel, 1)
        self.controller.set_channel_range(vbat_channel)
        self.controller.set_channel_range(v_measure_channel)
        self.controller.set_channel_range(cc_load_channel)
        #self.enable_channel(1)
        #self.enable_channel(1)
        #self.enable_channel(2)
        voltage_in = []
        voltage_out = []
        current_in = []
        current_out = []
        output = []
        counter = start_cc
        #self.set_current(cc_load_channel, -0.0001)
        self.controller.channel_off(cc_load_channel)
        time.sleep(0.1)
        # 获取基准电流和电压时转换为浮点数
        iload_base = float(self.controller.get_current(cc_load_channel))
        print(f"iload_base={iload_base}")
        voltage_base = float(self.get_avr_voltage(vbat_channel, 4))
        current_base = float(self.get_avr_current(vbat_channel, 4))
        self.controller.channel_on(cc_load_channel)
        self.controller.set_current(cc_load_channel, start_cc)

        time.sleep(0.1)
        efficiency = []
        # self.enable_channel(3)
        while counter >= stop_cc:

            self.controller.set_current(cc_load_channel, counter)
            time.sleep(0.003)

            # 将获取的电压和电流值转换为浮点数
            vbat = float(self.controller.get_voltage(vbat_channel))
            vout = float(self.controller.get_voltage(v_measure_channel))
            i_in = float(self.controller.get_current(vbat_channel))
            i_out = float(self.controller.get_current(cc_load_channel))

            eff = (vout * (iload_base - i_out)) / (vbat * (i_in - current_base))
            current_out.append(i_out)
            efficiency.append(eff)
            output.append((i_out, eff))
            counter += step_cc
            # print(f"{i_out} ,  {avr_efficiency}")

        #efficiency = (voltage_out * current_out) / (voltage_in * (current_in - current_base))

        #self.disable_channel(1)
        # self.disable_channel(2)
        # self.disable_channel(3)
        self.controller.set_current(cc_load_channel, -0.001)

        print(f"{voltage_base} {current_base} ")

        print(f"{voltage_in}")
        print(f"{voltage_out}")
        print(f"{current_in}")
        print(f"{current_out}")
        print(f"{efficiency}")
        print(output)
        result = [f"Iload  ,  eff"]
        for item in output:
            # 将集合转换为列表，并确保元素顺序一致
            item_list = list(item)
            # item_list.sort(key=lambda x: isinstance(x, str))  # 字符串排在后面
            # result.append(f"{item_list[0]},   {item_list[1]}")
            result.append("%.3f , %.3f%%" % (abs(item_list[0]), item_list[1] * 100))
        self.test_result_text_eff.delete("1.0", tk.END)
        self.test_result_text_eff.insert(tk.END, "\n".join(result))


    def run_dcdc_eff_test2(self):
        start_cc = self.start_Iload.get()
        stop_cc = self.end_Iload.get()
        step_cc = self.step_Iload.get()
        print(start_cc + " " + stop_cc + " " +step_cc )
        self.set_dcdc_eff_mode()
        vbat_channel = self.dcdc_eff_vsys_channel_var.get()[-1]
        v_measure_channel = self.dcdc_eff_measure_channel_var.get()[-1]
        cc_load_channel = self.dcdc_eff_iloed_channel_var.get()[-1]
        self.controller.set_voltage(vbat_channel, 3.8)
        #self.set_current_limit(1, 0.3)
        self.controller.set_current_limit(vbat_channel, 1)
        self.controller.set_channel_range(vbat_channel)
        self.controller.set_channel_range(v_measure_channel)
        self.controller.set_channel_range(cc_load_channel)
        #self.enable_channel(1)
        #self.enable_channel(2)
        voltage_in = []
        voltage_out = []
        current_in = []
        current_out = []
        counter = start_cc
        output = []
        #self.set_current(cc_load_channel, -0.0001)
        self.controller.channel_off(cc_load_channel)
        time.sleep(0.1)
        iload_base = self.controller.get_current(cc_load_channel)
        print(f"iload_base={iload_base}")
        voltage_base = self.get_avr_voltage(vbat_channel, 9)
        current_base = self.get_avr_current(vbat_channel, 9)
        self.controller.channel_on(cc_load_channel)
        self.controller.set_current(cc_load_channel, start_cc)

        time.sleep(0.1)
        efficiency = []
        # self.enable_channel(3)
        while counter >= stop_cc :
            counter += step_cc
            self.controller.set_current(cc_load_channel, counter)
            time.sleep(0.01)

            vbat = self.controller.get_voltage(vbat_channel)
            vout = self.controller.get_voltage(v_measure_channel)
            i_in = self.controller.get_current(vbat_channel)
            i_out = self.controller.get_current(cc_load_channel)
            # voltage_in.append(vbat)
            # voltage_out.append(vout)
            # current_in.append(i_in)
            # current_out.append(i_out)
            eff = (vout * (iload_base - i_out)) / (vbat * (i_in - current_base))
            current_out.append(i_out)
            efficiency.append(eff)
            output.append((i_out, eff))
            # print(f"{i_out} ,  {avr_efficiency}")

        #efficiency = (voltage_out * current_out) / (voltage_in * (current_in - current_base))

        #self.disable_channel(1)
        # self.disable_channel(2)
        # self.disable_channel(3)
        self.controller.set_current(cc_load_channel, -0.001)

        print(f"{voltage_base} {current_base} ")

        print(f"{voltage_in}")
        print(f"{voltage_out}")
        print(f"{current_in}")
        print(f"{current_out}")
        print(f"{efficiency}")
        result = []
        result.append(f"    Iload ,    eff   ")
        for item in output:
            # 将集合转换为列表，并确保元素顺序一致
            item_list = list(item)
            # item_list.sort(key=lambda x: isinstance(x, str))  # 字符串排在后面
            result.append(f"{item_list[0]},   {item_list[1]}")
        self.test_result_text_eff.delete("1.0", tk.END)
        self.test_result_text_eff.insert(tk.END, "\n".join(result))

    def help_eff(self):
        messagebox.showinfo("Help", f"""OUTPUT Value TEST:
        1. Choose the correct N6705C
        2. Click the "Check IIC Reg ADDR Weight" button to check the iic addres bit width
        3. Set the value 
        4. Click the start button to start 
        5. Wait a moment and get the result from OUTPUT""")