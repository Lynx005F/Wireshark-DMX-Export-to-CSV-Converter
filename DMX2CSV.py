from tkinter import Tk
from tkinter.filedialog import *
from os.path import basename
import os


def SetValues(Line):
    Temp = [x for x in Line.split(" ") if x != ""]
    for y in range(1,17):
        Packet[1] += (str(Temp[y]) + ";")

def SetHeader(Line):
    Temp = [x for x in Line.split(" ") if x != ""]
    Packet[0] = (str(Temp[0]) + ";" + str(Temp[1]) + ";")

def SavePacket():
    global PacketNo
    if Output[Universe] == []:
        Save()
    elif Packet[1] != Output[Universe][-1][1]:
        Save()
    else:
        Discard()
    PacketNo += 1

def Save():
    global Packet
    Output[Universe].append([str(Packet[0]), str(Packet[1])])
    Packet = ["", ""]
    print("Packet " + str(PacketNo) + " in Universe " + str(Universe) + " saved")

def Discard():
    global Packet
    Packet = ["", ""]
    print("Packet " + str(PacketNo) + " in Universe " + str(Universe) + " discarded")
    

Tk().withdraw() 
DataRaw = askopenfilename()

with open (DataRaw) as file:
    Packet = ["", ""]
    PacketNo = 0
    Output = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    Universe = 0
    for Line in file:
        if "Time" in Line:
            Next = True
        elif Next:
            Next = False
            SetHeader(Line)
        elif "0x1f1" in Line:
            SetValues(Line)
            SavePacket()
        elif "0x0" in Line or "0x1" in Line:
            SetValues(Line)

    for Index, Universe in enumerate(Output):
        if Universe != []:
            OutputText = ""
            OutputDir = askdirectory()
            print("Saving...")
            for Packet in Universe:
                OutputText += str(Packet[0]) + str(Packet[1]) + "\n"
            UniverseFile = open(str(OutputDir) +"/" + str(os.path.splitext(basename(DataRaw))[0]) + "_Universe_" + str(Index) +".csv", "w")
            UniverseFile.write(OutputText)
            UniverseFile.close()
            print("Finished")
