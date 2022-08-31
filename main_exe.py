import photosorterlib


def main():
    input_folder = None
    output_folder = None

    photosorterlib.SUPPRESS_WARNINGS = True
    photosorterlib.VERBOSE = True

    if input_folder is None:
        input_folder = input("Please enter your input folder :")
    if output_folder is None:
        output_folder = input("Please enter your output folder :")

    if photosorterlib.VERBOSE:
        print(f"Copying and ordering photos from {input_folder} to {output_folder}.")

    photosorterlib.sorter_starter(photosorterlib.get_photo_files(photosorterlib.get_all_files_from(input_folder)),
                                  output_folder,
                                  get_gps=False)

    input("Finished! Press enter to quit.")


if __name__ == '__main__':
    main()
