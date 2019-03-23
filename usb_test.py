import usb.core
import usb.util
import usb.backend.libusb1

class BeeModules():
    idVendor = "0x4d8"
    modules_available = list()


def send_data_to_relay_bee(bee_module, data1, data2):
    data = [4,data1,data2]
    bee_module.write(2, data)

#backend = usb.backend.libusb1.get_backend(find_library=lambda x: "C:/Users/Alberto Enrique/Google Drive/Freelancer Projects/Hugo Project/libusb-1.0.dll")
device = usb.core.find(find_all=True)

for dev in device:
    try:
        #print(hex(dev.idDevice)+"\n")
        print("USB device, product id {0}, vendor id {1}".format( hex(dev.idProduct), hex(dev.idVendor) ) )
        #print(hex(dev.idProduct)+"\n")
        #print(hex(dev.idVendor)+"\n")
        if hex(dev.idVendor) == BeeModules.idVendor:
            print("Board found")
            try:
                dev.detach_kernel_driver(0)
            except:
                pass
            dev.set_configuration()
            BeeModules.modules_available.append(dev)
    except NotImplementedError:
        print("There is an error")
print(len(BeeModules.modules_available))

while True:
    if len(BeeModules.modules_available) > 0:
        value1 = input("Type the value for the first byte")
        value2 = input("Type the value for the second byte")

        for dev in BeeModules.modules_available:
            send_data_to_relay_bee(dev, int(value1), int(value2))
    else:
        pass
