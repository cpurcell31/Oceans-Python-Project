import os, sys
import oceans2 as o2
import argparse
from onc.onc import ONC
from oceans2 import onc

parser = argparse.ArgumentParser(description='ONC Search: searches ' +
        'for ONC installation locations, location codes, and device codes' +
        'prints out results to command line')

parser.add_argument('-l', '--locationName', type=str,
        help='Input partial or full location name to find location code of '+
        'ONC installations')
parser.add_argument('-c', '--locationCode', type=str,
        help='Input location code for ONC installation to find all devices '+
        'at the respective location')
parser.add_argument('-d', '--deviceCategory', type=str,
        help='Input device category code to find all locations with given ' +
        'device type')
parser.add_argument('-D', '--deviceCode', type=str,
        help='')
parser.add_argument('-p', '--findProduct', action='store_true',
        help='')

args = parser.parse_args()
location_name = args.locationName
location_code = args.locationCode
device_category_code = args.deviceCategory
device_code = args.deviceCode
product_code = args.findProduct

if product_code and (device_code or device_category_code or location_code):
    filters = {'locationCode' : location_code,
            'deviceCategoryCode' : device_category_code,
            'deviceCode' : device_code}
    o2.getDataProductCodes(filters)

elif location_name:
    filters = {'locationName' : location_name}
    o2.getLocationCodes(filters)

elif location_code:
    filters = {'locationCode' : location_code}
    o2.getDeviceCodes(filters)

elif device_category_code:
    filters = {'deviceCategoryCode' : device_category_code}
    o2.getLocationsByCategory(filters)

exit()
