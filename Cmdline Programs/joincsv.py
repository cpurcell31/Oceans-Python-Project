import pandas as pd
import glob
import argparse


def get_file_lists(device_code1, device_code2, dir_path):
    device1_list = glob.glob(dir_path + device_code1 + "*.csv")
    device2_list = glob.glob(dir_path + device_code2 + "*.csv")
    return device1_list, device2_list


def create_device_frames(device1_files, device2_files):
    header_rows = list(range(0, 50))
    all_headers = list(range(0, 52))
    header_rows.append(51)

    df = pd.read_csv(device1_files[0], skiprows=header_rows, low_memory=False)
    dev1_num_cols = df.shape[1]
    dev1_cols = [0]
    for i in range(1, dev1_num_cols):
        if i % 2 != 0:
            dev1_cols.append(i)

    df = pd.read_csv(device1_files[0], skiprows=header_rows, usecols=dev1_cols)

    frame1_list = list()
    frame1_list.append(df)
    for file in device1_files[1:]:
        df = pd.read_csv(file, skiprows=all_headers, usecols=dev1_cols)
        frame1_list.append(df)

    df = pd.read_csv(device2_files[0], skiprows=header_rows, low_memory=False)
    dev2_num_cols = df.shape[1]
    dev2_cols = [0]
    for i in range(1, dev2_num_cols):
        if i % 2 != 0:
            dev2_cols.append(i)

    df = pd.read_csv(device2_files[0], skiprows=header_rows, usecols=dev2_cols)

    frame2_list = list()
    frame2_list.append(df)
    for files in device2_files[1:]:
        df = pd.read_csv(file, skiprows=all_headers, usecols=dev2_cols)
        frame2_list.append(df)

    device1_frame = pd.concat(frame1_list, axis=0, ignore_index=True)
    device2_frame = pd.concat(frame2_list, axis=0, ignore_index=True)
    return device1_frame, device2_frame


def main(arguments):
    device_code1 = arguments.device1
    device_code2 = arguments.device2
    dir_path = arguments.path

    device1_files, device2_files = get_file_lists(device_code1, device_code2, dir_path)
    device1_frame, device2_frame = create_device_frames(device1_files, device2_files)

    device1_columns = list(device1_frame.columns.values.tolist())
    device2_columns = list(device2_frame.columns.values.tolist())

    if device1_columns[0] != device2_columns[0]:
        exit()

    df_result = pd.merge(device1_frame, device2_frame, on=device1_columns[0], how='outer')
    df_result.to_csv(device_code1 + " and " + device_code2 + ".csv")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Joins two ONC device time series scalar data CSV sets and creates a result CSV ' +
                    'in the current working directory')

    parser.add_argument('device1', type=str, help='The device ID of the first CSV file set')
    parser.add_argument('device2', type=str, help='The device ID of the second CSV file set')
    parser.add_argument('path', type=str, help='The absolute path to the directory containing both CSV file sets')

    args = parser.parse_args()
    main(args)
