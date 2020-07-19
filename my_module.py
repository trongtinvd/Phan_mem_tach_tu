import tkinter as tk
import re
import pandas as pd
from tkinter import filedialog, messagebox, Menu

class PhanMemTachTu():
	def __init__(self, root):
		self.root = root

		self.tach_cau_button = tk.Button(self.root, text='Tách câu', command=self.tach_cau)
		self.tach_tu_button = tk.Button(self.root, text='Tách từ', command=self.tach_tu)
		self.gan_nhan_tu_button = tk.Button(self.root, text='Gán nhãn từ', command=self.gan_nhan_tu)
		self.gan_thuc_the_button = tk.Button(self.root, text='Gán thực thể', command=self.gan_thuc_the)

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

	def gan_nhan_tu(self):
		top_level = tk.Toplevel(self.root)
		dan_nhan_tu_window = GanNhanTu(top_level)
		dan_nhan_tu_window.pack()

		top_level.grab_set()
		top_level.wait_window()
		top_level.grab_release()

	def gan_thuc_the(self):
		top_level = tk.Toplevel(self.root)
		dan_nhan_tu_window = GanThucThe(top_level)
		dan_nhan_tu_window.pack()

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
		sentences = LanguageTool.paragraph_to_sentences(self.input.get('1.0', tk.END))
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
		words = LanguageTool.sentence_to_words(self.input.get('1.0', tk.END))
		text = ' '.join(words)
		self.add_text(self.output, text)

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
			self.add_text(self.output, text.replace(' ', '_'))

	def add_text(self, widget, text):
		return_val = messagebox.askyesnocancel(parent=self.root, message='-nhấn yes để thêm từ mới vào cuối văn bản\n-nhấn no để thay văn bản cũ bằng từ mới', default='yes')
		if return_val == True:
			widget.insert(tk.END, text + ' ')
		elif return_val == False:
			widget.delete('1.0', tk.END)
			widget.insert(tk.END, text + ' ')

		# self.update_output_background()

	def update_output_background(self):
		self.output.tag_remove('yellow_background', '1.0', tk.END)

		text = self.output.get('1.0', tk.END).strip()
		words = text.split()
		for word in words:
			self.output.highlight_pattern(word, 'yellow_background')


