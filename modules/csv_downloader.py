import os
import sys
import time
import urllib.request
import pandas as pd

from modules.utils import bcolors as bc

OID_URL_v4 = 'https://storage.googleapis.com/openimages/2018_04/'
OID_URL_v5 = 'https://storage.googleapis.com/openimages/v5/'
OID_URL_v6 = 'https://storage.googleapis.com/openimages/v6/'

def TTV(csv_dir, name_file, args_y):
    '''
    Manage error_csv and read the correct .csv file.

    :param csv_dir: folder of the .csv files
    :param name_file: name of the correct .csv file
    :return: None
    '''
    CSV = os.path.join(csv_dir, name_file)
    error_csv(name_file, csv_dir, args_y)
    df_val = pd.read_csv(CSV)
    return df_val

def error_csv(file, csv_dir, args_y):
    '''
    Check the presence of the required .csv files.

    :param file: .csv file missing
    :param csv_dir: folder of the .csv files
    :return: None
    '''
    if not os.path.isfile(os.path.join(csv_dir, file)):
        print(bc.FAIL + "Missing the {} file.".format(os.path.basename(file)) + bc.ENDC)
        if args_y:
            ans = 'y'
            print(bc.OKBLUE + "Automatic download." + bc.ENDC)
        else:
            ans = input(bc.OKBLUE + "Do you want to download the missing file? [Y/n] " + bc.ENDC)

        if ans.lower() == 'y':
            prefix = str(os.path.basename(file)).split('-')[0]
            if prefix == 'oidv6': # for train
                FILE_URL = str(OID_URL_v6 + file)
            elif prefix == 'validation' or prefix == 'test': # for validation and test
                FILE_URL = str(OID_URL_v5 + file)
            elif prefix == 'class': # for metadata/class names
                FILE_URL = str(OID_URL_v5 + file)

            FILE_PATH = os.path.join(csv_dir, file)
            save(FILE_URL, FILE_PATH)
            print('\n' + bc.OKBLUE + "File {} downloaded into {}.".format(file, FILE_PATH) + bc.ENDC)

        else:
            exit(1)

def save(url, filename):
    '''
    Download the .csv file.

    :param url: Google url for download .csv files
    :param filename: .csv file name
    :return: None
    '''
    urllib.request.urlretrieve(url, filename, reporthook)

def reporthook(count, block_size, total_size):
    '''
    Print the progression bar for the .csv file download.

    :param count:
    :param block_size:
    :param total_size:
    :return:
    '''
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / ((1024 * duration) + 1e-5))
    percent = int(count * block_size * 100 / (total_size + 1e-5))
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                     (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()
