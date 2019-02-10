#!/usr/bin/python3

#Promos 2.2

from tkinter import *
import re
import time
import datetime
from datetime import datetime, date, time
from tkinter import filedialog
from tkinter import scrolledtext as ScrolledText 
import os
Form1 = Tk()
Form1.title("Promos 2.2")

class PromosClass:
    StartSearchTime = datetime.now()
    TakeList = []
    Billboard = 0
    LowerThird = 0
    LineCount = 0
    OutputStr = ""

def FindTag(Input, Tag):
    #Used to find data in logfile
    #Format: <COMPUTER>EPTVTRIO-203</COMPUTER><TIME>1/20/2019 7:00:39 AM</TIME><CHANNEL>A</CHANNEL><TALLY>1</TALLY><PAGE>2660</PAGE><TEMPLATE>ANIMATED_L3RD2</TEMPLATE>
    Result = re.findall("<" + Tag +">(.+?)</" + Tag + ">", Input)
    if len(Result) != 0:
        return str(Result[0])
    else:
        return ""

def OpenFile(Input):
    #Open the file for reading, returns list of lines
    if Input != "":
        f = open(Input, encoding="ansi")
        Lines = f.readlines()
        f.close
        return Lines
    
def AmPm(Input):
    #Used to convert vbs timestamp in logfile to python timestamp in 24 hour format
    #Called in findpromos
    if Input.find("AM") != -1:
        return 0
    else:
        return 12

def FindPromos(File, Object):
    #Loops through log
    #Finds take entry echo
    #Only counts if tally was on
    #Gets timestamp and checks against search range, will need to rewrite before the year 9999
    #Filters out non promo template types (blacklist)
    #Counts lower thirds and billboards
    #Blank pagename counts all
    #A pagename will search for that page and return take timestamps
    #* as a page name will return timestamps for all promo pages
    if DateState.get() == 1:
        PromoStartTime = datetime.strptime(txtDate1.get("1.0", "end-1c"), "%Y-%m-%d %H:%M:%S")
        PromoEndTime = datetime.strptime(txtDate2.get("1.0", "end-1c"), "%Y-%m-%d %H:%M:%S")
    else:
        PromoStartTime = datetime.strptime("1870-12-20 14:56:09", "%Y-%m-%d %H:%M:%S")
        PromoEndTime = datetime.strptime("9999-12-20 14:56:09", "%Y-%m-%d %H:%M:%S")
    for Line in File:
        Line = Line.upper()
        if Line.find("<TALLY>1</TALLY>") != -1:
            if Line.find("LOG_MESSAGE") < 0:
                PageTime = FindTag(Line, "TIME")
                PageAmPm = AmPm(PageTime) 
                PageTime = datetime.strptime(PageTime, "%m/%d/%Y %H:%M:%S %p")    #2/6/2019 10:00:13 AM
                PageHour = int(PageTime.hour)+ int(PageAmPm)
                if PageHour == 24:
                    PageHour = "00"
                PageTime = datetime.strptime(str(PageTime.year) + "-" + str(PageTime.month) + "-" + str(PageTime.day) + " " + str(PageHour) + ":" + str(PageTime.minute) + ":" + str(PageTime.second), "%Y-%m-%d %H:%M:%S")
                Template = FindTag(Line, "TEMPLATE")
                if Template.find("TOWER") < 0 and Template.find("SIDE_SWIPE") < 0 and Template.find("20005") < 0 and Template.find("TRAFFICLIGHT") < 0 and Template.find("20001") < 0 and Template.find("CUSTOMER_CHOICE") < 0:
                    if (PageTime > PromoStartTime and PageTime < PromoEndTime) == True:
                        PageSearch = txtPageName.get("1.0", "end-1c")
                        PageSearch = PageSearch.upper()
                        if PageSearch == "":
                            PageTime = ""
                        else:
                            PageTime = str(PageTime) + " "
                        if PageSearch == "" or PageSearch == "*":
                            Object.TakeList.append(" :" + PageTime + FindTag(Line, "PAGE") + ": ")
                            if Template.find("L3RD") != -1:
                                Object.LowerThird = Object.LowerThird + 1
                            if Template.find("BILLBOARD") != -1:
                                Object.Billboard = Object.Billboard + 1
                        elif PageSearch == FindTag(Line, "PAGE"):
                            Object.TakeList.append(" :" + PageTime + FindTag(Line, "PAGE") + ": ")
                            if Template.find("L3RD") != -1:
                                Object.LowerThird = Object.LowerThird + 1
                            if Template.find("BILLBOARD") != -1:
                                Object.Billboard = Object.Billboard + 1
    return Object

def SortTakes(Input):
    #Bubble sort the list
    #Numbers then A-Z
    for y in range(0, len(Input.TakeList) - 1):
        for i in range(0, len(Input.TakeList) - 1):
            if Input.TakeList[i] > Input.TakeList[i + 1]:
                Swap = Input.TakeList[i]
                Input.TakeList[i] = Input.TakeList[i + 1]
                Input.TakeList[i + 1] = Swap
    return Input

def CountTakes(Input):
    #Find how many takes of each list item there are
    #Only add reseilt to the output if is a new result
    for i in range(0, len(Input.TakeList)):
        if Input.OutputStr.find(str(Input.TakeList[i]) + str(Input.TakeList.count(Input.TakeList[i]))) < 0:
            Input.OutputStr = Input.OutputStr + str(Input.TakeList[i]) + str(Input.TakeList.count(Input.TakeList[i])) + "\n"
    return Input

