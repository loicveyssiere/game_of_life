import tkinter as tk
#from . import app as app
import app

def main():
    root = tk.Tk()
    root.title("Layout")
    root.geometry('{}x{}'.format(800, 600))
    app.MainFrame(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

if  __name__ == "__main__":
    main()