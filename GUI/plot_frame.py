import tkinter as tk
from Utils import database_util as dbu, oceans2 as o2
from Utils import gui_utils as gutil
from tkinter import filedialog

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as md
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)


class PlotFrame:

    def __init__(self, window):
        self.frame = tk.Frame()
        self.filename = ""

        self.data_plot_lbl = tk.Label(master=self.frame, text="ONC Plot")

        self.file_entry_lbl = tk.Label(master=self.frame, text="Data Source File")
        self.file_select_text = tk.Text(master=self.frame, height=1, width=20)
        self.file_select_button = tk.Button(master=self.frame, text="Select File", command=self.open_file_selector)

        self.data_plot_button = tk.Button(master=self.frame, text="Plot Data", command=self.handle_plot)

        self.selected_params_entry = tk.Entry()
        self.df = None

    def handle_plot(self):
        noval_flag = False
        inval_flag = False
        self.df = None
        col_names = list()

        if self.filename == "":
            noval_flag = True

        try:
            self.df = pd.read_csv(self.filename)
        except FileNotFoundError:
            print("Could not open csv file")
            inval_flag = True

        if not inval_flag:
            col_names = list(self.df.columns.values.tolist())
            self.create_selection_window(col_names, noval_flag, inval_flag)
        if inval_flag or noval_flag:
            self.create_plot_window(col_names, noval_flag, inval_flag)

        return

    def create_plot_window(self, col_names, noval_flag, inval_flag):
        plot_window = tk.Toplevel()

        error_text = tk.Text(master=plot_window)
        if noval_flag:
            error_text.insert(tk.END, "Error: No file selected")
            error_text.pack()
            return
        if inval_flag:
            error_text.insert(tk.END, "Error: Could not open CSV file")
            error_text.pack()
            return
        if self.df is None:
            error_text.insert(tk.END, "Error: No data read from CSV")
            error_text.pack()
            return
        if not self.selected_params_entry.get():
            error_text.insert(tk.END, "Error: No parameters selected")
            error_text.pack()
            return

        selections = self.selected_params_entry.get().split(", ")
        sample_times, data_param1, data_param2 = self.create_data_lists(selections)

        return

    def create_selection_window(self, col_names, noval_flag, inval_flag):
        selection_window = tk.Toplevel()
        confirm_button = tk.Button(master=selection_window, text="Confirm",
                                   command=lambda x=col_names, y=noval_flag, z=inval_flag:
                                   self.create_plot_window(x, y, z))

        self.selected_params_entry = tk.Entry(master=selection_window)
        self.selected_params_entry.config(state=tk.DISABLED)
        select_params_lbl = tk.Label(master=selection_window, text="Select One or Two Parameters to Graph")
        select_params_lbl.pack()

        for name in col_names[1:]:
            button = tk.Button(master=selection_window, text=name, command=lambda x=name: self.set_selection(x))
            button.pack()

        self.selected_params_entry.pack()
        confirm_button.pack()
        return

    def set_selection(self, name):
        selection = self.selected_params_entry.get()
        if selection:
            # temporary until better solution to limit to 2 options is made
            self.selected_params_entry.delete(0, tk.END)
        self.selected_params_entry.config(state=tk.NORMAL)
        self.selected_params_entry.insert(tk.END, name)
        return

    def create_data_lists(self, selections):
        sample_times = list()
        data_param1 = list()
        data_param2 = list()

        return sample_times, data_param1, data_param2

    def open_file_selector(self):
        f = filedialog.askopenfilename(defaultextension=".csv", title="Select File", initialdir=o2.cwd)
        self.filename = ""
        try:
            if f:
                self.filename = f
                self.file_select_text.delete("1.0", tk.END)
                self.file_select_text.insert(tk.END, f)
                self.file_select_text.see(tk.END)
        except FileNotFoundError:
            print("Unable to Find File")
        return