import PyPDF2 as ppdf
import pdfplumber as pp
import re
import pandas as pd
from collections import namedtuple
import tkinter
from tkinter.filedialog import askopenfilenames            
from tkinter.filedialog import asksaveasfilename
from pathlib import Path

def file_opener():  #opens a prompt via tinker to find the file you wish to read (csv reader)

    home = str(Path.home())

    root = tkinter.Tk()
    root.withdraw()
    root.update

    filename = askopenfilenames(initialdir = f"./",title = "Select File To Be Imported",filetypes = (("pdf","*.pdf"),("all files","*.*")))
    root.destroy()

    return (filename)

def pdf_maker(file):
    lines = []
    line_re = re.compile(r'\D{3}\d{2} \D{3}\d{2}')
    Line = namedtuple('Line', 'trans_date posting_date desc amt')
    pdf = pp.open(file)
    for page in pdf.pages:
        text =  page.extract_text()
        for line in text.split('\n'):
            if line_re.search(line):
                items = line.split()
                items[0] = date_parse(items[0])
                items[1] = date_parse(items[1])
                items[3] = float(remove_dollar(items[3]))
                lines.append(Line(*items))
    return lines



def date_parse(d):
    date_re = re.compile(r'(\D{3})(\d{2})')
    date_split = date_re.search(d)    
    return date_split.group(1) + " " + date_split.group(2)

def remove_dollar(s):
    s = s.replace("$", "")
    s = s.replace(",", "")
    return s.replace("$", "")

def rbc_parser():
    list_items = []
    files = file_opener()
    for file in files:
        list_items =  list_items + (pdf_maker(file))
    
    return list_items

def mainRBC(): 
    df = pd.DataFrame(rbc_parser())
    csvName = asksaveasfilename(initialdir = f"./",title = "Name of the CSV to be saved",filetypes = (("csv","*.csv"),("all files","*.*")))
    df.to_csv(csvName+".csv", index=False)


