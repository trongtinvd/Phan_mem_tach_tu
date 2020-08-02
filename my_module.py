import tkinter as tk
import re
import pandas as pd
from underthesea import sent_tokenize
from underthesea import word_tokenize
from underthesea import pos_tag
from underthesea import ner
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
		self.text = tk.Text(self.root)
		self.open_file_button = tk.Button(self.root, text='Mở file', command=self.open_file)
		self.save_file_button = tk.Button(self.root, text='Lưu file', command=self.save_file)


	def pack(self):
		self.text.pack()
		self.open_file_button.pack()
		self.save_file_button.pack()

	def open_file(self):
		file_name = filedialog.askopenfilename(parent=self.root, initialdir='./', title='Chọn file text', filetypes=(('file text', '*.txt'),))
		if file_name != '':
			with open(file_name, encoding='utf-8', mode='r') as file:
				text = file.read()
				text = '\n'.join(sent_tokenize(text))
				self.text.delete('1.0', tk.END)
				self.text.insert('1.0', text)

	def save_file(self):
		file_name = filedialog.asksaveasfilename(parent=self.root, confirmoverwrite=False, filetypes=(('txt file', '*.txt'),), defaultextension='.txt')

		if file_name != '':
			with open(file_name, mode='w', encoding='utf-8') as file:
				file.write(self.text.get('1.0', tk.END))
	


class TachTu():
	def __init__(self, root):
		self.root = root
		self.text = tk.Text(self.root)
		self.open_file_button = tk.Button(self.root, text='Mở file', command=self.open_file)
		self.save_file_button = tk.Button(self.root, text='Lưu file', command=self.save_file)

	def pack(self):
		self.text.pack()
		self.open_file_button.pack()
		self.save_file_button.pack()

	def open_file(self):
		file_name = filedialog.askopenfilename(parent=self.root, initialdir='./', title='Chọn file text', filetypes=(('file text', '*.txt'),))
		if file_name != '':
			with open(file_name, encoding='utf-8', mode='r') as file:
				text = file.read()
				text = word_tokenize(text, format='text')
				self.text.delete('1.0', tk.END)
				self.text.insert('1.0', text)

	def save_file(self):
		file_name = filedialog.asksaveasfilename(parent=self.root, confirmoverwrite=False, filetypes=(('txt file', '*.txt'),), defaultextension='.txt')
		if file_name != '':
			with open(file_name, mode='w', encoding='utf-8') as file:
				file.write(self.text.get('1.0', tk.END))



class GanNhanTu():

	def __init__(self, root):
		self.root = root
		self.text = CustomText(self.root)
		#self.text.bind('<Button-3>', self.open_menu)
		#self.main_menu = Menu(self.root, tearoff=0)
		#self.main_menu.add_command(label='Dán nhãn từ', command=self.assign)
		self.open_file_button = tk.Button(self.root, text='Mở file', command=self.open_file)
		self.save_file_button = tk.Button(self.root, text='Lưu file', command=self.save_file)
		
	def pack(self):
		self.text.pack()
		self.open_file_button.pack()
		self.save_file_button.pack()

	def open_file(self):
		file_name = filedialog.askopenfilename(parent=self.root, initialdir='./', title='Chọn file text', filetypes=(('file text', '*.txt'),))
		if file_name != '':
			with open(file_name, encoding='utf-8', mode='r') as file:
				temp = pos_tag(file.read())
				text = ''
				for word in temp:
					text += '/'.join(word) + ' '
				self.text.delete('1.0', tk.END)
				self.text.insert('1.0', text.strip())

	def save_file(self):
		file_name = filedialog.asksaveasfilename(parent=self.root, confirmoverwrite=False, filetypes=(('txt file', '*.txt'),), defaultextension='.txt')
		if file_name != '':
			with open(file_name, mode='w', encoding='utf-8') as file:
				file.write(self.text.get('1.0', tk.END))

	#def open_menu(self, event):
	#	try:
	#		self.main_menu.tk_popup(event.x_root, event.y_root)
	#	except error:
	#		print(error)
	#	finally:
	#		self.main_menu.grab_release()

	#def assign(self):
	#	if self.input.tag_ranges("sel"):
	#		text = self.input.get("sel.first", "sel.last").strip()
	#	else:
	#		messagebox.showerror(parent=self.root, title='Chưa chọn từ', message='Xin hãy bôi đen từ cần được dán nhãn')
	#		return None
	#
	#	if text == '':
	#		messagebox.showerror(parent=self.root, title='Từ được chọn không hợp lệ', message='Từ được bôi đen không hợp lệ')
	#		return None
	#
	#	top_level = tk.Toplevel(self.root)
	#	assign_window = AssignWindow(top_level, text, LanguageTool.pos)
	#	assign_window.pack()
	#	result = assign_window.show()
	#	self.add_text(self.output, result)

