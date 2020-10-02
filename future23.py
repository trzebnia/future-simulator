import math 
import sys
import copy
from os import system, name

#Numbers parent class ----------------------------------------------------------
class Numbers:
    def __init__(self, level, value):
        self.level = level
        self.value = value
              
                
#Events child class ----------------------------------------------------------                
class Events(Numbers):
    def __init__(self, name, level, value, happened = False):
        super().__init__(level, value)
        self.name = name
        self.happened = happened
        
    #Checks if any event should be displayed at given tick ----------------------------------------------------------   
    def check(self):
        if clockDict["year"].level == self.level:
            if clockDict["year"].value > self.value:
                if self.happened == False:
                    print (self.name)
                    self.happened = True
                
                
#ClockClass child class ----------------------------------------------------------        
class Clock(Numbers):
    def __init__(self, level, value):
        super().__init__(level, value)


#Default events ----------------------------------------------------------
def createEventsList():
    global eventsList
    eventsList = []
    eventsList.append (Events("Sea levels rise by 4 meters", 0, 1e+4)) 
    eventsList.append (Events("Milky Way and Andromeda collide", 0, 4e+9)) 
    eventsList.append (Events("Planets leave their orbits", 0, 4e+15)) 
    eventsList.append (Events("Stars fall into black holes", 0, 4e+30)) 
    eventsList.append (Events("Proton decay", 0, 2e+43)) 
    eventsList.append (Events("Rigid objects become smooth", 0, 1e+65)) 
    eventsList.append (Events("Positroniums appear", 0, 1e+85)) 
    eventsList.append (Events("Dark Age begins", 0, 1.7e+106)) 
    eventsList.append (Events("False vacuum colapses", 0, 1e+139)) 
    eventsList.append (Events("All nucleons decay", 0, 1e+200)) 
    eventsList.append (Events("Formation of iron stars", 1, 1500)) 
    eventsList.append (Events("Iron stars collapse into black holes (low estimate)", 1, 1e+26)) 
    eventsList.append (Events("Boltzmann brain appears", 1, 1e+50)) 
    eventsList.append (Events("Iron stars collapse into black holes (high estimate)", 1, 1e+76)) 
    eventsList.append (Events("Entropy reaches maximum", 1, 1e+120)) 
    eventsList.append (Events("New big bang", 2, 1e+56)) 

#Default clock values ----------------------------------------------------------
def createClockDict():
    global clockDict
    clockDict = {}
    clockDict["year"] = Clock(0, 2020)
    clockDict["speed"] = Clock(0, 1)
    clockDict["skip"] = Clock(0, 60)
    clockDict["duration"] = Clock(0, 0)
    clockDict["simulateTime"] = Clock(0, 60*60)
    
    acceleratorType = {}
    acceleratorType["base"] = Clock(0, 2)
    acceleratorType["time"] = Clock(0, 5)
    acceleratorList = []
    acceleratorList.append(acceleratorType)
    clockDict["accelerator"] = acceleratorList

#Displays duration of run and current date every self.skip.value (20) ticks ----------------------------------------------------------
def display():
    if clockDict["duration"].value % clockDict["skip"].value == 0:
        print ("")  
        print("Duration: ", displayTimers(clockDict["duration"]))
        print("Year: ", displayValues(clockDict["year"]))
   
#Changing time, speed and increments, needs update - stops working on higher levels ----------------------------------------------------------        
def forward():
    clockDict["duration"].value += 1

    count = len(clockDict["accelerator"])
    while count > 0:
        if count > 1:
            if clockDict["duration"].value % clockDict["accelerator"][count-1]["time"].value == 0:
                multiply(clockDict["accelerator"][count-2]["base"], clockDict["accelerator"][count-1]["base"])
        else:
            if clockDict["duration"].value % clockDict["accelerator"][count-1]["time"].value == 0:
                multiply(clockDict["speed"], clockDict["accelerator"][count-1]["base"])
        count -= 1
    
    add(clockDict["year"], clockDict["speed"])
    

#Checks if number's level should be increased, 1e+200 might be changed ----------------------------------------------------------
def increaseLevelCheck(self):
    if self.level == 0:
        if self.value > 1e+200:
            increaseLevel(self)      
        
