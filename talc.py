from __future__ import division
import wx
import numpy
import glob 
import os
import re
import string
import wx.grid

negations=["aint","aint","arent","arent","cannot","cant","cant","couldnt","couldnt","didnt","didnt","doesnt","doesnt","dont","dont","hadnt","hadnt","hasnt","hasnt","havent","havent","isnt","isnt","mustnt","mustnt","mustnt","neednt","neednt","neednt","negat*","neither","never","no","nobod*","none","nope","nor","not","nothing","nowhere","oughtnt","oughtnt","oughtnt","shant","shant","shouldnt","shouldnt","shouldnt","uhuh","wasnt","wasnt","werent","without","wont","wont","wouldnt","wouldnt"]
negations = "".join(["\\b"+str(word)+"\\b|" for word in negations])#get to the end of a sentence
negations = negations[:-1] 
negations=re.compile(negations,re.IGNORECASE)

adverbs=["absolutely","awfully","comfortably","completely","conspicuously","damned","decidedly","dreadfully","emphatically","enormously","enough","entirely","even","exactly","exceedingly ","extremely","fairly","far ","frightfully","genuinely","gloriously ","goddamn","god damn","good and","hardly","highly","how","incredibly","just","kind of","largely ","literally","mighty","monstrous","more","more and more","more or less ","most","much","only","own ","perfectly","plenty","pretty","pure","purely","quite","rather","rather ","real","really","reasonably","right","scrupulously","severely ","simply","so","sort of","some","somehow","somewhat","still","strongly","sure","surely","surprisingly","terribly","thoroughly","totally","truly","utterly","very","virtually","way","well","whole","wholly","wonderfully","hella","flipping","flippin","sorta","sort of","kinda","way","new","today","yesterday","tomorrow","fuckin","fucking","fing","freaking","freakin"]
adverbs = "".join(["\\b"+str(word)+"\\b|" for word in adverbs])#get to the end of a sentence
adverbs = adverbs[:-1] 
adverbs=re.compile(adverbs,re.IGNORECASE)

APP_SIZE_X = 550
APP_SIZE_Y = 365

def get_LIWC_dics(folder,case=False):
	LIWC_dic={}
	name_dic={}
	name_list=[]
	dic_list=[]
	name_list=[]
	dic_list=[]
	for file in folder:
		with open(file,"rb") as f:
			f.next()
			start=False
			for line in f:
				try:
					line=line.strip()
					#print line
					if len(line) > 0 and line[0] == "%":start=True
					elif start==False:
						' '.join(line.split())
						items=line.split()
						LIWC_dic[items[0]]=[]
						name_dic[items[0]]=items[1]
					else:
						line=line.split("\t")
						if "<" in line[1]:
							phrase = line[0]
							re.escape(phrase)
							keys=[x.split("/")[1] for x in line[1:]]
							for item in keys:LIWC_dic[item].append(phrase)
							
							phrase = line[0]+" "+re.search(r'\<(.*?)\>',line[1]).group(1)
							re.escape(phrase)
							keys=[re.sub('[^0-9]','',x.split("/")[0]) for x in line[1:]]
						else:
							phrase = line[0]
							
							print phrase
							phrase=re.escape(phrase)
							keys = line[1:]
							line[1:] = [re.sub(r'\<[^)]*\>', '', x) for x in line[1:]]
							line[1:] = [re.sub(r'\([^)]*\)', '', x) for x in line[1:]]
							joined = ' '.join(line[1:])
							joined = joined.replace('/', ' ')
							keys=joined.split()
							#keys  = items[1:]
							#for item in keys:LIWC_dic[item].append(items[0])
							for item in keys:LIWC_dic[item].append(phrase)
				except:pass
			
			if case==True:
				for dic in LIWC_dic:
					statement=""
					name_list.append(name_dic[dic])
					for word in LIWC_dic[dic]:
						statement+="\\b"+word+"\\b|" 
					statement=statement[:-1] 
					statement = statement.replace("\\b\\:\\)\\b","\\:\\)")
					statement = statement.replace("\\b\\:\\(\\b","\\:\\(")
					statement = statement.replace("\\b\\(\\:\\b","\\(\\:")
					statement = statement.replace("\\b\\)\\:\\b","\\)\\:")
					keywords=re.compile(statement) 
					dic_list.append(keywords)
			else:
				for dic in LIWC_dic:
					statement=""
					name_list.append(name_dic[dic])
					for word in LIWC_dic[dic]:
						statement+="\\b"+word+"\\b|" 
					statement=statement[:-1] 
					statement = statement.replace("\\b\\:\\)\\b","\\:\\)")
					statement = statement.replace("\\b\\:\\(\\b","\\:\\(")
					statement = statement.replace("\\b\\(\\:\\b","\\(\\:")
					statement = statement.replace("\\b\\)\\:\\b","\\)\\:")
					keywords=re.compile(statement, re.IGNORECASE) 
					dic_list.append(keywords)
	return name_list,dic_list
			

