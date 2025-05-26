from tkinter import filedialog
import pyvisa
import io
import numpy as np
import time
from tkinter import messagebox


class MSOX_OSCILLSCOPE:
    def __init__(self, resource_name):
        self.resource_name = resource_name
        self.rm = pyvisa.ResourceManager()
        self.scope = None

    def connect(self, resource_name="USB0::2391::6076::MY56180423::INSTR"):
        try:
            self.scope = self.rm.open_resource(resource_name, open_timeout=1)
            self.scope.write("*CLS")
            self.scope.timeout = 2000
        except pyvisa.VisaIOError:
            messagebox.showerror("Connection Error", "Failed to connect to the instrument.")

    def disconnect(self):
        if self.scope is not None:
            self.scope.close()
            self.scope = None

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

    def set_parameters(self, channel='1'):
        if self.scope is not None:
            # us
            time_scale = 0.001
            trigger_type = "EDGE"
            # V
            vertical_scale = 0.01
            # V
            dc_offset = 0.1
            try:
                # Set the time_scale
                self.scope.write(f":TIMebase:SCALe {time_scale}")
                # Set the trigger type
                self.scope.write(f":TRIGger:{trigger_type}:MODE AUTO")
                # Set the vertical scale
                self.scope.write(f":CHANnel{channel}:SCALe {vertical_scale}")
                time.sleep(0.01)
                # Set the DC Offset
                self.scope.write(f":CHANnel{channel}:OFFSet {dc_offset}")

                messagebox.showinfo("Parameters Set",
                                    "Time scale, trigger type, vertical scale, and DC Offset set successfully for Channel " + channel)
            except pyvisa.VisaIOError:
                messagebox.showerror("Parameter Error", "Failed to set parameters.")
        else:
            messagebox.showerror("Connection Error", "Not connected to the instrument.")

    def capture_screenshot(self):
        if self.scope is not None:
            try:
                delay = None,
                # 发送截图命令，确保使用文档中指定的正确格式
                # self.scope.write(":DISPlay:DATA? PNG, COLOR")
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


if __name__ == "__main__":
    visaname = "USB0::2391::6076::MY56180423::INSTR"
    msox4154a = MSOX_OSCILLSCOPE(visaname)
    msox4154a.connect()
    print(msox4154a.measure_frequency('4'))
    msox4154a.capture_screenshot()
    msox4154a.disconnect()