from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from PyPDF2 import PdfMerger

first_page = Tk()
first_page.title("PDF merger")
first_page.geometry("1000x600")

items = []  # list to keep Line objects


class Line:  # class to create objects with a Label, Entry, Button, number to help indexing, optional delete button
    def __init__(self, file, entry, choose_button, numb, delete_button=None, ):
        self.file = file
        self.entry = entry
        self.choose_button = choose_button
        self.numb = numb
        self.delete_button = delete_button

    def __str__(self):
        return f"{self.file} {self.entry} {self.choose_button} {self.numb} {self.delete_button}"

    def delete(self):  # delete button's command
        self.file.destroy()
        self.entry.destroy()
        self.choose_button.destroy()
        self.delete_button.destroy()


def next_page_f():  # next button's command, checks if the inputs are enough and correct
    if not items[0].entry.get():
        messagebox.showerror("Error", "Please choose the first file to begin with.")
    elif len(items) == 1:
        messagebox.showerror("Error", "Please add more files to merge.")
    else:
        for item in items:
            if not item.entry.get():
                messagebox.showerror("Error",
                                     "Please remove the lines with no chosen files or choose files in order to proceed.")
                break
        else:
            messagebox.showinfo("Proceed", f"You are ready to proceed with {len(items)} files.")
            second_page = Toplevel()

            def choose_folder():  # browse button's command, create and save merged file as...
                second_page.filename = asksaveasfile(filetypes=(("PDF files", "*.pdf"),), defaultextension="*pdf")
                part1 = str(second_page.filename).replace("<_io.TextIOWrapper name='", "")
                part2 = part1.replace("' mode='w' encoding='cp1252'>", "")
                part3 = part2.replace("\\", "/")
                pdfs = [item.entry.get().replace("\\", "/") for item in items]
                merger = PdfMerger()
                for pdf in pdfs:
                    merger.append(pdf)
                merger.write(part3)
                merger.close()

            def continue_merge():  # continue button's command, destroys the toplevel windows and resets first page
                second_page.destroy()
                for item in items:
                    item.entry.delete(0, END)

            final_file = Label(second_page, text="Save file as:")
            final_file.grid(row=0, column=0)

            final_choose_button = Button(second_page, text="Browse",
                                         command=choose_folder)  # option to create and save merged file
            final_choose_button.grid(row=0, column=1)

            continue_button = Button(second_page, text="Click to continue merging",
                                     command=continue_merge)  # option to continue using the program
            continue_button.grid(row=1, column=0)

            exit_button = Button(second_page, text="Exit program",
                                 command=first_page.quit)  # option to terminate program
            exit_button.grid(row=2, column=0)


def open_first_file():  # dialog to open file
    first_page.filename = filedialog.askopenfilename(initialdir="/", title="Choose",
                                                     filetypes=(("PDF files", "*.pdf"),))
    first_entry.insert(0, first_page.filename)


def add_file():  # gathers the necessary info to crate a Line obj
    def delete_file():
        for item in items:
            if item.numb == int(str(delete_button)[1:]):
                item.delete()
                items.remove(item)

    def open_another_file():  # dialog to open file
        first_page.filename = filedialog.askopenfilename(initialdir="/", title="Choose",
                                                         filetypes=(("PDF files", "*.pdf"),))
        another_entry.insert(0, first_page.filename)

    another_file = Label(first_page, text="Choose another file:")
    another_file.grid(row=len(items) + 1, column=0)

    another_entry = Entry(first_page, width=50)
    another_entry.grid(row=len(items) + 1, column=1)

    another_choose_button = Button(first_page, text="Choose a file", command=open_another_file)
    another_choose_button.grid(row=len(items) + 1, column=2)

    delete_button = Button(first_page, text="X", command=delete_file, name=f"{len(items) + 1}")
    delete_button.grid(row=len(items) + 1, column=3)

    another = Line(another_file, another_entry, another_choose_button, len(items) + 1, delete_button)
    items.append(another)


first_file = Label(first_page, text="Choose a file:")
first_file.grid(row=1, column=0)

first_entry = Entry(first_page, width=50)
first_entry.grid(row=1, column=1)

first_choose_button = Button(first_page, text="Choose a file", command=open_first_file)
first_choose_button.grid(row=1, column=2)

first = Line(first_file, first_entry, first_choose_button, 1)
items.append(first)

add_button = Button(first_page, text="Add a file", command=add_file)  # Button to add a new file
add_button.grid(row=1, column=3)

next_button = Button(first_page, text="Next step", command=next_page_f)  # Button to proceed to the next page
next_button.place(relx=0.9, rely=0.9, anchor=SE)

first_page.mainloop()
