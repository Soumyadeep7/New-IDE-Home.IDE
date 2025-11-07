from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import sys
import io

compiler = Tk()
compiler.title("Home.IDE")

# ---------- Save, Open, New, Exit ---------- #
file_path = ""

def open_file():
    global file_path
    path = askopenfilename(filetypes=[("Python Files", "*.py")])
    if path:
        with open(path, "r") as file:
            code = file.read()
            editor.delete("1.0", END)
            editor.insert("1.0", code)
        file_path = path

def save():
    global file_path
    if file_path == "":
        save_as()
    else:
        with open(file_path, "w") as file:
            code = editor.get("1.0", END)
            file.write(code)

def save_as():
    global file_path
    path = asksaveasfilename(filetypes=[("Python Files", "*.py")])
    if path:
        with open(path, "w") as file:
            code = editor.get("1.0", END)
            file.write(code)
        file_path = path

def new_file():
    global file_path
    editor.delete("1.0", END)
    file_path = ""

def exit_app():
    compiler.destroy()

# ---------- Run Code & Capture Output ---------- #
def run():
    code = editor.get("1.0", END)
    output_console.delete("1.0", END)

    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()

    try:
        exec(code)
    except Exception as e:
        output_console.insert(END, f"Error: {e}\n")
    else:
        output_console.insert(END, redirected_output.getvalue())

    sys.stdout = old_stdout


# ---------- Menu ---------- #
menu_bar = Menu(compiler)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save)
file_menu.add_command(label="Save As", command=save_as)
file_menu.add_command(label="New File", command=new_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menu_bar.add_cascade(label="File", menu=file_menu)

run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label="Run", command=run)
menu_bar.add_cascade(label="Run", menu=run_bar)
compiler.config(menu=menu_bar)

# ---------- Editor ---------- #
editor = Text(compiler, font=("Consolas", 14))
editor.pack(fill=BOTH, expand=True)

# ---------- Output Console ---------- #
output_console = Text(compiler, height=10, bg="#1e1e1e", fg="white", font=("Consolas", 12))
output_console.pack(fill=BOTH, expand=True)

compiler.mainloop()
