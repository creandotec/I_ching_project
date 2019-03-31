#import usb.core
#import usb.util
import ctypes
import time

relayBeeDll = ctypes.WinDLL("./dll/bee.dll")
boardDll = ctypes.cdll.LoadLibrary("./dll/bee.dll")
boardLibraries = ctypes.CDLL("./dll/bee.dll")

kernel32 = ctypes.windll.kernel32

class BeeModules():
    idVendor = "0x4d8"
    modules_available = list()

def getInitMbee (dll):
    address = (kernel32.LoadLibraryA("./dll/bee.dll")).Type_InitMbee.Type_InitMbee(kernel32.GetProcAddress(kernel32.LoadLibraryA("./dll/bee.dll"), "InitBee"))
    return address

def send_data_to_relay_bee(bee_module, data1, data2):
    data = [4, data1, data2]
    bee_module.write(2, data)

if boardDll is not None:
    print(boardDll)
    #InitMbee = getInitMbee(boardDll)
    #status = InitMbee()
    print("Library was loaded")
else:
    print("Library can't be loaded")

InitBee_prototype = ctypes.WINFUNCTYPE(ctypes.c_int)
Bee_Outputs_prototype = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int)

output_parameters =0,
InitBee = InitBee_prototype(("InitBee",boardDll))
Bee_Set_Outputs = Bee_Outputs_prototype(("MB_SetOutputs", boardDll))


status = InitBee()
#boardDll.MB_SetOutputs(1, 170)
if status == 0:
    print(status)
    print("No board was found")

elif status == 1:
    print("Just one board found")
    Bee_Set_Outputs(1, 0)
    #print(status)
    #Bee_Set_Outputs = boardDll.MB_SetOutputs(1, 170)
    #print("boards were found")

elif status == 2:
    print("Two boards found")
    Bee_Set_Outputs(1, 0)
    Bee_Set_Outputs(2, 0)

status = 2

if status is not 0:
    while True:
        lower_trigram = None
        upper_trigram = None
        lower_trigram = input("Enter the name for the first trigram:")
        u_trigram_lines = None
        l_trigram_ines = None

        if lower_trigram == "":
            lower_trigram = "zero"

        if lower_trigram == "quit":
            break
        try:
            l_trigram_file = open(lower_trigram+".txt", "r")
            l_trigram_lines = l_trigram_file.readlines()
            l_trigram_file.close()
            print("{0} trigram loaded".format(lower_trigram))
        except IOError:
            print("Can't found the file for {0}".format(lower_trigram))

        if status == 2:
            upper_trigram = input("Enter the name for the second trigram:")
            if upper_trigram == "quit":
                break
            try:
                u_trigram_file = open(upper_trigram+".txt", "r")
                u_trigram_lines = u_trigram_file.readlines()
                u_trigram_file.close()
                print("{0} trigram loaded".format(upper_trigram))
            except IOError:
                print("Can't found the file for {0}".format(upper_trigram))
        number_of_lines = len(u_trigram_lines)

        if number_of_lines > 0:
            print("running {0}-{1}".format(lower_trigram, upper_trigram))
            for i in range(number_of_lines):
                u_trigram_code = int(u_trigram_lines[i])
                l_trigram_code = int(l_trigram_lines[i])

                Bee_Set_Outputs(1, l_trigram_code);
                if status == 2:
                    Bee_Set_Outputs(2, u_trigram_code);

                time.sleep(0.1)
        #int_command = int(lower_trigram)
        #Bee_Set_Outputs(1, int_command);
