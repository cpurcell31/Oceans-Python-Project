import oceans2 as o2
import argparse


def main(arguments):
    device_code = arguments.deviceCode
    product_code = arguments.productCode
    extension = arguments.extension
    start_date = arguments.start
    end_date = arguments.end
    filename = arguments.filename
    if product_code and extension and start_date and end_date and device_code:
        filters = {'deviceCode': device_code,
                   'dataProductCode': product_code,
                   'dateFrom': start_date,
                   'dateTo': end_date,
                   'extension': extension,
                   'dpo_qualityControl': 1,
                   'dpo_resample': 'none',
                   'dpo_dataGaps': 0}
        results = o2.download_data_product(filters)
    exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='OncDL.py downloads data' +
                                                 ' from ONC Oceans2.0 portal from specified device and of form ' +
                                                 'provided by the product code. Depending on the type of product ' +
                                                 'there may be several options for output file extension. All ' +
                                                 'launch options are required for successful downloads')

    parser.add_argument('-d', '--deviceCode', type=str,
                        help='The unique device code of desired device to download data from')
    parser.add_argument('-p', '--productCode', type=str,
                        help='The data product code identifies data product type ' +
                             'e.g. TSSD (Time Series Scalar Data)')
    parser.add_argument('-ex', '--extension', type=str,
                        help='The desired file output extension type. Will result in error ' +
                             'if extension type is not available for data product type')
    parser.add_argument('-e', '--end', type=str,
                        help='End date of instrument data specified in ISO-8601 format: ' +
                             'YYYY:MM:DDThh:dd:ss.000Z')
    parser.add_argument('-s', '--start', type=str,
                        help='Start date of instrument data specified in ISO-8601 format: ' +
                             'YYYY:MM:DDThh:dd:ss.000Z')
    parser.add_argument('-f', '--filename', type=str,
                        help='')

    args = parser.parse_args()
    main(args)
