from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox, Menu
import tkinter.scrolledtext as txtScr
import pandas as pd
from PIL import ImageTk, Image

root = Tk()
saved = 0

class Start_Page():

    def __init__(self, root):
        self.root = root
        root.geometry("1100x600+130+60")
        root.title("Gán nhãn ngữ liệu")
        root.configure(background = 'white')
        # Tạo 1 frame chứa 5 nút chức năng
        self.left_frame = LabelFrame(self.root, width=200, bg='purple1', bd=0)
        self.left_frame.pack(side=LEFT, fill=Y)
        #----------------------------------
        # Thiết lập các biến cần dùng
        self._frame = None
        self.pixelVirtual = PhotoImage(width=1, height=1)
        #---------------------------------
        # Tạo 5 Button
        self.Butts = []
        self.tach_cau_button = Button(self.left_frame, text='TÁCH CÂU', 
                                    command=lambda num=0 : self.Click(num, Tach_Cau))      
        self.tach_tu_button = Button(self.left_frame, text='TÁCH TỪ', 
                                    command=lambda num=1 : self.Click(num, Tach_Tu))       
        self.gan_nhan_tu_button = Button(self.left_frame, text='GÁN NHÃN TỪ', 
                                    command=lambda num=2 : self.Click(num, GanNhan_Tu))       
        self.gan_nhan_thuc_the_button = Button(self.left_frame, text='GÁN NHÃN THỰC THỂ', 
                                    command=lambda num=3 : self.Click(num, GanNhan_ThucThe))
        self.thoat_button = Button(self.left_frame, text='THOÁT',
                                    command=lambda : root.destroy())
        #--------------------------------
        # Add 4 button vào 1 list để tiện gọi hơn
        self.Butts.append(self.tach_cau_button)
        self.Butts.append(self.tach_tu_button)
        self.Butts.append(self.gan_nhan_tu_button)
        self.Butts.append(self.gan_nhan_thuc_the_button)
        self.Butts.append(self.thoat_button)
        #--------------------------------
        # setup linh tinh cho cái button dễ nhìn hơn
        for butt in self.Butts:
            butt.config(bd =0, image=self.pixelVirtual, font= ('Roboto', 13),
                        bg='purple1', activebackground='MediumPurple2', 
                        disabledforeground='white', activeforeground='white',
                        height=90, anchor='w', padx=10, fg='white', compound='c')

    def pack(self):
        for butt in self.Butts:
            butt.pack(side = TOP, fill = X)
  
    def Click(self, num, frame_class):
        global saved
        if saved == 1: 
            warn = messagebox.askquestion("Cảnh báo","Bạn chưa lưu file\n - Ấn Yes để bỏ qua lưu file\n - Ấn No để quay lại",
                                        icon='warning', default='no')
            if warn == 'no': 
                return 0
            else:         
                saved = 0
        #Button đc chọn sẽ đổi màu và k thể chọn, các button còn lại set về mặc định      
        for butt in self.Butts:
            butt.config(bg='purple1', state=NORMAL)
        self.Butts[num].config(bg='MediumPurple2', state=DISABLED)
        self.Swap_frame(frame_class)
  
    def Swap_frame(self, frame_class):
        new_frame = frame_class(self.root)
        #Mở frame mới, huỷ frame cũ, nếu chưa save thì hiện messagebox
        if self._frame is not None:
            self._frame.destroy()      
        self._frame = new_frame
        self._frame.pack()
        

