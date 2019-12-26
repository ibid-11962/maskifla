import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import ast

class Form:
	def __init__(self,properties=[],callback=None,submit=None,title="",icon=None):
		self.properties = properties
		self.values = {}
		self.callback=callback
		self.title=title
		self.icon=icon
		self.errstring=None
		self.submit=submit
		
		self.hasCategories=False
		self.hasSubcategories=False
		for property in properties:
			if "category" in property:
				self.hasCategories=True
			if "subcategory" in property:
				self.hasSubcategories=True

	def __loadFile(self):
		filename = filedialog.askopenfilename()
		try:
			f=open(filename,"r")
			self.setvalues(ast.literal_eval(f.readline()))
			f.close()
		except:
			return

	def __saveFile(self):
		filename = filedialog.asksaveasfilename()
		try:
			f=open(filename,"w")
			f.write(str(self.getvalues()))
			f.close()
		except:
			return

	def printError(self,errstring):
		self.root.children["error"]["text"]=errstring
	
	def clrError(self):
		self.printError("")

	def __printDescription(self,name):
		for x in self.properties:
			if x["name"] == name:
				self.root.children["description"]["text"]=x["description"]
				break

	def __clrDescription(self,name):
		self.root.children["description"]["text"]=""
		
	def __getWidgetName(self, event):
		return str(event.widget).split(".")[-1]

	def getvalues(self):
		return dict((x, y.get()) for x, y in self.values.items())

	def setvalues(self,dict):
		for key,value in dict.items():
			self.values[key].set(value)

	def getvalue(self,parameter):
		return self.values[parameter].get()

	def setvalue(self,parameter,value):
		self.values[parameter].set(value)
		
	def displayForm(self):
		#parent window
		self.root = tk.Tk()
		self.root.wm_title(self.title)
		self.root.iconbitmap(self.icon)
		#tabs
		if self.hasCategories:
			n = ttk.Notebook(self.root, name="n")
		else:
			n = ttk.Frame(self.root)
		n.pack()
		#text outputs 
		style = ttk.Style()
		style.configure("Err.TLabel", foreground="red")
		ttk.Label(self.root,name="description", text=None).pack()
		ttk.Label(self.root,name="error", style="Err.TLabel", text=None).pack()
		#buttons
		frame = ttk.Frame(self.root)
		frame.pack()
		quit = ttk.Button(frame, text="QUIT", command=self.root.destroy)
		quit.pack(side="left")
		if self.submit:
			submit = ttk.Button(frame, text="SUBMIT", command=lambda : self.submit(self.getvalues()))
			submit.pack(side="left")
		save = ttk.Button(frame, text="SAVE", command=self.__saveFile)
		save.pack(side="left")
		load = ttk.Button(frame, text="LOAD", command=self.__loadFile)
		load.pack(side="left")
		
		#loop through list of properties
		for property in self.properties:
			if self.hasCategories:
				try:
					frame = n.children[property.setdefault("category","misc").lower()]
				except: #tab doesn't exist, create new
					frame = ttk.Frame(n, name=property["category"].lower())
					n.add(frame, text=property["category"])
			else: #no tabs, add directly to parent
				frame=n
			if self.hasSubcategories:
				try:
					label = frame.children[property.setdefault("subcategory","misc").lower()]
				except: #group doesn't exist, create new
					label = ttk.Labelframe(frame, text=property["subcategory"], name=property["subcategory"].lower())
					label.grid()
			else: #no groups, add directly to parent
				label=frame
			row=len(label.children) #next open row
			#name of property
			l=ttk.Label(label,text=property["name"])
			l.grid(row=row, padx=5, pady=3)
			if property.get("description"):
				l.bind("<Enter>",lambda event : self.__printDescription(event.widget.cget("text")))
				l.bind("<Leave>",self.__clrDescription)
			#input field of property
			sv=self.values[property["name"]]=tk.StringVar(name=property["name"])
			e=ttk.Entry(label, name=property["name"] ,textvariable=self.values[property["name"]])
			e.grid(row=row, column=1, padx=5, pady=3)
			if property.get("description"):
				e.bind("<Enter>",lambda event : self.__printDescription(str(event.widget).split(".")[-1]))
				e.bind("<Leave>",self.__clrDescription)
			if property.get("default"):
				sv.set(property["default"])
			if property.setdefault("type","textbox")=="outputbox":
				e.configure(state='readonly')
			sv.trace_add("write",lambda name,i,m : self.callback(name,self.getvalue(name)))
#			switch above to this line to bind to focusout instead of entry change. Remove everything from the callback parentheses to not pass values to callback.
#			e.bind("<FocusOut>",lambda event : self.callback(self.__getWidgetName(event),self.getvalue(self.__getWidgetName(event))))

		self.root.mainloop()