#!/usr/bin/python3.5
import time
import os
#from tkinter import ttk
import random
import glob
import PIL.Image
import ctypes

import pygame

#Load the dll to control the Bee boards
boardDll = ctypes.cdll.LoadLibrary("./dll/bee.dll")
#This are the function prototypes to wrap the dll
InitBee_prototype = ctypes.WINFUNCTYPE(ctypes.c_int)
Bee_Outputs_prototype = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int)

InitBee = InitBee_prototype(("InitBee",boardDll))
Bee_Set_Outputs = Bee_Outputs_prototype(("MB_SetOutputs", boardDll))



#    lower and upper trigrams, ready to call the software which drives the relays (switches) and
#    the motors.  Hopefully the relay will come with the appropriate instructions as to how to call

rng = random.SystemRandom()  # (auto-)seeded, with os.urandom()

#method = "3 coin"
method = "modified 3 coins"

special_coin = 0

# We build in bottom to top
toss_array = [0, 0, 0, 0, 0, 0]

#Time in miliseconds
time_to_scan = 5000

#Time to keep alive a slide in miliseconds
time_to_keep_alive_slide = 5000

#near_devices = list()
#device_name = "TRY ME, OPEN YOUR BLUETOOTH"

def search_for_devices():
    global device_name
    #global near_devices
    GUI_interface.b.configure(text="STOP", command = stop_callback)
    GUI_interface.go_on = True

    try:
        #devices = bluetooth.discover_devices(duration=20, lookup_names = True)

        if GUI_interface.wait_before_read_again == False:
            nearDevicesInfo.nearDevices = list()

            GUI_interface.Update_device_name("Looking for devices...")
            devices = bluetooth.discover_devices(duration=5, lookup_names = True)
            nearDevicesInfo.found_devices = True
            for addr, name in devices:
                print("{0}-{1}".format(addr, name))
                nearDevicesInfo.nearDevices.append(name)
            GUI_interface.wait_before_read_again = True
        if Trigrams.wait_before_new_trigram == False:
            if Trigrams.number_of_hexagrams_shown < len(nearDevicesInfo.nearDevices):
                GUI_interface.Update_device_name("Hi "+nearDevicesInfo.nearDevices[Trigrams.number_of_hexagrams_shown]+" I ching says:")
                throw_i_ching()
                GUI_interface.Update_I_ching_text_results()
                Trigrams.wait_before_new_trigram = True
                if Trigrams.number_of_hexagrams_shown < len(nearDevicesInfo.nearDevices):
                    Trigrams.number_of_hexagrams_shown += 1
            else:
                GUI_interface.Update_device_name("Open your bluetooth to play")
                Trigrams.number_of_hexagrams_shown = 0
                nearDevicesInfo.nearDevices = list()
                Trigrams.wait_before_read_again = False
            #time.sleep(10)
    except OSError:
        nearDevicesInfo.found_devices = False
        print("no devices found")
        device_name = "No device found"
        nearDevicesInfo.nearDevices = list()
        GUI_interface.Update_device_name("No device found")
        GUI_interface.wait_before_read_again = False

    if GUI_interface.go_on == True:
        bluetooth_loop = bluetooth_devices()
    #Label1 = ttk.Label(root, text = device_name).grid(row=0)
    #Label1.grid(row=0)

def stop_callback():
    GUI_interface.go_on = False
    GUI_interface.b.configure(text="GO", command = search_for_devices)