#Adding numbers with level 0 and 1 ----------------------------------------------------------           
def add(number1, number2):
    ordered, tempOrder = order(number1, number2)
    
    if number1.level == 0:
        number1.value += number2.value
    
    elif number1.level == 1:
        increased = False
        if number2.level == 0:
            increased, tempIncrease = increaseLevel(number2)
        
        number2Integers = math.floor(number2.value)
        number1Decreased = number1.value - number2Integers
        number2Decreased = number2.value - number2Integers
        
        if number1Decreased < 100:
            number1.value += math.log10(10 ** number1Decreased + 10 ** number2Decreased) - number1Decreased
            
        if increased == True:
            number2.level = tempIncrease.level
            number2.value = tempIncrease.value
        
    reorder(number2, tempOrder, ordered)

#Multiplying numbers with level 0 and 1 ----------------------------------------------------------  
def multiply(number1, number2):
    ordered, tempOrder = order(number1, number2)
    
    if number1.level == 0:
        number1.value *= number2.value
        
    elif number1.level == 1:
        increased = False
        if number2.level == 0:
            increased, tempIncrease = increaseLevel(number2)
            
        number1.value += number2.value
        
        if increased == True:
            number2.level = tempIncrease.level
            number2.value = tempIncrease.value
        
    reorder(number2, tempOrder, ordered)
        
#Level increase ----------------------------------------------------------        
def increaseLevel(number):
    temp = copy.copy(number)
    number.value = (math.log10(number.value))
    number.level += 1 
    return True, temp


#Ordering numbers for adding so that the first number is always bigger, might be changed / deleted ----------------------------------------------------------
def order(number1, number2):
    if number1.level < number2.level or number1.level == number2.level and number1.value < number2.value:
        temp = copy.copy(number2)
        number2 = number1
        number1 = temp
        return True, temp
    else:
        return False, False

#Loads previous state of second value ----------------------------------------------------------
def reorder(number2, temp, ordered):
    if ordered == 1:
        number2 = temp

#Main Loop ----------------------------------------------------------
def simulate():
    initialYear = Clock(clockDict["year"].level, clockDict["year"].value)
    initialSpeed = Clock(clockDict["speed"].level, clockDict["speed"].value)
    initialAccelerators = copy.deepcopy(clockDict["accelerator"])
        
    
    while clockDict["duration"].value <= clockDict["simulateTime"].value:
        display()
        
        if clockDict["year"].level == 1:
            if clockDict["year"].value > 1e+120:
                print ("Past this point no event will be reached before program overflows.")
                input("Press Enter to continue...")
                console()
        
        for obj in eventsList:
            obj.check()
            
        for obj in clockDict:
            if obj != "accelerator":
                increaseLevelCheck(clockDict[obj])
            
        forward()
        
    clockDict["duration"].value = 0
    clockDict["year"] = initialYear
    clockDict["speed"] = initialSpeed
    clockDict["accelerator"] = copy.deepcopy(initialAccelerators)
    
    print("Simulation finished.")
    input("Press Enter to continue...")
    console()    
        
        
#Clear Console ----------------------------------------------------------
def clear(): 
    if name == 'nt': 
        _ = system('cls') 
  
    else: 
        _ = system('clear') 
        
#Prepare potentially values for display ----------------------------------------------------------
def displayValues(number):
    increased = False
    if number.value > 1e+6:
        increased, tempIncrease = increaseLevel(number) 

    if number.level == 0:
        value = number.value
    elif number.level == 1:
        value = "10^" + str(number.value)
    elif number.level == 2:
        value = "10^10^" + str(number.value)
    elif number.level == 3:
        value = "10^10^10^" + str(number.value)
        
    if increased == True:
        number.level = tempIncrease.level
        number.value = tempIncrease.value

    return value
    
#Prepare small values for display ----------------------------------------------------------
def displayTimers(number):
    value = number.value
    unit = " s"
    
    if value >= 600:
        value //= 60
        unit = " m"
        
        if value >= 600:
            value //= 60
            unit = " h"
            
            if value >= 72:
                value //= 24
                unit = " d"

    return str(int(value)) + unit
    
