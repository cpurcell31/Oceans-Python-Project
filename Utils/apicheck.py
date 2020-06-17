import os


def get_key(key_path):
    if key_path:
        try:
            key_file = open(key_path + "/Resources/OncKey.txt", 'r')
            key = key_file.readline().rstrip()
            return key
        except FileNotFoundError:
            print("ONC API Key file not found at given directory. Please ensure the API Key file exists and is named" +
                  " OncKey.txt")
            return None
    else:
        cwd = os.getcwd()
        try:
            key_file = open(cwd + "/Resources/OncKey.txt", 'r')
            key = key_file.readline().rstrip()
            return key
        except FileNotFoundError:
            print("ONC API Key file not found. Please ensure the API Key file exists and is named OncKey.txt")
            return None
