flow1limit = 6.0    # l/m
flow2limit = 6.0    # l/m
flow3limit = 6.0    # l/m
flow4limit = 6.0    # l/m

# Sensor data in p/l (pulses per liter)
flow1_ppl = 450.
flow2_ppl = 450.
flow3_ppl = 450.
flow4_ppl = 450.

limit1 = int(round(flow1limit*flow1_ppl/30))
limit2 = int(round(flow2limit*flow2_ppl/30))
limit3 = int(round(flow3limit*flow3_ppl/30))
limit4 = int(round(flow4limit*flow4_ppl/30))

print "Setting limits for the LED status"
print "Limit1: %.2f l/m (%.1f Hz)" % (flow1limit, limit1/2.)
print "Limit2: %.2f l/m (%.1f Hz)" % (flow2limit, limit2/2.)
print "Limit3: %.2f l/m (%.1f Hz)" % (flow3limit, limit3/2.)
print "Limit4: %.2f l/m (%.1f Hz)" % (flow4limit, limit4/2.)

lstr1 = "%04X" % limit1
lstr2 = "%04X" % limit2
lstr3 = "%04X" % limit3
lstr4 = "%04X" % limit4

import serial

serialport = serial.Serial("/dev/ttyS0", 9600, timeout=0.5)

serialport.write("SL1" + lstr1 + "\n")
serialport.write("SL2" + lstr2 + "\n")
serialport.write("SL3" + lstr3 + "\n")
serialport.write("SL4" + lstr4 + "\n")
serialport.write("STO\n")
