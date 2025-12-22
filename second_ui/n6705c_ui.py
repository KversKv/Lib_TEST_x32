import tkinter as tk
from tkinter import ttk
from ins import ins_n6705c
from tkinter import Menu, Text
from tkinter import messagebox
import time

class N6705CUI:
    def __init__(self, content_frame, controller):
        self.content_frame = content_frame
        # self.controller = controller
        self.controller = ins_n6705c.PowerSupplyController(self)  # 将self作为UI的引用传递

    def create_n6705c_module(self):

        # run test
        frame_run = ttk.LabelFrame(self.content_frame, text="RUN TEST", padding="10")
        frame_run.pack(padx=10, pady=10, fill="both")
        # ttk.Label(self.content_frame, text="N6705C Module", font=("Arial", 20)).pack(pady=20)
        # ttk.Label(self.content_frame, text="This is the N6705C module.").pack(pady=10)
        ttk.Button(frame_run, text="Run Test", command=self.run_n6705c_test).pack(side="left", pady=10)
        ttk.Button(frame_run, text="Run Test2", command=self.run_n6705c_test2).pack(side="left", pady=10)


        # 仪器选择框架
        frame_instr = ttk.LabelFrame(self.content_frame, text="Instrument Selection", padding="10")
        #frame_instr.pack(side="left", padx=10, pady=10)(padx=10, pady=10, fill="both")
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


        # 通道选择框架
        frame_channel = ttk.LabelFrame(self.content_frame, text="Channel Selection", padding="10")
        frame_channel.pack(padx=10, pady=10, fill="both")
        self.channel_label = ttk.Label(frame_channel, text="Select Channel:")
        self.channel_label.pack(side="left", padx=5, pady=5)
        self.channel_var = tk.StringVar(self.content_frame)
        self.channel_var.set("CH1")  # 默认通道为CH1
        self.channel_menu = ttk.OptionMenu(frame_channel, self.channel_var, "CH1", "CH1", "CH2", "CH3", "CH4")
        self.channel_menu.pack(side="left", padx=5, pady=5)
        self.channel_on_button = ttk.Button(frame_channel, text="Channel ON", command=self.channel_on)
        self.channel_on_button.pack(side="left", padx=5, pady=5)
        self.channel_off_button = ttk.Button(frame_channel, text="Channel OFF", command=self.channel_off)
        self.channel_off_button.pack(side="left", padx=5, pady=5)

        # 电压设置和显示框架
        frame_voltage = ttk.LabelFrame(self.content_frame, text="Voltage Control", padding="10")
        frame_voltage.pack(padx=10, pady=10, fill="both")
        self.voltage_label = ttk.Label(frame_voltage, text="Voltage (V): N/A")
        self.voltage_label.pack(side="left", padx=5, pady=5)
        self.voltage_entry = ttk.Entry(frame_voltage)
        self.voltage_entry.pack(side="left", padx=5, pady=5)
        self.voltage_entry.insert(0, "Enter Voltage")
        self.set_voltage_button = ttk.Button(frame_voltage, text="Set Voltage", command=self.set_voltage)
        self.set_voltage_button.pack(side="left", padx=5, pady=5)

        # 电流限流设置和显示框架
        frame_current = ttk.LabelFrame(self.content_frame, text="Current Control", padding="10")
        frame_current.pack(padx=10, pady=10, fill="both")
        self.current_label = ttk.Label(frame_current, text="Current Limit (A): N/A")
        self.current_label.pack(side="left", padx=5, pady=5)
        self.current_entry = ttk.Entry(frame_current)
        self.current_entry.pack(side="left", padx=5, pady=5)
        self.current_entry.insert(0, "Enter Current Limit")
        self.set_current_button = ttk.Button(frame_current, text="Set Current Limit", command=self.set_current_limit)
        self.set_current_button.pack(side="left", padx=5, pady=5)

        # 电流显示框架
        frame_measured = ttk.LabelFrame(self.content_frame, text="Measured Values", padding="10")
        frame_measured.pack(padx=10, pady=10, fill="both")
        self.measured_voltage_label = ttk.Label(frame_measured, text="Measured Voltage (V): N/A")
        self.measured_voltage_label.pack(side="left", padx=5, pady=5)
        self.measured_current_label = ttk.Label(frame_measured, text="Measured Current (A): N/A")
        self.measured_current_label.pack(side="left", padx=5, pady=5)
        self.update_button = ttk.Button(frame_measured, text="Update Values", command=self.update_values)
        self.update_button.pack(side="left", padx=5, pady=5)

        # 电流显示框架
        frame_Tools = ttk.LabelFrame(self.content_frame, text="Tools", padding="10")
        frame_Tools.pack(padx=10, pady=10, fill="both")

        # ========== 输入变量 ==========
        self.I_limit = tk.StringVar()
        self.V1 = tk.StringVar()
        self.V2 = tk.StringVar()
        self.V3 = tk.StringVar()

        # ========== 第一行：输入框 ==========
        ttk.Label(frame_Tools, text="I_limit (mA)").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_Tools, textvariable=self.I_limit, width=10).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_Tools, text="V1 (V)").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_Tools, textvariable=self.V1, width=10).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_Tools, text="V2 (V)").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_Tools, textvariable=self.V2, width=10).grid(row=0, column=5, padx=5, pady=5)

        ttk.Label(frame_Tools, text="V3 (V)").grid(row=0, column=6, padx=5, pady=5, sticky="w")
        ttk.Entry(frame_Tools, textvariable=self.V3, width=10).grid(row=0, column=7, padx=5, pady=5)

        # ========== 第二行：按钮 ==========
        self.tool_set_mearsure_button = ttk.Button(
            frame_Tools,
            text="Measure Mode",
            command=self.set_measure_mode
        )
        self.tool_set_mearsure_button.grid(row=1, column=0, columnspan=2, padx=5, pady=8, sticky="w")

        self.tool_set_vol_button = ttk.Button(
            frame_Tools,
            text="Power Mode",
            command=self.set_power_suplly_mode
        )
        self.tool_set_vol_button.grid(row=1, column=2, columnspan=2, padx=5, pady=8, sticky="w")

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


    def update_voltage_label(self, text):
        self.measured_voltage_label.config(text=text)

    def update_current_limit_label(self, text):
        self.current_label.config(text=text)

    def update_measured_current_label(self, text):
        self.measured_current_label.config(text=text)

    def get_selected_channel(self):
        return self.channel_var.get()[-1]


    def set_measure_mode(self):
        self.controller.set_mode(2, "VMETer")
        self.controller.set_mode(3, "VMETer")
        self.controller.set_mode(4, "VMETer")

    def _get_float_or_default(self, var: tk.StringVar, default: float) -> float:
        try:
            value = var.get().strip()
            if value == "":
                return default
            return float(value)
        except ValueError:
            return default

    def set_power_suplly_mode(self):
        # ---------- 设置模式 ----------
        for ch in (2, 3, 4):
            self.controller.set_mode(ch, "PS2Q")

        # ---------- 读取输入（带默认值） ----------
        I_limit = self._get_float_or_default(self.I_limit, 0.02)
        V2 = self._get_float_or_default(self.V1, 0.8)
        V3 = self._get_float_or_default(self.V2, 1.3)
        V4 = self._get_float_or_default(self.V3, 1.7)

        # ---------- 设置电压 ----------
        self.controller.set_voltage(2, V2)
        self.controller.set_voltage(3, V3)
        self.controller.set_voltage(4, V4)

        # ---------- 设置限流 ----------
        for ch in (2, 3, 4):
            self.controller.set_current_limit(ch, I_limit)

        # ---------- 上电 ----------
        for ch in (2, 3, 4):
            self.controller.channel_on(ch)

    def run_n6705c_test(self):
        print("Running N6705C Test...")
        self.controller.set_mode(2, "PS2Q")
        self.controller.set_voltage(2, 0.45)
        self.controller.set_current_limit(2, 0.2)
        self.controller.channel_on(2)

    def run_n6705c_test2(self):
        print("Running N6705C Test2...")
        self.controller.set_mode(2, "CCLoad")
        self.controller.set_current(2, -0.2)
        self.controller.channel_on(2)