def get_dics(folder,case=False):
	name_list=[]
	dic_list=[]
	if case==True:
		for file in folder:
			with open(file) as f: 
				statement=""
				for line in f:
					line = line.strip()
					statement+="\\b"+str(line)+"\\b|" 
			statement=statement[:-1] 
			keywords=re.compile(statement) 
			name_list.append(file.split(".")[0].split("\\")[-1])
			dic_list.append(keywords)
	else:
		for file in folder:
			with open(file) as f: 
				statement=""
				for line in f:
					line = line.strip()
					statement+="\\b"+str(line)+"\\b|" 
			statement=statement[:-1] 
			keywords=re.compile(statement, re.IGNORECASE) 
			name_list.append(file.split(".")[0].split("\\")[-1])
			dic_list.append(keywords)
	return  name_list, dic_list
	
def analyze_text(text,dics,filter,dichotomize,filename,linenumber):
	results = []
	words=len(string.split(text))
	results.append(str(filename))
	results.append(str(linenumber))
	results.append(str(words))
	if filter==False:
		for dic in dics:
			matches=dic.findall(text)
			if dichotomize==True:a="%.0f" % numpy.ceil(len(matches)/words)
			else:
				try:a="%.4f" % (((len(matches)/words))*100)
				except:a="0.000"
			results.append(a)
	else:#if filtering for negations
		for dic in dics:
			matches=[]
			matches=dic.findall(text) #"i am not happy"
			for entry in matches: #"happy"
				text_with_negation=[]
				text_with_negation=re.findall('(\w+) \\b'+entry+'\\b',text)#not
				for  item in text_with_negation:
					if negations.search(item):
						text=re.sub(entry,"#"*len(entry),text,1)
			text2=text
			matches=[]
			matches=dic.findall(text2)
			if dichotomize==True:a="%.0f" % numpy.ceil(len(matches)/words)
			else: a="%.4f" % (((len(matches)/words))*100)
			results.append(a)
	return results

def analyze_lines(files,output_file,name_list,dics,filter,dichotomize,remove_adverbs):
	labels= "\t".join(name_list)
	results = numpy.zeros((1000,len(dics)+3)).astype("S100")
	k=0
	with open(output_file,"wb") as j:
		j.write("filename"+"\t"+"linenumber"+"\t"+"numberwords"+"\t"+labels+"\n")
		for filename in files: 
			with open(filename,"rb") as g:
				linenumber=1
				for line in g:
					if remove_adverbs:line = adverbs.sub('', line)
					res = analyze_text(line,dics,filter,dichotomize,filename,linenumber)
					if k < 1000: 
						results[k,:] = numpy.array(res)
						k+=1
					j.write("\t".join(res)+"\n")
					linenumber+=1
	return results[0:k,:]

def analyze_lines2(files,output_file,name_list,dics,filter,dichotomize,remove_adverbs):
	labels= "\t".join(name_list)
	results = numpy.zeros((1000,len(dics)+3)).astype("S100")
	k=0
	for filename in files: 
		with open(filename,"rb") as g:
			linenumber=1
			for line in g:
				if remove_adverbs:line = adverbs.sub('', line)
				res = analyze_text(line,dics,filter,dichotomize,filename,linenumber)
				if k < 1000: 
					results[k,:] = numpy.array(res)
					k+=1
				linenumber+=1
	return results[0:k,:]
	
def filedialog(self):
	self.filelist=[]
	dlg = wx.FileDialog(self, message="Choose File",defaultFile="",style=wx.OPEN |  wx.MULTIPLE| wx.CHANGE_DIR)
	if dlg.ShowModal() == wx.ID_OK:
		paths = dlg.GetPaths()
		for path in paths:
			self.filelist.append(str(path))
	dlg.Destroy()
	return self.filelist

def folderdialog(self):
	self.filelist=[]
	dlg = wx.FileDialog(self, message="Choose File",defaultFile="", wildcard="*.dat",style=wx.SAVE | wx.OVERWRITE_PROMPT| wx.CHANGE_DIR)
	if dlg.ShowModal() == wx.ID_OK:
		infile = dlg.GetPath()
	dlg.Destroy()
	return infile

	
	