#changing starting values ----------------------------------------------------------
def change(option):
    if option == "year":
        try:
            clockDict["year"].value = int(input("Starting year: "))
        except ValueError:
            print("Please input only a number.")
            input("Press Enter to continue...")
            print("")
            change("year")
            
    elif option == "speed":
        try:
            clockDict["speed"].value = int(input("Starting speed in years/s: "))
        except ValueError:
            print("Please input only a number.")
            input("Press Enter to continue...")
            print("")
            change("speed")
        
    elif option == "skip":
        print ("Enter the time between each update")
        print ("ex. 5 m")
        print ("Units: s/m/h/d")
        
        skipOption = input("Time beetwen updates: ")
        skipOptionSplit = skipOption.split(" ")
        try:
            skipValue = int(skipOptionSplit[0])
        except ValueError:
            print("Value needs to be a number")
            input("Press Enter to continue...")
            print("")
            change("skip")
        
        try:
            if skipOptionSplit[1] == "s":
                pass
            elif skipOptionSplit[1] == "m":
                skipValue *= 60
            elif skipOptionSplit[1] == "h":
                skipValue *= 60*60
            elif skipOptionSplit[1] == "d":
                skipValue *= 60*60*24
            else:
                print("Incorrect unit")
                input("Press Enter to continue...")
                print ("")
                change("skip")
        except IndexError:
            print("Space is required between value and unit")
            input("Press Enter to continue...")
            print("")
            change("skip")
        
        clockDict["skip"].value = skipValue
        
    elif option == "max":
        print ("Enter the time for simulation with a unit of time")
        print ("ex. 5 m")
        print ("Units: s/m/h/d")
        
        maxOption = input("Maximum length of simulation: ")
        maxOptionSplit = maxOption.split(" ")
        try:
            maxValue = int(maxOptionSplit[0])
        except ValueError:
            print("Value needs to be a number")
            input("Press Enter to continue...")
            print("")
            change("max")
        
        try:
            if maxOptionSplit[1] == "s":
                pass
            elif maxOptionSplit[1] == "m":
                maxValue *= 60
            elif maxOptionSplit[1] == "h":
                maxValue *= 60*60
            elif maxOptionSplit[1] == "d":
                maxValue *= 60*60*24
            else:
                print("Incorrect unit")
                input("Press Enter to continue...")
                print ("")
                change("max")
        except IndexError:
            print("Space is required between value and unit")
            input("Press Enter to continue...")
            print("")
            change("max")
        
        clockDict["simulateTime"].value = maxValue
        
    #Accelerator panel ----------------------------------------------------------
    elif option == "accelerator":
        clear()
        print ("ACCELERATORS")
        count = 0
        while count < len(clockDict["accelerator"]):
            print ("Accelerator " + str(count) + ":  " + str(clockDict["accelerator"][count]["base"].value) + "x  :  " + str(clockDict["accelerator"][count]["time"].value) + "s")
            count += 1
            
        print ("""
ACCELERATOR OPTIONS:
add
delete n - deletes nth accelerator
change n value/time - changes value or time between activations
default
back
        """)
        choice = input("Option: ")
        command = choice.split(" ") 
        
        if command[0] == "add":   
            try:
                newAcceleratorBase = int(input("Starting multiplier: "))
                newAcceleratorTime = int(input("Timer: "))
            except ValueError:
                print("Please input only a number.")
                input("Press Enter to continue...")
                print("")
                change("accelerator")
            
            newAccelerator = {}
            newAccelerator["base"] = Clock(0, newAcceleratorBase)
            newAccelerator["time"] = Clock(0, newAcceleratorTime)
            clockDict["accelerator"].append(newAccelerator)
            
        elif command[0] == "delete":
            try:
                del clockDict["accelerator"][int(command[1])]
            except IndexError:
                print("Please choose an existing accelerator")
                input("Press Enter to continue...")
                print("")
                change("accelerator")
                
            
        elif command[0] == "change":
            try:
                if command[2] == "value": 
                    try:
                        clockDict["accelerator"][int(command[1])]["base"].value = int(input("Starting multiplier: "))
                    except ValueError:
                        print("Please input only a number.")
                        input("Press Enter to continue...")
                        print("")
                        change("accelerator")
                    
                elif command[2] == "time":
                    try:
                        clockDict["accelerator"][int(command[1])]["time"].value = int(input("Timer: "))
                    except ValueError:
                        print("Please input only a number.")
                        input("Press Enter to continue...")
                        print("")
                        change("accelerator")
            except IndexError:
                print("Please choose an existing accelerator and value to change")
                input("Press Enter to continue...")
                print("")
                change("accelerator")
            
        elif command[0] == "back":
            console()
            
        elif command[0] == "default":
            clockDict["accelerator"].clear()
            
            acceleratorType = {}
            acceleratorType["base"] = Clock(0, 2)
            acceleratorType["time"] = Clock(0, 5)
            clockDict["accelerator"].append(acceleratorType)
            
        else:
            print ("Invalid input")
            input("Press Enter to continue...")
            print ("")
            change("accelerator")
            
        change("accelerator")
        
    #Other options ----------------------------------------------------------
    elif option == "back":    
        pass 
        
    else:
        print ("Invalid input")
        input("Press Enter to continue...")
        
    console()    

        
