import tkinter as tk
from Utils import database_util as dbu, oceans2 as o2
from tkinter import filedialog
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as md
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

import time

path = o2.cwd + "/OncUtil.db"


class OceanGui:

    def __init__(self, *args, **kwargs):
        self.window = tk.Tk()
        self.frame_search = SearchFrame(self.window)
        self.frame_download = DownloadFrame(self.window)
        self.frame_plot = PlotFrame(self.window)
        self.__pack_download_widgets__()
        self.__pack_search_widgets__()
        self.__pack_plot_widgets__()
        self.window.mainloop()

    def __pack_download_widgets__(self):
        self.frame_download.label_download.grid(row=0, column=0, sticky='w')

        self.frame_download.dev_code_lbl.grid(row=1, column=0, padx=5, sticky='w')
        self.frame_download.dev_code_entry.grid(row=1, column=1, padx=62, sticky='w')

        self.frame_download.prd_code_lbl.grid(row=2, column=0, padx=5, sticky='w')
        self.frame_download.prd_code_entry.grid(row=2, column=1, padx=62, sticky='w')

        self.frame_download.extension_lbl.grid(row=3, column=0, padx=5, sticky='w')
        self.frame_download.extension_entry.grid(row=3, column=1, padx=62)

        self.frame_download.start_date_lbl.grid(row=4, column=0, padx=5, sticky='w')
        self.frame_download.start_date_entry.grid(row=4, column=1, padx=62, sticky='w')

        self.frame_download.end_date_lbl.grid(row=5, column=0, padx=5, sticky='w')
        self.frame_download.end_date_entry.grid(row=5, column=1, padx=62, sticky='w')

        self.frame_download.download_button.grid(row=6, column=1, sticky='w', padx=62, pady=5)

        self.frame_download.frame.grid(row=1, column=0, padx=5, sticky='w')
        return

    def __pack_search_widgets__(self):
        self.frame_search.label_search.grid(row=0, column=0, sticky='w')

        self.frame_search.loc_name_lbl.grid(row=1, column=0, padx=5, sticky='w')
        self.frame_search.loc_name_entry.grid(row=1, column=1, padx=5, sticky='w')

        self.frame_search.loc_code_lbl.grid(row=2, column=0, padx=5, sticky='w')
        self.frame_search.loc_code_entry.grid(row=2, column=1, padx=5, sticky='w')

        self.frame_search.dev_cat_lbl.grid(row=3, column=0, padx=5, sticky='w')
        self.frame_search.dev_cat_entry.grid(row=3, column=1, padx=5, sticky='w')

        self.frame_search.dev_code_lbl.grid(row=4, column=0, padx=5, sticky='w')
        self.frame_search.dev_code_entry.grid(row=4, column=1, padx=5, sticky='w')

        self.frame_search.find_product_check.grid(row=1, column=3, padx=10, sticky='w')
        self.frame_search.date_check.grid(row=2, column=3, padx=10, sticky='w')

        self.frame_search.search_button.grid(row=5, column=1, pady=5)
        self.frame_search.search_help.grid(row=0, column=3)

        self.frame_search.frame.grid(row=0, column=0, padx=5, sticky='w')
        return

    def __pack_plot_widgets__(self):
        self.frame_plot.data_plot_lbl.grid(row=0, column=0, padx=5, sticky='w')

        self.frame_plot.file_entry_lbl.grid(row=1, column=0, padx=5, sticky='w')
        self.frame_plot.file_select_text.grid(row=1, column=1, padx=44, sticky='w')
        self.frame_plot.file_select_button.grid(row=1, column=1, padx=215, sticky='w')

        self.frame_plot.data_plot_button.grid(row=2, column=1, padx=80, pady=5, sticky='w')

        self.frame_plot.frame.grid(row=2, column=0, padx=5, sticky='w')


