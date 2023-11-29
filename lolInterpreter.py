# Authors: 
# an interpreter for LOLCODE using python
# GUI created using CustomTkinter

from tkinter import filedialog
from CTkTable import *
import customtkinter as tk

fileDirectory = ""
lexemesList = []

def chooseFile():
    codeString = ""
    fileDirectory = filedialog.askopenfilename()

    if fileDirectory == "":
        return 0
    
    if fileDirectory.split(".")[1] != "lol":
        fileDirLabel.configure(text="Selected file is not a LOL CODE.")
        return 0

    inputFile = open(fileDirectory, "r")

    
    fileDirLabel.configure(text=fileDirectory.split("/")[-1])

    for line in inputFile:
        codeString+=line
        lexemesList.append(line[:-1].replace("    ", "").split(" "))

    textEditor.insert("0.0", codeString)
    print(lexemesList)

#--- initializing customtkinter ---#
root = tk.CTk()
root.title("LOL Code Interpreter")
# root.iconbitmap("./wine.ico")



#--- Setting up GUI ---#
tk.set_appearance_mode("dark")
tk.set_default_color_theme("dark-blue")

#--- title label ---#
titleLabel = tk.CTkLabel(root, text="LOLCODE INTERPRETER", text_color = "white", font = ("Helvetica", 35))
titleLabel.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 10)

#--- fdivision frames ---#
fileExpFrame = tk.CTkFrame(root, height=300, width=300)
fileExpFrame.grid(row = 1, column = 0, padx = 5, pady = 2)

lexemesFrame = tk.CTkScrollableFrame(root, height=300, width=300)
lexemesFrame.grid(row = 1, column = 1, padx = 5, pady = 2)

symbolTableFrame = tk.CTkFrame(root, height=200, width=300)
symbolTableFrame.grid(row = 1, column = 2, padx = 5, pady = 2)

terminalFrame = tk.CTkFrame(root, height=200, width=940)
terminalFrame.grid(row = 2, column = 0, columnspan = 3, padx = 5, pady = 2)

#--- file explorer ---#
fileDirLabel = tk.CTkLabel(fileExpFrame,text= "No File Selected")
fileDirLabel.grid(row = 0, column = 0, padx=5, pady=2)

selectFileButton = tk.CTkButton(fileExpFrame, text = "SELECT FILE", command=chooseFile)
selectFileButton.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = "e")

textEditor = tk.CTkTextbox(fileExpFrame, width = 280, height=265)
textEditor.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

#--- List of tokens ---#
lexemesLabel = tk.CTkLabel(lexemesFrame,text= "Lexemes")
lexemesLabel.pack(expand=True, fill="both", padx=5)

lexemesTable = CTkTable(lexemesFrame, row = 1, column = 0, values = [["Lexemes", "Classification"]])
lexemesTable.pack(expand=True, fill="both", padx=5, pady=5)

root.mainloop()