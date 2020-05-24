import os
from os import path
import oceans2 as o2
import argparse
from matplotlib import pyplot as plt
from matplotlib import dates as md
import pandas as pd


def main(arguments):
    device_code = arguments.deviceCode
    start_date = arguments.startDate
    end_date = arguments.endDate
    export = arguments.export
    filename = arguments.filename
    dir_path = arguments.path
    if device_code:
        filters = {'deviceCode': device_code,
                   'dateFrom': start_date,
                   'dateTo': end_date}
        graph_data = o2.get_device_data(filters)
        counter = 0
        cwd = os.getcwd()
        xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S.%f')
        for times in graph_data.sampleTimes:
            fig, ax = plt.subplots(figsize=(20, 10))
            plt.title(graph_data.locationName + " " + graph_data.sensorNames[counter] + " Over Time")
            plt.ylabel(graph_data.sensorNames[counter])
            plt.xlabel("Date")
            ax.xaxis.set_major_formatter(xfmt)
            image, = ax.plot(times, graph_data.readingValues[counter])
            graph_path = (graph_data.locationName +
                          "_graph{0}.png".format(counter))
            fig.savefig(path.join(cwd, graph_path))
            if export:
                o2.export_data(graph_data.locationName,
                               graph_data.sensorNames[counter],
                               graph_data.rawSampleTimes[counter],
                               graph_data.readingValues[counter])
            counter += 1
            plt.close(fig)

    elif filename:
        header_rows = list(range(0, 50))
        header_rows.append(51)
        df = pd.read_csv(filename, skiprows=header_rows, usecols=[0, 1, 3])

        column_names = list(df.columns.values.tolist())
        df[column_names[0]] = pd.to_datetime(df[column_names[0]])
        df[column_names[1]] = pd.to_numeric(df[column_names[1]], errors='coerce')
        df[column_names[1]] = df[column_names[1]].fillna(0)
        datenums = md.date2num(df[column_names[0]].to_list())

        xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S.%f')
        fig, ax = plt.subplots(figsize=(20, 10))
        plt.xlabel("Date")
        ax.xaxis.set_major_formatter(xfmt)
        image, = ax.plot(datenums, df[column_names[1]])
        plt.show()

    elif dir_path:
        print("")

    exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='OncPlot.py graphs ONC data' +
                                                 ' from the device supplied by the device code given. Raw data can ' +
                                                 'also be exported into a .txt file with the -x launch option.')

    parser.add_argument('-d', '--deviceCode', type=str,
                        help='The unique device code of the desired device to collect data ' +
                             'from')
    parser.add_argument('-s', '--startDate', type=str,
                        help='Start date of instrument data specified in ISO-8601 format: ' +
                             'YYYY:MM:DDThh:dd:ss.000Z')
    parser.add_argument('-e', '--endDate', type=str,
                        help='End date of instrument data specified in ISO-8601 format: ' +
                             'YYYY:MM:DDThh:dd:ss.000Z')
    parser.add_argument('-x', '--export', action='store_true',
                        help='Toggle option to export raw device data to a .txt file')
    parser.add_argument('-f', '--filename', type=str,
                        help='')
    parser.add_argument('-p', '--path', type=str,
                        help='')

    args = parser.parse_args()
    main(args)
