import divoom_protocol
import math
#import bluetooth

def read_bytes(filename):
	file = open(filename, 'r') 
	str = file.read()
	str_list = str.split()
	bytes_list = []
	for s in str_list:
		bytes_list.append(int(s, 16))
	return bytes_list
	
def print_hex(a_list):
	print '[{}]'.format(', '.join(hex(x) for x in a_list))
	
#def send_bytes(addr, bytes_list):
#		sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
#		sock.connect((addr, 4))
		#time.sleep(2)
#		sock.send(str(bytearray(bytes_list)))
		#time.sleep(2)
		#sock.recv(12)
#		sock.close()
	

thing = divoom_protocol.DivoomAuraBoxProtocol()

pkg = thing.create_package(read_bytes("testdata/inv_data1"))
#print (pkg)
print_hex(pkg)
#send_bytes(pk)