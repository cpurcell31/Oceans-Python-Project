import tkinter as tk
from Utils import database_util as dbu, oceans2 as o2
from tkinter import filedialog

PATH = o2.cwd + "/Resources/OncUtil.db"


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

