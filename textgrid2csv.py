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


def square_brackets(string_to_process):
    dp = []
    flag = False
    processed_string = ""
    for char in string_to_process:
        if char == "[":
            flag = True
        if char == "]" and flag:
            flag = False
            dp.append(processed_string)
            processed_string = ""
        if flag and char != "[":
            processed_string = processed_string + char
    return dp

def exclamation(string_to_process):
    ij = []
    str_beg = False
    processed_string = ""
    for char in string_to_process:
        if char == "!":
            if not processed_string:
                str_beg = True
            else:
                str_beg = False
                ij.append(processed_string)
                processed_string = ""

        if str_beg and char != "!":
            processed_string = processed_string + char
    return ij

def round_brackets(string_to_process):
    phenomena = ["ppb", "ppc", "ppl", "ppo"]
    fls = []
    flag = False
    processed_string = ""
    for char in string_to_process:
        if char == "(":
            flag = True
        if char == ")" and flag:
            flag = False
            if processed_string not in phenomena:
                fls.append(processed_string)
            processed_string = ""
        if flag and char != "(":
            processed_string = processed_string + char
    return fls

def hashes(string_to_process):
    fl = []
    str_beg = False
    processed_string = ""
    for char in string_to_process:
        if char == "#":
            if not processed_string:
                str_beg = True
            else:
                str_beg = False
                fl.append(processed_string)
                processed_string = ""

        if str_beg and char != "#":
            processed_string = processed_string + char
    return fl

def text_processing(df):
    discourse_particles = []
    fillers = []
    interjections = []
    foreign_language = []
    unclear_words = []
    short_pauses = []
    invalid = []
    non_english_utterances = []
    contains_fil = []
    paralinguistic_phenomena = []
    unknown_words = []
    background_sound = []
    for i in df['3']:
        if "[" in i:
            dp = square_brackets(i)
            if dp:
                discourse_particles.append(dp)
            else:
                discourse_particles.append(0)
        else:
            discourse_particles.append(0)
        if "!" in i:
            ij = exclamation(i)
            if ij:
                interjections.append(ij)
            else:
                interjections.append(0)
        else:
            interjections.append(0)
        if "(" in i:
            fls = round_brackets(i)
            if fls:
                fillers.append(fls)
            else:
                fillers.append(0)
        else:
            fillers.append(0)
        if "#" in i:
            fl = hashes(i)
            if fl:
                foreign_language.append(fl)
            else:
                foreign_language.append(0)
        else:
            foreign_language.append(0)
        if "<UNK>" in i:
            unclear_words.append(1)
        else:
            unclear_words.append(0)
        if "<S>" in i:
            short_pauses.append(1)
        else:
            short_pauses.append(0)
        if "<Z>" in i:
            invalid.append(1)
        else:
            invalid.append(0)
        if "<NEN>" in i:
            non_english_utterances.append(1)
        else:
            non_english_utterances.append(0)
        if "<FIL/>" in i:
            contains_fil.append(1)
        else:
            contains_fil.append(0)
        if "<SPK/>" in i:
            paralinguistic_phenomena.append(1)
        else:
            paralinguistic_phenomena.append(0)
        if "**" in i:
            unknown_words.append(1)
        else:
            unknown_words.append(0)
        if "<NON/>" in i:
            background_sound.append(1)
        else:
            background_sound.append(0)
        if "<NON/>" in i:
            background_sound.append(1)
        else:
            background_sound.append(0)

    df['discourse_particles'] = discourse_particles
    df['fillers'] = fillers
    df['interjections'] = interjections
    df['foreign_language'] = foreign_language
    df['unclear_words'] = unclear_words
    df['short_pauses'] = short_pauses
    df['invalid'] = invalid
    df['non_english_utterances'] = non_english_utterances
    df['contains_fil'] = contains_fil
    df['paralinguistic_phenomena'] = paralinguistic_phenomena
    df['unknown_words'] = unknown_words

    return df

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
    df = text_processing(df)
    df.to_csv(csvname)

print("Done.")
