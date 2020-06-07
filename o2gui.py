import tkinter as tk
import oceans2 as o2


def main():

    window = tk.Tk()
    frame_search = setup_search_frame(window)
    frame_download = setup_download_frame(window)
    search_widgets = frame_search.winfo_children()
    download_widgets = frame_download.winfo_children()
    window.mainloop()
    return


def setup_search_frame(window):
    frame_search = tk.Frame()

    label_search = tk.Label(master=frame_search, text="ONC Search")
    label_search.grid(row=0, column=0, sticky='w')

    loc_name_lbl = tk.Label(master=frame_search, text="Location Name")
    loc_code_lbl = tk.Label(master=frame_search, text="Location Code")
    dev_cat_lbl = tk.Label(master=frame_search, text="Device Category Code")
    dev_code_lbl = tk.Label(master=frame_search, text="Device Code")

    loc_name_entry = tk.Entry(master=frame_search)
    loc_code_entry = tk.Entry(master=frame_search)
    dev_cat_entry = tk.Entry(master=frame_search)
    dev_code_entry = tk.Entry(master=frame_search)

    find_product_check = tk.Checkbutton(master=frame_search, text="Find Data Products")
    date_check = tk.Checkbutton(master=frame_search, text="Find Deployment Dates")

    search_button = tk.Button(master=frame_search, text="Search")

    loc_name_lbl.grid(row=1, column=0, padx=5, sticky='w')
    loc_name_entry.grid(row=1, column=1, padx=5, sticky='w')

    loc_code_lbl.grid(row=2, column=0, padx=5, sticky='w')
    loc_code_entry.grid(row=2, column=1, padx=5, sticky='w')

    dev_cat_lbl.grid(row=3, column=0, padx=5, sticky='w')
    dev_cat_entry.grid(row=3, column=1, padx=5, sticky='w')

    dev_code_lbl.grid(row=4, column=0, padx=5, sticky='w')
    dev_code_entry.grid(row=4, column=1, padx=5, sticky='w')

    find_product_check.grid(row=1, column=3, padx=10, sticky='w')
    date_check.grid(row=2, column=3, padx=10, sticky='w')

    search_button.grid(row=5, column=1)

    frame_search.grid(row=0, column=0, padx=5, sticky='w')
    return frame_search


def setup_download_frame(window):
    frame_download = tk.Frame()

    label_download = tk.Label(master=frame_download, text='ONC Download')
    label_download.grid(row=0, column=0, sticky='w')

    frame_download.grid(row=1, column=0, padx=5, sticky='w')
    return frame_download


if __name__ == "__main__":
    main()