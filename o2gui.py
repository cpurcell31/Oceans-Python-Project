import tkinter as tk
import oceans2 as o2


class OceanGui:

    def __init__(self, *args, **kwargs):
        self.window = tk.Tk()
        self.frame_search = SearchFrame(self.window)
        self.frame_download = DownloadFrame(self.window)
        self.__pack_download_widgets__()
        self.__pack_search_widgets__()
        self.window.mainloop()

    def __pack_download_widgets__(self):
        self.frame_download.label_download.grid(row=0, column=0, padx=5)
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

        self.frame_search.frame.grid(row=0, column=0, padx=5, sticky='w')
        return


class SearchFrame:

    def __init__(self, window):
        self.loc_name = ""
        self.loc_code = ""
        self.dev_cat = ""
        self.dev_code = ""
        self.product_on = tk.IntVar()
        self.date_on = tk.IntVar()

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

    def handle_search(self):
        self.loc_name = self.loc_name_entry.get()
        self.loc_code = self.loc_code_entry.get()
        # check location code is a valid code
        self.dev_cat = self.dev_cat_entry.get()
        self.dev_code = self.dev_code_entry.get()
        filters_loc = {'locationName': self.loc_name,
                       'locationCode': self.loc_code,
                       'deviceCategoryCode': self.dev_cat,
                       'deviceCode': self.dev_code}
        filters_dev = {'locationCode': self.loc_code,
                       'deviceCategoryCode': self.dev_cat,
                       'deviceCode': self.dev_code}
        results_raw = list()
        results_trim = list()
        sections_list = list()

        if self.loc_name:
            result, locations = o2.get_location_codes(filters_loc)
            if result is not None:
                results_raw.append(result)
                results_trim.append(locations)
                sections_list.append("Locations")

        if self.loc_code:
            result, devices = o2.get_device_codes(filters_dev)
            if result is not None:
                results_raw.append(result)
                results_trim.append(devices)
                sections_list.append("Devices")

        if self.dev_cat:
            result, locations = o2.get_location_code_by_category(filters_loc)
            if result is not None:
                results_raw.append(result)
                results_trim.append(locations)
                sections_list.append("Locations with " + self.dev_cat)

        if self.product_on.get() and (self.dev_code or self.dev_cat or self.loc_code):
            result, products = o2.get_data_product_codes(filters_dev)
            if result is not None:
                results_raw.append(result)
                results_trim.append(products)
                sections_list.append("Products")

        if self.date_on.get() and self.dev_code:
            result, deployments = o2.get_date_information(filters_dev)
            results_raw.append(result)
            results_trim.append(deployments)

        self.create_results_window(results_raw, results_trim, sections_list)
        return

    # noinspection PyMethodMayBeStatic
    def create_results_window(self, results_raw, results_trim, sections_list):
        window_results = tk.Toplevel()
        window_results.title("Search Results")

        results_text_box = tk.Text(master=window_results)
        button_export = tk.Button(master=window_results, text="Export Results")

        counter = 0
        if len(results_trim) == 0:
            results_text_box.insert(tk.END, "No Results Found with Given Filters")
        else:
            for result in results_trim:
                results_text_box.insert(tk.END, sections_list[counter] + "\n")
                for key in result.keys():
                    results_text_box.insert(tk.END, key + "\n")
                    results_text_box.insert(tk.END, result[key] + "\n\n")
                counter += 1

        results_text_box.pack()
        button_export.pack()

        return


class DownloadFrame:

    def __init__(self, window):
        self.frame = tk.Frame()
        self.label_download = tk.Label(master=self.frame, text='ONC Download')


def main():

    gui = OceanGui()
    return


if __name__ == "__main__":
    main()