from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox, Menu
import tkinter.scrolledtext as txtScr
import pandas as pd
from PIL import ImageTk, Image

root = Tk()

class Start_Page():

    def __init__(self, root):
        self.root = root
        root.geometry("1100x600+130+60")
        root.title("Demo")
        root.configure(background = 'white')
        # Tạo 1 frame chứa 5 nút chức năng
        self.left_frame = LabelFrame(self.root, width=200, bg='purple1', bd=0)
        self.left_frame.pack(side=LEFT, fill=Y)
        #----------------------------------
        # Thiết lập các biến cần dùng, khi nào thấy gọi cái biến lạ hoắc thì chắc chắn nó ở đây
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

    def auto_segmentation(self):
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

    def auto_segmentation(self):
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
        return_val = messagebox.askyesnocancel(parent=self, default='yes',
                message='-nhấn yes để thêm từ mới vào cuối văn bản\n -nhấn no để thay văn bản cũ bằng từ mới')
        if return_val == True:
            widget.insert(END, text + ' ')
        elif return_val == False:
            widget.delete('1.0', END)
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

    def auto_assign(self):
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
        assign_window = AssignWindow(top_level, text, LanguageTool.pos)
        assign_window.pack()
        result = assign_window.show()
        self.add_text(self.output, result)


class GanNhan_ThucThe(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.right_frame = Frame(self, bg='yellow', width=900)
        self.right_frame.pack(side=RIGHT, fill=Y)

class AssignWindow():
    def __init__(self, root, text, val_and_desc):
        self.root = root
        self.text = text
        self.val_and_desc = val_and_desc
        self.intVars = []
        self.checkbuttons = []
        for val, description in self.val_and_desc:
            var = IntVar()
            self.intVars.append(var)
            self.checkbuttons.append(Checkbutton(self.root, text=f'{val}-{description}', variable=var, command=self.on_check))
        self.display_text = Label(self.root, text=self.text)
        self.submit_button = Button(self.root, text='Xác nhận', command=self.submit)

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


ok = Start_Page(root)
ok.pack()
root.mainloop()