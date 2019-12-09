from GuiApplication import Application
from tkinter.filedialog import *
from corpusTrie import Trie
from cProfile import Profile
import os
import sys
from string import ascii_letters,digits,punctuation
from functools import partial

class AppMethods(Application):

	def __init__(self):
		Application.__init__(self)
		self.trie = Trie()

		'''use these function to build Trie Datastructures from your corpus file'''
		# trie.formTrie()
		# trie.createPickledTrie()

		self.trie.loadTrie()
		self.filename = ''

	'''File menu functions'''
	def openFile(self,event):
		
		if self.text_area.get(0.0,END) != "\n":
			if messagebox.askyesnocancel(title='Untitled', message='''Opening new file will override any unsaved changes\nDo you wish to continue ?'''):
				self.text_area.delete(0.0, END)
			else:
				return False

		# 4 MB
		buff_size =  4194304
		
		t = askopenfilename(title = 'Select a file')

		if t:
			p,f = os.path.split(t)
			self.filename = p+'/'+f
			filesize = os.path.getsize(self.filename)

			if filesize > 1000000000:
				self.text_area.delete(0.0,END)
				self.text_area.insert(END,'File size too large, Files upto 1 GB are supported')

				return False

			
			with open(self.filename,'r') as file:

				self.text_area.delete(0.0,END)
				data = file.read(buff_size)
				while data:
					self.text_area.insert(END,data)
					self.text_area.update()
					data = file.read(buff_size)

		del t

	def newFile(self,event):
		if self.text_area.get(1.0, END) == '\n':
			self.text_area.delete(0.0, END)
		else:
			if messagebox.askyesnocancel(title='Untitled', message='''Opening new file will override any unsaved changes\nDo you wish to continue ?'''):
				self.text_area.delete(0.0, END)

	def saveFile(self,event):
		if self.filename == '':
			self.saveAs(None)
		else:
			data = self.text_area.get(0.0, END)
			with open(self.filename,'w') as file:
				file.write(data)

	def saveAs(self,event):
		data = self.text_area.get(0.0, END)
		file = asksaveasfile(mode='w', defaultextension='.txt')

		try:
			if file != None:
				file.write(data.rstrip())
		except:
			messagebox.showerror(message='Unable to save file')

	def quitApp(self,event):

		self.root.destroy()

	'''Spellcheck & suggestion functions'''
	def spellCheckCursor(self, event):

		flag,word,start,end = self.curWtCursor()

		if flag:
			if self.trie.wordSearch(word):
				self.text_area.tag_remove("badWordHighlight", start, end)
			else:
				self.text_area.tag_add("badWordHighlight", start,end)
		else:
			self.text_area.tag_remove("badWordHighlight", start, end)
		
	def spellCheckLine(self,cur,stop):
		
		while cur < stop:
		
			flag,word,start,end = self.curWtCursor(cur)

			if flag:
				if not self.trie.wordSearch(word):
					self.text_area.tag_add("badWordHighlight", start,end)
					self.text_area.update()
			
			cur = self.text_area.index(f'{end} + 1 chars')

	def spellCheck(self):
		#DISABLING TEXT AREA FOR FASTER SPELLCHECK CALLS
		self.text_area.config(state = DISABLED)
		end = float(self.text_area.index(END)) 
		cur = 5.0
		first = 1.0

		if end < cur:
			cur = end

		flag = True
		while cur <= end:

			self.spellCheckLine(str(first),str(cur))
			first = cur
			cur += 5.0
			if end < cur and flag:
				cur = end
				flag = False

		self.text_area.config(state = NORMAL)
			
	def suggestions(self,event):

		#only words if cursor is at the end of word
		flag,word,start,end = self.curWtCursor()

		if flag:
			result = self.trie.prefixSearch(word)

			if result != {} and result != word:
				
				result = sorted(result,key = result.get,reverse=True)

				# Adding suggestions pop up menu
				self.suggestions_menu = Menu(self.root,tearoff = 0)

				self.suggestions_menu.add_command(label="Cut", 
                     accelerator="Ctrl+X", 
                     command=lambda: 
                             self.text_area.focus_get().event_generate('<<Cut>>'))

				self.suggestions_menu.add_command(label="Copy", 
                     accelerator="Ctrl+C", 
                     command=lambda: 
                             self.text_area.focus_get().event_generate('<<Copy>>'))

				self.suggestions_menu.add_command(label="Paste", 
                     accelerator="Ctrl+V", 
                     command=lambda: 
                             self.text_area.focus_get().event_generate('<<paste>>'))
				
				self.suggestions_menu.add_separator()

				r = 5
				if len(result) < 5:
					r = len(result)

				for x in range(r):
					self.suggestions_menu.add_command(label=f"{result[x]}",command=partial(self.replaceWord,result[x], start, end))
					

				self.suggestions_menu.tk_popup(event.x_root,event.y_root, 0)

	def replaceWord(self,new_word,first_pos,current_pos):

        # Validating returned value and updating text accordingly
		if self.text_area.get(0.0, END) == '\n':
			self.text_area.replace(0.0, END, new_word.title())
		elif first_pos.split('.')[1] == '0':
			self.text_area.replace(first_pos, current_pos, new_word.title())
		else:
			self.text_area.replace(first_pos, current_pos, new_word)

	def curWtCursor(self,cur = None):
		if cur != None:
			while True:
				if self.text_area.get(cur) in ascii_letters+digits:
					end = self.text_area.index(f'{cur} wordend')
					break
				else:
					cur = self.text_area.index(f'{cur} +1 chars')
		else:
			cur = self.text_area.index('insert -1 chars wordstart')
			end = self.text_area.index('insert -1 chars wordend')

		word = self.text_area.get(cur,end)
		word = word.strip()
	
		flag = True
		for l in word:
			if l in punctuation or l in digits:
				flag = False
				break

		return flag,word.lower(),cur,end

	'''style and information functions'''
	def themeChange(self, theme):
		if theme == 'light':
			self.text_area.config(
						foreground="#000000",
						background="#F0EAEA",
						insertbackground="#181918",  # cursor
						selectforeground="#B6BAB6",  # selection
						selectbackground="#3C3D3C")
			self.text_area.tag_config("badWordHighlight",foreground='#EA0606')
			
		elif theme == 'dark':
			self.text_area.config(
						foreground="#F6F3F1",
						background="#363636",
						insertbackground="white",  # cursor
						selectforeground="#17202A",  # selection
						selectbackground="#E5E7E9")
			self.text_area.tag_config("badWordHighlight",foreground='#FCD03B')

	def fontChange(self,f,s):
		if f:
			self.fontfamily = f
			self.text_area.config(font=(self.fontfamily,self.fontsize))
			self.text_area.tag_config("badWordHighlight",font = (f"{self.fontfamily}",self.fontsize))
		if s:
			self.fontsize = s
			self.text_area.config(font=(self.fontfamily,self.fontsize))
			self.text_area.tag_config("badWordHighlight",font = (f"{self.fontfamily}",self.fontsize))

	def statusbarUpdate(self,event):
		line,col = str(self.text_area.index("insert")).split(".")
		self.status_bar['text'] = f"Line {line}, Column {col};           "
		
	'''Application mainloop function'''
	def runapp(self):
		self.text_area.focus_set()
		self.root.mainloop()