class LanguageTool():

	pos = [
		('Aa', 'Quality Adjectives'),
		('An', 'Quantity Adjectives'),
		('Cm', 'Prepositions'),
		('Cp', 'Parallel Conjunctions'),
		('Cs', 'Subordinating Conjunctions'),
		('D', 'Directional co-verb'),
		('E', 'Emotion Words'),
		('FW', 'Foreign Words'),
		('ID', 'Idioms'),
		('M', 'Modifiers'),
		('Nc', 'Countable Nouns'),
		('Nn', 'Common Nouns'),
		('Nq', 'Numerals'),
		('Nr', 'Proper Nouns'),
		('Nt', 'Temporal Nouns'),
		('Nu', 'Concrete Nouns'),
		('ON', 'Onomatopoeia'),
		('Pd', 'Demonstrative Pronouns'),
		('Pp', 'Personal Pronouns'),
		('R', 'Adverbs'),
		('Vc', 'Comparative Verbs'),
		('Vd', 'Directional Verbs'),
		('Ve', 'State Verbs'),
		('Vv', 'Volatile Verbs')
	]

	ne = [
		('NUM', 'Number'),
		('PER', 'Person'),
		('LOC', 'Location'),
		('DTM', 'Date time'),
		('ORG', 'Organization'),
		('MEA', 'Measurement'),
		('TTL', 'Title'),
		('DES', 'Designation'),
		('BRN', 'Brand'),
		('ABB', 'Abbreviation'),
		('TRM', 'Terminology')
	]

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
		if not 'LanguageTool.VN_dict' in locals():
			LanguageTool.create_dictionary()

		syllables = LanguageTool.sentence_to_syllables(text.strip())
		result = []
		i = 0
		while i < len(syllables):
			a_correct_word=''
			for j in range(i, len(syllables)):
				if j - i > max_word_len and max_word_len > 0:
					break;

				if ' '.join(syllables[i:j]) in LanguageTool.VN_dict:
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
		LanguageTool.VN_dict = LanguageTool.list_to_dict(VN_words)
		LanguageTool.POS_list = [str(pos_tags).replace(' ', '') for pos_tags in df[2]]

	@staticmethod
	def list_to_dict(a_list):
		a_dict = {a_list[i]: i for i in range(0, len(a_list))}
		return a_dict

	@staticmethod
	def pos_tagging(word_list):
		if not 'LanguageTool.VN_dict' in locals():
			LanguageTool.create_dictionary()

		result = []
		for word in word_list:
			word = word.replace('_', ' ')
			if word in LanguageTool.VN_dict:
				pos_tags = LanguageTool.POS_list[LanguageTool.VN_dict[word]]
				result.append('{}/{}'. format(word.replace(' ', '_'), pos_tags))
		return result

	@staticmethod
	def ne_tagging(word_list):
		if not 'LanguageTool.VN_dict' in locals():
			LanguageTool.create_dictionary()
		
		result = []		
		word_list_len = len(word_list)
		
		if word_list_len == 0:
			return []
		elif word_list_len == 1:
			entity = ClassifyNameEntity.classify('', word_list[0], '')
			result.append('{}/{}'.format(word_list[0].replace(' ', '_'), entity))
		else:
			for i in range(word_list_len):		
				if i == 0:
					entity = ClassifyNameEntity.classify('', word_list[0], word_list[1])
				elif i == len(word_list) - 1:
					entity = ClassifyNameEntity.classify(word_list[i-1], word_list[i], '')
				else: # 0 < i < len - 1
					entity = ClassifyNameEntity.classify(word_list[i-1], word_list[i], word_list[i+1])			
				result.append('{}/{}'.format(word_list[i].replace(' ', '_'), entity))
			
		return result
		
