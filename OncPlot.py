import os, sys
from os import path
import oceans2 as o2
import argparse
from oceans2 import onc
from oceans2 import GraphData
from matplotlib import pyplot as plt
from matplotlib import dates as md

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

args = parser.parse_args()

device_code = args.deviceCode
start_date = args.startDate
end_date = args.endDate
export = args.export

if device_code:
    filters = {'deviceCode' : device_code,
            'dateFrom' : start_date,
            'dateTo' : end_date}
    graph_data = o2.getDeviceData(filters)
    counter = 0
    cwd = os.getcwd()
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S.%f')
    for times in graph_data.sampleTimes:
        fig, ax = plt.subplots(figsize=(20,10))
        ax.xaxis.set_major_formatter(xfmt)
        image, = ax.plot(times, graph_data.readingValues[counter])
        graph_path = (graph_data.locationName + 
                "_graph{0}.png".format(counter))
        fig.savefig(path.join(cwd, graph_path))
        if export:
            o2.exportData(graph_data.locationName, 
                    graph_data.sensorNames[counter],
                    graph_data.rawSampleTimes[counter], 
                    graph_data.readingValues[counter])
        counter += 1
        plt.close(fig)


exit()

