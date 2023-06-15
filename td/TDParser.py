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

def parse_pdf(file):
    items =[]
    pdf = pp.open(file)
    for page in pdf.pages:
        epage = page.extract_text()
        text = epage.split("\n")
        items = items + (line_items(text))
    return items
            
    
def td_parse():
    list_items = []
    files = file_opener()
    for file in files:
        list_items =  list_items + (parse_pdf(file))
    
    return list_items

def line_items(file):
    line_re =  re.compile(r'[\d|\D|\s]+\s[\d]+\,*\d*\.\d+\s*[\D]{3}[\d]{2}')  

    Line = namedtuple('Line', "DESCRIPTION AMT DATE")
    year = ""
    def lines_extract(file):
        res = []
        for f in file:
            if line_re.search(f) is not None:
                descrip = desc(f)
                rest = amt_date(f).split()
                if len(rest) == 2:
                    res.append(Line(descrip,rest[0],date_parse(rest[1]))) 
                else:
                    text = rest[0]
                    amt = split_amt(text)
                    date =  split_date(text)
                    res.append(Line(descrip,"-"+amt,date_parse(date)))


        return res

    def desc(line):
        match = re.search(r'.+?(?=[\d]+\,*\d*\.\d+)', line)
        if match != None:
                description = match.group(0)
        return description
    def amt_date(line):
        match = re.search(r'[\d]+\,*\d*\.\d+\s*\S{5}', line)
        if match != None:
            text = match.group(0)
            return text

    def split_amt(line):
        match = re.search(r'[\d]+\,*\d*\.\d+', line)
        if match != None:
            text = match.group(0)
            return text

    def split_date(line):
        match = re.search(r'[\D]{3}[\d]{2}', line)
        if match != None:
            text = match.group(0)
            return text

    def date_parse(d):
        date_re = re.compile(r'(\D{3})(\d{2})')
        date_split = date_re.search(d)
        dateDict = {'OCT': "10/",
                    'NOV': "11/",
                    'DEC': "12/",
                    'JAN': "01/",
                    'FEB': "02/",
                    'MAR': "03/",
                    'APR': "04/",
                    'MAY': "05/",
                    'JUN': "06/",
                    'JUL': "07/",
                    'AUG': "08/",
                    'SEP': "09/",}
        


        return date_split.group(1)+" "+date_split.group(2)
    
    return lines_extract(file)

def mainTD():
    frame = pd.DataFrame(td_parse())
    root = tkinter.Tk()
    root.withdraw()
    root.update
    csvName = asksaveasfilename(initialdir = f"./",title = "Name of the CSV to be saved",filetypes = (("csv","*.csv"),("all files","*.*")))
    frame.to_csv(csvName+".csv", index=False)
    root.destroy()