def Summary(Input):
    #States that go on the end of the output
    EndSearchTime = datetime.now()
    Input.OutputStr = Input.OutputStr + "\n" + "Number of Promos: " + str(len(Input.TakeList)) + "\n"
    Input.OutputStr = Input.OutputStr + "Number of Lower Thirds: " + str(Input.LowerThird) + "\n"
    Input.OutputStr = Input.OutputStr + "Number of Billboards: " + str(Input.Billboard) + "\n"
    Input.OutputStr = Input.OutputStr + "Search Time: " + str(EndSearchTime - Input.StartSearchTime) + "\n"
    Input.OutputStr = Input.OutputStr.replace(" :" , "")
    txtOutput.insert(END, Input.OutputStr)

def ClearAll(Input):
    txtOutput.delete(1.0, END)
    Input.StartSearchTime = datetime.now()
    Input.TakeList = []
    Input.Billboard = 0
    Input.LowerThird = 0
    Input.LineCount = 0
    Input.OutputStr = ""
    return Input
    
def OpenOneFile():
    #Button to open a single log file to search
    #Lists file
    #Time range if used
    #Counts promos
    #Summery of search
    FilePath = filedialog.askopenfilename()
    if FilePath != "":
        Promos = PromosClass()
        Promos = ClearAll(Promos)
        Promos.OutputStr = FilePath + "\n"
        Lines = OpenFile(FilePath)
        Promos = FindPromos(Lines, Promos)
        Promos = SortTakes(Promos)
        if DateState.get() == 1:
            Promos.OutputStr = Promos.OutputStr + str(datetime.strptime(txtDate1.get("1.0", "end-1c"), "%Y-%m-%d %H:%M:%S")) + " - " + str(datetime.strptime(txtDate2.get("1.0", "end-1c"), "%Y-%m-%d %H:%M:%S")) + "\n"
        Promos.OutputStr = Promos.OutputStr + "Number Of Lines: " + str(len(Lines)) + "\n"
        PageSearch = txtPageName.get("1.0", "end-1c")
        PageSearch = PageSearch.upper()
        if PageSearch != "":
            Promos.OutputStr = Promos.OutputStr + "Page Search: " + PageSearch + "\n"
        Promos.OutputStr = Promos.OutputStr + "\n"
        CountTakes(Promos)
        Summary(Promos)

def OpenFolder():
    #Button to open a folder of log files to search
    #Won't search sub folders
    #Lists files
    #Time range if used
    #Counts promos
    #Summery of search
    DirList = filedialog.askdirectory()
    if str(DirList) != "":
        LineCount = 0
        Promos = PromosClass()
        Promos = ClearAll(Promos)
        ItemList = os.listdir(DirList)
        for Item in ItemList:
            if os.path.isfile(DirList + "/" + Item):
                Promos.OutputStr = Promos.OutputStr + DirList + "/" + Item + "\n"
                Lines = OpenFile(DirList + "/" + Item)
                Promos = FindPromos(Lines, Promos)
                LineCount = LineCount + len(Lines)
        Promos = SortTakes(Promos)
        if DateState.get() == 1:
            Promos.OutputStr = Promos.OutputStr + str(datetime.strptime(txtDate1.get("1.0", "end-1c"), "%Y-%m-%d %H:%M:%S")) + " - " + str(datetime.strptime(txtDate2.get("1.0", "end-1c"), "%Y-%m-%d %H:%M:%S")) + "\n"
        Promos.OutputStr = Promos.OutputStr + "Number Of Lines: " + str(LineCount) + "\n"
        PageSearch = txtPageName.get("1.0", "end-1c")
        PageSearch = PageSearch.upper()
        if PageSearch != "":
            Promos.OutputStr = Promos.OutputStr + "Page Search: " + PageSearch + "\n"
        Promos.OutputStr = Promos.OutputStr + "\n"
        CountTakes(Promos)
        Summary(Promos)

#Create form
#Grid manager
#Set dates to current start and end of hour
txtOutput = ScrolledText.ScrolledText(Form1, height=40, width=100)
lblPageName = Label(Form1, text="Optional Page Name or * ", justify=RIGHT)
txtPageName = Text(Form1, height=1, width=25)
lblStart = Label(Form1, text="Start Time", justify=RIGHT)
txtDate1 = Text(Form1, height=1, width=25)
lblEnd = Label(Form1, text="End Time", justify=RIGHT)
txtDate2 = Text(Form1, height=1, width=25)
DateState = IntVar()
ckDate = Checkbutton(Form1, text="Use YYYY-M-D H:M:S", variable=DateState)
btnFile = Button(Form1, text="Open File", command = OpenOneFile)
btnFolder = Button(Form1, text="Open Dir", command = OpenFolder)

txtOutput.grid(row=0,column=0,rowspan=40,columnspan=1)
lblPageName.grid(row=0,column=1)
txtPageName.grid(row=0,column=2)
lblStart.grid(row=1,column=1)
txtDate1.grid(row=1,column=2)
lblEnd.grid(row=2,column=1)
txtDate2.grid(row=2,column=2)
ckDate.grid(row=3,column=2)
btnFile.grid(row=3,column=1)
btnFolder.grid(row=4,column=1)

now = datetime.now()
# 2019-02-07 14:56:09.801933
txtDate1.insert(END, str(now.year) + "-" + str(now.month) + "-" + str(now.day) + " " + str(now.hour) + ":00:00")
txtDate2.insert(END, str(now.year) + "-" + str(now.month) + "-" + str(now.day) + " " + str(now.hour) + ":59:59")

mainloop()
