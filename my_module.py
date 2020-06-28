import tkinter as tk
import re
import pandas as pd
from tkinter import filedialog, messagebox

class PhanMemTachTu():
	def __init__(self, root):
		self.root = root

		self.tach_cau_button = tk.Button(self.root, text='Tách câu', command=self.tach_cau)
		self.tach_tu_button = tk.Button(self.root, text='Tách từ', command=self.tach_tu)
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

	def tach_tu(self):
		top_level = tk.Toplevel(self.root)
		tach_tu_window = TachTu(top_level)
		tach_tu_window.pack()

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
		sentences = VNSegmentation.paragraph_to_sentences(self.input.get('1.0', tk.END))
		text = '\n\n'.join(sentences)
		self.output.delete('1.0', tk.END)
		self.output.insert('1.0', text)

	


class TachTu():
	def __init__(self, root):
		self.root = root
		self.input = tk.Text(self.root)		
		self.input.bind('<ButtonRelease-1>', func=self.get_selected_text)
		self.open_file_button = tk.Button(self.root, text='Mở file', command=self.open_file)
		self.save_file_button = tk.Button(self.root, text='Lưu file', command=self.save_file)
		self.auto_segmentation_button = tk.Button(self.root, text='Auto tách từ', command=self.auto_segmentation)
		self.selected_text = tk.Entry(self.root)
		self.add_selected_text_button = tk.Button(self.root, text='Thêm từ đã chọn', command=self.add_selected_text)
		self.output = CustomText(self.root)
		self.output.tag_configure('yellow_background', background='#ffff00')

	def pack(self):
		self.input.pack()
		self.open_file_button.pack()
		self.save_file_button.pack()
		self.auto_segmentation_button.pack()
		self.selected_text.pack()
		self.add_selected_text_button.pack()
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
		words = VNSegmentation.sentence_to_words(self.input.get('1.0', tk.END))
		text = ' '.join(words)
		self.add_or_replace_text(self.output, text)

	def get_selected_text(self, event):
		if self.input.tag_ranges("sel"):
			text = self.input.get("sel.first", "sel.last")
			self.selected_text.delete(0, tk.END)
			self.selected_text.insert(0, text)

	def add_selected_text(self):
		text = self.selected_text.get().strip()
		if text == '':
			messagebox.showerror(parent=self.root, title='Lỗi dữ liệu đầu vào', message='Từ thêm vào không được phép rỗng.')
		else:
			self.add_or_replace_text(self.output, text.replace(' ', '_'))

	def add_or_replace_text(self, widget, text):
		return_val = messagebox.askyesnocancel(parent=self.root, message='-nhấn yes để thêm từ mới vào cuối văn bản\n-nhấn no để thay văn bản cũ bằng từ mới', default='yes')
		if return_val == True:
			widget.insert(tk.END, text + ' ')
		elif return_val == False:
			widget.delete('1.0', tk.END)
			widget.insert(tk.END, text + ' ')

		self.update_output_background()

	def update_output_background(self):
		self.output.tag_remove('yellow_background', '1.0', tk.END)

		text = self.output.get('1.0', tk.END).strip()
		words = text.split()
		for word in words:
			self.output.highlight_pattern(word, 'yellow_background')


class VNSegmentation():

	@staticmethod
	def paragraph_to_sentences(text):
		result = re.compile(r'(?<![A-Z|~\.\.\.])[\.|?|!][\s|$]+').split(text+' ')
		return result

	@staticmethod
	def sentence_to_syllables(text):
		regex = r"\W*[ |\n|$]+\W*"
		result = re.split(regex, text.lower()+' ')
		return result

	@staticmethod
	def sentence_to_words(text, max_word_len=5):
		if not 'VNSegmentation.VN_dict' in locals():
			VNSegmentation.create_dictionary()

		syllables = VNSegmentation.sentence_to_syllables(text.strip())
		result = []
		i = 0
		while i < len(syllables):
			a_correct_word=''
			for j in range(i, len(syllables)):
				if j - i > max_word_len and max_word_len > 0:
					break;

				if ' '.join(syllables[i:j]) in VNSegmentation.VN_dict:
					a_correct_word = ' '.join(syllables[i:j])
					new_i = j
			if a_correct_word == '':
				result.append(syllables[i].replace(' ', '_'))
				i += 1
			else:
				result.append(a_correct_word.replace(' ', '_'))
				i = new_i

		return result

	@staticmethod
	def create_dictionary():
		df = pd.read_csv('VDic_uni.csv', sep=';', header=None)
		VN_words = list(df[0])
		VNSegmentation.VN_dict = VNSegmentation.list_to_dict(VN_words)

	@staticmethod
	def list_to_dict(a_list):
		a_dict = {a_list[i]: i for i in range(0, len(a_list))}
		return a_dict

# https://stackoverflow.com/questions/3781670/how-to-highlight-text-in-a-tkinter-text-widget
class CustomText(tk.Text):
	'''A text widget with a new method, highlight_pattern()

    example:

    text = CustomText()
    text.tag_configure("red", foreground="#ff0000")
    text.highlight_pattern("this should be red", "red")

    The highlight_pattern method is a simplified python
    version of the tcl code at http://wiki.tcl.tk/3246
    '''
	def __init__(self, *args, **kwargs):
		tk.Text.__init__(self, *args, **kwargs)

	def highlight_pattern(self, pattern, tag, start="1.0", end="end", regexp=False):
		'''Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl's regular expression syntax.
        '''

		start = self.index(start)
		end = self.index(end)
		self.mark_set("matchStart", start)
		self.mark_set("matchEnd", start)
		self.mark_set("searchLimit", end)

		count = tk.IntVar()
		while True:
			index = self.search(pattern, "matchEnd","searchLimit", count=count, regexp=regexp)
			if index == "": break
			if count.get() == 0: break # degenerate pattern which matches zero-length strings
			self.mark_set("matchStart", index)
			self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
			self.tag_add(tag, "matchStart", "matchEnd")