class BeeModules:

    def __init__(self):
        self.bee_status = InitBee()
        self.u_trigram_file = None
        self.l_trigram_file = None
        self.u_trigram_lines = list()
        self.l_trigram_lines = list()
        self.number_of_lines = 0

    def Get_data_from_txt(self, upper_trigram, lower_trigram):

        try:
            self.u_trigram_file = open("./Text Files/"+upper_trigram+".txt", "r")
            self.u_trigram_lines = self.u_trigram_file.readlines()
            self.u_trigram_file.close()
            print("{0} trigram loaded".format(upper_trigram))
        except IOError:
            print("Can't found the file for {0}".format("zero"))
            self.u_trigram_file = open("./Text Files/zero.txt", "r")
            self.u_trigram_lines = self.u_trigram_file.readlines()
            self.u_trigram_file.close()
            print("{0} trigram loaded".format("zero"))

        try:
            self.l_trigram_file = open("./Text Files/"+lower_trigram+".txt", "r")
            self.l_trigram_lines = self.l_trigram_file.readlines()
            self.l_trigram_file.close()
            print("{0} trigram loaded".format(lower_trigram))
        except IOError:
            print("Can't found the file for {0}".format("zero"))
            self.l_trigram_file = open("./Text Files/zero.txt", "r")
            self.l_trigram_lines = self.l_trigram_file.readlines()
            self.l_trigram_file.close()
            print("{0} trigram loaded".format("zero"))
        self.number_of_lines = len(self.l_trigram_lines)
    def Set_bee_outputs(self, trigram1, trigram2):
        if self.bee_status > 0:
            Bee_Set_Outputs(1, l_trigram_code)
            Bee_Set_Outputs(2, u_trigram_code)
        else:
            print("No modules detected")

class Trigrams:
    wait_before_new_trigram = False
    number_of_hexagrams_shown = 0
    lower_trigram = "qian"
    upper_trigram = "kan"

    file_name = "./Hexagram/"+lower_trigram + "-" +upper_trigram + ".png"

    #i_ching_pictures = tk.PhotoImage(file=file_name)

    #def prepare_hexagram_picture(lower_trigram, upper_trigram):
    #    try:
    #        Trigrams.file_name = "./Hexagram/"+lower_trigram + "-" +upper_trigram + ".png"
    #    except tk.TclError:
    #        file_name = "./Hexagram/"+lower_trigram + "-" +upper_trigram + ".png"
    #    Trigrams.i_ching_pictures = tk.PhotoImage(file="./Hexagram/qian-kan.png")


def toss():
    val = 0
    for flip in range(3):        # 3 simulated coin flips
        val += rng.randint(2,3)  # tail=2, head=3
        if flip == 0:
            special_coin = val

    if method == "coin":
        return val
    else:
    # method similar to "yallow-stick"
        if val == 9:
            if rng.randint(2,3) == 3:
                val = 9
            else:
                value = 7
        if val == 8:
            if special_coin == 2:
                if rng.randint(2,3) == 2:
                    val = 6
                else:
                    val = 8
    return val

# hence we print in reverse
def print_lines_in_reverse(toss_array):
    for line in range(5,-1,-1):
        val = toss_array[line]

        if   val == 6: print('6  changing yin  :  == x == ')
        elif val == 7: print('7  static yang   :  ------- ')
        elif val == 8: print('8  static yin    :  ==   == ')
        elif val == 9: print('9  changing yang :  ---o--- ')

