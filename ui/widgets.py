# Small helpers used by all the screens (views), so each view stays short
from tkinter import BOTH, END, LEFT, RIGHT, Y
from tkinter import Button, Entry, Frame, Label, Scrollbar, StringVar, Tk, Toplevel
from tkinter import messagebox, ttk


def new_window(parent, title, size):
    """A window of its own when the screen is started alone, a child window under the menu."""
    win = Toplevel(parent) if parent else Tk()
    win.title(title)
    win.geometry(size)
    return win


def make_layout(win):
    """Form on the left, table on the right. Returns (form_frame, table_frame)."""
    form = Frame(win)
    form.pack(side=LEFT, anchor="n", padx=10, pady=10)
    table_frame = Frame(win)
    table_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
    return form, table_frame


def add_field(form, text, row, readonly=False):
    """Label + entry. Returns the StringVar that holds the text of the entry."""
    Label(form, text=text).grid(row=row, column=0, sticky="w", pady=4)
    var = StringVar()
    state = "readonly" if readonly else "normal"
    Entry(form, textvariable=var, width=24, state=state).grid(row=row, column=1, padx=5, pady=4)
    return var


def add_choice(form, text, row, values):
    """Label + drop-down list. Returns the StringVar (the drop-down is var.combobox)."""
    Label(form, text=text).grid(row=row, column=0, sticky="w", pady=4)
    var = StringVar()
    box = ttk.Combobox(form, textvariable=var, values=values, state="readonly", width=21)
    box.grid(row=row, column=1, padx=5, pady=4)
    var.combobox = box          # kept so a view can change the list later
    return var


def add_buttons(form, row, buttons):
    """buttons = [(text, command), ...] placed in one row under the fields."""
    frame = Frame(form)
    frame.grid(row=row, column=0, columnspan=2, pady=10)
    for text, command in buttons:
        Button(frame, text=text, command=command).pack(side=LEFT, padx=3)


def make_table(parent, headings, widths):
    table = ttk.Treeview(parent, show="headings", columns=list(range(1, len(headings) + 1)),
                         height=16)
    for number, (heading, width) in enumerate(zip(headings, widths), start=1):
        table.heading(number, text=heading)
        table.column(number, width=width)
    table.tag_configure("low", foreground="red")
    scroll = Scrollbar(parent, command=table.yview)
    table.configure(yscrollcommand=scroll.set)
    table.pack(side=LEFT, fill=BOTH, expand=True)
    scroll.pack(side=RIGHT, fill=Y)
    table.rows = []
    return table


def fill_table(table, rows, is_low=None):
    """Replace the content of the table. The rows are remembered in table.rows, so a click
    gives back the original values (Tk would turn a phone like 0401234 into a number)."""
    for item in table.get_children():
        table.delete(item)
    table.rows = []
    for index, row in enumerate(rows):
        table.rows.append(row)
        tags = ("low",) if is_low and is_low(row) else ()
        table.insert("", END, iid=str(index), values=row, tags=tags)


def selected_row(table):
    """The row (tuple) that is selected in the table, or None."""
    chosen = table.selection()
    if not chosen:
        return None
    return table.rows[int(chosen[0])]


def show_result(success, message):
    """Show a message box. Returns success so the caller can write: if show_result(...)."""
    if success:
        messagebox.showinfo("Success", message)
    else:
        messagebox.showerror("Error", message)
    return success


def need_selection(var):
    """True if the field has a value, otherwise tell the user to pick a row first."""
    if var.get().strip():
        return True
    messagebox.showerror("Error", "Please select a row in the table first")
    return False


def start(win, parent):
    """Only a screen started on its own needs its own main loop."""
    if parent is None:
        win.mainloop()
