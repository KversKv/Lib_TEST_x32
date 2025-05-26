import pyvisa
rm = pyvisa.ResourceManager('@py')
from drv import e36313a
from drv import n6705c
from second_ui import n6705c_ui
import time


class PowerSupplyController():
    def __init__(self, ui):
        self.rm = pyvisa.ResourceManager()
        self.instr = None
        self.instr_lib = None
        self.keep_updating = True
        self.ui = ui  # 保存UI的引用

    # 其他方法中，你现在可以通过self.ui访问UI实例的方法和属性

    def write_t(self, command):
        return self.instr.write(command)

    def query_t(self, command):
        return self.instr.query(command)

    def arb_set_staircafe(self, channel, start_value, stop_value):
        self.instr.write(f"VOLT:MODE ARB, (@{channel})")
        self.instr.write(f"ARB:FUNC:TYPE VOLT, (@{channel})")
        self.instr.write(f"ARB:FUNC:SHAP STA, (@{channel})")
        self.instr.write(f"ARB:VOLT:STA:STAR {start_value}, (@{channel})")
        self.instr.write(f"ARB:VOLT:STA:END {stop_value}, (@{channel})")
        self.instr.write(f"ARB:VOLT:STA:STAR:TIM 0.2, (@{channel})")
        self.instr.write(f"ARB:VOLT:STA:TIM 10, (@{channel})")
        self.instr.write(f"ARB:VOLT:STA:END:TIM 0.2, (@{channel})")
        self.instr.write(f"ARB:VOLT:STA:NST 500, (@{channel})")
        self.instr.write("VOLT:MODE ARB, (@1)")
        self.instr.write(f"TRIG:ARB:SOUR BUS")
        self.instr.write(f"INIT:TRAN (@{channel})")

    def dlog_config(self, channel):
        self.instr.write(f"SENS:DLOG:FUNC:VOLT OFF, (@1)")
        self.instr.write(f"SENS:DLOG:FUNC:CURR OFF, (@1)")
        self.instr.write(f"SENS:DLOG:FUNC:VOLT OFF, (@2)")
        self.instr.write(f"SENS:DLOG:FUNC:CURR OFF, (@2)")
        self.instr.write(f"SENS:DLOG:FUNC:VOLT OFF, (@3)")
        self.instr.write(f"SENS:DLOG:FUNC:CURR OFF, (@3)")
        self.instr.write(f"SENS:DLOG:FUNC:VOLT OFF, (@3)")
        self.instr.write(f"SENS:DLOG:FUNC:CURR OFF, (@3)")
        self.instr.write(f"SENS:DLOG:FUNC:VOLT ON, (@{channel})")
        self.instr.write(f"SENS:DLOG:FUNC:CURR ON, (@{channel})")
        self.instr.write(f"SENS:DLOG:CURR:RANG:AUTO ON, (@{channel})")
        self.instr.write(f"SENS:DLOG:VOLT:RANG:AUTO ON, (@{channel})")
        self.instr.write(f"SENS:DLOG:TIME 12")
        self.instr.write(f"SENS:DLOG:PER .0001")
        self.instr.write("TRIG:DLOG:SOUR BUS")
        self.instr.write("INIT:DLOG \"internal:\\data1.dlog\"")

    def export_file(self):
        self.instr.write("MMEM:EXP:DLOG \"datalog1.csv\"")

    def BUS_TRG(self):
        self.instr.write("*TRG")

    def connect(self, resource_name):
        """
        连接到选择的仪器
        """
        try:
            self.instr = self.rm.open_resource(resource_name)
            self.instr.write("*CLS")  # 清除状态
            self.instr.timeout = 30000  # 设置读取超时时间为2000ms
            self.ui.update_status("Connected", "green")
            self.keep_updating = True  # 连接成功后允许更新
            self.identify_instrument()
        except pyvisa.VisaIOError as e:
            self.ui.show_error("Connection Error", f"Failed to connect to the instrument: {e}")
            self.ui.update_status("Disconnected", "red")

    def identify_instrument(self):
        """
        识别仪器类型并加载相应的库
        """
        try:
            idn_response = self.instr.query("*IDN?")
            if "E36313A" in idn_response:
                self.instr_lib = e36313a.E36313A(self.instr)
            elif "N6705C" in idn_response:
                self.instr_lib = n6705c.N6705C(self.instr)
            else:
                self.instr_lib = None
                self.ui.show_warning("Unknown Instrument", "The connected instrument is not recognized.")
        except pyvisa.VisaIOError as e:
            self.ui.show_error("Identification Error", f"Failed to identify the instrument: {e}")
            self.instr_lib = None

    def disconnect(self):
        """
        断开与仪器的连接
        """
        if self.instr is not None:
            self.instr.close()
            self.instr = None
            self.ui.update_status("Disconnected", "red")
            self.keep_updating = False  # 断开连接后停止更新

    def set_current(self, channel, current):
        """
        设置选择的通道的电压
        """
        if self.instr_lib is not None:
            try:
                current = float(current)
                self.instr_lib.set_current(channel, current)
                # self.update_values(channel)
            except ValueError:
                self.ui.show_error("Invalid Input", "Please enter a valid number for the voltage.")
            except pyvisa.VisaIOError as e:
                self.ui.show_error("Write Error", f"Failed to write voltage to the instrument: {e}")
        else:
            self.ui.show_error("Connection Error", "Not connected to the instrument.")

    def set_voltage(self, channel, voltage):
        """
        设置选择的通道的电压
        """
        if self.instr_lib is not None:
            try:
                voltage = float(voltage)
                self.instr_lib.set_voltage(channel, voltage)
                # self.update_values(channel)
            except ValueError:
                self.ui.show_error("Invalid Input", "Please enter a valid number for the voltage.")
            except pyvisa.VisaIOError as e:
                self.ui.show_error("Write Error", f"Failed to write voltage to the instrument: {e}")
        else:
            self.ui.show_error("Connection Error", "Not connected to the instrument.")


    def set_CCmode(self, channel, current):
        """
        设置选择的通道的电压
        """
        if self.instr_lib is not None:
            try:
                # current = float(current)
                current = -0.2
                self.instr_lib.set_CCmode(channel, current)
                # self.update_values(channel)
            except ValueError:
                self.ui.show_error("Invalid Input", "Please enter a valid number for the voltage.")
            except pyvisa.VisaIOError as e:
                self.ui.show_error("Write Error", f"Failed to write voltage to the instrument: {e}")
        else:
            self.ui.show_error("Connection Error", "Not connected to the instrument.")

    def set_mode(self, channel, mode):
        """
        设置选择的通道的电压
        """
        if self.instr_lib is not None:
            try:
                mode = str(mode)
                self.instr_lib.set_mode(channel, mode)
                # self.update_values(channel)
            except ValueError:
                self.ui.show_error("Invalid Input", "Please enter a valid number for the voltage.")
            except pyvisa.VisaIOError as e:
                self.ui.show_error("Write Error", f"Failed to write voltage to the instrument: {e}")
        else:
            self.ui.show_error("Connection Error", "Not connected to the instrument.")

    def set_current_limit(self, channel, current):
        """
        设置选择的通道的电流限流
        """
        if self.instr_lib is not None:
            #try:
                #current = float(current)
                self.instr_lib.set_current_limit(channel, current)
                #self.ui.update_current_limit_label(f"Set Current Limit: {current:.3f} A")
        #     except ValueError:
        #         self.ui.show_error("Invalid Input", "Please enter a valid number for the current limit.")
        #     except pyvisa.VisaIOError as e:
        #         self.ui.show_error("Write Error", f"Failed to write current limit to the instrument: {e}")
        else:
            self.ui.show_error("Connection Error", "Not connected to the instrument.")

    def channel_on(self, channel):
        """
        打开选择的通道
        """
        if self.instr_lib is not None:
            try:
                self.instr_lib.channel_on(channel)
            except pyvisa.VisaIOError as e:
                self.ui.show_error("Write Error", f"Failed to turn on the channel: {e}")
        else:
            self.ui.show_error("Connection Error", "Not connected to the instrument.")

    def channel_off(self, channel):
        """
        关闭选择的通道
        """
        if self.instr_lib is not None:
            try:
                self.instr_lib.channel_off(channel)
            except pyvisa.VisaIOError as e:
                self.ui.show_error("Write Error", f"Failed to turn off the channel: {e}")
        else:
            self.ui.show_error("Connection Error", "Not connected to the instrument.")

    def set_voltagemode(self, channel):
        """
        打开选择的通道
        """
        if self.instr_lib is not None:
            try:
                self.instr_lib.set_voltagemode(channel)
            except pyvisa.VisaIOError as e:
                self.ui.show_error("Write Error", f"Failed to turn on the channel: {e}")
        else:
            self.ui.show_error("Connection Error", "Not connected to the instrument.")

    def set_channel_range(self, channel):
        self.instr_lib.set_channel_range(channel)


    def update_values(self, channel):
        """
        更新电压和电流显示
        """
        if self.instr_lib is not None:
            try:
                voltage = self.instr_lib.measure_voltage(channel)
                print(voltage)
                self.ui.update_voltage_label(f"Voltage (V): {voltage.strip()}")
                self.update_current(channel)
            except pyvisa.VisaIOError as e:
                self.ui.show_error("Read Error", f"Failed to read voltage from the instrument: {e}")
        else:
            self.ui.show_error("Connection Error", "Not connected to the instrument.")

    def get_voltage(self, channel):
        """
        更新电压和电流显示
        """
        if self.instr_lib is not None:
            try:
                voltage = self.instr_lib.measure_voltage(channel)
                return voltage
            except pyvisa.VisaIOError as e:
                self.ui.show_error("Read Error", f"Failed to read voltage from the instrument: {e}")
        else:
            self.ui.show_error("Connection Error", "Not connected to the instrument.")

    def arb_on(self, channel):
        """
        更新电压和电流显示
        """
        if self.instr_lib is not None:
            try:
                voltage = self.instr_lib.arb_on(channel)
                return voltage
            except pyvisa.VisaIOError as e:
                self.ui.show_error("Read Error", f"Failed to read voltage from the instrument: {e}")
        else:
            self.ui.show_error("Connection Error", "Not connected to the instrument.")

    def arb_status(self, channel):
        """
        更新电压和电流显示
        """
        if self.instr_lib is not None:
            try:
                voltage = self.instr_lib.arb_status(channel)
                return voltage
            except pyvisa.VisaIOError as e:
                self.ui.show_error("Read Error", f"Failed to read voltage from the instrument: {e}")
        else:
            self.ui.show_error("Connection Error", "Not connected to the instrument.")

    def arb_off(self, channel):
        """
        更新电压和电流显示
        """
        if self.instr_lib is not None:
            try:
                voltage = self.instr_lib.measure_voltage(channel)
                return voltage
            except pyvisa.VisaIOError as e:
                self.ui.show_error("Read Error", f"Failed to read voltage from the instrument: {e}")
        else:
            self.ui.show_error("Connection Error", "Not connected to the instrument.")

    def get_current(self, channel):
        """
        更新电压和电流显示
        """
        if self.instr_lib is not None:
            try:
                current = float(self.instr_lib.measure_current(channel))
                current_str = self.format_current(current)
                return current
            except pyvisa.VisaIOError as e:
                self.ui.show_error("Read Error", f"Failed to read voltage from the instrument: {e}")
        else:
            self.ui.show_error("Connection Error", "Not connected to the instrument.")

    def get_file(self, filename='datalog1.csv'):
        # 发送 SCPI 命令获取文件数据
        self.instr.write(f"MMEM:DATA? '{filename}'")
        # 读取原始数据（包含 IEEE 488.2 二进制块头）
        raw_data = self.instr.read_raw()
        # 解析二进制块头（如果存在）
        if raw_data.startswith(b'#'):
            # 头格式：b'#' + 一位数字（头长度位数）
            header_len = int(raw_data[1:2].decode())
            # 读取表示数据长度的数字字符串
            data_length_str = raw_data[2:2 + header_len]
            data_length = int(data_length_str.decode())
            # 提取实际文件数据
            file_data = raw_data[2 + header_len:2 + header_len + data_length]
        else:
            # 如果没有二进制块头，直接使用返回数据
            file_data = raw_data

        # 将文件数据保存到本地（以二进制方式写入）
        with open("datalog1.csv", "wb") as f:
            f.write(file_data)
        print("文件下载并保存成功！")
    def update_current(self, channel):
        """
        更新测量的电流显示
        """
        if self.instr_lib is not None:
            try:
                current = float(self.instr_lib.measure_current(channel))
                current_str = self.format_current(current)
                self.ui.update_measured_current_label(f"Measured Current: {current_str}")
            except pyvisa.VisaIOError as e:
                self.ui.update_measured_current_label("Measured Current: Read Error")
                self.keep_updating = False  # 发生错误时停止更新
        else:
            self.ui.update_measured_current_label("Measured Current: N/A")

    def format_current(self, current):
        """
        根据电流值自动转换单位并保留小数点后三位
        """
        if current >= 1:
            return f"{current:.3f} A"
        elif current >= 1e-3:
            return f"{current * 1e3:.3f} mA"
        elif current >= 1e-6:
            return f"{current * 1e6:.3f} uA"
        else:
            return f"{current * 1e9:.3f} nA"

    def update_current_periodically(self):
        """
        每0.5秒更新一次电流显示
        """
        if self.instr is not None and self.keep_updating:
            channel = self.ui.get_selected_channel()
            self.update_current(channel)
            self.ui.master.after(500, self.update_current_periodically)