def throw_i_ching():
    global toss_array

    for line in range(0,6,1):
        toss_array[line] = toss()
    print_lines_in_reverse(toss_array)

    if (toss_array[2] == 9 or toss_array[2] == 7) and (toss_array[1] == 9 or toss_array[1] == 7) and (toss_array[0] == 9 or toss_array[0] == 7):
            LowerTrigram = "qian"

    if (toss_array[2] == 9 or toss_array[2] == 7) and (toss_array[1] == 6 or toss_array[1] == 8) and (toss_array[0] == 6 or toss_array[0] == 8):
            LowerTrigram = "gen"

    if (toss_array[2] == 6 or toss_array[2] == 8) and (toss_array[1] == 9 or toss_array[1] == 7) and (toss_array[0] == 6 or toss_array[0] == 8):
            LowerTrigram = "kan"

    if (toss_array[2] == 6 or toss_array[2] == 8) and (toss_array[1] == 6 or toss_array[1] == 8) and (toss_array[0] == 9 or toss_array[0] == 7):
            LowerTrigram = "zhen"

    if (toss_array[2] == 6 or toss_array[2] == 8) and (toss_array[1] == 6 or toss_array[1] == 8) and (toss_array[0] == 6 or toss_array[0] == 8):
            LowerTrigram = "kun"
    if (toss_array[2] == 6 or toss_array[2] == 8) and (toss_array[1] == 9 or toss_array[1] == 7) and (toss_array[0] == 9 or toss_array[0] == 7):
            LowerTrigram = "dui"
    if (toss_array[2] == 9 or toss_array[2] == 7) and (toss_array[1] == 6 or toss_array[1] == 8) and (toss_array[0] == 9 or toss_array[0] == 7):
            LowerTrigram = "li"
    if (toss_array[2] == 9 or toss_array[2] == 7) and (toss_array[1] == 9 or toss_array[1] == 7) and (toss_array[0] == 6 or toss_array[0] == 8):
            LowerTrigram = "sun"
    if (toss_array[5] == 9 or toss_array[5] == 7) and (toss_array[4] == 9 or toss_array[4] == 7) and (toss_array[3] == 9 or toss_array[3] == 7):
            UpperTrigram = "qian"

    if (toss_array[5] == 9 or toss_array[5] == 7) and (toss_array[4] == 6 or toss_array[4] == 8) and (toss_array[3] == 6 or toss_array[3] == 8):
            UpperTrigram = "gen"
    if (toss_array[5] == 6 or toss_array[5] == 8) and (toss_array[4] == 9 or toss_array[4] == 7) and (toss_array[3] == 6 or toss_array[3] == 8):
            UpperTrigram = "kan"
    if (toss_array[5] == 6 or toss_array[5] == 8) and (toss_array[4] == 6 or toss_array[4] == 8) and (toss_array[3] == 9 or toss_array[3] == 7):
            UpperTrigram = "zhen"
    if (toss_array[5] == 6 or toss_array[5] == 8) and (toss_array[4] == 6 or toss_array[4] == 8) and (toss_array[3] == 6 or toss_array[3] == 8):
            UpperTrigram = "kun"
    if (toss_array[5] == 6 or toss_array[5] == 8) and (toss_array[4] == 9 or toss_array[4] == 7) and (toss_array[3] == 9 or toss_array[3] == 7):
            UpperTrigram = "dui"
    if (toss_array[5] == 9 or toss_array[5] == 7) and (toss_array[4] == 6 or toss_array[4] == 8) and (toss_array[3] == 9 or toss_array[3] == 7):
            UpperTrigram = "li"
    if (toss_array[5] == 9 or toss_array[5] == 7) and (toss_array[4] == 9 or toss_array[4] == 7) and (toss_array[3] == 6 or toss_array[3] == 8):
            UpperTrigram = "sun"

    Trigrams.lower_trigram = LowerTrigram
    Trigrams.upper_trigram = UpperTrigram

    #Trigrams.prepare_hexagram_picture(LowerTrigram, UpperTrigram)

    print("Upper Trigram is ", UpperTrigram)
    print("Lower Trigram is ", LowerTrigram)


    #os.system("./Hexagram/"+ hexagram)

def main():
    pygame.init()
    gameDisplay = pygame.display.set_mode((0,0))

    black = (0,0,0)
    #Start the Bee modules
    Relay_bee_module = BeeModules()
    #Generate the trigrams
    throw_i_ching()


    hexagram = Trigrams.lower_trigram + "-" + Trigrams.upper_trigram+".png"
    hexagram_path = "./Hexagram/"



    img_path = glob.glob(os.path.join(hexagram_path, hexagram))

    #img = PIL.Image.open(img_path[0])
    #img.show();
    img = pygame.image.load(img_path[0])
    gameDisplay.blit(img, (0,0))

    pygame.display.update()

    Relay_bee_module.Get_data_from_txt(Trigrams.upper_trigram, Trigrams.lower_trigram)

    for i in range(Relay_bee_module.number_of_lines):
        u_trigram_code = int(Relay_bee_module.u_trigram_lines[i])
        l_trigram_code = int(Relay_bee_module.l_trigram_lines[i])

        Relay_bee_module.Set_bee_outputs(u_trigram_code, l_trigram_code)

        time.sleep(0.1)

    pygame.quit()
    quit()
if __name__ == "__main__":
    main()
