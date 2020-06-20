import tkinter as tk
from Utils import database_util as dbu, oceans2 as o2
from Utils import gui_utils as gutil
from Utils.gui_utils import PATH
from tkinter import filedialog


class DownloadFrame:

    def __init__(self, window):

        self.frame = tk.Frame()
        self.label_download = tk.Label(master=self.frame, text='ONC Download')

        extensions = dbu.get_extensions(PATH)
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
        self.start_date_entry.bind(sequence='<FocusIn>', func=lambda f: gutil.on_focus_date(self.start_date_entry))
        self.start_date_entry.bind(sequence='<FocusOut>', func=lambda f: gutil.on_unfocus_date(self.start_date_entry))
        self.start_date_entry.config(fg="grey")

        self.end_date_entry = tk.Entry(master=self.frame)
        self.end_date_entry.insert(0, date_string)
        self.end_date_entry.bind(sequence='<FocusIn>', func=lambda f: gutil.on_focus_date(self.end_date_entry))
        self.end_date_entry.bind(sequence='<FocusOut>', func=lambda f: gutil.on_unfocus_date(self.end_date_entry))
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

        if not (dbu.search_devices(dev_code, PATH) and dbu.search_products(prd_code, PATH)):
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


