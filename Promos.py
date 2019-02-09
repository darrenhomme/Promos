import re
import time
from tkinter import filedialog
from tkinter import *
import tkinter as tk

root = tk.Tk()
#root.withdraw()


TakeList = []
Billboard = 0
LowerThird = 0
OutputStr = ""

def FindTag(Input):
    if Input.find("<PAGE>") != -1 and Input.find("</PAGE>") != -1:
        Tag1 = Input.split("<PAGE>")
        Tag2 = Tag1[1].split("</PAGE>")
        return Tag2[0]

Start = time.time()
file_path = filedialog.askopenfilename()

print(file_path)

f = open(file_path, encoding="ansi")

Lines = f.readlines()
f.close
print("Number of Lines:", len(Lines))
print()


for Line in Lines:
    Line = Line.upper()
    if Line.find("<TALLY>1</TALLY>") != -1:
        if Line.find("LOG_MESSAGE") < 0:
            if Line.find("TOWER") < 0 and Line.find("SIDE_SWIPE") < 0 and Line.find("20005") < 0 and Line.find("TRAFFICLIGHT") < 0 and Line.find("20001") < 0 and Line.find("CUSTOMER_CHOICE") < 0:
                TakeList.append(" :" + FindTag(Line) + ": ")
                if Line.find("L3RD") != -1:
                    Billboard = Billboard + 1
                if Line.find("BILLBOARD") != -1:
                    LowerThird = LowerThird + 1


for y in range(0, len(TakeList) - 1):
    for i in range(0, len(TakeList) - 1):
        if TakeList[i] > TakeList[i + 1]:
            Swap = TakeList[i]
            TakeList[i] = TakeList[i + 1]
            TakeList[i + 1] = Swap


for i in range(0, len(TakeList)):
    if OutputStr.find(str(TakeList[i]) + str(TakeList.count(TakeList[i]))) < 0:
        OutputStr = OutputStr + str(TakeList[i]) + str(TakeList.count(TakeList[i])) + "\n"

OutputStr = OutputStr.replace(" :" , "")
      
print(OutputStr)
print("Total Promos:", len(TakeList))
print("Billboards:", Billboard)
print("Lower Thids:", LowerThird)

End = time.time()

print()
print("Seconds to Process Request:", int(End - Start))
#input()


T = Text(root, height=40, width=100)
T.pack()
T.insert(END, OutputStr)

B = tk.Button(root, text ="Hello")

B.pack()

mainloop()
