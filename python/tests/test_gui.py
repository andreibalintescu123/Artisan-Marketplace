import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Test Window")
root.geometry("400x300")

frame = ttk.Frame(root)
frame.pack(fill="both", expand=True)

label = ttk.Label(frame, text="Hello, Tkinter!")
label.pack(pady=20)

root.mainloop()
