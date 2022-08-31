import sys

from PIL import Image
from PIL.ExifTags import TAGS
import os
import re
from datetime import datetime
import warnings
import shutil
import time
import numpy as np


SUPPRESS_WARNINGS = True
VERBOSE = False

VALID_FILE_EXTENSIONS = [".PNG", ".png", ".JPG", ".jpg", ".jpeg"]
VALID_FILE_EXTENSIONS_REGEX = []
for exten in VALID_FILE_EXTENSIONS:
    VALID_FILE_EXTENSIONS_REGEX.append('\\' + f"{exten}$")


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
        # decode bytes
        if isinstance(data, bytes):
            try:
                data = data.decode()
            except UnicodeDecodeError as e:
                if not SUPPRESS_WARNINGS:
                    warnings.warn(f"{info_dict['Filename']}'s exif data {tag} cannot be decoded")
                # print(info_dict['Filename'])
                # print(tag)
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


def copy_file_to_new_folder(file_name, output_dir):
    image = Image.open(file_name)
    exifdata = get_meta_data(image)
    image.close()

    photo_date = datetime.strptime(exifdata['DateTime'], "%Y:%m:%d %H:%M:%S")

    year_folder = f"{photo_date.year}"
    month_folder = f"{photo_date.strftime('%B')}"
    output_folder = f"{year_folder}/{month_folder}"

    # if not os.path.exists(f"{output_dir}/{year_folder}"):
    #     os.makedirs(f"{output_dir}/{year_folder}")
    if not os.path.exists(f"{output_dir}/{output_folder}"):
        os.makedirs(f"{output_dir}/{output_folder}")

    shutil.copy2(file_name, f"{output_dir}/{output_folder}")


def sorter(photo_file_list, output_dir):
    for pf in photo_file_list:
        copy_file_to_new_folder(pf, output_dir)


def sorter_verbose(photo_file_list, output_dir):
    nb_file = len(photo_file_list)
    file_processed = 0

    times = []

    print(f"Processing {nb_file} files...")

    for pf in photo_file_list:
        _to_print = f"\rProcessing {pf}"
        t = time.time()
        copy_file_to_new_folder(pf, output_dir)
        duration = time.time() - t

        times.append(duration)

        file_processed += 1
        _to_print += f" --- {round(float(file_processed)/float(nb_file) * 100.0, 2)}%"
        _to_print += f" --- {round(np.mean(times) * (nb_file-file_processed), 2)}s remaining"
        print(f"\r{_to_print}", end="")


def sorter_starter(photo_file_list, output_dir):
    if VERBOSE:
        sorter_verbose(photo_file_list, output_dir)
    else:
        sorter(photo_file_list, output_dir)
