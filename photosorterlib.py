from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
import os
import re
from datetime import datetime
import warnings
import shutil
import time
import numpy as np
import tqdm

import exifgpslib


SUPPRESS_WARNINGS = True
VERBOSE = False

VALID_FILE_EXTENSIONS = [".PNG", ".png", ".JPG", ".jpg", ".jpeg"]
VALID_FILE_EXTENSIONS_REGEX = []
for exten in VALID_FILE_EXTENSIONS:
    VALID_FILE_EXTENSIONS_REGEX.append('\\' + f"{exten}$")

TOTAL_PHOTOS = 0
PROCESSED_PHOTOS = 0
GUI_PRINT = ""


def get_meta_data(image):
    info_dict = {
        "Filename": image.filename,
        "Image Size": image.size,
        "Image Height": image.height,
        "Image Width": image.width,
        "Image Format": image.format,
        "Image Mode": image.mode,
        "Image is Animated": getattr(image, "is_animated", False),
        "Frames in Image": getattr(image, "n_frames", 1)
    }

    exif_data = image.getexif()
    for tag_id in exif_data:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exif_data.get(tag_id)

        if isinstance(data, bytes):
            try:
                data = data.decode()
            except UnicodeDecodeError as e:
                if not SUPPRESS_WARNINGS:
                    warnings.warn(f"{info_dict['Filename']}'s exif data {tag} cannot be decoded")
        info_dict[tag] = data

    return info_dict


def get_all_files_from(dirpath):
    lres = []
    for subdir, dirs, files in os.walk(dirpath):
        for file in files:
            lres.append(os.path.join(subdir, file).replace('\\', '/'))
    return lres


def get_photo_files(file_list):
    new_list = []

    for file in file_list:
        passed = False
        for regex in VALID_FILE_EXTENSIONS_REGEX:
            match = re.search(regex, file)
            if match:
                passed = True
                break
        if passed:
            new_list.append(file)

    return new_list


def copy_file_to_new_folder(file_name, output_dir, get_gps=True):
    image = Image.open(file_name)
    exifdata = get_meta_data(image)
    image.close()

    if get_gps:
        gps_data = exifgpslib.get_location_data(file_name)
    else:
        gps_data = None

    try:
        photo_date = datetime.strptime(exifdata['DateTime'], "%Y:%m:%d %H:%M:%S")
        year_folder = f"{photo_date.year}"
        month_folder = f"{photo_date.strftime('%B')}"
        output_folder = f"{year_folder}/{month_folder}"
    except KeyError:
        output_folder = "Others"

    if gps_data is not None:
        if "nodata" in gps_data:
            output_folder += "/Unlocalised"
        else:
            output_folder += f"/{gps_data['City']}"


    # if not os.path.exists(f"{output_dir}/{year_folder}"):
    #     os.makedirs(f"{output_dir}/{year_folder}")
    if not os.path.exists(f"{output_dir}/{output_folder}"):
        os.makedirs(f"{output_dir}/{output_folder}")

    shutil.copy2(file_name, f"{output_dir}/{output_folder}")


def sorter(photo_file_list, output_dir, get_gps=True):
    global PROCESSED_PHOTOS, TOTAL_PHOTOS, GUI_PRINT
    TOTAL_PHOTOS = len(photo_file_list)

    nb_file = len(photo_file_list)
    file_processed = 0
    times = []
    for pf in photo_file_list:
        PROCESSED_PHOTOS += 1
        _to_print = f"Processing {pf}"
        t = time.time()
        copy_file_to_new_folder(pf, output_dir, get_gps=get_gps)
        duration = time.time() - t
        times.append(duration)
        file_processed += 1
        _to_print += f" --- {round(float(file_processed) / float(nb_file) * 100.0, 2)}%"
        _to_print += f" --- {round(np.mean(times) * (nb_file - file_processed), 2)}s remaining"
        GUI_PRINT = _to_print


def sorter_verbose(photo_file_list, output_dir, get_gps=True):
    nb_file = len(photo_file_list)
    file_processed = 0

    times = []

    # print(f"Processing {nb_file} files...")

    for i in tqdm.tqdm(range(len(photo_file_list)), unit="file"):
        pf = photo_file_list[i]
        _to_print = f"\rProcessing {pf}"
        t = time.time()
        copy_file_to_new_folder(pf, output_dir, get_gps=get_gps)
        duration = time.time() - t

        times.append(duration)

        file_processed += 1
        _to_print += f" --- {round(float(file_processed)/float(nb_file) * 100.0, 2)}%"
        _to_print += f" --- {round(np.mean(times) * (nb_file-file_processed), 2)}s remaining"
        # print(f"\r{_to_print}", end="")


def sorter_starter(photo_file_list, output_dir, get_gps=True):
    global TOTAL_PHOTOS, PROCESSED_PHOTOS
    TOTAL_PHOTOS = 0
    PROCESSED_PHOTOS = 0
    if VERBOSE:
        sorter_verbose(photo_file_list, output_dir, get_gps=get_gps)
    else:
        sorter(photo_file_list, output_dir, get_gps=get_gps)
