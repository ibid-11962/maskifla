import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import ast

class Form:
	def __init__(self,properties=[],callback=None,submit=None,title="",icon=None,forceValidate=True):
		self.properties = properties
		self.values = {}
		self.callback=callback
		self.title=title
		self.icon=icon
		self.errstring=None
		self.submit=submit
		self.forceValidate=forceValidate
		
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
		if self.forceValidate:
			if self.submit:
				self.root.children["buttons"].children["submit"]["state"]=("disabled" if errstring else "normal")
			self.root.children["buttons"].children["save"]["state"]=("disabled" if errstring else "normal")

	def clrError(self):
		self.printError("")

	def __printDescription(self,name):
		for x in self.properties:
			if x["name"] == name:
				self.root.children["description"]["text"]=x["description"]
				break

	def __clrDescription(self,name):
		self.root.children["description"]["text"]=""
		
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
		frame = ttk.Frame(self.root,name="buttons")
		frame.pack()
		quit = ttk.Button(frame, text="QUIT", command=self.root.destroy)
		quit.pack(side="left")
		if self.submit:
			submit = ttk.Button(frame, name="submit", text="SUBMIT", command=lambda : self.submit(self.getvalues()))
			submit.pack(side="left")
		save = ttk.Button(frame, name="save", text="SAVE", command=self.__saveFile)
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
					label.grid(padx=5, sticky="we")
			else: #no groups, add directly to parent
				label=frame

			row = len(label.children) #next open row
			name = property.setdefault("name",str(row)) #property names default to row numbers if left out. Not sure this'll actually help anyone.
			type = property.setdefault("type","textbox")
			options = property.setdefault("options",[])
			default = property.get("default")

			#name label
			l=ttk.Label(label,text=name)
			l.grid(row=row, padx=5, pady=3, sticky="we")
			#label mouseover
			if property.get("description"):
				l.bind("<Enter>",lambda event : self.__printDescription(event.widget.cget("text")))
				l.bind("<Leave>",self.__clrDescription)
			#variable
			sv=self.values[name]=tk.StringVar(name=name)
			if default:
				sv.set(default)
			sv.trace_add("write",lambda name,i,m : self.callback(name,self.getvalue(name),"trace"))
			#input field
			if type == "textbox":
				e=ttk.Entry(label, name=name ,textvariable=sv)
				e.grid(row=row, column=1, padx=5, pady=3, sticky="we")
				e.bind("<FocusOut>",lambda event : self.callback(event.widget.winfo_name(),self.getvalue(event.widget.winfo_name()),"focusout"))
			elif type == "outputbox":
				e=ttk.Entry(label, name=name ,textvariable=sv)
				e.configure(state='readonly')
				e.grid(row=row, column=1, padx=5, pady=3, sticky="we")
			elif type == "checkbox":
				e=ttk.Checkbutton(label, name=name, variable=sv)
				e.grid(row=row, column=1, padx=5, pady=3, sticky="w")
			elif type == "dropdown":
				e=ttk.Combobox(label, name=name, textvariable=sv)
				e['values'] = options
				e.configure(state='readonly') #remove this line to also allow custom input
				e.grid(row=row, column=1, padx=5, pady=3, sticky="we")
			elif type == "radio":
				for i, option in enumerate(options):
					f=ttk.Frame(label)	#seperate parent frames so we can still give each button the same name
					f.grid(row=row+i, column=1, padx=5, pady=3, sticky="w")
					e=ttk.Radiobutton(f, text=option, variable=sv, value=option, name=name)
					e.grid()
					if property.get("description"):
						e.bind("<Enter>",lambda event : self.__printDescription(event.widget.winfo_name()))
						e.bind("<Leave>",self.__clrDescription)
			#input mouseover
			if property.get("description"):
				e.bind("<Enter>",lambda event : self.__printDescription(event.widget.winfo_name()))
				e.bind("<Leave>",self.__clrDescription)

		self.root.mainloop()