import usb.core
import usb.util
import usb.backend.libusb1

#backend = usb.backend.libusb1.get_backend(find_library=lambda x: "C:/Users/Alberto Enrique/Google Drive/Freelancer Projects/Hugo Project/libusb-1.0.dll")
device = usb.core.find(find_all=True)

for dev in device:
    try:
        print(dev)
    except NotImplementedError:
        print("There is an error")
