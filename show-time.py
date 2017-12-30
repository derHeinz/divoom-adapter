import sys
import time
import divoom_protocol
import divoom_device


# create time
hour12 = time.strftime('%I')
minute = time.strftime('%M')
print("setting time to "  + hour12 + ":" + minute)

DIVOMM_ADR = sys.argv[1]
thing = divoom_protocol.DivoomAuraBoxProtocol()
dev = divoom_device.DivoomDevice(DIVOMM_ADR)

dev.connect()
dev.send(thing.create_set_time_package(hour12, minute))
dev.send(thing.create_time_package())
time.sleep(10)
dev.disconnect()