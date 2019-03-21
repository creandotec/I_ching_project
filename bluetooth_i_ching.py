#!/usr/bin/python3.5
import bluetooth
import time
import tkinter as tk
import os
#from tkinter import ttk
import random
import glob
import usb.core

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

class nearDevicesInfo:
    nearDevices = list()
    found_devices = False

class bluetooth_devices:
    #devices = ()
    #found_devices = False
    def __init__(self):
        #GUI_interface.b.configure(text="STOP")
        self.label = tk.Label(GUI_interface.root, text="0 s", font="Arial 30", width=10)
        if Trigrams.wait_before_new_trigram == True:
            print("Waiting for the user stop reading the message")
            Trigrams.wait_before_new_trigram = False
            self.label.after(time_to_keep_alive_slide, self.search_for_devices)
        elif GUI_interface.wait_before_read_again == False:
            print("waiting to scan")
            self.label.after(time_to_scan, self.search_for_devices)

    def search_for_devices(self):
        try:
            if GUI_interface.wait_before_read_again == False:
                nearDevicesInfo.nearDevices = list()

                GUI_interface.Update_device_name("Looking for devices...")
                bluetooth_devices.devices = bluetooth.discover_devices(duration=5, lookup_names = True)
                bluetooth_devices.found_devices = True
                for addr, name in bluetooth_devices.devices:
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
                    GUI_interface.Update_device_name("Open your bluetooth device to play")
                    GUI_interface.Clear_I_Ching()
                    Trigrams.number_of_hexagrams_shown = 0
                    nearDevicesInfo.nearDevices = list()
                    GUI_interface.wait_before_read_again = False
                #time.sleep(10)
        except OSError:
            bluetooth_devices.found_devices = False
            print("no devices found")
            device_name = "No device found"
            nearDevicesInfo.nearDevices = list()
            GUI_interface.Update_device_name("No device found")
            Trigrams.wait_before_new_trigram = False
            GUI_interface.wait_before_read_again = False

        if GUI_interface.go_on == True:
            if Trigrams.wait_before_new_trigram == True:
                print("Waiting for the user stop reading the message2")
                Trigrams.wait_before_new_trigram = False
                self.label.after(time_to_keep_alive_slide, self.search_for_devices)
            elif GUI_interface.wait_before_read_again == False:
                print("waiting to scan")
                self.label.after(time_to_scan, self.search_for_devices)

class GUI_interface:
    go_on = False
    device_name = "TRY ME, OPEN YOUR BLUETOOTH"
    root = tk.Tk()
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()

    wait_before_read_again = False

    root.overrideredirect(True)
    root.geometry("{0}x{1}".format(w, h))

    root.focus_set()  # <-- move focus to this widget

    root.configure(bg = 'black')

    root.title('Aplicaci�n')

    device_name_frame = tk.Frame(height = 2, bd = 1, relief=tk.SUNKEN)

    Label1 = tk.Label(root, text = device_name,fg="white", bg="black",font=("Comics Sans", 30))
    Label1.pack()

    device_name_frame.pack(fill=tk.X, padx=5, pady=5)
    I_ching_text_container = tk.Text(root, height = 8, width=30)

    b = tk.Button(root, text='GO', command = search_for_devices)
    b.pack()
    I_ching_text_container.pack(side=tk.LEFT, anchor=tk.N)

    i_ching_slider = tk.Label(root, bg="black")
    i_ching_slider.pack(side = tk.RIGHT, fill=tk.BOTH, expand = 1)

    I_ching_screen_saver_image = tk.PhotoImage(file="./i-ching.png")
    i_ching_slider.config(image = I_ching_screen_saver_image)
    root.update()

    def Update_device_name(user_name):
        GUI_interface.Label1.config(text=user_name)

        GUI_interface.root.update()
    def Update_I_ching_text_results():
        GUI_interface.I_ching_text_container.delete(1.0, tk.END)
        for line in range(5,-1,-1):
            val = toss_array[line]

            if   val == 6:
                #print('6  changing yin  :  == x == ')
                GUI_interface.I_ching_text_container.insert(tk.END,'6  changing yin  :  == x == \n')
            elif val == 7:
                #print('7  static yang   :  ------- ')
                GUI_interface.I_ching_text_container.insert(tk.END,'6  changing yin  :  ------- \n')
            elif val == 8:
                #print('8  static yin    :  ==   == ')
                GUI_interface.I_ching_text_container.insert(tk.END,'6  changing yin  :  ==   == \n')
            elif val == 9:
                #print('9  changing yang :  ---o--- ')
                GUI_interface.I_ching_text_container.insert(tk.END,'6  changing yin  :  ---o--- \n')
        GUI_interface.I_ching_text_container.insert(tk.END, "Lower trigram = "+Trigrams.lower_trigram+"\n")
        GUI_interface.I_ching_text_container.insert(tk.END, "Higher trigram = "+Trigrams.upper_trigram+"\n")
        GUI_interface.i_ching_slider.config(image = Trigrams.i_ching_pictures)
        GUI_interface.root.update()
    def Clear_I_Ching():
        GUI_interface.i_ching_slider.config(image = GUI_interface.I_ching_screen_saver_image)
        GUI_interface.root.update()

class Trigrams:
    wait_before_new_trigram = False
    number_of_hexagrams_shown = 0
    lower_trigram = "qian"
    upper_trigram = "kan"

    file_name = "./Hexagram/"+lower_trigram + "-" +upper_trigram + ".png"

    i_ching_pictures = tk.PhotoImage(file=file_name)

    def prepare_hexagram_picture(lower_trigram, upper_trigram):
        try:
            Trigrams.file_name = "./Hexagram/"+lower_trigram + "-" +upper_trigram + ".png"
        except tk.TclError:
            file_name = "./Hexagram/"+lower_trigram + "-" +upper_trigram + ".png"
        Trigrams.i_ching_pictures = tk.PhotoImage(file="./Hexagram/qian-kan.png")


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

    Trigrams.prepare_hexagram_picture(LowerTrigram, UpperTrigram)

    print("Upper Trigram is ", UpperTrigram)
    print("Lower Trigram is ", LowerTrigram)

if __name__ == "__main__":
    GUI_interface.root.mainloop()