class ClassifyNameEntity():

	person_prefix = ['ông', 'bà', 'anh', 'chị', 'chú', 'bác', 'cô', 'dì', 'con', 'thằng', 'chủ tịch', 'giám_đốc', 'trưởng_phòng']
	person_lastname = ['nguyễn', 'trần', 'lê', 'phạm', 'huỳnh', 'hoàng', 'phan', 'võ', 'đặng', 'bùi', 'đổ', 'hồ', 'ngô', 'dương', 'lý']
	location_hint = ['phố', 'phường', 'cầu', 'chùa', 'tháp', 'đại_lộ', 'cao_tốc', 'núi', 'rừng', 'sông', 'suối', 'hồ', 'biển', 'vịnh', 'vũng', 'châu', 'đại_dương', 'đại_lục', 'đồng_bằng', 'cao_nguyên', 'thiên_thể']
	direction_prefix = ['phương', 'đông', 'tây', 'nam', 'bắc', 'đông_bắc', 'nam_bắc', 'đông_nam', 'tây_nam']
	organization_hint = ['đạo', 'giáo', 'bộ', 'trường', 'nhà máy', 'xưởng', 'công_ty']
	number_pattern = [
		re.compile(r'(^\d*\.?\d*[1-9]+\d*$)|(^[1-9]+\d*\.\d*$)'),
		re.compile(r'^[-+]?\d+(\.\d+)?$')
	]
	datetime_pattern = [
		re.compile(r'^((([0]?[1-9]|1[0-2])(:|\.)[0-5][0-9]((:|\.)[0-5][0-9])?( )?(AM|am|aM|Am|PM|pm|pM|Pm))|(([0]?[0-9]|1[0-9]|2[0-3])(:|\.)[0-5][0-9]((:|\.)[0-5][0-9])?))$'),
		re.compile(r'^((31(?!\ (Feb(ruary)?|Apr(il)?|June?|(Sep(?=\b|t)t?|Nov)(ember)?)))|((30|29)(?!\ Feb(ruary)?))|(29(?=\ Feb(ruary)?\ (((1[6-9]|[2-9]\d)(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)))))|(0?[1-9])|1\d|2[0-8])\ (Jan(uary)?|Feb(ruary)?|Ma(r(ch)?|y)|Apr(il)?|Ju((ly?)|(ne?))|Aug(ust)?|Oct(ober)?|(Sep(?=\b|t)t?|Nov|Dec)(ember)?)\ ((1[6-9]|[2-9]\d)\d{2})$'),
		# re.compile(r'?n:^(?=\d)((?<month>(0?[13578])|1[02]|(0?[469]|11)(?!.31)|0?2(?(.29)(?=.29.((1[6-9]|[2-9]\d)(0[48]|[2468][048]|[13579][26])|(16|[2468][048]|[3579][26])00))|(?!.3[01])))(?<sep>[-./])(?<day>0?[1-9]|[12]\d|3[01])\k<sep>(?<year>(1[6-9]|[2-9]\d)\d{2})(?(?=\x20\d)\x20|$))?(?<time>((0?[1-9]|1[012])(:[0-5]\d){0,2}(?i:\x20[AP]M))|([01]\d|2[0-3])(:[0-5]\d){1,2})?$'),
		re.compile(r'^\d{1,2}\/\d{1,2}\/\d{4}$')
	]
	measure_pattern = [
		re.compile(r'(\d*\.?\d+)\s?(cm|dm|m|km|ha|g|mg|kg|t|l|ml|px|em|ex|%|in|cn|mm|pt|pc+)')
	]
	
	@staticmethod
	def classify(previous_word, word, next_word):
		property = {
			'capital': False,
			'maybe a person': False,
			'maybe a location': False,
			'maybe a organization': False,
			'maybe a number': False,
			'maybe a datetime': False,
			'maybe a measure': False
		}
		
		if word.replace('_', ' ') == word.replace('_', ' ').title():
			property['capital'] = True
		if previous_word in ClassifyNameEntity.person_prefix:
			property['maybe a person'] = True
		for lastname in ClassifyNameEntity.person_lastname:
			if word.lower().startswith(lastname):
				property['maybe a person'] = True
				break
		for hint in ClassifyNameEntity.location_hint:
			if hint in word.lower():
				property['maybe a location'] = True
				break
		for prefix in ClassifyNameEntity.direction_prefix:
			if word.lower().startswith(prefix):
				property['maybe a location'] = True
				break
		for hint in ClassifyNameEntity.organization_hint:
			if hint in word.lower():
				property['maybe a organization'] = True
				break
		for pattern in ClassifyNameEntity.number_pattern:
			if pattern.match(word.lower()):
				property['maybe a number'] = True
				break
		for pattern in ClassifyNameEntity.datetime_pattern:
			if pattern.match(word.lower()):
				property['maybe a datetime'] = True
				break
		for pattern in ClassifyNameEntity.measure_pattern:
			if pattern.match(word.lower()):
				property['maybe a measure'] = True
				break
		
		
		
		
		# print(word, word.replace('_', ' '), word.replace('_', ' ').title())
		# print('cap',property['capital'])
		# print('per',property['maybe a person'])
		# print('loc',property['maybe a location'])
		# print('org',property['maybe a organization'])
		# print('------------------------------------')
		
		
		
		if property['maybe a number'] == True:
			return 'NUM'
		elif property['maybe a datetime'] == True:
			return 'DTM'
		elif property['maybe a measure'] == True:
			return 'MEA'
			
		if property['capital'] == True:
			if property['maybe a person'] == True:
				return 'PER'
			if property['maybe a location'] == False and property['maybe a organization'] == False:
				return 'TRM'
			
			
		if property['maybe a location'] == True and property['maybe a organization'] == False:
			return 'LOC'
		elif property['maybe a organization'] == True and property['maybe a location'] == False:
			return 'ORG'
			
		return 'O'



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

