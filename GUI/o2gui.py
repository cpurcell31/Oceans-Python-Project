import tkinter as tk
from Utils import database_util as dbu, oceans2 as o2
from Utils.gui_utils import PATH
from tkinter import filedialog

from GUI.plot_frame import PlotFrame
from GUI.download_frame import DownloadFrame
from GUI.search_frame import SearchFrame


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


def main():
    gui = OceanGui()
    return


if __name__ == "__main__":
    main()
