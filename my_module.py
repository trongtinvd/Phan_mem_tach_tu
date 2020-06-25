import tkinter as tk
import re
from tkinter import filedialog

class PhanMemTachTu():
	def __init__(self, root):
		self.root = root

		self.tach_cau_button = tk.Button(self.root, text='Tách câu', command=self.tach_cau)
		self.tach_tu_button = tk.Button(self.root, text='Tách từ')
		self.gan_nhan_tu_button = tk.Button(self.root, text='Gán nhãn từ')
		self.gan_thuc_the_button = tk.Button(self.root, text='Gán thực thể')

	def pack(self):
		self.tach_cau_button.pack()
		self.tach_tu_button.pack()
		self.gan_nhan_tu_button.pack()
		self.gan_thuc_the_button.pack()

	def tach_cau(self):
		top_level = tk.Toplevel(self.root)
		tach_cau_window = TachCau(top_level)
		tach_cau_window.pack()

		top_level.grab_set()
		top_level.wait_window()
		top_level.grab_release()


class TachCau():
	def __init__(self, root):
		self.root = root
		self.input = tk.Text(self.root)
		self.open_file_button = tk.Button(self.root, text='Mở file', command=self.open_file)
		self.save_file_button = tk.Button(self.root, text='Lưu file', command=self.save_file)
		self.auto_segmentation_button = tk.Button(self.root, text='Auto tách câu', command=self.auto_segmentation)
		self.output = tk.Text(self.root)


	def pack(self):
		self.input.pack()
		self.open_file_button.pack()
		self.save_file_button.pack()
		self.auto_segmentation_button.pack()
		self.output.pack()

	def open_file(self):
		file_name = filedialog.askopenfilename(parent=self.root, initialdir='./', title='Chọn file text', filetypes=(('file text', '*.txt'),))
		
		if file_name != '':
			with open(file_name, encoding='utf-8', mode='r') as file:
				text = file.read()
			self.input.delete('1.0', tk.END)
			self.input.insert('1.0', text)

	def save_file(self):
		file_name = filedialog.asksaveasfilename(parent=self.root, confirmoverwrite=False, filetypes=(('txt file', '*.txt'),), defaultextension='.txt')

		if file_name != '':
			with open(file_name, mode='w', encoding='utf-8') as file:
				file.write(self.output.get('1.0', tk.END))


	def auto_segmentation(self):
		sentences = self.split_paragraph_to_sentences(self.input.get('1.0', tk.END))
		text = '\n\n'.join(sentences)
		self.output.delete('1.0', tk.END)
		self.output.insert('1.0', text)

	def split_paragraph_to_sentences(self, text):
		result = re.compile(r'(?<![A-Z|~\.\.\.])[\.|?|!][\s|$]+').split(text+' ')
		return result