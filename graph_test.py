import pytest
from matplotlib import dates as md
import dateutil.parser
import oceans2 as o2

graph_data = o2.GraphData("Burrard")


def test_add_reading():
    graph_data.add_reading_values([0.5])
    assert graph_data.readingValues == [[0.5]]


def test_add_reading_type():
    with pytest.raises(TypeError):
        graph_data.add_reading_values(["0.5"])


def test_add_sample():
    rawstr = "2016-09-01T00:00:07.037Z"
    date = dateutil.parser.parse(rawstr)
    datenum = md.date2num(date)
    graph_data.add_sample_times([datenum])
    assert graph_data.sampleTimes == [[datenum]]


def test_add_sample_type():
    with pytest.raises(TypeError):
        graph_data.add_sample_times(["test string"])


def test_add_raw_sample():
    graph_data.add_raw_sample_times(["2016-09-01T00:00:07.037Z"])
    assert graph_data.rawSampleTimes == [["2016-09-01T00:00:07.037Z"]]


def test_add_raw_sample_type():
    with pytest.raises(TypeError):
        graph_data.add_reading_values(["test string"])


def test_add_unit():
    graph_data.add_unit_of_measure("Pressure")
    assert graph_data.unitsOfMeasure[0] == "Pressure"


def test_add_unit_type():
    with pytest.raises(TypeError):
        graph_data.add_unit_of_measure(120)


def test_add_sensor():
    graph_data.add_sensor_name("CTD")
    assert graph_data.sensorNames[0] == "CTD"


def test_add_sensor_type():
    with pytest.raises(TypeError):
        graph_data.add_sensor_name(120)