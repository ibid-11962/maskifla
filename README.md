maskifla 
-

Maskifla is a python library to facilitate getting user input for a list of parameters through a simple tk gui. The name maskifla comes from the talmudic phrase מתקיף לה, meaning to ask a question.

Usage
-

As of now maskifla is just one python file with a single class, and can be imported like this:

```
from maskifla import Form
```

To display a form you must first create a list of property dictionaries of the following form. (With the exception of `name`, all the attributes are optional.)   

```
properties = [
{	"name":"num_words",								#name of property
	"type":"textbox",								#type, defaults to textbox
	"default":"2",									#initial default value
	"category":"Configuration options",				#the tab to display it in	
	"subcategory":"Size parameters",				#the group to display it in	
	"description": "Number of words",			},	#the mouseover description
{	"name":"word_size",
	"type":"textbox",
	"default":"16",
	"category":"Configuration options",
	"subcategory":"Size parameters",
	"description": "Size of word, must be even",},
]
```

You can then create and display a Form object

```
f = Form(properties=properties)
f.displayForm()
```

This will allow a user to set all of the values and then save them to a file.

If you wish to handle the values in the program itself you can also define a callback function for the output. This will add a submit button and pass a dictionary of all the values as an argument.

```
def submit(values):
	print(values)

f = Form(properties=properties, submit=submit)
f.displayForm()
```

You can also create a callback function that gets activated whenever one of the inputs is modified. This one will be passed the name of the modified property and its new value (as a string).

```
def callback(name,value):
	try:
		if name == "word_size" and int(value)%2:
			f.printError("ERROR: word_size must be even. Please fix.")
		else:
			f.clrError()
	except: #things that will throw errors when casting to int
		f.printError("ERROR: invalid input")

f = Form(properties=properties, callback=callback, submit=submit)
f.displayForm()
```

`printError(string)` and `clrError()` will modify the error message field on the bottom of the form.

Other available methods are `getvalue(name)`, `setvalue(name,value)`, `getvalues()`, `setvalues(dict)`.

The form constructor can also take strings for `title` and `icon` which would be reflected in the title bar of the form window.


Consider the following example:

```
properties = [
{	"name":"num_words",								
	"type":"textbox",								
	"default":"2",									
	"category":"Configuration options",					
	"subcategory":"Size parameters",					
	"description": "Number of words",				},	
{	"name":"word_size",
	"type":"textbox",
	"default":"16",
	"category":"Configuration options",
	"subcategory":"Size parameters",
	"description": "Size of word, must be even",	},
{	"name":"memory_size",
	"type":"outputbox",					#like a textbox, but not user editable
	"default":"32",
	"category":"Configuration options",
	"subcategory":"Size parameters",
	"description": "Calculated total memory size",	}
]

def submit(values):
	print(values)

def callback(name,value):
	try:
		if int(f.getvalue("word_size"))%2:
			f.printError("ERROR: word_size must be even. Please fix.")
		else:
			f.printError("")
		f.setvalue("memory_size",int(f.getvalue("num_words"))*int(f.getvalue("word_size")))
	except: #things that will throw errors when casting to int
		f.printError("ERROR: invalid input")


f = Form(properties=properties, callback=callback, title="Form", submit=submit, icon="logo.ico")
f.displayForm()
```