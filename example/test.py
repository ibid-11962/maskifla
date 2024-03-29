from maskifla import Form
properties = [
{	"name":"num_words",
	"type":"textbox",
	"default":"2",
	"category":"Configuration options",
	"subcategory":"Size parameters",
	"description": "Number of words",					},
{	"name":"word_size",
	"type":"textbox",
	"default":"16",
	"category":"Configuration options",
	"subcategory":"Size parameters",
	"description": "Size of word, must be even",		},
{	"name":"num_rw_ports",
	"type":"dropdown",
	"options":["0","1","2","4","8"],
	"default":"1",
	"category":"Configuration options",
	"subcategory":"Port configuration",	
	"description": "Number of ReadWrite ports",			},
{	"name":"num_r_ports",
	"type":"dropdown",
	"options":["0","1","2","4","8"],
	"default":"0",
	"category":"Configuration options",
	"subcategory":"Port configuration",	
	"description": "Number of Read ports",				},
{	"name":"num_w_ports",
	"type":"dropdown",
	"options":["0","1","2","4","8"],
	"default":"0",
	"category":"Configuration options",
	"subcategory":"Port configuration",	
	"description": "Number of Write ports",				},
{	"name":"delete_temp_files",
	"type":"checkbox",
	"default":"1",
	"category":"Configuration options",
	"description": "Delete temporary files on exit",	},
{	"name":"memory_type",
	"type":"radio",
	"options":["SRAM","DRAM","GC-eDRAM"],
	"default":"SRAM",
	"category":"Configuration options",
	"description": "Number of words",					},
{	"name":"total_ports",
	"default":"1",
	"type":"outputbox",
	"category":"Configuration options",
	"subcategory":"Port configuration",	
	"description": "Calculated total number of ports",	},
{	"name":"input_path",
	"type":"textbox",
	"default":"C:\Input",
	"category":"File paths",
	"subcategory":"Input/Output"						},
{	"name":"output_path",
	"type":"textbox",
	"default":"C:\Output",
	"category":"File paths",
	"subcategory":"Input/Output"						},
]

def callback(name,value,trigger):
	if trigger=="trace":
		return
	try:
		if int(f.getvalue("word_size"))%2:
			f.printError("ERROR: word_size must be even. Please fix.")
		else:
			f.printError("")
		f.setvalue("total_ports",int(f.getvalue("num_rw_ports"))+int(f.getvalue("num_r_ports"))+int(f.getvalue("num_w_ports")))
	except: #things that will throw errors when casting to int
		f.printError("ERROR: invalid input")

def submit(values):
	print(values)

f = Form(properties=properties, defaults={"word_size":32,"num_words":64},callback=callback, submit=submit, title="Compiler configuration", icon="logo.ico")

f.displayForm()

