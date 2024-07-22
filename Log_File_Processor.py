import os
import configparser
import pyperclip
import tkinter as tk
import tkinter.filedialog as filedialog
from PIL import Image, ImageTk

#**********************************
#*****FUNCTIONS********************
#**********************************

#if a configuration file exists, load last file name from it
#if config file doesn't exist, hide file info until a file is selected
def load_config():
    #bring in global variable
    global semicolon_file
    
    if os.path.exists('config.ini'):
        config.read('config.ini')
        semicolon_file = config.get('main','filename')
        print("semicolon file loaded: " + str(semicolon_file))
        file_label.configure(text=str(semicolon_file))
    else:
        file_label.grid_forget()
        copy_frame.grid_forget()

#allows user to pick a file to process, updates config file and gui with file name
def select_file():

    #specify file types
    ftypes = [
        ('Text files', '*.txt'), 
        ('All files', '*'), 
    ]

    #bring in global variable for tab delim data
    global semicolon_file

    #open file picker dialog and store to a variable
    new_file = filedialog.askopenfilename(filetypes=ftypes)
    
    #if new_file == "" then the user has cancelled the file dialog
    if(new_file != ""):
        semicolon_file = new_file
    semicolon_file_name = str(semicolon_file)
    print(semicolon_file_name + " selected")

    #if config file doesn't exist create one and store last file name
    if not os.path.exists('config.ini'):
        #config['main'] = {'filename':semicolon_file}
        config.add_section('main')
        config.set('main','filename',semicolon_file)
        config.write(open('config.ini','w'))
    #if it exists already, just update the file name
    else:
        config.set('main','filename',semicolon_file)
        config.write(open('config.ini','w'))

    #display file name in gui
    #semicolon_file_name = os.path.split(semicolon_file)[1]
    file_label.configure(text=semicolon_file_name)
    file_label.grid(row = 1, column=0, sticky="nsew") #open_frame grid
    copy_frame.grid(row=3, column = 0, sticky="nsew", padx=20, pady=(0,50)) #root grid

#opens file, reads each line and replaces semicolons with tabs
#searches for the header row starting with "Delta Time" and then begins copying lines
#this can be pasted into excel directly wihout import wizard
def copy_file(is_vit = False):

    #bring in global variable for tab delim data
    global semicolon_file

    #modify file name if vit is to be copied instead of regular data file
    if(is_vit):
        index = semicolon_file.find('.txt')
        file_to_copy = semicolon_file[:index]+'VIT.txt'
    else:
        file_to_copy = semicolon_file
    print("copying: " + file_to_copy)

    tab_delimited_data = r""

    #open each line in the importted file, replace semicolons with tabs, store in tab delim variable
    with open(file_to_copy, "r") as in_file:
        reached_first_line = False
        for i, line in enumerate(in_file):
            if line[:10] == "Delta Time":
                reached_first_line = True
            if reached_first_line:
                tab_delimited_data += line.replace(';','\t')

    #copy to clipboard
    pyperclip.copy(tab_delimited_data)
    print("Tab delimited data is copied to clipboard")

#**********
#*Global Variables

semicolon_file = r""
config = configparser.ConfigParser()


#**********************************
#*****CREATE GUI ELEMENTS**********
#**********************************

#setup some style variables
style_bg_color="black"
#style_button_bg_color="#808080"
style_font_color="white"
style_font="Arial"
style_heading_font_size=20
style_heading_bg_color = "#1a1a1a"
style_label_frame_font_size=20
style_button_font_size=15
style_normal_font_size=15

#************
#create a window called root
root = tk.Tk()
try:
    root.iconbitmap(r'favicon.ico')
except:
    print("icon file not found")
#root.iconbitmap(r'X:\ENGR ADMIN\Python Projects\BriarTek STB100 Log File Processor\v2_2019-07-24\favicon.ico')
#root.minsize(200,200)
root.geometry('+%d+%d'%(1100,0))
root.title("BriarTek STB100 Log File Copier")
root.configure(bg=style_bg_color)
root.columnconfigure(0,weight=1) #first column of body grid, makes it fill window
root.tk.call('tk','scaling',1.0) #scales widget size down, default is 2.0

#************
#create top header image

header_image = tk.Label(root,
                        text="BriarTek",
                        bg=style_bg_color,
                        fg=style_font_color,
                        font = ("Arial",30))
header_image.grid(row=0, column=0, sticky="ew", padx=20, pady=20) # root grid

try:
    img = Image.open("logo.png")
except:
    print("image not found")
else:
    img_h = 70 #new height
    img_w = int(img_h*(float(img.size[0])/float(img.size[1]))) #proportionate width
    img = img.resize((img_w,img_h), Image.ANTIALIAS)
    tkimage = ImageTk.PhotoImage(img)
    header_image.configure(image=tkimage,
                           text="",
                           height=img_h,
                           width=img_w)
#************
#create top header text

header_text = tk.Label(root,
                  text="STB100 Log File Copier",
                  bg=style_bg_color,
                  fg=style_font_color,
                  font = ("Arial",style_heading_font_size))
header_text.grid(row=1, column=0, sticky="ew", padx=20, pady=(0,20)) # root grid


#************
#create label frame for open file button
open_frame = tk.LabelFrame(root,
                      text="Select Log File",
                      bg=style_bg_color,
                      fg=style_font_color,
                      font = (style_font, style_label_frame_font_size),
                      padx=20,
                      pady=20)
open_frame.grid(row=2, column = 0, sticky="nsew", padx=20, pady=(0,20)) #root grid
open_frame.columnconfigure(0,weight=1)

#create open button within the open frame
open_button = tk.Button(open_frame,
                         text = "Open STB100 Log File",
                         font = (style_font, style_normal_font_size),
                         width = 15,
                         command = select_file)
open_button.grid(row = 0, column=0, pady = (0,20), sticky="new") #open_frame grid

#create file name label within the open frame
file_label = tk.Label(open_frame,
                      text = "",
                      bg=style_bg_color,
                      fg=style_font_color,
                      font = (style_font, style_button_font_size),
                      wraplength = 300,
                      justify = "left")
file_label.grid(row = 1, column=0, sticky="nsew") #open_frame grid
#file_label.grid_forget()
file_label.grid(row = 1, column=0, sticky="nsew") #open_frame grid

#create label frame for copy data button
copy_frame = tk.LabelFrame(root,
                      text="Copy Data in Excel Format",
                      bg=style_bg_color,
                      fg=style_font_color,
                      font = (style_font, style_label_frame_font_size),
                      padx=20,
                      pady=20)
copy_frame.columnconfigure(0,weight=1)
#copy_frame.grid_forget()
copy_frame.grid(row=3, column = 0, sticky="nsew", padx=20, pady=(0,50)) #root grid

#create copy_burst_data_button within the copy frame
copy_burst_data_button = tk.Button(copy_frame,
                         text = "Copy Burst Data to Clipboard",
                         font = (style_font, style_button_font_size),
                         width = 15,
                         command = lambda: copy_file(False))
copy_burst_data_button.grid(row = 0, column=0, padx = (0,20), pady = (0,20), sticky="new") #copy_frame grid

#create copy_vit_data_button within the copy frame
copy_vit_data_button = tk.Button(copy_frame,
                         text = "Copy VIT Data to Clipboard",
                         font = (style_font, style_button_font_size),
                         width = 15,
                         command = lambda: copy_file(True))
copy_vit_data_button.grid(row = 1, column=0, padx = (0,20), sticky="new") #copy_frame grid

#load config file
load_config()

#runs the tkinter gui
root.mainloop()