class MyForm(wx.Frame):
	global myGrid
	
	#----------------------------------------------------------------------
	def __init__(self):
		global main_self
		
		wx.Frame.__init__(self, None, wx.ID_ANY,title="TALC: The Automated Language Counter",size=(APP_SIZE_X, APP_SIZE_Y))
		self.SetMaxSize((APP_SIZE_X, APP_SIZE_Y))
		self.SetMinSize((APP_SIZE_X, APP_SIZE_Y))

		self.Bind(wx.EVT_CLOSE, self.onClose)
		
		
		self.panel_one = PanelOne(self)
		self.panel_two = PanelTwo(self)
		
		self.panel_two.Hide()
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.panel_one, 1, wx.EXPAND)
		self.sizer.Add(self.panel_two, 1, wx.EXPAND)
		
	
		self.SetSizer(self.sizer)
 
 
		
		fileMenu = wx.Menu()
		#switch_panels_menu_item1 = fileMenu.Append(wx.ID_ANY, "Compute Aggregation","Some text")
		switch_panels_menu_item1 = fileMenu.Append(wx.ID_ANY,"Analyze","Some text")
		switch_panels_menu_item2 = fileMenu.Append(wx.ID_ANY,"Results","Some text")
		switch_panels_menu_item3 = fileMenu.Append(wx.ID_ANY,"About","Some text")
		switch_panels_menu_item4 = fileMenu.Append(wx.ID_ANY,"Exit Program","Some text")
		
		#self.Bind(wx.EVT_MENU, self.onSwitchPanels1,switch_panels_menu_item1)
		self.Bind(wx.EVT_MENU, self.analyze,switch_panels_menu_item1)
		self.Bind(wx.EVT_MENU, self.results,switch_panels_menu_item2)
		self.Bind(wx.EVT_MENU, self.about,switch_panels_menu_item3)
		self.Bind(wx.EVT_MENU, self.onExitProgram,switch_panels_menu_item4)
		

		
		menubar = wx.MenuBar()
		menubar.Append(fileMenu, '&Menu')
		self.SetMenuBar(menubar)
		main_self=self
    #----------------------------------------------------------------------
	

	
	def analyze(self, event):
		self.SetTitle("TALC: Analyze Text")
		self.panel_two.Hide()
		self.panel_one.Show()
		self.Layout()
		
		
	def results(self, event=True):
		self.SetTitle("TALC: Analysis Results")
		self.panel_one.Hide()
		self.panel_two = PanelTwo(self)
		self.sizer.Add(self.panel_two, 1, wx.EXPAND)
		self.SetSizer(self.sizer)
		self.Layout()
		
	def about(self, event):
		wx.MessageBox('Hernandez, I, Newman, D.A., & Jeon, G. (2014)', 'About')

	def onTaskbar(self, evt):
		mainopen=0
		self.Hide()
		
	def onClose(self, evt):
		self.Destroy()
	
	def onExitProgram(self, event):
		dlg = wx.MessageDialog(self,"Do you really want to close this application?","Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
		result = dlg.ShowModal()
		dlg.Destroy()
		if result == wx.ID_OK:
			self.Destroy()

global outputdata
global headers
headers=["","","","","","",""]
outputdata=numpy.zeros((0,0))


class PanelTwo(wx.Panel):
	""""""
	
	
	def __init__(self, parent):

		"""Constructor"""
		wx.Panel.__init__(self, parent=parent)
		global outputdata
		global headers
		datafile=outputdata
		self.myGrid = wx.grid.Grid(self)
		self.myGrid.CreateGrid(datafile.shape[0], datafile.shape[1])
		for x in range(len(headers)):
			self.myGrid.SetColLabelValue(x, str(headers[x]))
		for i in range(0,datafile.shape[0]):
			for j in range(0,datafile.shape[1]):
				self.myGrid.SetCellValue(i,j, str(datafile[i,j]))
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.myGrid, 1, wx.EXPAND)
		self.SetSizer(sizer)	
	
	
