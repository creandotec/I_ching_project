import usb.core
import usb.backend.libusb1

#backend = usb.backend.libusb1.get_backend(find_library=lambda x: "C:/Users/Alberto Enrique/Google Drive/Freelancer Projects/Hugo Project/libusb-1.0.dll")
device = usb.core.find()
