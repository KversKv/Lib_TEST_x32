from ctypes import *

# import parameter
#from Logger import log
#import Logger
import time
import os

#import appPath

class DeviceI2C:
    def __init__(self):
        self.i2c_dll = "D:\CodeProject\PyProject\IIC_TEST\Tool\I2C\I2C_io.dll"
        print("I2C tool path: %s" % self.i2c_dll)
        self.i2cDll = windll.LoadLibrary(self.i2c_dll)



    def read_register_value_8bit(self, device_addr=0x16, reg_addr=0):
        # print("Get register 0x%x value" % reg_addr)
        if reg_addr > 0xff:
            self.i2cDll.I2C_write_reg(device_addr,0x0,0xa010)
            reg_addr = reg_addr & 0x00ff
            dllExeResult = self.i2cDll.I2C_read_reg(device_addr, reg_addr)
            # print("register read value is: %x" % dllExeResult)
            self.i2cDll.I2C_write_reg(device_addr, 0x0, 0xa000)
        else :
            dllExeResult = self.i2cDll.I2C_read_reg(device_addr, reg_addr)
        #     print("register read value is: %x" % dllExeResult)
        # print("dllExeResult read value is: %x" % dllExeResult)
        return dllExeResult

    def read_register_value_10bit(self, device_addr=0x16, reg_addr=0):

        #reg_addr = reg_addr & 0x00ff
        # print(f"dev_addr={device_addr:x}, reg_addr= {reg_addr:x}")
        dllExeResult = self.i2cDll.I2C_read_reg_2003(device_addr, reg_addr)
        # print(f"dev_addr={device_addr:x}, reg_addr= {reg_addr:x} is 0x{dllExeResult:x}")
        return dllExeResult

    def read_register_value_dig(self, device_addr=0x16, reg_addr=0):

        #reg_addr = reg_addr & 0x00ff
        # print(f"dev_addr={device_addr:x}, reg_addr= {reg_addr:x}")
        dllExeResult = self.i2cDll.I2C_read_data(device_addr, reg_addr)
        print(f"dev_addr=0x{device_addr:x}, reg_addr= 0x{reg_addr:x} is 0x{dllExeResult:x}")
        return dllExeResult


    def read_register_value_bit(self, device_addr=0x16, reg_addr=0, wbit=8):
        global dllExeResult
        if wbit == 8:
            dllExeResult = self.read_register_value_8bit(device_addr, reg_addr)
        elif wbit == 10:
            dllExeResult = self.read_register_value_10bit(device_addr, reg_addr)
        return dllExeResult

    def write_register_value_8bit(self, device_addr=0x16, reg_addr=0, val=0):
        #print("Set register 0x%x value" % reg_addr)
        if reg_addr > 0xff :
            self.i2cDll.I2C_write_reg(device_addr,0x0,0xa010)
            reg_addr = reg_addr & 0x00ff
            dllExeResult = self.i2cDll.I2C_write_reg(device_addr, reg_addr, val)
            #print("set register result: %x" % dllExeResult)
            self.i2cDll.I2C_write_reg(device_addr, 0x0, 0xa000)
        else:
            dllExeResult = self.i2cDll.I2C_write_reg(device_addr, reg_addr, val)
            #print("set register result: %x" % dllExeResult)
        return dllExeResult

    def write_register_value_10bit(self, device_addr=0x16, reg_addr=0, val=0):
        # print("Set register 0x%x value" % reg_addr)
        dllExeResult = self.i2cDll.I2C_write_reg_2003(device_addr, reg_addr, val)
        #print("set register result: %x" % dllExeResult)
        return dllExeResult

    def write_register_value_dig(self, device_addr=0x16, reg_addr=0, val=0):

        dllExeResult = self.i2cDll.I2C_write_data(device_addr, reg_addr, val)
        #print("set register result: %x" % dllExeResult)
        return dllExeResult
    def write_register_value_bit(self, device_addr=0x16, reg_addr=0, val=0, wbit=8 ):

        if wbit == 8:
            dllExeResult = self.write_register_value_8bit(device_addr, reg_addr, val)
        elif wbit == 10:
            dllExeResult = self.write_register_value_10bit(device_addr, reg_addr, val)
        return dllExeResult



    def enter_nosignal_mode(self, wifitype):
        print("Enter to no signal test mode: %d" % wifitype)
        dllExeResult = self.i2cDll.BES_EnterNonSigMode(wifitype)
        print("Enter to no signal test mode, code: %s" % dllExeResult)
        if dllExeResult != 0:
            ## log.error("Enter to no signal test mode fail, code: %s" % dllExeResult)
            return False
        else:
            return True

    def enter_signal_mode(self, band, bandwidth=20, shortGI = 0):
        print("Enter in to signal mode: %s, channel width:%s, shortGI:%s"%(str(band),str(bandwidth),str(shortGI)))
        dllExeResult = None
        if band == "5g":
            dllExeResult = self.i2cDll.BES_EnterSigMode(2, int(bandwidth), int(shortGI))
        elif band == "2g4":
            dllExeResult = self.i2cDll.BES_EnterSigMode(1, int(bandwidth), int(shortGI))
        print("Enter to signal test mode, code: %s" % dllExeResult)
        if dllExeResult != 0:
            # log.error("Enter to signal test mode fail, code: %s" % dllExeResult)
            return False
        else:
            return True

    def set_wifi_sig_bandwidth(self, width):
        print("Set wifi signal mode band width: %s"%str(width))
        dllExeResult = self.i2cDll.BES_SetSigWide(int(width))
        print("Enter to signal test mode, code: %s"%dllExeResult)
        if dllExeResult != 0:
            # log.error("Enter to signal band width fail, code: %s" % dllExeResult)
            return False
        else:
            return True

    def set_wifi_sig_shortGI(self, GI):
        print("Set wifi signal mode short GI: %s"%str(GI))
        dllExeResult = self.i2cDll.BES_SetSigGI(int(GI))
        print("Set to signal test mode short GI, code: %s"%dllExeResult)
        if dllExeResult != 0:
            # log.error("Set to signal test mode short GI fail, code: %s" % dllExeResult)
            return False
        else:
            return True

    def set_wifi_channel(self, channel):
        print("I2C set channel: {data}".format(data = channel))
        dllExeResult = self.i2cDll.BES_SetChannel(int(channel))
        if dllExeResult != 0:
            # log.error("Set channel fail, code: %s" % dllExeResult)
            return False
        else:
            return True

    def set_wifi_band(self, band):
        #1 - 2.4g, 2 - 5G
        print("I2C set band: {data}".format(data=band))
        dllExeResult = self.i2cDll.BES_SetBand(int(band))
        if dllExeResult != 0:
            # log.error("Set band fail, code: %s" % dllExeResult)
            return False
        else:
            print("Device I2C set band to 5G ok")
            return True

    def set_wifi_bandwidth(self, bandwidth):
        #unit: mHz
        print("I2C set bandwidth: {data}".format(data=bandwidth))
        dllExeResult = self.i2cDll.BES_SetBandWidth(int(bandwidth))
        if dllExeResult != 0:
            # log.error("Set band width fail, code: %s" % dllExeResult)
            return False
        else:
            return True

    def set_wifi_rate(self, rate, bandwidth = 20, shortGI = 0, aboveconfig = 0):
        # print("I2C set rate: {data}, bandwidh: {band}, shortGI: {GI}, above channel:{above}".format(data=rate, band = bandwidth, GI = parameter.wifiDevice_ShortGI, above = aboveconfig))
        #     dllExeResult = self.i2cDll.BES_SetRate(int(rate),0,0)
        # if int(rate >13):
        #     dllExeResult = self.i2cDll.BES_SetRate(int(rate))
        # else:
        print("I2C set rate: {data}".format(data =rate ))
        dllExeResult = self.i2cDll.BES_SetRate(int(rate))
        if dllExeResult != 0:
            # log.error("Set rate fail, code: %s" % dllExeResult)
            return False
        else:
            print("Set device rate ok")
            return True

    def set_wifi_nosig_width(self, width):
        print("Set wifi nosig width: %s"%str(width))
        dllExeResult = self.i2cDll.BES_SetNonsigWide(int(width))
        if dllExeResult != 0:
            # log.error("Set wifi nosig width fail, code: %s" % dllExeResult)
            return False
        else:
            print("Set wifi nosig width ok")
            return True

    def set_wifi_nosig_shortGI(self, shortGI):
        print("Set wifi nosig shortGI: %s"%str(shortGI))
        dllExeResult = self.i2cDll.BES_SetNonsigGI(int(shortGI))
        if dllExeResult != 0:
            # log.error("Set wifi nosig shortGI fail, code: %s" % dllExeResult)
            return False
        else:
            print("Set wifi nosig shortGI ok")
            return True

    def set_wifi_power(self,power):
        print("I2C set power: {data}".format(data=power))
        dllExeResult = self.i2cDll.BES_SetPower(int(power))
        if dllExeResult != 0:
            # log.error("Set power fail, code: %s" % dllExeResult)
            return False
        else:
            return True

    def save_wifi_power(self):
        print("I2C save power")
        dllExeResult = self.i2cDll.BES_SavePower()
        if dllExeResult != 0:
            # log.error("Save power fail, code: %s" % dllExeResult)
            return False
        else:
            return True

    def set_wifi_FreqOffset(self,offset):
        print("I2C set freq offset: {data}".format(data=offset))
        dllExeResult = self.i2cDll.BES_SetFreqoffset(int(offset))
        if dllExeResult != 0:
            # log.error("Set offset fail, code: %s" % dllExeResult)
            return False
        else:
            return True

    def save_wifi_offset(self):
        print("I2C save freq offset")
        dllExeResult = self.i2cDll.BES_SaveFreqoffset()
        if dllExeResult != 0:
            # log.error("Save offset fail, code: %s" % dllExeResult)
            return False
        else:
            return True

    def start_wifi_tx_test(self):
        print("Start wifi tx test")
        dllExeResult = self.i2cDll.BES_StartNonSigTxTest()
        if dllExeResult != 0:
            # log.error("Start wifi tx test fail, code: %s" % dllExeResult)
            return False
        else:
            print("Enter to wifi tx mode ok")
            return True

    def stop_wifi_tx_test(self):
        print("Stop wifi tx test")
        dllExeResult = self.i2cDll.BES_StopNonSigTxTest()
        if dllExeResult != 0:
            # log.error("Stop wifi tx test fail, code: %s" % dllExeResult)
            return False
        else:
            print("stop wifi tx test mode ok")
            return True

    def start_wifi_rx_test(self):
        print("Start wifi rx test")
        dllExeResult = self.i2cDll.BES_StartNonSigRxTest()
        if dllExeResult != 0:
            # log.error("Stop wifi tx test fail, code: %s" % dllExeResult)
            return False
        else:
            print("WIFI enter to rx mode ok")
            return True

    def stop_wifi_rx_test(self):
        print("Stop wifi i2c rx test")
        dllExeResult = self.i2cDll.BES_StartNonSigRxTest()
        if dllExeResult != 0:
            # log.error("Stop wifi tx test fail, code: %s" % dllExeResult)
            return False
        else:
            return True

    def clear_wifi_packet(self):
        print("Clear wifi packet")
        dllExeResult = self.i2cDll.BES_ClearPktNum()
        if dllExeResult != 0:
            # log.error("Clear wifi rx packet fail, code: %s" % dllExeResult)
            return False
        else:
            print("Clear wifi rx packet ok")
            return True

    def read_wifi_packet(self):
        print("Read wifi packet")
        dllExeResult = self.i2cDll.BES_ReadPktNum()
        # if dllExeResult != 0:
        #     # log.error("Read wifi rx packet fail, code: %s" % dllExeResult)
        #     return False
        # else:
        print("Read wifi tx recieved packet ok, value: {data}".format(data = dllExeResult))
        return int(dllExeResult)

    def enterSignalTestMode(self):
        dllExeResult = self.i2cDll.BES_ClearPktNum()
        if dllExeResult != 0:
            # log.error("Enter into signal test mode fail, code: %s" % dllExeResult)
            return False
        else:
            print("Enter into signal test mode ok")


    # def write_Chip_Efuse_For_UART_Useful(self):
    #     # this is uart download efuse set.
    #     if parameter.chip == "1600":
    #         val = self.i2cDll.efs_read_reg_1600(0x27, 0x00)
    #         val |= 0x800
    #         self.i2cDll.efs_write_reg_1600(0x27, 0x0, val)
    #         val1 = self.i2cDll.efs_read_reg_1600(0x27, 0x00)
    #
    #         print("register read page 0 value is: %x" % val1)
    #
    #         val = self.i2cDll.efs_read_reg_1600(0x27, 0x01)
    #         val |= 0x3
    #         self.i2cDll.efs_write_reg_1600(0x27, 0x1, val)
    #         val2 = self.i2cDll.efs_read_reg_1600(0x27, 0x01)
    #         print("register read page 1 value is: %x" % val2)
    #
    #         #if val2 & 0x3 == 0x3 and val1 & 0x800 == 0x800:
    #         if val2 & 0x3 == 0x3:
    #             print("### enable download mode OK ###")
    #             return True
    #
    #     elif parameter.chip == "2002":
    #         val = self.i2cDll.efs_read_reg_2002(0x17, 0x01)
    #         print("uart efuse value is %x" % val)
    #         val |= 0x8003
    #         self.i2cDll.efs_write_reg_2002(0x17, 0x1, val)
    #
    #         val = self.i2cDll.efs_read_reg_2002(0x17, 0x01)
    #
    #         if val == 0x8003:
    #             print("### enable download mode OK ###")
    #             return True
    #
    #     # log.error("enable download mode Fail")
    #     return False
    #
    def read_register_data(self, device_addr=0x27, reg_addr=0):
        print("%x" % device_addr)
        print("Get register 0x%x data" % reg_addr)
        dllExeResult = self.i2cDll.I2C_read_data(device_addr, reg_addr)
        print("register read data is: %x" % dllExeResult)
        return dllExeResult


    #
    def write_register_data(self, device_addr=0x11, reg_addr=0, val=0):
        #print("Set register 0x%x data" % val)
        dllExeResult = self.i2cDll.I2C_write_data(device_addr, reg_addr, val)

        dllExeResult = self.i2cDll.I2C_read_data(device_addr, reg_addr)
        #print("set  result: %x"  % dllExeResult)
        return dllExeResult