class Tach_Cau(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.config(self, bg='white')
        #----------------------------
        self.box = LabelFrame(self, text="Chọn tính năng", font=('Roboto', 12), 
                            relief=GROOVE, bg='white')
        #----------------------------
        self.but1 = ttk.Button(self.box, text='Mở file', command=self.open_file)
        self.but2 = ttk.Button(self.box, text='Lưu file', command=self.save_file)
        self.but3 = ttk.Button(self.box, text='Auto tách câu', command=self.auto_segmentation)
        #----------------------------
        self.input = txtScr.ScrolledText(self, wrap = WORD, font=("LucidaConsole",13),
                                         padx=5, bd=4, height=14, relief=GROOVE)
        self.output = txtScr.ScrolledText(self, wrap = WORD, font=("LucidaConsole",13), 
                                        padx=5, bd=4, height=14, relief=GROOVE)
        
        
    def pack(self):
        Frame.pack(self, fill= BOTH)
        self.box.pack(side=LEFT, padx=5, anchor= N)
        #-----------------------------
        self.but1.pack(padx= 3, pady=5, fill = BOTH)
        self.but2.pack(padx= 3, pady=5, fill = BOTH)
        self.but3.pack(padx= 3, pady=5, fill = BOTH)
        #-----------------------------
        self.input.pack(side=TOP, fill=X, padx=5, pady=5)
        self.output.pack(side=TOP, fill=X, padx=5, pady=5)

    def open_file(self):
        file_name = filedialog.askopenfilename(parent=self, initialdir='./', 
                                title='Chọn file text', filetypes=(('file text', '*.txt'),))
        if file_name != '':
            with open(file_name, encoding='utf-8', mode='r') as file:
                text = file.read()
            self.input.delete('1.0', END)
            self.input.insert('1.0', text)

    def save_file(self):
        file_name = filedialog.asksaveasfilename(parent=self, confirmoverwrite=False, 
                                filetypes=(('txt file', '*.txt'),), defaultextension='.txt')
        if file_name != '':
            with open(file_name, mode='w', encoding='utf-8') as file:
                file.write(self.output.get('1.0', END))
                global saved
                saved = 0
               
    def auto_segmentation(self):
        global saved
        saved = 1
        sentences = LanguageTool.paragraph_to_sentences(self.input.get('1.0', END))
        text = '\n\n'.join(sentences)
        self.output.delete('1.0', END)
        self.output.insert('1.0', text)
      

  
class Tach_Tu(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.config(self, bg='white')
        #------------------------------
        self.box = LabelFrame(self, text="Chọn tính năng", font=('Roboto', 12), 
                            relief=GROOVE, bg='white')
        #------------------------------
        self.but1 = ttk.Button(self.box, text='Mở file', command=self.open_file)
        self.but2 = ttk.Button(self.box, text='Lưu file', command=self.save_file)
        self.but3 = ttk.Button(self.box, text='Auto tách từ', command=self.auto_segmentation)
        self.selected_text = Entry(self.box, font=('Roboto',12), bd=2, relief=GROOVE)
        self.but4 = ttk.Button(self.box, text='Thêm từ đã chọn', command=self.add_selected_text)
        #------------------------------
        self.input = txtScr.ScrolledText(self, wrap = WORD, font=("LucidaConsole",13),
                                        padx=5, bd=4, height=14, relief=GROOVE)		
        self.input.bind('<ButtonRelease-1>', func=self.get_selected_text)
        self.output = CustomText(self, wrap = WORD, font=("LucidaConsole",13), 
                                bd=4, padx=5, height=14, relief=GROOVE)
        self.output.tag_configure('yellow_background', background='#ffff00')

    def pack(self):
        Frame.pack(self, fill=BOTH)
        self.box.pack(side=LEFT, padx=5, anchor= N)
        #-----------------------------
        self.but1.pack(padx= 3, pady=5, fill = BOTH)
        self.but2.pack(padx= 3, pady=5, fill = BOTH)
        self.but3.pack(padx= 3, pady=5, fill = BOTH)
        self.selected_text.pack(padx= 3, pady=10, ipady=7)
        self.but4.pack(padx= 3, pady=5, fill = BOTH)
        #-----------------------------
        self.input.pack(side=TOP, fill=X, padx=5, pady=5)
        self.output.pack(side=TOP, fill=X, padx=5, pady=5)

    def open_file(self):
        file_name = filedialog.askopenfilename(parent=self, initialdir='./', 
                                    title='Chọn file text', filetypes=(('file text', '*.txt'),))
        
        if file_name != '':
            with open(file_name, encoding='utf-8', mode='r') as file:
                text = file.read()
            self.input.delete('1.0', END)
            self.input.insert('1.0', text)

    def save_file(self):
        file_name = filedialog.asksaveasfilename(parent=self, confirmoverwrite=False, 
                                    filetypes=(('txt file', '*.txt'),), defaultextension='.txt')

        if file_name != '':
            with open(file_name, mode='w', encoding='utf-8') as file:
                file.write(self.output.get('1.0', END))
                global saved
                saved = 0
               

    def auto_segmentation(self):
        global saved
        saved = 1
        words = LanguageTool.sentence_to_words(self.input.get('1.0', END))
        text = ' '.join(words)
        self.add_text(self.output, text)
        
       

    def get_selected_text(self, event):
        if self.input.tag_ranges("sel"):
            text = self.input.get("sel.first", "sel.last")
            self.selected_text.delete(0, END)
            self.selected_text.insert(0, text)

    def add_selected_text(self):
        text = self.selected_text.get().strip()
        if text == '':
            messagebox.showerror(parent=self, title='Lỗi dữ liệu đầu vào', 
                                message='Từ thêm vào không được phép rỗng.')
        else:
            self.add_text(self.output, text.replace(' ', '_'))

    def add_text(self, widget, text):     
        widget.insert(END, text + ' ')
        #self.update_output_background()

    def update_output_background(self):
        self.output.tag_remove('yellow_background', '1.0', END)

        text = self.output.get('1.0', END).strip()
        words = text.split()
        for word in words:
            self.output.highlight_pattern(word, 'yellow_background')


class GanNhan_Tu(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.config(self, bg='white')
        #------------input--------------
        self.input = CustomText(self, wrap = WORD, font=("LucidaConsole",13), 
                                bd=4, padx=5, height=14, relief=GROOVE)
        self.input.bind('<Button-3>', self.open_menu)
        # menu chính
        self.main_menu = Menu(self, tearoff=0)
        self.main_menu.add_command(label='Dán nhãn từ', command=self.assign)
        #-------------------------------
        self.box = LabelFrame(self, text="Chọn tính năng", font=('Roboto', 12), 
                            relief=GROOVE, bg='white')
        #-------------------------------
        self.but1 = ttk.Button(self.box, text='Mở file', command=self.open_file)
        self.but2 = ttk.Button(self.box, text='Lưu file', command=self.save_file)
        self.but3 = ttk.Button(self.box, text='Tự động gán nhãn từ', command=self.auto_assign)
        #--------ouput------------------
        self.output = CustomText(self,wrap = WORD, font=("LucidaConsole",13), 
                                bd=4, padx=5, height=14, relief=GROOVE)

    def pack(self):
        Frame.pack(self, fill=BOTH)
        #-------------------------------
        self.box.pack(side=LEFT, padx=5, anchor=N)
        #-------------------------------
        self.but1.pack(padx= 3, pady=5, fill = BOTH)
        self.but2.pack(padx= 3, pady=5, fill = BOTH)
        self.but3.pack(padx= 3, pady=5, ipadx=5, ipady=3 , fill = BOTH)
        #-------------------------------
        self.input.pack(side=TOP, fill=X, padx=5, pady=5)
        self.output.pack(side=TOP, fill=X, padx=5, pady=5)

    def open_file(self):
        file_name = filedialog.askopenfilename(parent=self, initialdir='./', title='Chọn file text', filetypes=(('file text', '*.txt'),))
        
        if file_name != '':
            with open(file_name, encoding='utf-8', mode='r') as file:
                text = file.read()
            self.input.delete('1.0', END)
            self.input.insert('1.0', text)

    def save_file(self):
        file_name = filedialog.asksaveasfilename(parent=self, confirmoverwrite=False, filetypes=(('txt file', '*.txt'),), defaultextension='.txt')

        if file_name != '':
            with open(file_name, mode='w', encoding='utf-8') as file:
                file.write(self.output.get('1.0', END))
                global saved
                saved = 0
               

    def auto_assign(self):
        global saved
        saved = 1
        text = self.input.get('1.0', END)
        words = text.split()
        pos_tagged_words = LanguageTool.pos_tagging(words)
        self.add_text(self.output, ' '.join(pos_tagged_words))
        

    def add_text(self, widget, text):
        widget.insert(END, text + ' ')

    def open_menu(self, event):
        try:
            self.main_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.main_menu.grab_release()

    def assign(self):
        if self.input.tag_ranges("sel"):
            text = self.input.get("sel.first", "sel.last").strip()
        else:
            messagebox.showerror(parent=self, title='Chưa chọn từ', message='Xin hãy bôi đen từ cần được dán nhãn')
            return None

        if text == '':
            messagebox.showerror(parent=self, title='Từ được chọn không hợp lệ', message='Từ được bôi đen không hợp lệ')
            return None
        top_level = Toplevel(root)
        top_level.geometry("+350+100")
        assign_window = AssignWindow(top_level, text, LanguageTool.pos)
        assign_window.pack()
        result = assign_window.show()
        self.add_text(self.output, result)


class GanNhan_ThucThe(GanNhan_Tu):
    def __init__(self, root):
        GanNhan_Tu.__init__(self, root)
        self.but3['text'] = 'Tự động dán thực thể'
        #self.auto_assign_button['state'] = 'disable'
        self.main_menu.entryconfigure(1, label='Dán nhãn thực thể')

    def auto_assign(self):
        global saved
        saved = 1
        text = self.input.get('1.0', END)
        words = text.split()
        ne_tagged_words = LanguageTool.ne_tagging(words)
        self.add_text(self.output, ' '.join(ne_tagged_words))
      

    def assign(self):
        if self.input.tag_ranges("sel"):
            text = self.input.get("sel.first", "sel.last").strip()
        else:
            messagebox.showerror(parent=self, title='Chưa chọn từ', message='Xin hãy bôi đen từ cần được dán nhãn thực thể')
            return None

        if text == '':
            messagebox.showerror(parent=self, title='Từ được chọn không hợp lệ', message='Từ được bôi đen không hợp lệ')
            return None
        
        toplevel = Toplevel(self)
        toplevel.geometry("+350+100")
        assign_window = AssignWindow(toplevel, text, LanguageTool.ne)
        assign_window.pack()
        result = assign_window.show()

        self.add_text(self.output, result)


class AssignWindow():
    def __init__(self, root, text, val_and_desc):
        self.root = root
        self.text = text
        self.val_and_desc = val_and_desc
        self.list = []
        self.choose = StringVar()
        self.comboBox = ttk.Combobox(self.root, width=20, textvariable=self.choose)
        for val, description in self.val_and_desc:
            self.list.append(f'{val}-{description}')
        self.comboBox['values'] = self.list
        self.Lb = ttk.Label(self.root, text = 'Chọn 1 nhãn:', font=('Roboto',13))
        self.submit_button = ttk.Button(self.root, text='Xác nhận', command=self.submit)

    def pack(self):
        self.Lb.pack(side=TOP)
        self.comboBox.pack(padx=5)
        self.submit_button.pack(pady=5)
    
    def show(self):
        self.root.deiconify()
        self.root.wait_window()
        return self.result

    def submit(self):
        val = (self.choose.get()).split("-")
        self.result = '{}/{}'.format(self.text,val[0])
        self.root.destroy()     

class CustomText(txtScr.ScrolledText):
    '''A text widget with a new method, highlight_pattern()

    example:

    text = CustomText()
    text.tag_configure("red", foreground="#ff0000")
    text.highlight_pattern("this should be red", "red")

    The highlight_pattern method is a simplified python
    version of the tcl code at http://wiki.tcl.tk/3246
    '''
    def __init__(self, *args, **kwargs):
        txtScr.ScrolledText.__init__(self, *args, **kwargs)

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

        count = IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit", count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")


class LanguageTool():

	pos = [
		('Np', 'danh từ riêng'),
		('Nc', 'danh từ đơn thể'),
		('Ng', 'danh từ tổng thể'),
		('Nt', 'danh từ loại thể'),
		('Nu', 'danh từ chỉ đơn vị'),
		('Na', 'danh từ trừu tượng'),
		('Nn', 'danh từ số lượng'),
		('Nl', 'danh từ vị trí'),
		('Vt', 'động từ ngoại động'),
		('Vit' ,'động từ nội động'),
		('Vim' ,'động từ cảm nghĩ'),
		('Vo', 'động từ chỉ hướng'),
		('Vs', 'động từ tồn tại'),
		('Vb', 'động từ biến hoá'),
		('Vv', 'động từ ý chí'),
		('Va', 'động từ tiếp thụ'),
		('Vc', 'động từ so sánh'),
		('Vm', 'động từ chuyển động'),
		('Vla', 'động từ "là"'),
		('Vtim', 'động từ ngoại động cảm nghĩ'),
		('Vta', 'động từ ngoại động tiếp thụ'),
		('Vtc', 'động từ ngoại động so sánh'),
		('Vtb', 'động từ ngoại động biến hoá'),
		('Vto', 'động từ ngoại động chỉ hướng'),
		('Vts', 'động từ ngoại động tồn tại'),
		('Vtm', 'động từ ngoại động chuyển động'),
		('Vtv', 'động từ ngoại động ý chí'),
		('Vitim', 'động từ nội động cảm nghĩ'),
		('Vitb', 'động từ nội động biến hoá'),
		('Vits', 'động từ nội động tồn tại'),
		('Vitc', 'động từ nội động so sánh'),
		('Vitm', 'động từ nội động chuyển động'),
		('Aa', 'tính từ hàm chất'),
		('An', 'tính từ hàm lượng'),
		('Pp', 'đại từ xưng hô'),
		('Pd', 'đại từ không gian, thời gian'),
		('Pn', 'đại từ số lượng'),
		('Pa', 'đại từ hoạt động, tính chất'),
		('Pi', 'đại từ nghi vấn'),
		('Jt', 'phụ từ chỉ thời gian'),
		('Jd', 'phụ từ chỉ mức độ'),
		('Jr', 'phụ từ so sánh'),
		('Ja', 'phụ từ khẳng định, phủ định'),
		('Ji', 'phụ từ mệnh lệnh'),
		('Cm', 'giới từ'),
		('Cc', 'liên từ'),
		('E',' cảm từ'),
		('I',' trợ từ'),
		('X',' không')
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
					break

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



ok = Start_Page(root)
ok.pack()
root.mainloop()