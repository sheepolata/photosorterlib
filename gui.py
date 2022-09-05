import sys
import tkinter as tk
from tkinter import ttk, filedialog

import photosorterlib

import threading


class PhotoSorterGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # self.geometry("600x150")
        self.title("Photo Sorter")
        self.resizable(0, 0)
        self.eval('tk::PlaceWindow . center')
        self.sorter_thread = None

        # self.grid_columnconfigure(0, minsize=75, weight=1)
        self.grid_columnconfigure(1, minsize=420)
        # self.grid_columnconfigure(3, minsize=75, weight=1)

        self.create_widgets()

        self.after(100, self.update_loading_bar)

    def create_widgets(self):
        # username
        input_folder = ttk.Label(self, text="Input folder:")
        input_folder.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        self.input_entry_var = tk.StringVar()
        self.input_entry_var_short = tk.StringVar()
        self.input_entry = ttk.Entry(self, textvariable=self.input_entry_var_short)
        self.input_entry.grid(column=1, row=0, sticky="we", padx=5, pady=5)

        # login button
        input_browse_button = ttk.Button(self, text="Browse", command=self.browse_input_on_press)
        input_browse_button.grid(column=2, row=0, sticky=tk.E, padx=5, pady=5)

        # password
        output_folder = ttk.Label(self, text="Output folder:")
        output_folder.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        self.output_entry_var = tk.StringVar()
        self.output_entry_var_short = tk.StringVar()
        self.output_entry = ttk.Entry(self, textvariable=self.output_entry_var_short)
        self.output_entry.grid(column=1, row=1, sticky="we", padx=5, pady=5)

        output_browse_button = ttk.Button(self, text="Browse", command=self.browse_output_on_press)
        output_browse_button.grid(column=2, row=1, sticky=tk.E, padx=5, pady=5)

        self.gps_var = tk.IntVar()
        gps_tick = tk.Checkbutton(self, text='Get GPS', variable=self.gps_var, onvalue=1, offvalue=0)
        gps_tick.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)

        start_button = ttk.Button(self, text="Go!", command=self.go_on_press)
        start_button.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

        self.loading_var = tk.StringVar()
        self.loading_var.set(f"{photosorterlib.PROCESSED_PHOTOS}/{photosorterlib.TOTAL_PHOTOS}")
        loading_bar = ttk.Label(self, textvariable=self.loading_var)
        loading_bar.grid(column=0, columnspan=3, row=4, sticky="we", padx=5, pady=5)

    def browse_input_on_press(self):
        _input = filedialog.askdirectory()
        self.input_entry_var.set(_input)
        # _input_tab = _input.split('/')
        # try:
        #     self.input_entry_var_short.set(f"{_input_tab[0]}/[...]/{_input_tab[-2]}/{_input_tab[-1]}")
        # except IndexError:
        #     self.input_entry_var_short.set(_input)
        self.input_entry_var_short.set(_input)

    def browse_output_on_press(self):
        _output = filedialog.askdirectory()
        self.output_entry_var.set(_output)
        # _output_tab = _output.split('/')
        # try:
        #     self.output_entry_var_short.set(f"{_output_tab[0]}/[...]/{_output_tab[-2]}/{_output_tab[-1]}")
        # except IndexError:
        #     self.output_entry_var_short.set(_output)
        self.output_entry_var_short.set(_output)

    def go_on_press(self):
        self.sorter_thread = threading.Thread(target=photosorterlib.sorter_starter,
                                              args=(photosorterlib.get_photo_files(photosorterlib.get_all_files_from(self.input_entry_var.get())),
                                                   self.output_entry_var.get(),
                                                   (self.gps_var.get() == 1)),
                                              daemon=True)

        self.sorter_thread.start()

    def update_loading_bar(self):
        _print = photosorterlib.GUI_PRINT
        if photosorterlib.GUI_PRINT != "":
            _print_tab = _print.split("---")
            # print(_print_tab)
            _print_tab_file = _print_tab[0].split(" ")[1]
            # print(_print_tab_file)
            _new_print_tab_file = _print_tab_file.replace(self.input_entry_var.get(), ".../")
            # print(_new_print_tab_file)
            _print = _print.replace(_print_tab_file, _new_print_tab_file)
        if 0 < photosorterlib.TOTAL_PHOTOS == photosorterlib.PROCESSED_PHOTOS:
            self.loading_var.set(f"{_print} - Done!")
        else:
            self.loading_var.set(f"{_print}")
        self.after(100, self.update_loading_bar)

    def start(self):
        self.mainloop()


def main():
    photosorterlib.SUPPRESS_WARNINGS = True
    photosorterlib.VERBOSE = False

    gui = PhotoSorterGUI()
    gui.start()


if __name__ == "__main__":
    main()