class GanNhanTu():

	def __init__(self, root):
		self.root = root
		# textbox cho văn bản đã được tách từ
		self.input = CustomText(self.root)
		self.input.bind('<Button-3>', self.open_menu)

		# menu chính
		self.main_menu = Menu(self.root, tearoff=0)
		self.main_menu.add_command(label='Dán nhãn từ', command=self.assign)

		# nút mở/lưu file
		self.open_file_button = tk.Button(self.root, text='Mở file', command=self.open_file)
		self.save_file_button = tk.Button(self.root, text='Lưu file', command=self.save_file)

		# nút tự dán nhãn từ
		self.auto_assign_button = tk.Button(self.root, text='Tự động gán nhãn từ', command=self.auto_assign)

		# kết quả
		self.output = CustomText(self.root)

	def pack(self):
		self.input.pack()
		self.open_file_button.pack()
		self.save_file_button.pack()
		self.auto_assign_button.pack()
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

	def auto_assign(self):
		text = self.input.get('1.0', tk.END)
		words = text.split()
		pos_tagged_words = LanguageTool.pos_tagging(words)
		self.add_text(self.output, ' '.join(pos_tagged_words))

	def add_text(self, widget, text):
		widget.insert(tk.END, text + ' ')

	def open_menu(self, event):
		try:
			self.main_menu.tk_popup(event.x_root, event.y_root)
		finally:
			self.main_menu.grab_release()

	def assign(self):
		if self.input.tag_ranges("sel"):
			text = self.input.get("sel.first", "sel.last").strip()
		else:
			messagebox.showerror(parent=self.root, title='Chưa chọn từ', message='Xin hãy bôi đen từ cần được dán nhãn')
			return None

		if text == '':
			messagebox.showerror(parent=self.root, title='Từ được chọn không hợp lệ', message='Từ được bôi đen không hợp lệ')
			return None

		top_level = tk.Toplevel(self.root)
		assign_window = AssignWindow(top_level, text, LanguageTool.pos)
		assign_window.pack()
		result = assign_window.show()
		self.add_text(self.output, result)

class GanThucThe(GanNhanTu):
	def __init__(self, root):
		GanNhanTu.__init__(self, root)
		self.auto_assign_button['text'] = 'Tự động dán thực thể'
		# self.auto_assign_button['state'] = 'disable'
		self.main_menu.entryconfigure(1, label='Dán nhãn thực thể')

	def auto_assign(self):
		text = self.input.get('1.0', tk.END)
		words = text.split()
		ne_tagged_words = LanguageTool.ne_tagging(words)
		self.add_text(self.output, ' '.join(ne_tagged_words))

	def assign(self):
		if self.input.tag_ranges("sel"):
			text = self.input.get("sel.first", "sel.last").strip()
		else:
			messagebox.showerror(parent=self.root, title='Chưa chọn từ', message='Xin hãy bôi đen từ cần được dán nhãn thực thể')
			return None

		if text == '':
			messagebox.showerror(parent=self.root, title='Từ được chọn không hợp lệ', message='Từ được bôi đen không hợp lệ')
			return None

		top_level = tk.Toplevel(self.root)
		assign_window = AssignWindow(top_level, text, LanguageTool.ne)
		assign_window.pack()
		result = assign_window.show()
		self.add_text(self.output, result)

class AssignWindow():
	def __init__(self, root, text, val_and_desc):
		self.root = root
		self.text = text
		self.val_and_desc = val_and_desc
		self.intVars = []
		self.checkbuttons = []
		for val, description in self.val_and_desc:
			var = tk.IntVar()
			self.intVars.append(var)
			self.checkbuttons.append(tk.Checkbutton(self.root, text=f'{val}-{description}', variable=var, command=self.on_check))
		self.display_text = tk.Label(self.root, text=self.text)
		self.submit_button = tk.Button(self.root, text='Xác nhận', command=self.submit)

	def pack(self):
		for button in self.checkbuttons:
			button.pack()
		self.display_text.pack()
		self.submit_button.pack()

	def show(self):
		self.root.deiconify()
		self.root.wait_window()
		return self.result

	def on_check(self):
		val = []
		for i in range(len(self.intVars)):
			if self.intVars[i].get() == 1:
				val.append(self.val_and_desc[i][0])
		self.display_text['text'] = '{}/{}'.format(self.text, ','.join(val))

	def submit(self):
		self.result = self.display_text['text']
		self.root.destroy()
