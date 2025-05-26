import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
from drv import vt6002
from drv import mt3065

instr_list = ["vt6002", "mt3065"]

class CHAMBER_UI:
    def __init__(self, content_frame):
        self.content_frame = content_frame
        self.chamber = None
        self.updating = False
        self.style = ttk.Style()

        # 配置自定义样式
        self.style.configure("TempDisplay.TFrame", background="#2E2E2E", borderwidth=2, relief="sunken")
        self.style.configure("TempLabel.TLabel",
                           font=("DS-Digital", 24, "bold"),
                           foreground="#00FF00",
                           background="#2E2E2E",
                           padding=5)
        self.style.configure("StatusLight.TLabel",
                           width=3,
                           background="gray",
                           borderwidth=2,
                           relief="raised")

    def create_chamber_module(self):
        # 外层标签
        ttk.Label(self.content_frame, text="Chamber", font=("Arial", 20)).grid(row=0, column=0, pady=20, sticky="nsew")

        # 仪器选择框架
        frame_instr = ttk.LabelFrame(self.content_frame, text="Instrument Selection", padding="10")
        frame_instr.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # 仪器选择组件
        self.instr_label = ttk.Label(frame_instr, text="Select Instrument:")
        self.instr_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.instr_list = instr_list
        self.instr_var = tk.StringVar(self.content_frame)
        self.instr_var.set(self.instr_list[0])
        self.instr_menu = ttk.OptionMenu(frame_instr, self.instr_var, self.instr_list[0], *self.instr_list)
        self.instr_menu.grid(row=0, column=1, padx=5, pady=5)

        self.com_ports = serial.tools.list_ports.comports()
        self.instr_com_var = tk.StringVar(self.content_frame)
        self.instr_com_var.set(self.com_ports[0])
        self.instr_com_menu = ttk.OptionMenu(frame_instr, self.instr_com_var, self.com_ports[0], *self.com_ports)
        self.instr_com_menu.grid(row=0, column=2, padx=5, pady=5)

        self.status_label = ttk.Label(frame_instr, text="Status: Disconnected", foreground="red")
        self.status_label.grid(row=0, column=3, padx=5, pady=5)

        # 按钮行
        self.channel_on_button = ttk.Button(frame_instr, text="Connect", command=self.connect)
        self.channel_on_button.grid(row=1, column=0, padx=5, pady=5)

        self.channel_off_button = ttk.Button(frame_instr, text="Disconnect", command=self.disconnect)
        self.channel_off_button.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame_instr, text="Help", command=self.help_eff).grid(row=1, column=2, padx=5, pady=5)

        # 修改后的Instrument Control框架
        ins_ctrl = ttk.LabelFrame(self.content_frame, text="Instrument Control", padding="10")
        ins_ctrl.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # 温度控制区
        temp_frame = ttk.Frame(ins_ctrl)
        temp_frame.grid(row=1, column=0, columnspan=5, pady=10, sticky="ew")

        # 目标温度设置
        self.target_temp = tk.StringVar(self.content_frame)
        ttk.Label(temp_frame, text="Target Temperature:").grid(row=0, column=0, padx=5)
        ttk.Entry(temp_frame, textvariable=self.target_temp, width=8).grid(row=0, column=1, padx=5)
        ttk.Button(temp_frame, text="SET", command=self.set_temp, width=6).grid(row=0, column=2, padx=5)

        # 当前温度显示面板
        display_frame = ttk.Frame(temp_frame, style="TempDisplay.TFrame")
        display_frame.grid(row=0, column=3, padx=10)

        ttk.Label(display_frame, text="Current Temperature:",
                  font=("Arial", 9)).pack(side=tk.TOP, pady=(0, 5))

        self.current_temp_var = tk.StringVar(value="--.- °C")
        self.temp_display = ttk.Label(display_frame,
                                      textvariable=self.current_temp_var,
                                      style="TempLabel.TLabel")
        self.temp_display.pack(side=tk.TOP)

        # 状态指示灯
        self.status_light = ttk.Label(temp_frame, style="StatusLight.TLabel")
        self.status_light.grid(row=0, column=4, padx=5)

        # 运行测试框架
        frame_run = ttk.LabelFrame(self.content_frame, text="RUN TEST", padding="10")
        frame_run.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        # 运行测试按钮
        ttk.Button(frame_run, text="Run Test", command=self.run_vt6002_test).grid(row=0, column=0, pady=10)

        # 配置父容器的网格布局权重
        self.content_frame.grid_columnconfigure(0, weight=1)
        frame_instr.grid_columnconfigure((0, 1, 2, 3), weight=0)
        frame_run.grid_columnconfigure(0, weight=1)

    def update_temperature(self):
        if self.chamber and self.updating:
            try:
                temp = self.chamber.get_temp()
                self.current_temp_var.set(f"{temp:.1f} °C")
                self.update_display_color(float(temp))
                self.status_light.config(background="green")
            except Exception as e:
                self.current_temp_var.set("ERR °C")
                self.status_light.config(background="red")
            finally:
                self.content_frame.after(1000, self.update_temperature)

    def update_display_color(self, temperature):
        """根据温度值更新显示颜色"""
        if temperature < 0:
            color = "#00BFFF"  # 低温蓝色
        elif 0 <= temperature < 50:
            color = "#00FF00"  # 正常绿色
        elif 50 <= temperature < 80:
            color = "#FFA500"  # 警告橙色
        else:
            color = "#FF0000"  # 危险红色
        self.style.configure("TempLabel.TLabel", foreground=color)

    def chamber_on(self):
        if self.chamber:
            self.chamber.start()
        self.updating = False
        self.current_temp_label.config(text="N/A")
        print("chamber_on")


    def chamber_off(self):
        if self.chamber:
            self.chamber.stop()
        self.updating = False
        self.current_temp_label.config(text="N/A")
        print("chamber_off")

    def set_temp(self):
        target_temp = self.target_temp.get()
        if self.chamber:
            self.chamber.set_temperature(target_temp)

    def connect(self):
        try:
            if self.instr_var.get() == "vt6002":
                port = self.instr_com_var.get()
                self.chamber = vt6002.VT6002(port)
                self.updating = True
                self.status_label.config(text="Status: Connected", foreground="green")
                self.status_light.config(background="green")
                self.update_temperature()
        except Exception as e:
            self.status_label.config(text="Status: Connection Failed", foreground="red")
            self.status_light.config(background="red")


    def disconnect(self):
        self.updating = False
        if self.chamber:
            self.chamber.close()
        self.status_label.config(text="Status: Disconnected", foreground="red")
        self.current_temp_var.set("--.- °C")
        self.status_light.config(background="gray")
        self.style.configure("TempLabel.TLabel", foreground="#00FF00")
    def help_eff(self):
        print("discon")

    def run_vt6002_test(self):
        print("Running run_vt6002_test Test...")
