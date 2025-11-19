import tkinter as tk
from tkinter import ttk, filedialog
import pyvisa
import io
import numpy as np
import time
from tkinter import Menu, Text
from tkinter import messagebox
import pyautogui
from PIL import Image
import pyperclip
from io import BytesIO
from drv import mt3065

from tm_devices import DeviceManager
from tm_devices.drivers import MSO6B



class MSO64B_UI:
    def __init__(self, content_frame):
        self.content_frame = content_frame
        self.rm = pyvisa.ResourceManager()
        self.scope = None

    def create_mso64b_module(self):
        ttk.Label(self.content_frame, text=f"MSO64B Oscilloscope", font=("Arial", 20)).pack(pady=20)
        # Instrument Selection Frame
        frame_instr = ttk.LabelFrame(self.content_frame, text="Instrument Selection", padding="10")
        frame_instr.pack(padx=10, pady=10, fill="both")

        self.instr_label = ttk.Label(frame_instr, text="Select Instrument:")
        self.instr_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.instr_list = self.rm.list_resources()
        self.instr_var = tk.StringVar(self.content_frame)
        # print(self.instr_list[0])
        self.instr_var.set(self.instr_list[0] if self.instr_list else "No instruments found")
        self.instr_menu = ttk.OptionMenu(frame_instr, self.instr_var, *self.instr_list)
        self.instr_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.status_label = ttk.Label(frame_instr, text="Status: Disconnected", foreground="red")
        self.status_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.connect_button = ttk.Button(frame_instr, text="Connect", command=self.connect)
        self.connect_button.grid(row=0, column=3, padx=5, pady=5)
        self.disconnect_button = ttk.Button(frame_instr, text="Disconnect", command=self.disconnect)
        self.disconnect_button.grid(row=0, column=4, padx=5, pady=5)

        # Oscilloscope Control Frame
        frame_control = ttk.LabelFrame(self.content_frame, text="Oscilloscope Control", padding="10")
        frame_control.pack(padx=10, pady=10, fill="both")

        # Channel Selection
        self.channel_var = tk.StringVar(self.content_frame)
        self.channel_var.set("1")  # default to channel 1
        channel_label = ttk.Label(frame_control, text="Select Channel:")
        channel_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.channel_menu = ttk.OptionMenu(frame_control, self.channel_var, "1", "1", "2", "3", "4")
        self.channel_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Time Scale Entry
        self.time_scale_entry = ttk.Entry(frame_control)
        self.time_scale_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(frame_control, text="Time Scale (s/div):").grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Trigger Type Entry
        self.trigger_type_entry = ttk.Entry(frame_control)
        self.trigger_type_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(frame_control, text="Trigger Type (e.g., EDGE, VIDEO):").grid(row=2, column=0, padx=5, pady=5,
                                                                                sticky="w")

        # Vertical Scale Entry
        self.vertical_scale_entry = ttk.Entry(frame_control)
        self.vertical_scale_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(frame_control, text="Vertical Scale (V/div):").grid(row=3, column=0, padx=5, pady=5, sticky="w")

        # DC Offset Entry
        self.dc_offset_entry = ttk.Entry(frame_control)
        self.dc_offset_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(frame_control, text="DC Offset (V):").grid(row=4, column=0, padx=5, pady=5, sticky="w")

        # Set Parameters Button
        self.set_params_button = ttk.Button(frame_control, text="Set Parameters", command=self.set_parameters)
        self.set_params_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Acquire Data Button
        self.acquire_button = ttk.Button(frame_control, text="Acquire Data", command=self.acquire_data)
        self.acquire_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Screenshot Button
        self.screenshot_button = ttk.Button(frame_control, text="Capture Screenshot", command=self.capture_screenshot)
        self.screenshot_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Data Display Frame
        frame_data = ttk.LabelFrame(self.content_frame, text="Data Display", padding="10")
        frame_data.pack(padx=10, pady=10, fill="both")

        self.data_label = ttk.Label(frame_data, text="Waveform Data: Not Acquired")
        self.data_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Function Button Frame
        fun_button_data = ttk.LabelFrame(self.content_frame, text="Function Set", padding="10")
        fun_button_data.pack(padx=10, pady=10, fill="both")

        self.set_ripple_test_button = ttk.Button(fun_button_data, text="Ripple", command=self.set_ripple_mode)
        self.set_ripple_test_button.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.set_test_button = ttk.Button(fun_button_data, text="Test", command=self.test_func)
        self.set_test_button.grid(row=0, column=5, columnspan=2, padx=5, pady=5, sticky="ew")

        # Function Button Frame
        fun_button_data = ttk.LabelFrame(self.content_frame, text="TEST", padding="10")
        fun_button_data.pack(padx=10, pady=10, fill="both")

        self.set_test_f_test_button = ttk.Button(fun_button_data, text="TEST", command=self.test_func_mso64b)
        self.set_test_f_test_button.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")


    def connect(self):
        try:
            resource_name = self.instr_var.get()
            # resource_name = "USB0::2391::6076::MY56180423::INSTR"
            self.scope = self.rm.open_resource(resource_name, open_timeout=1)
            self.scope.write("*CLS")

            self.scope.timeout = 2000
            self.status_label.config(text="Status: Connected", foreground="green")
        except pyvisa.VisaIOError:
            messagebox.showerror("Connection Error", "Failed to connect to the instrument.")
            self.status_label.config(text="Status: Disconnected", foreground="red")

    def disconnect(self):
        if self.scope is not None:
            self.scope.close()
            self.scope = None
            self.status_label.config(text="Status: Disconnected", foreground="red")


    def power_on_seq_test(self):
        with DeviceManager(verbose=True) as device_manager:
            scope: MSO6B = device_manager.add_scope("192.168.3.24")

            # Specifying source as Channel1
            scope.commands.display.select.source.write("CH1")
            scope.commands.ch[1].scale.write(0.5)
            scope.commands.ch[1].position.write(-3)
            scope.commands.ch[1].bandwidth.write(20)

            scope.commands.display.select.source.write("CH2")
            scope.commands.ch[2].scale.write(0.5)
            scope.commands.ch[2].position.write(-3)
            scope.commands.ch[2].bandwidth.write(20)

            scope.commands.display.select.source.write("CH3")
            scope.commands.ch[3].scale.write(0.5)
            scope.commands.ch[3].position.write(-3)
            scope.commands.ch[3].bandwidth.write(20)

            scope.commands.display.select.source.write("CH4")
            scope.commands.ch[4].scale.write(0.5)
            scope.commands.ch[4].position.write(-3)
            scope.commands.ch[4].bandwidth.write(20)

            scope.commands.horizontal.scale.write("0.005")
            scope.commands.horizontal.position.write(10)

            scope.commands.trigger.a.type.write("EDGE")
            scope.commands.trigger.a.edge.source.write("CH1")

            # ✅ 设置 CH1 的触发电平为 1.0V
            scope.commands.trigger.a.level.ch[1].write(0.3)

            scope.commands.acquire.state.write("ON")
            scope.commands.acquire.mode.write("Sample")
            scope.commands.acquire.stopafter.write("Sequence")

            # Identifying pk2pk as the measurement we would like to make
            # scope.commands.measurement.addmeas.write("PK2Pk-")
            # scope.commands.opc.query()

            # # Store the value locally before we print
            # chlpk2pk = float(scope.commands.measurement.meas[1].results.allacqs.mean.query())
            # print(f'Channel 1 pk2pk: {chlpk2pk}')

            scope.save_screenshot()

            # Save a screenshot as "example.png". This will create a screenshot on the device,
            # copy it to the current working directory on the local machine,
            # and then delete the screenshot file from the device.
            scope.save_screenshot("PowerOn Seq.png")

            # Save a screenshot as "example.jpg". This will create a screenshot on the device
            # using INVERTED colors in the "./device_folder" folder,
            # copy it to "./images/example.jpg" on the local machine,
            # but this time the screenshot file on the device will not be deleted.
            scope.save_screenshot(
                "PowerOn Seq.jpg",
                colors="INVERTED",
                local_folder="./images",
                device_folder="./device_folder",
                keep_device_file=True,
            )

    def ripple_test(self):
        with DeviceManager(verbose=True) as device_manager:
            scope: MSO6B = device_manager.add_scope("192.168.3.24")
            scope.commands.measurement.deleteall.write()
            scope.commands.display.waveview1.ch[1].state.write("OFF")
            scope.commands.display.waveview1.ch[2].state.write("OFF")
            scope.commands.display.waveview1.ch[3].state.write("OFF")
            scope.commands.display.waveview1.ch[4].state.write("OFF")
            # Specifying source as Channel1
            # scope.commands.display.select.source.write("CH1")
            # scope.commands.ch[1].scale.write(0.01)
            # scope.commands.ch[1].position.write(-3)
            # scope.commands.ch[1].bandwidth.write(20)

            scope.commands.display.select.source.write("CH2")
            scope.commands.ch[2].scale.write(0.01)
            scope.commands.ch[2].position.write(-3)
            scope.commands.ch[2].bandwidth.write(20)
            scope.commands.ch[2].coupling.write("AC")

            scope.commands.display.select.source.write("CH3")
            scope.commands.ch[3].scale.write(0.01)
            scope.commands.ch[3].position.write(0)
            scope.commands.ch[3].bandwidth.write(20)
            scope.commands.ch[3].coupling.write("AC")

            scope.commands.display.select.source.write("CH4")
            scope.commands.ch[4].scale.write(0.01)
            scope.commands.ch[4].position.write(3)
            scope.commands.ch[4].bandwidth.write(20)
            scope.commands.ch[4].coupling.write("AC")

            scope.commands.horizontal.scale.write("0.005")
            scope.commands.horizontal.position.write(10)

            scope.commands.trigger.a.type.write("EDGE")
            scope.commands.trigger.a.edge.source.write("CH1")

            # ✅ 设置 CH1 的触发电平为 1.0V
            scope.commands.trigger.a.level.ch[1].write(0.3)

            scope.commands.acquire.state.write("ON")
            scope.commands.acquire.mode.write("Sample")
            scope.commands.acquire.stopafter.write("RUNSTop")

            scope.commands.measurement.addmeas.write("MEAN")
            scope.commands.measurement.addmeas.write("PK2PK")
            scope.commands.measurement.meas[1].source.write("CH2")
            scope.commands.measurement.meas[2].source.write("CH2")

            scope.commands.measurement.addmeas.write("MEAN")
            scope.commands.measurement.addmeas.write("PK2PK")
            scope.commands.measurement.meas[3].source.write("CH3")
            scope.commands.measurement.meas[4].source.write("CH3")

            scope.commands.measurement.addmeas.write("MEAN")
            scope.commands.measurement.addmeas.write("PK2PK")
            scope.commands.measurement.meas[5].source.write("CH4")
            scope.commands.measurement.meas[6].source.write("CH4")

    def measure_VAVerage(self, channel, interval="DISPlay"):
        # 构建查询命令
        command = f":MEASure:VAVerage? {interval},CHANnel{channel}"

        # 通过设备查询指令获取该通道的平均值
        VAVerage = self.scope.query(command)
        # 返回获取到的结果
        return VAVerage

    def measure_VPP(self, channel):
        return self.scope.query(f":MEASure:VPP? CHANnel{channel}")

    def measure_counter(self, channel):
        return self.scope.query(f":MEASure:COUNter? CHANnel{channel}")

    def measure_frequency(self, channel):
        return self.scope.query(f":MEASure:FREQuency? CHANnel{channel}")

    def measure_period(self, channel):
        return self.scope.query(f" :MEASure:PERiod? CHANnel{channel}")

    def measure_area(self, channel, interval="DISPlay"):
        return self.scope.query(f":MEASure:AREa? {interval},CHANnel{channel}")

    def measure_clear(self):
        return self.scope.write(f":MEASure:CLEar")

    def measure_results(self):
        res = self.scope.write(f":MEASure:RESults?")
        return res

    def get_RSTate(self):
        return self.scope.query(f":RSTate?")

    def run_control(self, state):
        # <state> ::= {RUN | STOP | SINGle }
        return self.scope.write(f":{state}")

    def set_time_scale(self, time_scale):
        self.scope.write(f":TIMebase:SCALe {time_scale}")

    def set_vertical_scale(self, channel, vertical_scale):
        self.scope.write(f":CHANnel{channel}:SCALe {vertical_scale}")

    def set_bwlimit_on(self, channel):
        self.scope.write(f":CHANnel{channel}:BWLimit ON")

    def set_time_delay(self, delay):
        # dc_offset = 0.65
        self.scope.write(f":TIMebase:DELay {delay}")

    def set_trigger_sweep(self, mode="AUTO"):
        # dc_offset = 0.65
        # mode:   AUTO | NORMAL
        self.scope.write(f":TRIGger:SWEep {mode}")

    def set_trigger_channel(self, channel):
        # dc_offset = 0.65
        self.scope.write(f":TRIGger:EDGE:SOURce CHANnel{channel}")

    def set_trigger_level(self, level):
        # dc_offset = 0.65
        self.scope.write(f":TRIGger:EDGE:LEVel {level}")

    def set_trigger_slope(self, slpoe="POSitive"):
        # <slope> ::= {NEGative | POSitive | EITHer | ALTernate}
        self.scope.write(f":TRIGger:EDGE:SLOPe {slpoe}")

    def set_force_trigger(self):
        # <slope> ::= {NEGative | POSitive | EITHer | ALTernate}
        self.scope.write(f":TRIGger:FORCe")

    def set_dc_offset(self, channel, dc_offset):
        # dc_offset = 0.65
        self.scope.write(f":CHANnel{channel}:OFFSet {dc_offset}")

    def channel_on(self, channel):
        self.scope.write(f":CHANnel{channel}:DISPlay ON")

    def channel_off(self, channel):
        self.scope.write(f":CHANnel{channel}:DISPlay OFF")

    def test_func(self):
        print(self.measure_frequency('4'))
        #print(self.measure_results())
    def test_func_mso64b(self):
        with DeviceManager(verbose=True) as device_manager:
            scope : MSO6B = device_manager.add_scope("192.168.3.24")

            # Specifying source as Channel1
            scope.commands.display.select.source.write("CH1")
            scope.commands.ch[1].scale.write(0.5)
            scope.commands.ch[1].position.write(-3)
            scope.commands.ch[1].bandwidth.write(20)
            scope.commands.display.select.source.write("CH2")
            scope.commands.ch[2].scale.write(0.5)
            scope.commands.ch[2].position.write(-3)
            scope.commands.ch[2].bandwidth.write(20)
            scope.commands.display.select.source.write("CH3")
            scope.commands.ch[3].scale.write(0.5)
            scope.commands.ch[3].position.write(-3)
            scope.commands.ch[3].bandwidth.write(20)
            scope.commands.display.select.source.write("CH4")
            scope.commands.ch[4].scale.write(0.5)
            scope.commands.ch[4].position.write(-3)
            scope.commands.ch[4].bandwidth.write(20)
            scope.commands.horizontal.scale.write("0.01")
            scope.commands.horizontal.position.write(10)
            scope.commands.trigger.a.type.write("EDGE")
            scope.commands.trigger.a.level.ch.write(1)
            # Identifying pk2pk as the measurement we we would like to make
            scope.commands.measurement.addmeas.write("PK2Pk-")
            # Make sure the operation is complete using the opc command
            scope.commands.opc.query()
            # Store the value locally before we print
            chlpk2pk = float(scope.commands.measurement.meas[1].results.allacqs.mean.query())
            # Printing the value onto the console
            print(f'Channel 1 pk2pk: {chlpk2pk}')

        #print(self.measure_results())

    def set_ripple_mode(self):
        self.set_time_scale(0.001)
        self.set_trigger_sweep("AUTO")
        self.set_bwlimit_on('1')
        self.set_bwlimit_on('2')
        self.set_bwlimit_on('3')
        self.set_bwlimit_on('4')
        self.set_vertical_scale('1', 0.5)
        self.set_vertical_scale('2', 0.5)
        self.set_vertical_scale('3', 0.5)
        self.set_vertical_scale('4', 0.5)
        self.set_dc_offset('1', 0)
        self.set_dc_offset('2', 0)
        self.set_dc_offset('3', 0)
        self.set_dc_offset('4', 0)
        time.sleep(0.1)
        temp_value_ch1 = self.measure_VAVerage('1')
        time.sleep(0.1)
        temp_value_ch2 = self.measure_VAVerage('2')
        time.sleep(0.1)
        temp_value_ch3 = self.measure_VAVerage('3')
        time.sleep(0.1)
        temp_value_ch4 = self.measure_VAVerage('4')
        temp_value_ch1 = str(f"%.3f" % (float(temp_value_ch1) + 0.03))
        temp_value_ch2 = str(f"%.3f" % (float(temp_value_ch2) + 0.01))
        temp_value_ch3 = str(f"%.3f" % (float(temp_value_ch3) - 0.01))
        temp_value_ch4 = str(f"%.3f" % (float(temp_value_ch4) - 0.03))
        self.set_vertical_scale('1', 0.01)
        self.set_vertical_scale('2', 0.01)
        self.set_vertical_scale('3', 0.01)
        self.set_vertical_scale('4', 0.01)
        self.set_dc_offset('1', temp_value_ch1)
        self.set_dc_offset('2', temp_value_ch2)
        self.set_dc_offset('3', temp_value_ch3)
        self.set_dc_offset('4', temp_value_ch4)
        self.set_time_scale(0.00001)
        self.measure_clear()

    def set_parameters(self):
        if self.scope is not None:
            channel = self.channel_var.get()
            try:
                # Set the time scale
                time_scale = self.time_scale_entry.get()
                self.scope.write(f":TIMebase:SCALe {time_scale}")

                # Set the trigger type
                trigger_type = self.trigger_type_entry.get()
                self.scope.write(f":TRIGger:{trigger_type}:MODE AUTO")

                # Set the vertical scale
                vertical_scale = self.vertical_scale_entry.get()
                self.scope.write(f":CHANnel{channel}:SCALe {vertical_scale}")
                time.sleep(0.01)
                # Set the DC Offset
                dc_offset = self.dc_offset_entry.get()

                self.scope.write(f":CHANnel{channel}:OFFSet {dc_offset}")

                messagebox.showinfo("Parameters Set",
                                    "Time scale, trigger type, vertical scale, and DC Offset set successfully for Channel " + channel)
            except pyvisa.VisaIOError:
                messagebox.showerror("Parameter Error", "Failed to set parameters.")
        else:
            messagebox.showerror("Connection Error", "Not connected to the instrument.")

    def acquire_data(self):
        if self.scope is not None:
            channel = self.channel_var.get()
            try:
                self.scope.write(f":WAVeform:SOURce CHANnel{channel}")
                self.scope.write(":WAVeform:FORMat ASCII")
                data = self.scope.query(":WAVeform:DATA?")
                print("Debug - Raw Data:", repr(data))

                start_index = data.find(',')
                if start_index != -1:
                    data = data[start_index:]

                clean_data = data.strip()
                if clean_data:
                    data_io = io.StringIO(clean_data)
                    waveform_data = np.genfromtxt(data_io, delimiter=',')
                    if waveform_data.size > 0:
                        self.data_label.config(text=f"Waveform Data: {waveform_data[:10]}...")
                    else:
                        self.data_label.config(text="Waveform Data: Empty or Invalid Format")
                else:
                    self.data_label.config(text="Waveform Data: No Data Returned or Invalid Data")
            except pyvisa.VisaIOError:
                messagebox.showerror("Data Acquisition Error", "Failed to acquire waveform data.")
        else:
            messagebox.showerror("Connection Error", "Not connected to the instrument.")

    def capture_screenshot(self):
        if self.scope is not None:
            try:
                delay = None,
                # 发送截图命令，确保使用文档中指定的正确格式
                #self.scope.write(":DISPlay:DATA? PNG, COLOR")
                # 使用 read_raw() 读取大量的二进制数据
                rstate = self.get_RSTate()
                print(rstate)
                self.run_control("STOP")
                self.scope.write(":DISPlay:DATA? PNG, COLor")
                time.sleep(1)
                raw_image_data = self.scope.read_binary_values(datatype='s', container=bytes, )
                self.run_control(rstate)
                # with open(setup_file_name, "wb") as f:
                #     f.write(raw_image_data)
                # print(f"Setup bytes saved: {len(raw_image_data)}")
                if raw_image_data:
                    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                             filetypes=[("PNG files", "*.png")])
                    if file_path:
                        with open(file_path, "wb") as img_file:
                            img_file.write(raw_image_data)
                        messagebox.showinfo("Screenshot Captured", f"Screenshot saved as {file_path}")
                else:
                    messagebox.showerror("Screenshot Error", "No data received from the oscilloscope.")
            except pyvisa.VisaIOError as e:
                messagebox.showerror("Screenshot Error", f"Failed to capture screenshot: {str(e)}")
        else:
            messagebox.showerror("Connection Error", "Not connected to the instrument.")

    def run_msox_test(self):
        print("Running run_msox_test Test...")
