class N6705C:
    def __init__(self, instr):
        self.instr = instr

    def set_channel_range(self, channel):
        self.instr.write(f"SENS:CURR:RANG:AUTO ON, (@{channel})")

    def set_voltage(self, channel, voltage):
        # 设置电压
        # self.instr.write(f"FUNC VOLT,(@{channel})")
        self.instr.write(f"VOLT {voltage}, (@{channel})")
        # self.channel_on(channel)

    def set_mode(self, channel, mode):
        #设置模式
        #mode option: PS4Q |PS2Q |PS1Q |BATTery |CHARger |CCLoad |CVLoad |VMETer |AMETer
        self.instr.write(f"EMULation {mode},(@{channel})")
        # self.channel_on(channel)

    def set_current(self, channel, current):
        # 设置电流
        # self.instr.write(f"FUNC CURR,(@{channel})")
        self.instr.write(f"CURR {current},(@{channel})")
        # self.channel_on(channel)

    def set_current_limit(self, channel, current_limit):
        # 设置输出电流的限制
        self.instr.write(f"CURR:LIM {current_limit}, (@{channel})")
        self.instr.write(f"SENS:CURR:RANG:AUTO ON, (@{channel})")

    def set_measurement_range(self, channel, measurement_type, range_value):
        # 设置测试范围
        if measurement_type.lower() == 'voltage':
            self.instr.write(f"VOLT:RANG {range_value}, (@{channel})")
        elif measurement_type.lower() == 'current':
            self.instr.write(f"CURR:RANG {range_value}, (@{channel})")
        else:
            raise ValueError("Invalid measurement type specified. Use 'voltage' or 'current'.")

    def channel_on(self, channel):
        # 打开通道
        self.instr.write(f"OUTP ON, (@{channel})")

    def channel_off(self, channel):
        # 关闭通道
        self.instr.write(f"OUTP OFF, (@{channel})")

    def set_voltagemode(self, channel):
        # 打开通道
        self.instr.write(f"EMULation VMETer,(@{channel})")


    def measure_voltage(self, channel):
        # 测量电压
        return self.instr.query(f"MEAS:VOLT? (@{channel})")

    def measure_current(self, channel):
        # 测量电流
        return self.instr.query(f"MEAS:CURR? (@{channel})")

    def arb_on(self, channel):
        # 测量电压
        return self.instr.write(f"INIT:TRAN (@{channel})")

    def arb_off(self, channel):
        # 测量电压
        return self.instr.write(f"ABOR:TRAN? (@{channel})")

    def arb_status(self, channel):
        return self.instr.query(f"STAT:OPER:COND? (@{channel})")

    def trg(self):
        return self.instr.write(f"*TRG")

