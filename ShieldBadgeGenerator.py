import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk
from tkinter import messagebox
import requests
import webbrowser

# Color Chooser
def choose_backcolor():
    buttonBackColor.config(fg=colorchooser.askcolor(title ="Choose color") [1])
def choose_logocolor():
    buttonLogoColor.config(fg=colorchooser.askcolor(title ="Choose color")[1])

# AutocompleteEntry
def fetch_icon_names():
    url = "https://raw.githubusercontent.com/simple-icons/simple-icons/develop/data/simple-icons.json"
    response = requests.get(url)
    if response.status_code == 200:
        return [item['title'] for item in response.json()]
    else:
        return ""

ICON_LIST = fetch_icon_names()

class AutocompleteEntry(tk.Entry):
    def __init__(self, master, icon_list, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.icon_list = sorted(icon_list)
        self.listbox = None
        self.bind("<KeyRelease>", self.check_input)
        self.bind("<Down>", self.move_down)

    def check_input(self, event):
        if event.keysym in ("Up", "Down", "Return"):
            return
        value = self.get()
        if value == '':
            self.close_listbox()
            return

        matches = [icon for icon in self.icon_list if value.lower() in icon.lower()]
        self.show_matches(matches)

    def show_matches(self, matches):
        if self.listbox:
            self.listbox.destroy()

        if not matches:
            return

        self.listbox = tk.Listbox(height=min(6, len(matches)))
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.listbox.bind("<Return>", self.on_return)
        self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())

        for match in matches:
            self.listbox.insert(tk.END, match)

    def on_select(self, event):
        if not self.listbox:
            return
        index = self.listbox.curselection()
        if index:
            selected = self.listbox.get(index)
            self.delete(0, tk.END)
            self.insert(0, selected)
            self.close_listbox()

    def on_return(self, event):
        self.on_select(event)

    def move_down(self, event):
        if self.listbox:
            self.listbox.focus()
            self.listbox.select_set(0)
            self.listbox.activate(0)
            self.listbox.event_generate("<Down>")

    def close_listbox(self):
        if self.listbox:
            self.listbox.destroy()
            self.listbox = None

# Button
def generate_badge():
    if (entryText.get()!="" and buttonBackColor.cget("fg")!="" and comboBadgeType.get()!="" and entryLogo.get()!="" and buttonLogoColor.cget("fg")!=""):
        badge = "https://img.shields.io/badge/" + entryText.get() + "-%23" + buttonBackColor.cget("fg").replace("#", "") + ".svg?style=" + comboBadgeType.get() + "&logo=" + entryLogo.get() + "&logoColor=" + buttonLogoColor.cget("fg").replace("#", "")
        labelResult.config(text=badge)
    else:
        messagebox.showinfo(title="All fields are required", message="Please fill all fields")
def callback(event):
    webbrowser.open_new(event.widget.cget("text"))

# GUI Setup
root = tk.Tk()
# Window
root.geometry("400x230")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)
root.title("Shield Badge Generator")
root.resizable(False, False)
# Text
tk.Label(root, text="Text:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
entryText = tk.Entry(root)
entryText.grid(row=0, column=1, sticky='we', padx=5, pady=5)
# Background Color
tk.Label(root, text="Background color:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
buttonBackColor = tk.Button(root,text="Choose color",command=choose_backcolor)
buttonBackColor.grid(row=1, column=1, sticky='we', padx=5, pady=5)
# Badge Type
tk.Label(root, text="Badge type:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
options = ["plastic", "flat", "flat-square", "for-the-badge", "social"]
comboBadgeType = ttk.Combobox(root, values=options)
comboBadgeType.grid(row=2, column=1, sticky='we', padx=5, pady=5)
# Logo
tk.Label(root, text="Brand logo:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
entryLogo = AutocompleteEntry(root, ICON_LIST)
entryLogo.grid(row=3, column=1, sticky='we', padx=5, pady=5)
# Logo Color
tk.Label(root, text="Logo color:").grid(row=4, column=0, sticky='e', padx=5, pady=5)
buttonLogoColor = tk.Button(root,text="Choose color",command=choose_logocolor)
buttonLogoColor.grid(row=4, column=1, sticky='we', padx=5, pady=5)
# Generate
tk.Button(root,text="Generate badge",command=generate_badge).grid(row=5, column=0, columnspan=2, sticky='we', padx=5, pady=5)
labelResult = tk.Label(root, fg="blue", cursor="hand2", anchor='w', justify='left')
labelResult.grid(row=6, column=0, columnspan=2, sticky='we', padx=5, pady=5)
labelResult.bind("<Button-1>", callback)

root.mainloop()
