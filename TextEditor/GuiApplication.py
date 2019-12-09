from tkinter import ttk,Tk,messagebox , Scrollbar
from tkinter.filedialog import *
from tkinter.font import Font
from functools import partial
from string import ascii_letters,digits,punctuation
import webbrowser

class Application(object):

	def __init__(self):

		self.root = Tk()
		self.root.geometry("800x600")

		# GUI Title
		self.root.title("Beta 5.0")

		# Application Icon / change path after completing the application
		self.root.iconbitmap(r"C:\Users\vishaljs\Desktop\MY\Python\text Editor\image.jpg")

		#Adding scroll bar
		self.scroll_bar = Scrollbar(self.root, bd=1, bg='#75787A', orient=VERTICAL, cursor='arrow', relief=FLAT,
                               activebackground='#75787A')
		self.scroll_bar.pack(side=RIGHT, fill=Y)

        # #  Text Area for typing
		self.fontfamily = 'calibri'
		self.fontsize = 12

		self.text_area = Text(self.root)
		self.text_area.pack(expand=True, fill=BOTH)
		self.text_area.config(font=(f"self.fontfamily",self.fontsize),
                        foreground="#F6F3F1",
                         background="#363636",
                         insertbackground="white",  # cursor
                         selectforeground="#17202A",  # selection
                         selectbackground="#E5E7E9",
                         wrap="word",
                         yscrollcommand=self.scroll_bar.set
                         )

		# Highlighting bad words
		self.text_area.tag_config("badWordHighlight", #underline = True,
									  foreground='#FCD03B' ,
									  font = (f"{self.fontfamily}",self.fontsize))

		#Allow scrolling with mouse movement
		self.scroll_bar.config(command = self.text_area.yview)

		self.status_bar = Label(self.root, text = f'Line 0, Column 0;           ',
									# bg='#75787A',
									relief=FLAT,
									bd = 1, 
									anchor = E)

		self.status_bar.pack(side = BOTTOM,fill=X)

		#building application menu
		self.menu()

		#building event handlers
		self.events()

	def menu(self):
		# Main menu bar at the top
		menu = Menu(self.root)
		self.root.config(menu=menu)

		# File menu inside main menu
		file_menu = Menu(menu, bd=1, relief=FLAT, tearoff=0)
		file_menu.add_command(label='New       Ctrl+N',command = partial(self.newFile,None))
		file_menu.add_command(label='Open      Ctrl+O', command=partial(self.openFile,None))   #partial(self.open_file, self.text_area)
		file_menu.add_command(label='Save       Ctrl+S', command=partial(self.saveFile,None))
		file_menu.add_command(label='Save as  Ctrl+Shft+S', command=partial(self.saveAs,None))
		# file_menu.add_separator()
		file_menu.add_command(label='Exit        Esc', command=partial(self.quitApp,None))
		

		# Edit menu inside main menu
		tools_menu = Menu(menu, bd=1, relief=FLAT, tearoff=0)
		tools_menu.add_command(label='Spell check',command = self.spellCheck)
		
		#view menu
		view_menu = Menu(menu, bd=1, relief=FLAT, tearoff=0)
		theme_menu = Menu(menu, bd=1, relief=FLAT, tearoff=0)
		theme_menu.add_command(label = 'Light',command= partial(self.themeChange,'light'))
		theme_menu.add_command(label = 'Dark',command= partial(self.themeChange,'dark'))

		view_menu.add_cascade(label = 'Theme',menu = theme_menu)
		
		# fonts menu inside View menu
		edit_font = Menu(menu, bd=1, relief=FLAT, tearoff=0)
		edit_font.add_command(label='Calibri', command=partial(self.fontChange, "Calibri",False))
		edit_font.add_command(label='Arial', command=partial(self.fontChange, "Arial",False))
		edit_font.add_command(label='Georgia', command=partial(self.fontChange, "Georgia",False))
		edit_font.add_command(label='Times New Roman', command=partial(self.fontChange, "TimesNewRoman",False))
		edit_font.add_command(label='Verdana', command=partial(self.fontChange, "Verdana",False))

		edit_fontsize = Menu(menu, bd=1, relief=FLAT, tearoff=0)

		for x in range(6,26,2):
			edit_fontsize.add_command(label=f'{x}', command=partial(self.fontChange,False,f"{x}"))

		# adding font meinu to style
		view_menu.add_cascade(label='Font Family', menu=edit_font)
		view_menu.add_cascade(label='Font Size', menu=edit_fontsize)


		# Help Menu inside main menu
		self.help_menu = Menu(menu, bd=1, relief=FLAT, tearoff = 0)
		
		#adding all sub-menu to main
		menu.add_cascade(label='File', menu=file_menu)
		menu.add_cascade(label='View',menu = view_menu)
		menu.add_cascade(label='Tools', menu=tools_menu)
		menu.add_cascade(label="Credit", command= lambda : webbrowser.open("https://www.linkedin.com/in/vishaljeet-singh-2b6099128/"))

	def events(self):
		
		#file control events - shortcuts
		self.text_area.bind("<Control-O>",self.openFile)
		self.text_area.bind("<Control-N>",self.newFile)
		self.text_area.bind("<Control-S>",self.saveFile)
		self.text_area.bind("<Control-o>",self.openFile)
		self.text_area.bind("<Control-n>",self.newFile)
		self.text_area.bind("<Control-s>",self.saveFile)	
		self.text_area.bind("<Control-Shift-S>",self.saveAs)
		self.text_area.bind("<Control-Shift-s>",self.saveAs)
		self.text_area.bind("<Escape>",self.quitApp)

		# spell check events
		self.text_area.bind("<space>", self.spellCheckCursor)
		self.text_area.bind("<Left>", self.spellCheckCursor)
		self.text_area.bind("<Right>", self.spellCheckCursor)
		self.text_area.bind("<Return>", self.spellCheckCursor)

		# suggestions events
		self.text_area.bind("<Button-3>", self.suggestions)

		self.text_area.bind("<Control-Tab>", self.suggestions)

		for cat in [ascii_letters,digits]:
			for alp in cat:
				self.text_area.bind(f"{alp}",self.statusbarUpdate)

		for alp in ["exclam","quotedbl","numbersign","dollar","percent","ampersand","quoteright","parenleft","parenright","asterisk","plus","comma","minus","period","slash","colon","semicolon","less","equal","greater","question","at","bracketleft","backslash","bracketright","asciicircum","underscore","quoteleft","braceleft","bar","braceright","asciitilde","nobreakspace","exclamdown","cent","sterling","currency","yen","brokenbar","section","diaeresis","copyright","ordfeminine","guillemotleft","notsign","hyphen","registered","macron","degree","plusminus","twosuperior","threesuperior","acute","mu","paragraph","periodcentered","cedilla","onesuperior","masculine","guillemotright","onequarter","onehalf","threequarters","questiondown","Agrave","Aacute","Acircumflex","Atilde","Adiaeresis","Aring","AE","Ccedilla","Egrave","Eacute","Ecircumflex","Ediaeresis","Igrave","Iacute","Icircumflex","Idiaeresis","Eth","Ntilde","Ograve","Oacute","Ocircumflex","Otilde","Odiaeresis","multiply","Ooblique","Ugrave","Uacute","Ucircumflex","Udiaeresis","Yacute","Thorn","ssharp","agrave","aacute","acircumflex","atilde","adiaeresis","aring","ae","ccedilla","egrave","eacute","ecircumflex","ediaeresis","igrave","iacute","icircumflex","idiaeresis","eth","ntilde","ograve","oacute","ocircumflex","otilde","odiaeresis","division","oslash","ugrave","uacute","ucircumflex","udiaeresis","yacute","thorn","ydiaeresis","Aogonek","breve","Lstroke","Lcaron","Sacute","Scaron","Scedilla","Tcaron","Zacute","Zcaron","Zabovedot","aogonek","ogonek","lstroke","lcaron","sacute","caron","scaron","scedilla","tcaron","zacute","doubleacute","zcaron","zabovedot","Racute","Abreve","Cacute","Ccaron","Eogonek","Ecaron","Dcaron","Nacute","Ncaron","Odoubleacute","Rcaron","Uring","Udoubleacute","Tcedilla","racute","abreve","cacute","ccaron","eogonek","ecaron","dcaron","nacute","ncaron","odoubleacute","rcaron","uring","udoubleacute","tcedilla","abovedot","Hstroke","Hcircumflex","Iabovedot","Gbreve","Jcircumflex","hstroke","hcircumflex","idotless","gbreve","jcircumflex","Cabovedot","Ccircumflex","Gabovedot","Gcircumflex","Ubreve","Scircumflex","cabovedot","ccircumflex","gabovedot","gcircumflex","ubreve","scircumflex","kappa","Rcedilla","Itilde","Lcedilla","Emacron","Gcedilla","Tslash","rcedilla","itilde","lcedilla","emacron","gacute","tslash","ENG","eng","Amacron","Iogonek","Eabovedot","Imacron","Ncedilla","Omacron","Kcedilla","Uogonek","Utilde","Umacron","amacron","iogonek","eabovedot","imacron","ncedilla","omacron","kcedilla","uogonek","utilde","umacron","overline","kana_fullstop","kana_openingbracket","kana_closingbracket","kana_comma","kana_middledot","kana_WO","kana_a","kana_i","kana_u","kana_e","kana_o","kana_ya","kana_yu","kana_yo","kana_tu","prolongedsound","kana_A","kana_I","kana_U","kana_E","kana_O","kana_KA","kana_KI","kana_KU","kana_KE","kana_KO","kana_SA","kana_SHI","kana_SU","kana_SE","kana_SO","kana_TA","kana_TI","kana_TU","kana_TE","kana_TO","kana_NA","kana_NI","kana_NU","kana_NE","kana_NO","kana_HA","kana_HI","kana_HU","kana_HE","kana_HO","kana_MA","kana_MI","kana_MU","kana_ME","kana_MO","kana_YA","kana_YU","kana_YO","kana_RA","kana_RI","kana_RU","kana_RE","kana_RO","kana_WA","kana_N","voicedsound","semivoicedsound","Arabic_comma","Arabic_semicolon","Arabic_question_mark","Arabic_hamza","Arabic_maddaonalef","Arabic_hamzaonalef","Arabic_hamzaonwaw","Arabic_hamzaunderalef","Arabic_hamzaonyeh","Arabic_alef","Arabic_beh","Arabic_tehmarbuta","Arabic_teh","Arabic_theh","Arabic_jeem","Arabic_hah","Arabic_khah","Arabic_dal","Arabic_thal","Arabic_ra","Arabic_zain","Arabic_seen","Arabic_sheen","Arabic_sad","Arabic_dad","Arabic_tah","Arabic_zah","Arabic_ain","Arabic_ghain","Arabic_tatweel","Arabic_feh","Arabic_qaf","Arabic_kaf","Arabic_lam","Arabic_meem","Arabic_noon","Arabic_heh","Arabic_waw","Arabic_alefmaksura","Arabic_yeh","Arabic_fathatan","Arabic_dammatan","Arabic_kasratan","Arabic_fatha","Arabic_damma","Arabic_kasra","Arabic_shadda","Arabic_sukun","Serbian_dje","Macedonia_gje","Cyrillic_io","Ukranian_je","Macedonia_dse","Ukranian_i","Ukranian_yi","Serbian_je","Serbian_lje","Serbian_nje","Serbian_tshe","Macedonia_kje","Byelorussian_shortu","Serbian_dze","numerosign","Serbian_DJE","Macedonia_GJE","Cyrillic_IO","Ukranian_JE","Macedonia_DSE","Ukranian_I","Ukranian_YI","Serbian_JE","Serbian_LJE","Serbian_NJE","Serbian_TSHE","Macedonia_KJE","Byelorussian_SHORTU","Serbian_DZE","Cyrillic_yu","Cyrillic_a","Cyrillic_be","Cyrillic_tse","Cyrillic_de","Cyrillic_ie","Cyrillic_ef","Cyrillic_ghe","Cyrillic_ha","Cyrillic_i","Cyrillic_shorti","Cyrillic_ka","Cyrillic_el","Cyrillic_em","Cyrillic_en","Cyrillic_o","Cyrillic_pe","Cyrillic_ya","Cyrillic_er","Cyrillic_es","Cyrillic_te","Cyrillic_u","Cyrillic_zhe","Cyrillic_ve","Cyrillic_softsign","Cyrillic_yeru","Cyrillic_ze","Cyrillic_sha","Cyrillic_e","Cyrillic_shcha","Cyrillic_che","Cyrillic_hardsign","Cyrillic_YU","Cyrillic_A","Cyrillic_BE","Cyrillic_TSE","Cyrillic_DE","Cyrillic_IE","Cyrillic_EF","Cyrillic_GHE","Cyrillic_HA","Cyrillic_I","Cyrillic_SHORTI","Cyrillic_KA","Cyrillic_EL","Cyrillic_EM","Cyrillic_EN","Cyrillic_O","Cyrillic_PE","Cyrillic_YA","Cyrillic_ER","Cyrillic_ES","Cyrillic_TE","Cyrillic_U","Cyrillic_ZHE","Cyrillic_VE","Cyrillic_SOFTSIGN","Cyrillic_YERU","Cyrillic_ZE","Cyrillic_SHA","Cyrillic_E","Cyrillic_SHCHA","Cyrillic_CHE","Cyrillic_HARDSIGN","Greek_ALPHAaccent","Greek_EPSILONaccent","Greek_ETAaccent","Greek_IOTAaccent","Greek_IOTAdiaeresis","Greek_IOTAaccentdiaeresis","Greek_OMICRONaccent","Greek_UPSILONaccent","Greek_UPSILONdieresis","Greek_UPSILONaccentdieresis","Greek_OMEGAaccent","Greek_alphaaccent","Greek_epsilonaccent","Greek_etaaccent","Greek_iotaaccent","Greek_iotadieresis","Greek_iotaaccentdieresis","Greek_omicronaccent","Greek_upsilonaccent","Greek_upsilondieresis","Greek_upsilonaccentdieresis","Greek_omegaaccent","Greek_ALPHA","Greek_BETA","Greek_GAMMA","Greek_DELTA","Greek_EPSILON","Greek_ZETA","Greek_ETA","Greek_THETA","Greek_IOTA","Greek_KAPPA","Greek_LAMBDA","Greek_MU","Greek_NU","Greek_XI","Greek_OMICRON","Greek_PI","Greek_RHO","Greek_SIGMA","Greek_TAU","Greek_UPSILON","Greek_PHI","Greek_CHI","Greek_PSI","Greek_OMEGA","Greek_alpha","Greek_beta","Greek_gamma","Greek_delta","Greek_epsilon","Greek_zeta","Greek_eta","Greek_theta","Greek_iota","Greek_kappa","Greek_lambda","Greek_mu","Greek_nu","Greek_xi","Greek_omicron","Greek_pi","Greek_rho","Greek_sigma","Greek_finalsmallsigma","Greek_tau","Greek_upsilon","Greek_phi","Greek_chi","Greek_psi","Greek_omega","leftradical","topleftradical","horizconnector","topintegral","botintegral","vertconnector","topleftsqbracket","botleftsqbracket","toprightsqbracket","botrightsqbracket","topleftparens","botleftparens","toprightparens","botrightparens","leftmiddlecurlybrace","rightmiddlecurlybrace","topleftsummation","botleftsummation","topvertsummationconnector","botvertsummationconnector","toprightsummation","botrightsummation","rightmiddlesummation","lessthanequal","notequal","greaterthanequal","integral","therefore","variation","infinity","nabla","approximate","similarequal","ifonlyif","implies","identical","radical","includedin","includes","intersection","union","logicaland","logicalor","partialderivative","function","leftarrow","uparrow","rightarrow","downarrow","blank","soliddiamond","checkerboard","ht","ff","cr","lf","nl","vt","lowrightcorner","uprightcorner","upleftcorner","lowleftcorner","crossinglines","horizlinescan1","horizlinescan3","horizlinescan5","horizlinescan7","horizlinescan9","leftt","rightt","bott","topt","vertbar","emspace","enspace","em3space","em4space","digitspace","punctspace","thinspace","hairspace","emdash","endash","signifblank","ellipsis","doubbaselinedot","onethird","twothirds","onefifth","twofifths","threefifths","fourfifths","onesixth","fivesixths","careof","figdash","leftanglebracket","decimalpoint","rightanglebracket","marker","oneeighth","threeeighths","fiveeighths","seveneighths","trademark","signaturemark","trademarkincircle","leftopentriangle","rightopentriangle","emopencircle","emopenrectangle","leftsinglequotemark","rightsinglequotemark","leftdoublequotemark","rightdoublequotemark","prescription","minutes","seconds","latincross","hexagram","filledrectbullet","filledlefttribullet","filledrighttribullet","emfilledcircle","emfilledrect","enopencircbullet","enopensquarebullet","openrectbullet","opentribulletup","opentribulletdown","openstar","enfilledcircbullet","enfilledsqbullet","filledtribulletup","filledtribulletdown","leftpointer","rightpointer","club","diamond","heart","maltesecross","dagger","doubledagger","checkmark","ballotcross","musicalsharp","musicalflat","malesymbol","femalesymbol","telephone","telephonerecorder","phonographcopyright","caret","singlelowquotemark","doublelowquotemark","cursor","leftcaret","rightcaret","downcaret","upcaret","overbar","downtack","upshoe","downstile","underbar","jot","quad","uptack","circle","upstile","downshoe","rightshoe","leftshoe","lefttack","righttack","hebrew_aleph","hebrew_beth","hebrew_gimmel","hebrew_daleth","hebrew_he","hebrew_waw","hebrew_zayin","hebrew_het","hebrew_teth","hebrew_yod","hebrew_finalkaph","hebrew_kaph","hebrew_lamed","hebrew_finalmem","hebrew_mem","hebrew_finalnun","hebrew_nun","hebrew_samekh","hebrew_ayin","hebrew_finalpe","hebrew_pe","hebrew_finalzadi","hebrew_zadi","hebrew_kuf","hebrew_resh","hebrew_shin","hebrew_taf","BackSpace","Tab","Linefeed","Clear","Pause","Scroll_Lock","Sys_Req","Multi_key","Kanji","Home","Up","Down","Prior","Next","End","Begin","Win_L","Win_R","App","Select","Print","Execute","Insert","Undo","Redo","Menu","Find","Cancel","Help","Break","Hebrew_switch","Num_Lock","KP_Space","KP_Tab","KP_Enter","KP_F1","KP_F2","KP_F3","KP_F4","KP_Multiply","KP_Add","KP_Separator","KP_Subtract","KP_Decimal","KP_Divide","KP_0","KP_1","KP_2","KP_3","KP_4","KP_5","KP_6","KP_7","KP_8","KP_9","KP_Equal","F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","L1","L2","L3","L4","L5","L6","L7","L8","L9","L10","R1","R2","R3","R4","R5","R6","R7","R8","R9","R10","R11","R12","F33","R14","R15","Shift_L","Shift_R","Control_L","Control_R","Caps_Lock","Shift_Lock","Meta_L","Meta_R","Alt_L","Alt_R","Super_L","Super_R","Hyper_L","Hyper_R","Delete"]:
			self.text_area.bind(f"<{alp}>",self.statusbarUpdate)
