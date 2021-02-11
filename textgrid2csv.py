import os, sys, re
import pandas as pd

def inputtextlines(filename):
    handle = open(filename,'r')
    linelist = handle.readlines()
    handle.close()
    return linelist

def converttextgrid2csv(textgridlines,textgridname):

    csvtext = ''
    csv_content = []
    for line in textgridlines[9:]:
        line = re.sub('\n','',line)
        line = re.sub('^ *','',line)
        linepair = line.split(' = ')
        if len(linepair) == 2:
            if linepair[0] == 'class':
                classname = linepair[1]
            if linepair[0] == 'name':
                tiername = linepair[1]
            if linepair[0] == 'xmin':
                xmin = linepair[1]
            if linepair[0] == 'xmax':
                xmax = linepair[1]
            if linepair[0] == 'text':
                text = linepair[1]
                diff = str(float(xmax)-float(xmin))
                csvtext += textgridname + '\t' + classname + '\t' + tiername + '\t' + text + '\t' + xmin + '\t' + xmax + '\t' + diff + '\n'
                csvline = [textgridname, classname, tiername, text, xmin, xmax, diff]
                csv_content.append(csvline)
    return csvtext, csv_content

textgridfiles = sorted(os.listdir('C:/Projects/Python/Work/Scripts Same'))

textgridfiles = [x for x in textgridfiles if x.endswith('.TextGrid')]
if textgridfiles == []:
    print( "No TextGrid files to process.")

for filename in textgridfiles:

# Create TextGrid name and CSV file name.
    tgname = re.sub('.TextGrid','',filename)
    csvname = re.sub('.TextGrid','.csv',filename)

# Convert.
    print(f'Converting {filename} to {csvname}')
    filename = 'C:/Users/Preetam/Scripts Same/' + filename
    textgrid = inputtextlines(filename)
    if textgrid == '':
        print(f'No input from file {filename}')
    csvtext, csv_content = converttextgrid2csv(textgrid,tgname)
    if csvtext == '':
        print(f'No data in file {filename}')

# Create separate CSV output for each TextGrid.
    df = pd.DataFrame(csv_content)
    df.to_csv(csvname)

print("Done.")
