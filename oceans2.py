import os
from matplotlib import dates as md
import dateutil.parser
from onc.onc import ONC
import traceback

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

    def add_reading_values(self, values):
        self.readingValues.append(values)
        return

    def add_sample_times(self, times):
        self.sampleTimes.append(times)
        return

    def add_raw_sample_times(self, times):
        self.rawSampleTimes.append(times)
        return

    def add_unit_of_measure(self, unit):
        self.unitsOfMeasure.append(unit)
        return

    def add_sensor_name(self, name):
        self.sensorNames.append(name)
        return


def get_device_data(filters):
    try:
        results = onc.getDirectByDevice(filters)
    except:
        exit()
    try:
        location = onc.getLocations(filters)
    except:
        print("Could not find location.")
        location = {"locationName": ""}
    if len(results) == 0:
        print("Could not find location code with filters: " + filters)
        exit()
    graph_data = GraphData(location[0]["locationName"])
    counter = 0
    for parameter in results["sensorData"]:
        reading_values = list()
        sample_times = list()
        dates = list()
        for value in parameter["data"]["values"]:
            reading_values.append(value)
        for time in parameter["data"]["sampleTimes"]:
            sample_times.append(time)
        if len(reading_values) != 0 and len(sample_times) != 0:
            graph_data.add_reading_values(reading_values)
            graph_data.add_raw_sample_times(sample_times)
            graph_data.add_unit_of_measure(parameter["unitOfMeasure"])
            graph_data.add_sensor_name(parameter["sensorName"])
            for time in sample_times:
                dates.append(dateutil.parser.parse(time))
            datenums = md.date2num(dates)
            graph_data.add_sample_times(datenums)
    return graph_data


def export_data(name, parameter, dates, values):
    try:
        f = open(os.getcwd() + "/" + name + "-" + parameter + ".txt", "w+")
    except FileNotFoundError or FileExistsError:
        print("Unable to create file please confirm file path")
        return
    f.write(name + "\n")
    f.write("Sample Time: " + parameter + "\n")
    counter = 0
    for date in dates:
        f.write(date + " |  %f\n" % values[counter])
    f.close()
    return


def get_device_codes(filters):
    try:
        results = onc.getDevices(filters)
    except:
        exit()
    if len(results) == 0:
        print("Could not find location code with filters: " + filters)
        exit()
    for device in results:
        print(device["deviceName"], "\n", "Device Code: ",
              device["deviceCode"], "\n",
              "Device ID: ", device["deviceId"], "\n")
    return results


def get_location_codes(filters):
    try:
        results = onc.getLocations(filters)
    except:
        exit()
    if len(results) == 0:
        print("Could not find location code with filters: " + filters)
        exit()
    counter = 1
    for location in results:
        print("{0}. ".format(counter) + location["locationName"])
        print("Location Code: " + location["locationCode"] + "\n")
        counter += 1
    return results


def get_location_code_by_category(filters):
    try:
        results = onc.getLocations(filters)
    except:
        exit()
    if len(results) == 0:
        print("Could not find location code with filters: " + filters)
        exit()
    counter = 1
    for location in results:
        print("{0}. ".format(counter) + location["locationName"])
        print("Location Code: " + location["locationCode"] + "\n")
        counter += 1
    return results


def get_data_product_codes(filters):
    try:
        results = onc.getDataProducts(filters)
    except:
        exit()
    if len(results) == 0:
        print("Could not find location code with filters: " + filters)
        exit()
    counter = 1
    for product in results:
        print("{0}. ".format(counter) + product["dataProductName"])
        print(product["dataProductCode"] + "\n")
        counter += 1
    return results


def download_data_product(filters):
    try:
        results = onc.orderDataProduct(filters)
    except:
        exit()
    if len(results) == 0:
        print("Could not find location code with filters: " + filters)
        exit()
    onc.print(results)
    return results