# deviceI2C.check_rf_register_value(0xF6)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('PyCharm')
    deviceI2C = DeviceI2C()
    # device_addr = self.device_addr_var.get()
    # device_addr = int(device_addr, 16)
    # reg_addr = self.reg_addr_var.get()
    # reg_addr = int(reg_addr, 16)
    # lsb = self.lsb_var.get()
    # msb = self.msb_var.get()
    #
    # start_bit = int(lsb)
    # stop_bit = int(msb)

    device_addr = 0x17
    reg_addr = 0x0107
    # start_bit = 5
    # stop_bit = 9
    # step_bit = 1
    # w_bit = stop_bit - start_bit + 1
    output = []
    default_reg = deviceI2C.read_register_value_8bit(device_addr, reg_addr)
    print("%x" % default_reg)
    deviceI2C.write_register_value_8bit(device_addr, reg_addr, 0xAAAA)
    default_reg = deviceI2C.read_register_value_8bit(device_addr, reg_addr)
    print("%x" % default_reg)

    device_addr = 0x27
    reg_addr = 0x0000
    default_reg = deviceI2C.read_register_value_10bit(device_addr, reg_addr)
    # deviceI2C.write_register_value_10bit(device_addr, reg_addr, 0x7212)


    device_addr = 0x11
    reg_addr = 0x4008001c
    default_reg = deviceI2C.read_register_value_dig(device_addr, reg_addr)
    deviceI2C.write_register_value_dig(device_addr, reg_addr, 0x00050200)
    default_reg = deviceI2C.read_register_value_dig(device_addr, reg_addr)
    # deviceI2C.write_register_value_10bit(device_addr, reg_addr, 0x7212)
    # print("Begin dump 1700 PMU Reg:")
    # for reg_addr in range(0x00, 0xFff, 0x1):
    #     default_reg = deviceI2C.read_register_value_10_bit(device_addr, reg_addr)
    #     print("%x" % default_reg)

    # # data_base = data_base & (~(offset[MSB - LSB - 1] << LSB));
    # offset = [0x3, 0x7, 0xf, 0x1f, 0x3f, 0x7f, 0xff]
    # data_base = default_reg & (~(offset[stop_bit - start_bit - 1] << start_bit))
    # for i in range(0, pow(2, w_bit), 1):
    #     write_reg = data_base | i << start_bit
    #     deviceI2C.write_register_value(device_addr, reg_addr, write_reg)
    #     output.append(i)
    # voltage = str(float(self.get_voltage()))
    # current = self.get_current()
    # output.append({voltage, current})
    # print(voltage + "," + str(current))
    # print("OUTPUT is:")
    # print(output)

    # result = ""

    # for i in output:
    #     result = result + "\n"
    #
    #     result = result + str(i)
    # print("\n\nresult is:")
    # print(result)
    # self.test_result_text.delete("1.0", tk.END)
    # self.test_result_text.insert(tk.END, result)












