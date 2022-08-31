import photosorterlib
import sys


def main():
    input_folder = None
    output_folder = None

    for i in range(len(sys.argv)):
        if sys.argv[i] == "--help":
            print("Usage : python3 main.py -in INPUT_FOLDER -out OUTPUT_FOLDER [--suppress_warnings|-sw] [--verbose]")
            print("     -in : the input folder. Can have nested folders.")
            print("     -out : the output folder. Can already contain folders.")
            print("     --suppress_warnings|-sw : If enabled, do not display warning messages in console.")
            print("     --verbose : if enabled, will display progression in console.")
            return

        if sys.argv[i] in ["-in"]:
            input_folder = sys.argv[i + 1]
            i += 1
        if sys.argv[i] in ["-out"]:
            output_folder = sys.argv[i + 1]
            i += 1
        if sys.argv[i] in ["--suppress_warnings", "-sw"]:
            photosorterlib.SUPPRESS_WARNINGS = True
        if sys.argv[i] in ["--verbose"]:
            photosorterlib.VERBOSE = True

    if input_folder is None:
        input_folder = input("Please enter your input folder :")
    if output_folder is None:
        output_folder = input("Please enter your output folder :")

    if photosorterlib.VERBOSE:
        print(f"Copying and ordering photos from {input_folder} to {output_folder}.")

    photosorterlib.sorter_starter(photosorterlib.get_photo_files(photosorterlib.get_all_files_from(input_folder)),
                                  output_folder,
                                  get_gps=True)


if __name__ == '__main__':
    main()
