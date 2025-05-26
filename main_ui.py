import tkinter as tk
from tkinter import ttk
from tkinter import Menu, Text
from tkinter import messagebox
from ins import ins_n6705c

from second_ui import chamber_ui
from second_ui import n6705c_ui
from second_ui import msox_ui
from second_ui import output_vol_ui
from second_ui import dcdc_eff_ui
from second_ui import charger_voreg_ui
from second_ui import charger_cc_ui
from second_ui import charger_iterm_ui
from second_ui import pmu_gpadc_test_ui

import  devicei2c
import time


class HexEntry(ttk.Entry):
    def __init__(self, *args, **kwargs):
        self.var = kwargs.pop('textvariable', tk.StringVar())
        super().__init__(*args, textvariable=self.var, **kwargs)
        self.var.trace_add('write', self.validate_hex)

    def validate_hex(self, *args):
        value = self.var.get()
        try:
            int(value, 16)
        except ValueError:
            if value:
                self.var.set(value[:-1])


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        # 其他代码
        self.controller = ins_n6705c.PowerSupplyController(self)  # 将self作为UI的引用传递
        # 其他代码


        # 设置主窗口的标题和尺寸
        self.title("KversK's APP")
        self.geometry("1000x1000")

        # 创建菜单栏
        self.create_menu_bar()

        # 初始化模块字典
        self.modules = {
            "Instrument": self.create_ins_module,
            "PMU Test": self.create_pmu_module,
            "Charger Test": self.create_charger_module
        }



        # 创建主框架
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=1)

        # 创建导航栏
        self.create_navigation_bar()

        # 创建内容区域框架
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        # 默认显示 "Instrument" 模块
        self.show_module("Instrument")


    def create_menu_bar(self):
        menu_bar = Menu(self)
        self.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.quit)

        help_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=lambda: self.show_module("About"))

    def create_navigation_bar(self):
        # 创建样式并配置背景色
        style = ttk.Style()
        style.configure('Nav.TFrame', background='#E1E8F6')

        # 定义一个新的样式用于菜单按钮
        style.configure('Nav.TMenubutton', background='#E1E8F6', font=("Arial", 12))

        # 应用自定义样式到frame
        nav_frame = ttk.Frame(self.main_frame, width=200, relief=tk.SUNKEN, style='Nav.TFrame')
        nav_frame.pack(side=tk.LEFT, fill=tk.Y)

        # 使用同样样式配置标签（如果需要）
        style.configure('Nav.TLabel', background='#E1E8F6', font=("Arial", 16))
        ttk.Label(nav_frame, text="Navigation", style='Nav.TLabel').pack(pady=10)

        for module_name in self.modules.keys():
            if module_name == "Instrument":
                self.create_instrument_submenu(nav_frame, style)
            elif module_name == "PMU Test":
                self.create_pmu_submenu(nav_frame, style)
            elif module_name == "Charger Test":
                self.create_charger_submenu(nav_frame, style)
            else:
                btn = ttk.Button(nav_frame, text=module_name,
                                 command=lambda m=module_name: self.show_module(m))
                btn.pack(fill=tk.X, padx=10, pady=5)

    def create_instrument_submenu(self, parent_frame, style):
        ins_button = ttk.Menubutton(parent_frame, text="Instrument", direction=tk.RIGHT, style="Nav.TMenubutton")

        # 创建菜单
        ins_menu = Menu(ins_button, tearoff=0)
        ins_button['menu'] = ins_menu

        # 配置Menu样式
        ins_menu.config(bg='#E1E8F6', activebackground='#C9D9F1')

        instruments = ["N6705C", "E36313A", "MOSX", "CHAMBER"]

        for item in instruments:
            ins_menu.add_command(label=item, command=lambda i=item: self.show_instrument(i))

        ins_button.pack(fill=tk.X, padx=10, pady=5)

    def create_pmu_submenu(self, parent_frame, style):
        pmu_button = ttk.Menubutton(parent_frame, text="PMU Test", direction=tk.RIGHT, style="Nav.TMenubutton")
        pmu_menu = Menu(pmu_button, tearoff=0)
        pmu_button['menu'] = pmu_menu

        # 配置Menu样式
        pmu_menu.config(bg='#E1E8F6', activebackground='#C9D9F1')

        pmu_tests = ["Output Voltage", "DCDC Efficiency", "Load Tran", "GPADC TEST"]

        for item in pmu_tests:
            pmu_menu.add_command(label=item, command=lambda i=item: self.show_pmu_test(i))

        pmu_button.pack(fill=tk.X, padx=10, pady=5)

    def create_charger_submenu(self, parent_frame, style):
        charger_button = ttk.Menubutton(parent_frame, text="Charger Test", direction=tk.RIGHT, style="Nav.TMenubutton")
        charger_menu = Menu(charger_button, tearoff=0)
        charger_button['menu'] = charger_menu

        # 配置Menu样式
        charger_menu.config(bg='#E1E8F6', activebackground='#C9D9F1')

        charger_tests = ["Voreg", "CC CURRENT", "Iterm CURRENT"]

        for item in charger_tests:
            charger_menu.add_command(label=item, command=lambda i=item: self.show_charger_test(i))

        charger_button.pack(fill=tk.X, padx=10, pady=5)

    def show_instrument(self, instrument_name):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if instrument_name == "N6705C":
            n6705c_ui_ac = n6705c_ui.N6705CUI(self.content_frame, self.controller)
            n6705c_ui_ac.create_n6705c_module()
        elif instrument_name == "CHAMBER":
            vt6002_ui_ac = chamber_ui.CHAMBER_UI(self.content_frame)
            vt6002_ui_ac.create_chamber_module()
            # self.create_vt6002_module()
        elif instrument_name == "MOSX":
            msox_ui_ac = msox_ui.MSOX_UI(self.content_frame)
            msox_ui_ac.create_msox_module()
        else:
            ttk.Label(self.content_frame, text=f"{instrument_name} Module", font=("Arial", 20)).pack(pady=20)
            ttk.Label(self.content_frame, text=f"Welcome to the {instrument_name} module!").pack(pady=10)

    def show_pmu_test(self, test_name):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        if test_name == "Output Voltage":
            output_vol_ui_ac = output_vol_ui.OUTPUT_VOL_UI(self.content_frame, self.controller)
            output_vol_ui_ac.create_output_voltage_module()
        elif test_name == "DCDC Efficiency":
            dcdc_eff_ui_ac = dcdc_eff_ui.DCDC_EFF_UI(self.content_frame, self.controller)
            dcdc_eff_ui_ac.create_dcdc_effiency_module()
        elif test_name == "GPADC TEST":
            gpadc_test_ui_ac = pmu_gpadc_test_ui.PMU_GPADC_TEST_UI(self.content_frame, self.controller)
            gpadc_test_ui_ac.create_pmu_gpadc_module()
        else:
            ttk.Label(self.content_frame, text=f"{test_name} Module", font=("Arial", 20)).pack(pady=20)
            ttk.Label(self.content_frame, text=f"Welcome to the {test_name} module!").pack(pady=10)

    def show_charger_test(self, test_name):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        if test_name == "Voreg":
            voreg_ac = charger_voreg_ui.VOREG_UI(self.content_frame, self.controller)
            voreg_ac.create_voreg_module()
        elif test_name == "CC CURRENT":
            charger_cc_ac = charger_cc_ui.CHARGER_CC_UI(self.content_frame, self.controller)
            charger_cc_ac.create_charger_cc_module()

        elif test_name == "Iterm CURRENT":
            charger_iterm_ac = charger_iterm_ui.CHARGER_ITERM_UI(self.content_frame, self.controller)
            charger_iterm_ac.create_iterm_module()

        else:
            ttk.Label(self.content_frame, text=f"{test_name} Module", font=("Arial", 20)).pack(pady=20)
            ttk.Label(self.content_frame, text=f"Details of {test_name} go here.").pack(pady=10)

    def show_module(self, module_name):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.modules[module_name]()

    def create_ins_module(self):
        ttk.Label(self.content_frame, text="Instrument Module", font=("Arial", 20)).pack(pady=20)
        ttk.Label(self.content_frame, text="Welcome to the Instrument module!").pack(pady=10)


    # def set_voltage(self):
    #     voltage = self.voltage_entry.get()
    #     channel = self.channel_var.get()[-1]
    #     self.controller.set_voltage(channel, voltage)
    #
    #
    # def set_current_limit(self):
    #     current = self.current_entry.get()
    #     channel = self.channel_var.get()[-1]
    #     self.controller.set_current_limit(channel, current)
    #
    # def channel_on(self):
    #     channel = self.channel_var.get()[-1]
    #     self.controller.channel_on(channel)
    #
    # def channel_off(self):
    #     channel = self.channel_var.get()[-1]
    #     self.controller.channel_off(channel)
    #
    # def set_voltagemode(self):
    #     channel = self.channel_var.get()[-1]
    #     self.controller.set_voltagemode(channel)



    # def update_status(self, status, color):
    #     self.status_label.config(text=f"Status: {status}", foreground=color)

    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def show_warning(self, title, message):
        messagebox.showwarning(title, message)




    def create_pmu_module(self):
        ttk.Label(self.content_frame, text="PMU Test Module", font=("Arial", 20)).pack(pady=20)
        ttk.Label(self.content_frame, text="PMU Test details go here.").pack(pady=10)





    def create_charger_module(self):
        ttk.Label(self.content_frame, text="Charger Test Module", font=("Arial", 20)).pack(pady=20)
        ttk.Label(self.content_frame, text="Charger Test details go here.").pack(pady=10)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
