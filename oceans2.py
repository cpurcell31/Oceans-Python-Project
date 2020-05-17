import sys, os
from os import path
import argparse
from matplotlib import dates as md
import dateutil.parser

from onc.onc import ONC
cwd = os.getcwd()
onc = ONC('APIHERE', outPath=cwd)

locationNames = list()
locationCodes = list()
deviceCodes = list()


class GraphData:
    def __init__(self, location):
        self.locationName = location
        self.sensorNames = list()
        self.unitsOfMeasure = list()
        self.sampleTimes = list()
        self.rawSampleTimes = list()
        self.readingValues = list()

    def addReadingValues(self, values):
        self.readingValues.append(values)
        return

    def addSampleTimes(self, times):
        self.sampleTimes.append(times)
        return
    
    def addRawSampleTimes(self, times):
        self.rawSampleTimes.append(times)
        return

    def addUnitOfMeasure(self, unit):
        self.unitsOfMeasure.append(unit)
        return

    def addSensorName(self, name):
        self.sensorNames.append(name)
        return

def getDeviceData(filters):
    try:
        results = onc.getDirectByDevice(filters)
    except:
        print("Invalid device code. Please confirm device code")
        exit()
    try:
        location = onc.getLocations(filters)
    except:
        print("Could not find location.")
        location = {"locationName": ""}
    graph_data = GraphData(location[0]["locationName"])
    counter = 0
    for parameter in results["sensorData"]:
        readingValues = list()
        sampleTimes = list()
        dates = list()
        for value in parameter["data"]["values"]:
            readingValues.append(value)
        for time in parameter["data"]["sampleTimes"]:
            sampleTimes.append(time)
        if len(readingValues) != 0 and len(sampleTimes) != 0:
            graph_data.addReadingValues(readingValues)
            graph_data.addRawSampleTimes(sampleTimes)
            graph_data.addUnitOfMeasure(parameter["unitOfMeasure"])
            graph_data.addSensorName(parameter["sensorName"])
            for time in sampleTimes:
                dates.append(dateutil.parser.parse(time))
            datenums = md.date2num(dates)
            graph_data.addSampleTimes(datenums)
    return graph_data

def exportData(name, parameter, dates, values):
    try:
        f = open(os.getcwd() + "/" + name + "-" + parameter + ".txt", "w+")
    except:
        print("Unable to create file please confirm file path")
        return
    f.write(name + "\n")
    f.write("Sample Time: " + parameter + "\n")
    counter = 0
    for date in dates:
        f.write(date +" |  %f\n" %values[counter])
    f.close()
    return

def getDeviceCodes(filters):
    try:
        results = onc.getDevices(filters)
    except:
        print("Could not find location with given location code. " +
                "Please confirm location code")
        exit()
    for device in results:
        print(device["deviceName"], "\n", "Device Code: ",
                device["deviceCode"], "\n",
                "Device ID: ", device["deviceId"], "\n")
    return results

def getLocationCodes(filters):
    try:
        results = onc.getLocations(filters)
    except:
        print("Could not find any locations with the name: ", location_name)
        exit()
    if len(results) == 0:
        print("Could not find any locations with the name: ", location_name)
    counter = 1
    for location in results:
        print("{0}. ".format(counter) + location["locationName"])
        print("Location Code: " + location["locationCode"] + "\n")
        counter += 1
    return results

def getLocationCodeByCategory(filters):
    try:
        results = onc.getLocations(filters)
    except:
        print("No devices with given category code found. Please confirm" +
                " device category code")
        exit()
    counter = 1
    for location in results:
        print("{0}. ".format(counter) + location["locationName"])
        print("Location Code: " + location["locationCode"] + "\n")
        counter += 1
    return results

def getDataProductCodes(filters):
    try:
        results = onc.getDataProducts(filters)
    except:
        print("No data products could be found with the given filters" +
                " please confirm codes entered")
        exit()
    counter = 1
    for product in results:
        print("{0}. ".format(counter) + product["dataProductName"])
        print(product["dataProductCode"] + "\n")
        counter += 1
    return results

def downloadDataProduct(filters):
    try:
        results = onc.orderDataProduct(filters)
    except:
        print("")
        exit()
    onc.print(results)
    return results
