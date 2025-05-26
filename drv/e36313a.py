class E36313A:
    def __init__(self, instr):
        self.instr = instr

    def set_voltage(self, channel, voltage):
        self.instr.write(f"INSTrument:NSELect {channel}")
        self.instr.write(f"VOLT {voltage}")

    def set_current_limit(self, channel, current):
        self.instr.write(f"INSTrument:NSELect {channel}")
        self.instr.write(f"CURR {current}")

    def channel_on(self, channel):
        # self.instr.write(f"INSTrument:NSELect {channel}")
        # self.instr.write("OUTP ON")
        self.instr.write(f"OUTP ON, (@{channel})")

    def channel_off(self, channel):
        # self.instr.write(f"INSTrument:NSELect {channel}")
        # print(f"INSTrument:NSELect {channel}")
        # self.instr.write("OUTP OFF")
        # print("OUTP OFF")
        self.instr.write(f"OUTP OFF, (@ {channel}) \n")


    def measure_voltage(self, channel):
        self.instr.write(f"INSTrument:NSELect {channel}")
        return self.instr.query("MEAS:VOLT?")

    def measure_current(self, channel):
        self.instr.write(f"INSTrument:NSELect {channel}")
        return self.instr.query("MEAS:CURR?")
