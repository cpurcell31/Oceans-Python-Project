import tkinter as tk
from Utils import database_util as dbu, oceans2 as o2
from tkinter import filedialog

import time

path = o2.cwd + "/OncUtil.db"


class OceanGui:

    def __init__(self, *args, **kwargs):
        self.window = tk.Tk()
        self.frame_search = SearchFrame(self.window)
        self.frame_download = DownloadFrame(self.window)
        self.__pack_download_widgets__()
        self.__pack_search_widgets__()
        self.window.mainloop()

    def __pack_download_widgets__(self):
        self.frame_download.label_download.grid(row=0, column=0, sticky='w')

        self.frame_download.dev_code_lbl.grid(row=1, column=0, padx=5, sticky='w')
        self.frame_download.dev_code_entry.grid(row=1, column=1, padx=62, sticky='w')

        self.frame_download.prd_code_lbl.grid(row=2, column=0, padx=5, sticky='w')
        self.frame_download.prd_code_entry.grid(row=2, column=1, padx=62, sticky='w')

        self.frame_download.extension_lbl.grid(row=3, column=0, padx=5, sticky='w')
        self.frame_download.extension_entry.grid(row=3, column=1, padx=62, sticky='w')

        self.frame_download.start_date_lbl.grid(row=4, column=0, padx=5, sticky='w')
        self.frame_download.start_date_entry.grid(row=4, column=1, padx=62, sticky='w')

        self.frame_download.end_date_lbl.grid(row=5, column=0, padx=5, sticky='w')
        self.frame_download.end_date_entry.grid(row=5, column=1, padx=62, sticky='w')

        self.frame_download.download_button.grid(row=6, column=1)

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

        self.frame_search.search_button.grid(row=5, column=1)
        self.frame_search.search_help.grid(row=0, column=3)

        self.frame_search.frame.grid(row=0, column=0, padx=5, sticky='w')
        return


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

        search_help_lbl = tk.Label(master=window_help, text="ONC Search Instructions")
        download_help_lbl = tk.Label(master=window_help, text="ONC Download Instructions")

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

        search_help_lbl.pack()
        search_help_text.pack()
        search_help_text1.pack()
        search_help_text2.pack()
        search_help_text3.pack()
        download_help_lbl.pack()


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
        self.start_date_entry = tk.Entry(master=self.frame)
        self.end_date_entry = tk.Entry(master=self.frame)
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
        if not (dev_code and prd_code and start_date and end_date and extension):
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


def main():
    gui = OceanGui()
    return


if __name__ == "__main__":
    main()
