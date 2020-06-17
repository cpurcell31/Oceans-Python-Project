import tkinter as tk
from Utils import database_util as dbu, oceans2 as o2
from Utils import gui_utils as gutil
from Utils.gui_utils import PATH
from tkinter import filedialog


class SearchFrame:

    def __init__(self, window):
        self.product_on = tk.IntVar()
        self.date_on = tk.IntVar()
        help_icon = tk.PhotoImage(file=o2.cwd + "/Resources/help_icon.gif")

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
        loc_name = self.loc_name_entry.get()
        loc_code = self.loc_code_entry.get()
        inval_flag = False
        # check location code is a valid code
        if not dbu.search_locations(loc_code, PATH) and len(loc_code) != 0:
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
            master=window_results, text="Export Results", command=lambda: gutil.export_results(results_text_box))
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