class SearchFrame:

    def __init__(self, window):
        self.product_on = tk.IntVar()
        self.date_on = tk.IntVar()
        help_icon = tk.PhotoImage(file=o2.cwd + "/help_icon.gif")

        self.frame = tk.Frame()

        self.loc_name_entry = tk.Entry(master=self.frame)
        self.loc_code_entry = tk.Entry(master=self.frame)
        self.dev_cat_entry = tk.Entry(master=self.frame)
        self.dev_code_entry = tk.Entry(master=self.frame)

        self.label_search = tk.Label(master=self.frame, text="ONC Search")
        self.loc_name_lbl = tk.Label(master=self.frame, text="Location Name")
        self.loc_code_lbl = tk.Label(master=self.frame, text="Location Code")
        self.dev_cat_lbl = tk.Label(master=self.frame, text="Device Category Code")
        self.dev_code_lbl = tk.Label(master=self.frame, text="Device Code")

        self.find_product_check = tk.Checkbutton(master=self.frame, text="Find Data Products", variable=self.product_on)
        self.date_check = tk.Checkbutton(master=self.frame, text="Find Deployment Dates", variable=self.date_on)
        self.search_button = tk.Button(master=self.frame, text="Search", command=self.handle_search)
        self.search_help = tk.Button(master=self.frame, image=help_icon, command=self.open_help)
        self.search_help.image = help_icon

    def handle_search(self):
        path = o2.cwd + "/OncUtil.db"
        loc_name = self.loc_name_entry.get()
        loc_code = self.loc_code_entry.get()
        inval_flag = False
        # check location code is a valid code
        if not dbu.search_locations(loc_code, path) and len(loc_code) != 0:
            loc_code = ""
            inval_flag = True
        dev_cat = self.dev_cat_entry.get()
        dev_code = self.dev_code_entry.get()
        filters_loc = {'locationName': loc_name,
                       'locationCode': loc_code,
                       'deviceCategoryCode': dev_cat,
                       'deviceCode': dev_code}
        filters_dev = {'locationCode': loc_code,
                       'deviceCategoryCode': dev_cat,
                       'deviceCode': dev_code}
        results_raw = list()
        results_trim = list()
        sections_list = list()

        if loc_name:
            result, locations = o2.get_location_codes(filters_loc)
            if result is not None:
                results_raw.append(result)
                results_trim.append(locations)
                sections_list.append("Locations")

        if loc_code:
            result, devices = o2.get_device_codes(filters_dev)
            if result is not None:
                results_raw.append(result)
                results_trim.append(devices)
                sections_list.append("Devices")

        if dev_cat:
            result, locations = o2.get_location_code_by_category(filters_loc)
            if result is not None:
                results_raw.append(result)
                results_trim.append(locations)
                sections_list.append("Locations with " + dev_cat)

        if self.product_on.get() and (dev_code or dev_cat or loc_code):
            result, products = o2.get_data_product_codes(filters_dev)
            if result is not None:
                results_raw.append(result)
                results_trim.append(products)
                sections_list.append("Data Products")

        if self.date_on.get() and dev_code:
            result, deployments = o2.get_date_information(filters_dev)
            results_raw.append(result)
            results_trim.append(deployments)
            sections_list.append("Deployment Dates")

        self.create_results_window(results_trim, sections_list, inval_flag)
        return

    def create_results_window(self, results_trim, sections_list, inval_flag):
        window_results = tk.Toplevel()
        window_results.title("Search Results")

        results_text_box = tk.Text(master=window_results)

        counter = 0
        if inval_flag:
            results_text_box.insert(tk.END, "Invalid Location Code Supplied\n\n")
        if len(results_trim) == 0:
            results_text_box.insert(tk.END, "No Results Found With Given Filters")
        else:
            for result in results_trim:
                results_text_box.insert(tk.END, sections_list[counter] + "\n\n")
                for key in result.keys():
                    results_text_box.insert(tk.END, key + " - ")
                    results_text_box.insert(tk.END, result[key] + "\n\n")
                counter += 1

        results_text_box.pack()
        button_export = tk.Button(
            master=window_results, text="Export Results", command=lambda: export_results(results_text_box))
        button_export.pack()
        return

    def open_help(self):
        window_help = tk.Toplevel()
        window_help.title("ONC Data Util Help")

        search_help_lbl = tk.Label(master=window_help, text="ONC Search Instructions\n")
        download_help_lbl = tk.Label(master=window_help, text="ONC Download Instructions\n")

        search_help_text = tk.Label(master=window_help, text=(
            "The ONC Search Module processes searches for ONC instrument locations, devices, data products, "
            "and deployment dates.\n\n"))
        search_help_text1 = tk.Label(master=window_help, text=("Search Instructions:\n\n1. Input as much data as you "
                                                               "know, if you are a new user try searching for "
                                                               "locations by inputting 'Underwater' in the location "
                                                               "entry box.\n"))
        search_help_text2 = tk.Label(master=window_help, text=("2. Check any boxes that you want to apply. If you "
                                                               "want to search for deployment dates make sure to "
                                                               "input a device code as well.\nIf you want to search "
                                                               "for data products make sure to input a device code or "
                                                               "location code or device category\n"))
        search_help_text3 = tk.Label(master=window_help, text=("3. Hit the Search button and wait for results."
                                                               "A window containing any potential results will popup "
                                                               "and give the option to export the results\n\n"))
        download_help_text = tk.Label(master=window_help, text=("The ONC Download Module processes downloads of ONC "
                                                                "instrument data.\n"))
        download_help_text1 = tk.Label(master=window_help, text=("Download Instructions:\n\n1. Input data for all "
                                                                 "entry fields. If you need to find any options use "
                                                                 "the ONC Search Module.\n"))
        download_help_text2 = tk.Label(master=window_help, text=("2. Click the Download button and wait for results. "
                                                                 "Be patient as depending on data set sizes it may "
                                                                 "take awhile to process requests\n"))

        search_help_lbl.pack()
        search_help_text.pack()
        search_help_text1.pack()
        search_help_text2.pack()
        search_help_text3.pack()
        download_help_lbl.pack()
        download_help_text.pack()
        download_help_text1.pack()
        download_help_text2.pack()


