import math
import time
import sys
import os

def fileReading():
    dir_name = os.path.dirname(__file__)
    file_name = os.path.join(dir_name, 'Antoine_Coefficients.csv')
    file_reading = open(file_name, "r")
    Formula_list, Compound_list, A_list, B_list, C_list, Tmin_list, Tmax_list = [], [], [], [], [], [], []
    return Formula_list, Compound_list, A_list, B_list, C_list, Tmin_list, Tmax_list, file_reading

def dictionaryCreation(Formula_list, Compound_list, A_list, B_list, C_list, Tmin_list, Tmax_list, file):
    dictionary = {}
    for row in file:
        row_list = row.split(",")
        Formula_list.append(row_list[0])
        Compound_list.append(row_list[1])
        A_list.append(row_list[2])
        B_list.append(row_list[3])
        C_list.append(row_list[4])
        Tmin_list.append(row_list[5])
        Tmax_list.append(row_list[6])
        dictionary_value_list = []
        dictionary_value_list.append(row_list[0])
        dictionary_value_list.append(row_list[2])
        dictionary_value_list.append(row_list[3])
        dictionary_value_list.append(row_list[4])
        dictionary_value_list.append(row_list[5])
        dictionary_value_list.append(row_list[6])
        dictionary_value_list.append(row_list[1])
        dictionary[row_list[1]] = dictionary_value_list
    return dictionary_value_list, dictionary

def Ongoing(quit_key):
    while True and quit_key != "Q":
        quit_key = main(Formula_list, Compound_list, A_list, B_list, C_list, Tmin_list, Tmax_list, file_read)
    return

def main(Formula_list, Compound_list, A_list, B_list, C_list, Tmin_list, Tmax_list, file_read):
    quit_key = ""
    compound_input, parameter_input, value_input = userInputs(dictionary, quit_key)
    dictionary_value_list_inputs = dictionary[compound_input]
    a_input = float(dictionary_value_list_inputs[1])
    b_input = float(dictionary_value_list_inputs[2])
    c_input = float(dictionary_value_list_inputs[3])
    compound_name = dictionary_value_list_inputs[6]
    quit_key = Calculations(a_input, b_input, c_input, value_input, dictionary_value_list_inputs, parameter_input)
    return quit_key

def userInputs(dictionary, quit_key):
    print("\n***Note: If you want water between 1 and 100 degrees C, type \"water_low\", if you want water between 99 and 374 degrees C, type \"water_high\"")
    compound_input = (input("\nEnter the name for the compound. If it has a space, replace it with \"-\" like carbon-monoxide: ")).lower()
    isCompoundinDatabase(compound_input, dictionary, quit_key)
    paramater_input = input("\nEnter \"T\" for a temperature, or \"P\" for a pressure for the value you are inputting: ")
    isParameterInputValid(paramater_input, quit_key)
    value_input = input("\nEnter input pressure or temperature value. If Pressure, it must be in mmHg or Torr. If Temperature, it must be in Celsius: ")
    value_input = isValueInputValid(value_input, quit_key)
    return compound_input, paramater_input, value_input

def isCompoundinDatabase(compound_input, dictionary, quit_key):
    if compound_input in dictionary:
        print("\nThe compound is in the database!")
    else:
        print("\nSorry, it appears the compound you entered is not in the database. Try again!")
        Ongoing(quit_key)
    return

def isParameterInputValid(parameter_input, quit_key):
    if (parameter_input != "P" and parameter_input != "T"):
        print("\nSorry, but the parameter you entered is not valid. Maybe try uppercase P or T?")
        Ongoing(quit_key)
    return

def isValueInputValid(value_input, quit_key):
    try:
        value_input = float(value_input)
    except:
        print("\n Sorry, but the value you entered is not a valid number. Try again! ")
        Ongoing(quit_key)
    return value_input

def Calculations(a_input, b_input, c_input, value_input, dictionary_value_list_inputs, paramater_input):
    if a_input != None:
        if paramater_input == "T" and value_input > float(dictionary_value_list_inputs[4]) and value_input < float(dictionary_value_list_inputs[5]):
            calculation = Temperature(a_input, b_input, c_input)
            calculation.TemperatureCalc(value_input, a_input, b_input, c_input, dictionary_value_list_inputs)
        elif paramater_input == "T" and (value_input < float(dictionary_value_list_inputs[4]) or value_input > float(dictionary_value_list_inputs[5])):
            print("The entered temperature will not give an accurate value for an equilibrium vapour pressure")
            print("Try a temperature between: " + str(float(dictionary_value_list_inputs[4])) + " and "+ str(float(dictionary_value_list_inputs[5])) + " degrees Celsius")
        elif paramater_input == "P":
            calculation = Pressure(a_input, b_input, c_input)
            calculation.PressureCalc(value_input, a_input, b_input, c_input, dictionary_value_list_inputs)
        quit_key= input("\nIf you wish the exit the calculator, press \"Q\" now. If not, press any other key to continue. ")
        if quit_key == "Q":
            print("\nThank you for using the calculator, have a good day! =)")
            sys.exit()
    return quit_key

class AntoineAnalysis:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
class Temperature(AntoineAnalysis):
    def TemperatureCalc(self, value_input, a_input, b_input, c_input, dictionary_value_list_inputs):
        antoine = AntoineAnalysis(a_input, b_input, c_input)
        exponent = antoine.a - (antoine.b)/(value_input + antoine.c)
        final_pressure = 10 ** exponent
        final_pressure = "{:.3f}".format(final_pressure)
        print("\nFor the compound " + str(dictionary_value_list_inputs[0]) + ", (" + str(dictionary_value_list_inputs[6])+") and the entered temperature, the equilibrium vapour pressure is " + final_pressure + " mmHg.")
class Pressure(AntoineAnalysis):
    def PressureCalc(self, value_input, a_input, b_input, c_input, dictionary_value_list_inputs):
        antoine = AntoineAnalysis(a_input, b_input, c_input)
        final_temperature = antoine.b / (antoine.a - math.log(value_input, 10)) - antoine.c
        final_temperature = "{:.3f}".format(final_temperature)
        print("\nFor the compound " + str(dictionary_value_list_inputs[0])+ ", (" + str(dictionary_value_list_inputs[6])+") and the entered vapour pressure, the equilibrium temperature is "+ final_temperature + " degrees C.")

quit_key = ""
for i in range(1, 4):
    display = "Loading" + "." * i
    print(display)
    time.sleep(0.25)
print("\nAntoine Equation Calculator")
time.sleep(0.5)
Formula_list, Compound_list, A_list, B_list, C_list, Tmin_list, Tmax_list, file_read = fileReading()
dictionary_value_list, dictionary = dictionaryCreation(Formula_list, Compound_list, A_list, B_list, C_list, Tmin_list,Tmax_list, file_read)
Ongoing(quit_key)
