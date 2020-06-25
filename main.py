import tkinter as tk
from my_module import PhanMemTachTu

root = tk.Tk()

phan_mem_tach_tu = PhanMemTachTu(root)
phan_mem_tach_tu.pack()

root.mainloop()