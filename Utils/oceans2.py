from Utils.apicheck import get_key
import os
from matplotlib import dates as md
import dateutil.parser
from onc.onc import ONC
import re

cwd = os.getcwd()
apikey = get_key(None)
onc = ONC(apikey, outPath=cwd)

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
        for value in values:
            if type(value) is not float:
                raise TypeError("Input is a not list of floats")
        self.readingValues.append(values)
        return

    def add_sample_times(self, times):
        for time in times:
            if type(time) is not float:
                raise TypeError("Input not a list of matplotlib date objects")
        self.sampleTimes.append(times)
        return

    def add_raw_sample_times(self, times):
        pattern = re.compile("[0-9]{4}[-][0-9]{2}[-][0-9]{2}[T][0-9]{2}[:][0-9]{2}[:][0-9]{2}[.][0-9]{3}[Z]")
        for time in times:
            if not pattern.match(time):
                raise TypeError("Input is not a list of raw date strings")
        self.rawSampleTimes.append(times)
        return

    def add_unit_of_measure(self, unit):
        if type(unit) is not str:
            raise TypeError("Input is not a string")
        self.unitsOfMeasure.append(unit)
        return

    def add_sensor_name(self, name):
        if type(name) is not str:
            raise TypeError("Input is not a string")
        self.sensorNames.append(name)
        return


def get_graph_data(filters):
    try:
        results = onc.getDirectByDevice(filters)
    except:
        return None, None
    try:
        location = onc.getLocations(filters)
    except:
        print("Could not find location.")
        location = {"locationName": ""}
    if len(results) == 0:
        print("Could not find location code with filters: " + filters)
        return None, None
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
    return results, graph_data


def get_device_data(filters):
    try:
        results = onc.getDirectByDevice(filters)
    except:
        print("Could not find device data with given filters")
        return None, None
    if len(results) == 0:
        print("Could not find device data with given filters")
        return None, None
    trimmed_results = dict()
    sample_times = dict()
    if results["sensorData"] is not None:
        for parameter in results["sensorData"]:
            trimmed_results[parameter["sensorName"]] = parameter["data"]["values"]
            sample_times[parameter["sensorName"]] = parameter["data"]["sampleTimes"]
    return trimmed_results, sample_times


def get_device_properties(filters):
    try:
        results = onc.getProperties(filters)
    except:
        print("Could not find device properties with given filters")
        return None, None
    if not results:
        print("Could not find device properties with given filters")
        return None, None
    properties = dict()
    for param in results:
        properties[param["propertyCode"]] = (param["propertyName"], param["description"], param["hasDeviceData"])
    return results, properties


def export_data(name, parameter, dates, values, extension):
    try:
        f = open(os.getcwd() + "/" + name + "-" + parameter + "." + extension, "w+")
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
        return None, None
    if len(results) == 0:
        print("Could not find location code with given filters")
        return None, None
    devices = dict()
    for device in results:
        devices[device["deviceName"]] = device["deviceCode"]
    return results, devices


def get_location_codes(filters):
    try:
        results = onc.getLocations(filters)
    except:
        return None, None
    if len(results) == 0:
        print("Could not find location code with given filters")
        return None, None
    locations = dict()
    for location in results:
        locations[location["locationName"]] = location["locationCode"]
    return results, locations


def get_location_code_by_category(filters):
    try:
        results = onc.getLocations(filters)
    except:
        return None, None
    if len(results) == 0:
        print("Could not find location code with given filters")
        return None, None
    locations = dict()
    for location in results:
        locations[location["locationName"]] = location['locationCode']
    return results, locations


def get_device_categories(filters):
    try:
        results = onc.getDeviceCategories(filters)
    except:
        return None, None
    if len(results) == 0:
        print("Could not find categories with given filters")
        return None, None
    categories = dict()
    for category in results:
        categories[category["deviceCategoryName"]] = (category["deviceCategoryCode"], category["description"])
    return results, categories


# Needs to consider location code input and provide all devices
def get_data_product_codes(filters):
    try:
        results = onc.getDataProducts(filters)
    except:
        return None, None
    if len(results) == 0:
        print("Could not find location code with given filters")
        return None, None
    products = dict()
    for product in results:
        products[product["dataProductName"]] = (product["dataProductCode"], product["extension"])
    return results, products


def get_date_information(filters):
    try:
        results = onc.getDeployments(filters)
    except:
        return None, None
    if len(results) == 0:
        print("Could not find date information with given filters")
        return None, None
    deployments = dict()
    for deployment in results:
        if deployment["end"] is None:
            deployments[deployment["begin"]] = "Present"
        else:
            deployments[deployment["begin"]] = deployment["end"]
    return results, deployments


def download_data_product(filters):
    try:
        results = onc.orderDataProduct(filters)
    except:
        return None
    if len(results) == 0:
        print("Could not find location code with given filters")
        return None
    return results