class GanThucThe():
	def __init__(self, root):
		self.root = root
		self.text = CustomText(self.root)
		self.open_file_button = tk.Button(self.root, text='Mở file', command=self.open_file)
		self.save_file_button = tk.Button(self.root, text='Lưu file', command=self.save_file)
		
	def pack(self):
		self.text.pack()
		self.open_file_button.pack()
		self.save_file_button.pack()

	def open_file(self):
		file_name = filedialog.askopenfilename(parent=self.root, initialdir='./', title='Chọn file text', filetypes=(('file text', '*.txt'),))
		if file_name != '':
			with open(file_name, encoding='utf-8', mode='r') as file:
				temp = ner(file.read())
				text = ''
				for word in temp:
					text += '/'.join(word) + ' '
				self.text.delete('1.0', tk.END)
				self.text.insert('1.0', text.strip())

	def save_file(self):
		file_name = filedialog.asksaveasfilename(parent=self.root, confirmoverwrite=False, filetypes=(('txt file', '*.txt'),), defaultextension='.txt')
		if file_name != '':
			with open(file_name, mode='w', encoding='utf-8') as file:
				file.write(self.text.get('1.0', tk.END))


				
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


#class LanguageTool():
#
#	pos = [
#		('Np', 'danh từ riêng'),
#		('Nc', 'danh từ đơn thể'),
#		('Ng', 'danh từ tổng thể'),
#		('Nt', 'danh từ loại thể'),
#		('Nu', 'danh từ chỉ đơn vị'),
#		('Na', 'danh từ trừu tượng'),
#		('Nn', 'danh từ số lượng'),
#		('Nl', 'danh từ vị trí'),
#		('Vt', 'động từ ngoại động'),
#		('Vit' ,'động từ nội động'),
#		('Vim' ,'động từ cảm nghĩ'),
#		('Vo', 'động từ chỉ hướng'),
#		('Vs', 'động từ tồn tại'),
#		('Vb', 'động từ biến hoá'),
#		('Vv', 'động từ ý chí'),
#		('Va', 'động từ tiếp thụ'),
#		('Vc', 'động từ so sánh'),
#		('Vm', 'động từ chuyển động'),
#		('Vla', 'động từ "là"'),
#		('Vtim', 'động từ ngoại động cảm nghĩ'),
#		('Vta', 'động từ ngoại động tiếp thụ'),
#		('Vtc', 'động từ ngoại động so sánh'),
#		('Vtb', 'động từ ngoại động biến hoá'),
#		('Vto', 'động từ ngoại động chỉ hướng'),
#		('Vts', 'động từ ngoại động tồn tại'),
#		('Vtm', 'động từ ngoại động chuyển động'),
#		('Vtv', 'động từ ngoại động ý chí'),
#		('Vitim', 'động từ nội động cảm nghĩ'),
#		('Vitb', 'động từ nội động biến hoá'),
#		('Vits', 'động từ nội động tồn tại'),
#		('Vitc', 'động từ nội động so sánh'),
#		('Vitm', 'động từ nội động chuyển động'),
#		('Aa', 'tính từ hàm chất'),
#		('An', 'tính từ hàm lượng'),
#		('Pp', 'đại từ xưng hô'),
#		('Pd', 'đại từ không gian, thời gian'),
#		('Pn', 'đại từ số lượng'),
#		('Pa', 'đại từ hoạt động, tính chất'),
#		('Pi', 'đại từ nghi vấn'),
#		('Jt', 'phụ từ chỉ thời gian'),
#		('Jd', 'phụ từ chỉ mức độ'),
#		('Jr', 'phụ từ so sánh'),
#		('Ja', 'phụ từ khẳng định, phủ định'),
#		('Ji', 'phụ từ mệnh lệnh'),
#		('Cm', 'giới từ'),
#		('Cc', 'liên từ'),
#		('E',' cảm từ'),
#		('I',' trợ từ'),
#		('X',' không')
#	]
#
#	ne = [
#		('NUM', 'Number'),
#		('PER', 'Person'),
#		('LOC', 'Location'),
#		('DTM', 'Date time'),
#		('ORG', 'Organization'),
#		('MEA', 'Measurement'),
#		('TTL', 'Title'),
#		('DES', 'Designation'),
#		('BRN', 'Brand'),
#		('ABB', 'Abbreviation'),
#		('TRM', 'Terminology')
#	]
#
#	@staticmethod
#	def paragraph_to_sentences(text):
#		result = re.compile(r'(?<![A-Z|~\.\.\.])[\.|?|!][\s|$]+').split(text+' ')
#		print(result)
#		return result
#
#	@staticmethod
#	def sentence_to_syllables(text):
#		regex = r"\W*[ |\n|$]+\W*"
#		result = re.split(regex, text.lower()+' ')
#		return result
#
#	@staticmethod
#	def sentence_to_words(text, max_word_len=5):
#		if not 'LanguageTool.VN_dict' in locals():
#			LanguageTool.create_dictionary()
#
#		syllables = LanguageTool.sentence_to_syllables(text.strip())
#		result = []
#		i = 0
#		while i < len(syllables):
#			a_correct_word=''
#			for j in range(i, len(syllables)):
#				if j - i > max_word_len and max_word_len > 0:
#					break;
#
#				if ' '.join(syllables[i:j]) in LanguageTool.VN_dict:
#					a_correct_word = ' '.join(syllables[i:j])
#					new_i = j
#			if a_correct_word == '':
#				result.append(syllables[i].replace(' ', '_'))
#				i += 1
#			else:
#				result.append(a_correct_word.replace(' ', '_'))
#				i = new_i
#
#		return result
#
#	@staticmethod
#	def create_dictionary():
#		df = pd.read_csv('VDic_uni.csv', sep=';', header=None)
#		VN_words = list(df[0])
#		LanguageTool.VN_dict = LanguageTool.list_to_dict(VN_words)
#		LanguageTool.POS_list = [str(pos_tags).replace(' ', '') for pos_tags in df[2]]
#
#	@staticmethod
#	def list_to_dict(a_list):
#		a_dict = {a_list[i]: i for i in range(0, len(a_list))}
#		return a_dict
#
#	@staticmethod
#	def pos_tagging(word_list):
#		if not 'LanguageTool.VN_dict' in locals():
#			LanguageTool.create_dictionary()
#
#		result = []
#		for word in word_list:
#			word = word.replace('_', ' ')
#			if word in LanguageTool.VN_dict:
#				pos_tags = LanguageTool.POS_list[LanguageTool.VN_dict[word]]
#				result.append('{}/{}'. format(word.replace(' ', '_'), pos_tags))
#		return result
#
#	@staticmethod
#	def ne_tagging(word_list):
#		if not 'LanguageTool.VN_dict' in locals():
#			LanguageTool.create_dictionary()
#		
#		result = []		
#		word_list_len = len(word_list)
#		
#		if word_list_len == 0:
#			return []
#		elif word_list_len == 1:
#			entity = ClassifyNameEntity.classify('', word_list[0], '')
#			result.append('{}/{}'.format(word_list[0].replace(' ', '_'), entity))
#		else:
#			for i in range(word_list_len):		
#				if i == 0:
#					entity = ClassifyNameEntity.classify('', word_list[0], word_list[1])
#				elif i == len(word_list) - 1:
#					entity = ClassifyNameEntity.classify(word_list[i-1], word_list[i], '')
#				else: # 0 < i < len - 1
#					entity = ClassifyNameEntity.classify(word_list[i-1], word_list[i], word_list[i+1])			
#				result.append('{}/{}'.format(word_list[i].replace(' ', '_'), entity))
#			
#		return result
#		
#class ClassifyNameEntity():
#
#	person_prefix = ['ông', 'bà', 'anh', 'chị', 'chú', 'bác', 'cô', 'dì', 'con', 'thằng', 'chủ tịch', 'giám_đốc', 'trưởng_phòng']
#	person_lastname = ['nguyễn', 'trần', 'lê', 'phạm', 'huỳnh', 'hoàng', 'phan', 'võ', 'đặng', 'bùi', 'đổ', 'hồ', 'ngô', 'dương', 'lý']
#	location_hint = ['phố', 'phường', 'cầu', 'chùa', 'tháp', 'đại_lộ', 'cao_tốc', 'núi', 'rừng', 'sông', 'suối', 'hồ', 'biển', 'vịnh', 'vũng', 'châu', 'đại_dương', 'đại_lục', 'đồng_bằng', 'cao_nguyên', 'thiên_thể']
#	direction_prefix = ['phương', 'đông', 'tây', 'nam', 'bắc', 'đông_bắc', 'nam_bắc', 'đông_nam', 'tây_nam']
#	organization_hint = ['đạo', 'giáo', 'bộ', 'trường', 'nhà máy', 'xưởng', 'công_ty']
#	number_pattern = [
#		re.compile(r'(^\d*\.?\d*[1-9]+\d*$)|(^[1-9]+\d*\.\d*$)'),
#		re.compile(r'^[-+]?\d+(\.\d+)?$')
#	]
#	datetime_pattern = [
#		re.compile(r'^((([0]?[1-9]|1[0-2])(:|\.)[0-5][0-9]((:|\.)[0-5][0-9])?( )?(AM|am|aM|Am|PM|pm|pM|Pm))|(([0]?[0-9]|1[0-9]|2[0-3])(:|\.)[0-5][0-9]((:|\.)[0-5][0-9])?))$'),
#		re.compile(r'^((31(?!\ (Feb(ruary)?|Apr(il)?|June?|(Sep(?=\b|t)t?|Nov)(ember)?)))|((30|29)(?!\ Feb(ruary)?))|(29(?=\ Feb(ruary)?\ (((1[6-9]|[2-9]\d)(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00)))))|(0?[1-9])|1\d|2[0-8])\ (Jan(uary)?|Feb(ruary)?|Ma(r(ch)?|y)|Apr(il)?|Ju((ly?)|(ne?))|Aug(ust)?|Oct(ober)?|(Sep(?=\b|t)t?|Nov|Dec)(ember)?)\ ((1[6-9]|[2-9]\d)\d{2})$'),
#		# re.compile(r'?n:^(?=\d)((?<month>(0?[13578])|1[02]|(0?[469]|11)(?!.31)|0?2(?(.29)(?=.29.((1[6-9]|[2-9]\d)(0[48]|[2468][048]|[13579][26])|(16|[2468][048]|[3579][26])00))|(?!.3[01])))(?<sep>[-./])(?<day>0?[1-9]|[12]\d|3[01])\k<sep>(?<year>(1[6-9]|[2-9]\d)\d{2})(?(?=\x20\d)\x20|$))?(?<time>((0?[1-9]|1[012])(:[0-5]\d){0,2}(?i:\x20[AP]M))|([01]\d|2[0-3])(:[0-5]\d){1,2})?$'),
#		re.compile(r'^\d{1,2}\/\d{1,2}\/\d{4}$')
#	]
#	measure_pattern = [
#		re.compile(r'(\d*\.?\d+)\s?(cm|dm|m|km|ha|g|mg|kg|t|l|ml|px|em|ex|%|in|cn|mm|pt|pc+)')
#	]
#	
#	@staticmethod
#	def classify(previous_word, word, next_word):
#		property = {
#			'capital': False,
#			'maybe a person': False,
#			'maybe a location': False,
#			'maybe a organization': False,
#			'maybe a number': False,
#			'maybe a datetime': False,
#			'maybe a measure': False
#		}
#		
#		if word.replace('_', ' ') == word.replace('_', ' ').title():
#			property['capital'] = True
#		if previous_word in ClassifyNameEntity.person_prefix:
#			property['maybe a person'] = True
#		for lastname in ClassifyNameEntity.person_lastname:
#			if word.lower().startswith(lastname):
#				property['maybe a person'] = True
#				break
#		for hint in ClassifyNameEntity.location_hint:
#			if hint in word.lower():
#				property['maybe a location'] = True
#				break
#		for prefix in ClassifyNameEntity.direction_prefix:
#			if word.lower().startswith(prefix):
#				property['maybe a location'] = True
#				break
#		for hint in ClassifyNameEntity.organization_hint:
#			if hint in word.lower():
#				property['maybe a organization'] = True
#				break
#		for pattern in ClassifyNameEntity.number_pattern:
#			if pattern.match(word.lower()):
#				property['maybe a number'] = True
#				break
#		for pattern in ClassifyNameEntity.datetime_pattern:
#			if pattern.match(word.lower()):
#				property['maybe a datetime'] = True
#				break
#		for pattern in ClassifyNameEntity.measure_pattern:
#			if pattern.match(word.lower()):
#				property['maybe a measure'] = True
#				break
#		
#		
#		
#		
#		# print(word, word.replace('_', ' '), word.replace('_', ' ').title())
#		# print('cap',property['capital'])
#		# print('per',property['maybe a person'])
#		# print('loc',property['maybe a location'])
#		# print('org',property['maybe a organization'])
#		# print('------------------------------------')
#		
#		
#		
#		if property['maybe a number'] == True:
#			return 'NUM'
#		elif property['maybe a datetime'] == True:
#			return 'DTM'
#		elif property['maybe a measure'] == True:
#			return 'MEA'
#			
#		if property['capital'] == True:
#			if property['maybe a person'] == True:
#				return 'PER'
#			if property['maybe a location'] == False and property['maybe a organization'] == False:
#				return 'TRM'
#			
#			
#		if property['maybe a location'] == True and property['maybe a organization'] == False:
#			return 'LOC'
#		elif property['maybe a organization'] == True and property['maybe a location'] == False:
#			return 'ORG'
#			
#		return 'O'





#class AssignWindow():
#	def __init__(self, root, text, val_and_desc):
#		self.root = root
#		self.text = text
#		self.val_and_desc = val_and_desc
#		self.intVars = []
#		self.checkbuttons = []
#		for val, description in self.val_and_desc:
#			var = tk.IntVar()
#			self.intVars.append(var)
#			self.checkbuttons.append(tk.Checkbutton(self.root, text=f'{val}-{description}', variable=var, command=self.on_check))
#		self.display_text = tk.Label(self.root, text=self.text)
#		self.submit_button = tk.Button(self.root, text='Xác nhận', command=self.submit)
#
#	def pack(self):
#		for button in self.checkbuttons:
#			button.pack()
#		self.display_text.pack()
#		self.submit_button.pack()
#
#	def show(self):
#		self.root.deiconify()
#		self.root.wait_window()
#		return self.result
#
#	def on_check(self):
#		val = []
#		for i in range(len(self.intVars)):
#			if self.intVars[i].get() == 1:
#				val.append(self.val_and_desc[i][0])
#		self.display_text['text'] = '{}/{}'.format(self.text, ','.join(val))
#
#	def submit(self):
#		self.result = self.display_text['text']
#		self.root.destroy()