class DownloadFrame:

    def __init__(self, window):

        self.frame = tk.Frame()
        self.label_download = tk.Label(master=self.frame, text='ONC Download')

        extensions = dbu.get_products(path)
        self.drop_options = tk.StringVar()
        self.drop_options.set(extensions[0])

        self.dev_code_lbl = tk.Label(master=self.frame, text="Device Code")
        self.prd_code_lbl = tk.Label(master=self.frame, text="Product Code")
        self.start_date_lbl = tk.Label(master=self.frame, text="Start Date")
        self.end_date_lbl = tk.Label(master=self.frame, text="End Date")
        self.extension_lbl = tk.Label(master=self.frame, text="Extension")

        self.dev_code_entry = tk.Entry(master=self.frame)
        self.prd_code_entry = tk.Entry(master=self.frame)

        date_string = "YYYY-MM-DDThh:mm:ss.dddZ"

        self.start_date_entry = tk.Entry(master=self.frame)
        self.start_date_entry.insert(0, date_string)
        self.start_date_entry.bind(sequence='<FocusIn>', func=lambda f: on_focus_date(self.start_date_entry))
        self.start_date_entry.bind(sequence='<FocusOut>', func=lambda f: on_unfocus_date(self.start_date_entry))
        self.start_date_entry.config(fg="grey")

        self.end_date_entry = tk.Entry(master=self.frame)
        self.end_date_entry.insert(0, date_string)
        self.end_date_entry.bind(sequence='<FocusIn>', func=lambda f: on_focus_date(self.end_date_entry))
        self.end_date_entry.bind(sequence='<FocusOut>', func=lambda f: on_unfocus_date(self.end_date_entry))
        self.end_date_entry.config(fg="grey")

        self.extension_entry = tk.OptionMenu(self.frame, self.drop_options, *extensions)

        self.download_button = tk.Button(master=self.frame, text="Search and Download", command=self.handle_download)

    def handle_download(self):
        dev_code = self.dev_code_entry.get()
        prd_code = self.prd_code_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        extension = self.drop_options.get()
        inval_flag = False
        noval_flag = False

        date_string = "YYYY-MM-DDThh:mm:ss.dddZ"

        filters = {'deviceCode': dev_code,
                   'dataProductCode': prd_code,
                   'dateFrom': start_date,
                   'dateTo': end_date,
                   'extension': extension,
                   'dpo_qualityControl': 1,
                   'dpo_resample': 'none',
                   'dpo_dataGaps': 0}

        if not (dbu.search_devices(dev_code, path) and dbu.search_products(prd_code, path)):
            inval_flag = True
        if not (dev_code and prd_code and extension):
            noval_flag = True
        if start_date == date_string or end_date == date_string:
            noval_flag = True

        if inval_flag:
            window_loading = self.create_download_screen(inval_flag, noval_flag)
        elif noval_flag:
            window_loading = self.create_download_screen(inval_flag, noval_flag)
        else:
            window_loading = self.create_download_screen(inval_flag, noval_flag)
            window_loading.update_idletasks()
            results = o2.download_data_product(filters)
            print(results)
            window_loading.destroy()
        return

    def create_download_screen(self, inval_flag, noval_flag):
        window_loading = tk.Toplevel()
        window_loading.wm_minsize(width=100, height=50)
        if inval_flag:
            loading_lbl = tk.Label(master=window_loading, text="Invalid Device Code or Product Code")
        elif noval_flag:
            loading_lbl = tk.Label(master=window_loading, text="Error Missing Values: Please Fill All Input Sections")
        else:
            window_loading.wm_attributes('-type', 'splash')
            loading_lbl = tk.Label(master=window_loading, text="Downloading Results Please Wait...")
        loading_lbl.pack(pady=25)
        return window_loading


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


def export_results(results_text_box):
    f = filedialog.asksaveasfilename(defaultextension=".txt", title="Save File", initialdir=o2.cwd)
    try:
        if f:
            output = open(f, "w")
            output.write(results_text_box.get("1.0", tk.END))
            output.close()
    except FileExistsError:
        print("Unable to Create File")
    return


def on_unfocus_date(date_entry):
    date_string = "YYYY-MM-DDThh:mm:ss.dddZ"
    if date_entry.get() == "":
        date_entry.insert(0, date_string)
        date_entry.config(fg="grey")
    return


def on_focus_date(date_entry):
    date_string = "YYYY-MM-DDThh:mm:ss.dddZ"
    if date_entry.get() == date_string:
        date_entry.delete(0, tk.END)
        date_entry.insert(0, "")
        date_entry.config(fg="black")
    return


def main():
    gui = OceanGui()
    return


if __name__ == "__main__":
    main()
