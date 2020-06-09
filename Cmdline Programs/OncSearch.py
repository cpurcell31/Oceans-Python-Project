import argparse
from Utils import oceans2 as o2


def main(arguments):
    location_name = arguments.locationName
    location_code = arguments.locationCode
    device_category_code = arguments.deviceCategory
    device_code = arguments.deviceCode
    product_code = arguments.findProduct
    date = arguments.date

    if product_code and (device_code or device_category_code or location_code):
        filters = {'locationCode': location_code,
                   'deviceCategoryCode': device_category_code,
                   'deviceCode': device_code}
        o2.get_data_product_codes(filters)

    elif location_name:
        filters = {'locationName': location_name}
        results, locations = o2.get_location_codes(filters)
        print(locations)

    elif location_code:
        filters = {'locationCode': location_code}
        results, devices = o2.get_device_codes(filters)
        print(devices)

    elif device_category_code:
        filters = {'deviceCategoryCode': device_category_code}
        o2.get_location_code_by_category(filters)

    if date and device_code:
        filters = {'deviceCode': device_code}
        o2.get_date_information(filters)

    exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ONC Search: searches ' +
                                                 'for ONC installation locations, location codes, data product codes' +
                                                 'and device codes prints out results to command line')

    parser.add_argument('-l', '--locationName', type=str,
                        help='Input partial or full location name to find location code of ' +
                             'ONC installations')
    parser.add_argument('-c', '--locationCode', type=str,
                        help='Input location code for ONC installation to find all devices ' +
                             'at the respective location. Can be used in conjunction with the -p option')
    parser.add_argument('-d', '--deviceCategory', type=str,
                        help='Input device category code to find all locations with given ' +
                             'device type. Can be used in conjunction with the -p option')
    parser.add_argument('-D', '--deviceCode', type=str,
                        help='Input device code to find all data product codes with specified device. Used ' +
                             'in conjunction with the -p option')
    parser.add_argument('-p', '--findProduct', action='store_true',
                        help='Find all data product codes on given deviceCode, deviceCategory, or locationCode. ' +
                             'Must be used in conjunction with one or more of the following options: -c, -d, or -D')
    parser.add_argument('-t', '--date', action='store_true',
                        help='Find all deployment dates based on given deviceCode. Must be used in conjunction' +
                        ' with the -D option.')

    args = parser.parse_args()
    main(args)