########################################################################
class PanelOne(wx.Panel):
	#----------------------------------------------------------------------
	def __init__(self, parent):
		global filename
		global filename2
		global outputname
		"""Constructor"""
		wx.Panel.__init__(self, parent=parent)

	
		filename =""
		filename2 =""
		outputname =""
		
		self.label_1 = wx.StaticText(self, -1, "Please Enter the Following Information:",(20, 20))
		self.label_1 = wx.StaticText(self, -1, "Dictionary File(s):",(50, 55))
		self.text_ctrl_filename = wx.TextCtrl(self, -1, filename,(140, 50),(200, 20) )
		wx.Button(self, 2, 'Select Dictionaries', (350, 48), (110, -1))
		
		self.label_1 = wx.StaticText(self, -1, "Dictionary Type:",(50, 90))
		List2 = ['Plain Text (.txt)', 'LIWC (.dic)']
 		self.type = wx.Choice(self, -1, (140, 88),(155, 20), choices=List2)
		self.type.SetSelection(0)
				 
		self.label_1 = wx.StaticText(self, -1, "Analysis Options:",(50, 122))
		self.label_1 = wx.StaticText(self, -1, "Case-sensitive:",(140, 132))
		self.case= wx.CheckBox(self, -1, '', (230, 134))
		self.label_1 = wx.StaticText(self, -1, "Filter Negations:",(275, 132))
		self.filter= wx.CheckBox(self, -1, '', (360, 134))	
		
		self.label_1 = wx.StaticText(self, -1, "Remove Adverbs:",(140, 155))
		self.remove_adverbs= wx.CheckBox(self, -1, '', (230, 154))		
		self.label_1 = wx.StaticText(self, -1, "Binary Coding:",(275, 155))
		self.dichotomize= wx.CheckBox(self, -1, '', (360, 154))	
		
		self.label_2 = wx.StaticText(self, -1, "Document(s):",(50, 195))
		self.text_ctrl_filename2 = wx.TextCtrl(self, -1, filename2,(140, 193),(200, 20) )
		wx.Button(self, 4, 'Select File(s)', (350, 193), (110, -1))

		self.label_1 = wx.StaticText(self, -1, "Output file name:",(50, 230 ))
		self.text_ctrl_output = wx.TextCtrl(self, -1, "",(140, 228),(200, 20) )	
		wx.Button(self, 3, 'Create Output File', (350, 228), (110, -1))
		
		
		wx.Button(self, 1, 'Analyze', (200, 270),(110, -1))
		#self.label_3 = wx.StaticText(self, -1, "\xa9 Hernandez, Newman, Jeon 2014",(360, 240))

		
		self.Bind(wx.EVT_BUTTON, self.Start, id=1)
		self.Bind(wx.EVT_BUTTON, self.Files, id=2)
		self.Bind(wx.EVT_BUTTON, self.destfile, id=3)
		self.Bind(wx.EVT_BUTTON, self.Files2, id=4)


		

###What happends when you press the Analyze button      
	def Start(self, event):
		global filename
		global filename2
		global outputname
		global main_self
		global outputdata
		global headers
		case=self.case.GetValue()
		filter=self.filter.GetValue()
		dichotomize=self.dichotomize.GetValue()
		remove_adverbs=self.remove_adverbs.GetValue()
		dic_type=self.type.GetSelection()
		if dic_type==0:name_list,dics=get_dics(filename,case)
		else:name_list,dics=get_LIWC_dics(filename,case)
		headers=["filename","linenumber","words"]+name_list
		wx.MessageBox('The program will now begin analyzing the text\n \n Please be patitent while the program is running', 'Status')
		if outputname!="":outputdata = analyze_lines(filename2,outputname,name_list,dics,filter,dichotomize,remove_adverbs)
		else:outputdata = analyze_lines2(filename2,outputname,name_list,dics,filter,dichotomize,remove_adverbs)
		#wx.MessageBox('The analysis is finished', 'Status')
		main_self.results()
		return 
####What happens when you press the Test Mode button	

	def display_results(self):
		global main_self
		main_self.panel_one.Hide()
		main_self.panel_two = PanelTwo(self)
		main_self.sizer.Add(main_self.panel_two, 1, wx.EXPAND)
		main_self.SetSizer(main_self.sizer)
		main_self.Layout()


	def destfile(self, event):
			global outputname
			outputname = folderdialog(self)
			self.text_ctrl_output.SetValue(str(outputname))

	def Files(self, event):
		global filename
		filename = filedialog(self)
		self.text_ctrl_filename.SetValue(",".join(filename))
		self.filename=filename
	
	def Files2(self, event):
		global filename2
		filename2 = filedialog(self)
		self.text_ctrl_filename2.SetValue(",".join(filename2))
		self.filename2=filename2
		



		
# Run the program
if __name__ == "__main__":
	app = wx.App(False)

	frame = MyForm()
	frame.Show()
	app.MainLoop()