#Saves current settings to txt file ----------------------------------------------------------
def save():
    file = open("Settings.txt", "w")
    
    year = "year " + str(clockDict["year"].level) + " " + str(clockDict["year"].value) + "\n"
    file.write(year)
    
    speed = "speed " + str(clockDict["speed"].level) + " " + str(clockDict["speed"].value) + "\n"
    file.write(speed)
    
    skip = "skip " + str(clockDict["skip"].level) + " " + str(clockDict["skip"].value) + "\n"
    file.write(skip)
    
    simulateTime = "simulateTime " + str(clockDict["simulateTime"].level) + " " + str(clockDict["simulateTime"].value) + "\n"
    file.write(simulateTime)
    
    count = 0
    while count < len(clockDict["accelerator"]):
        acceleratorBase = "accelerator " + str(count) + " base " + str(clockDict["accelerator"][count]["base"].level) + " " + str(clockDict["accelerator"][count]["base"].value) + "\n"
        acceleratorTime = "accelerator " + str(count) + " time " + str(clockDict["accelerator"][count]["time"].level) + " " + str(clockDict["accelerator"][count]["time"].value) + "\n"
        file.write(acceleratorBase)
        file.write(acceleratorTime)
        count += 1
        
    file.close()
    console()
    
#Loads settings from txt file ----------------------------------------------------------
def load():
    try:
        file = open("Settings.txt", "r")
        
        acceleratorType = {}
        acceleratorList = []
        clockDict["accelerator"] = []

        for line in file:
            lineList = line.split(" ")  
            if lineList[0] == "year" or lineList[0] == "speed" or lineList[0] == "skip" or lineList[0] == "simulateTime":
                clockDict[lineList[0]].level = int(lineList[1])
                clockDict[lineList[0]].value = int(lineList[2])
                
            elif lineList[0] == "accelerator":
                acceleratorType[lineList[2]] = Clock(int(lineList[3]), int(lineList[4]))
                if lineList[2] == "time":
                    acceleratorList.append(acceleratorType)
                    acceleratorType = {}
                    
        clockDict["accelerator"] = acceleratorList        
        
            
        file.close()
        console()
    except:
        print ("Cannot locate the settings file")
        input("Press Enter to continue...")
        print("")
        console()
    
#Console ----------------------------------------------------------
def console():
    clear()
    
    print ("""OPTIONS:
start
exit
change year/speed/skip/max/accelerator - changes starting values (don't enter values in this field)
default
save
load
    """)
    
    print ("CONFIGURATION: ")
    print ("Starting year: ", displayValues(clockDict["year"]))
    print ("Starting speed: ", displayValues(clockDict["speed"]), " years per second")
    print ("Display intervals: ", displayTimers(clockDict["skip"]))
    print ("Maximum length of simulation: ", displayTimers(clockDict["simulateTime"]))

    count = 0
    while count < len(clockDict["accelerator"]):
        print ("Accelerator " + str(count) + ":  " + str(clockDict["accelerator"][count]["base"].value) + "x  :  " + str(clockDict["accelerator"][count]["time"].value) + "s")
        count += 1
    
    print ("")
    
    choice = input("Option: ")
    
        
    if choice == "start":
        simulate()
        
    elif choice == "exit":
        sys.exit()
        
    elif choice[0 : 6] == "change":
        change(choice[7 :])
        
    elif choice == "default":
        createEventsList()
        createClockDict()
        console()
        
    elif choice == "save":
        save()
    
    elif choice == "load":
        load()
        
    else:
        print ("Invalid input")
        input("Press Enter to continue...")
        console()

createEventsList()
createClockDict()
console()