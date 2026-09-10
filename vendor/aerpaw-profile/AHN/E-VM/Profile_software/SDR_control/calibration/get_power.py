import pyvisa

rm = pyvisa.ResourceManager()
print(rm.list_resources())
inst = rm.open_resource("USB0::10893::42776::MY58020003::0::INSTR")
# inst.write("SYST:PRES DEF")
# inst.write("CAL:ZERO:AUTO ONCE")
freq = 3500000000
inst.write(f"FREQ {freq}Hz")
inst.write("INIT:CONT ON")
print(inst.query("FETC?"))
