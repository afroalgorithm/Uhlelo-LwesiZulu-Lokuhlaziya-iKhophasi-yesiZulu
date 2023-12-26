from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from nltk import FreqDist
from nltk import Text as nltk_text
from nltk.tokenize import RegexpTokenizer

root = Tk()
tokenizer = RegexpTokenizer(r'\w+')
study_corpus_file = None
reference_corpus_file = None
top_1 = None
top_2 = None

def calcWordList(event=None):
    global top_1
    file = askopenfilename(filetypes=[('Plain Text Files', '*.txt')])
    if file:
        with open(file, 'r', encoding='utf-8') as f:
            text_list = tokenizer.tokenize(f.read())
            freqDist = FreqDist(text_list)
            freqDist = dict(sorted(freqDist.items(), key=lambda item: item[1], reverse=True))
            text_box.delete(1.0, "end")
            text_box.insert(1.0, 'Word\t\t\t\t\tFrequency\n')
            counter = 2.0
            for key, value in freqDist.items():
                text_box.insert(counter, "{}\t\t\t\t\t{}\n".format(key, value))
                counter += 1
        if top_1:
            top_1.destroy()

def calcConcord(event=None):
    global top_2
    file = askopenfilename(filetypes=[('Plain Text Files', '*.txt')])
    if file:
        with open(file, 'r', encoding='utf-8') as f:
            text = nltk_text(tokenizer.tokenize(f.read()))
            top_2 = Toplevel(root)
            top_2.title("Concordance")
            top_2.geometry("600x400")

            entry_label = Label(top_2, text="Enter word:")
            entry_label.pack()

            entry_1 = Entry(top_2)
            entry_1.pack()

            concord_button = Button(top_2, text='Imvumelwanomagama', command=lambda: calcConcordance(entry_1.get(), text))
            concord_button.pack(pady=10)

def calcConcordance(word, text):
    concordance_list = text.concordance_list(word)
    text_box.delete(1.0, "end")
    counter = 1.0
    if concordance_list:
        for concordance in concordance_list:
            text_box.insert(counter, concordance.line + "\n")
            counter += 1
    else:
        text_box.insert(counter, "No matches found for the word: {}".format(word))

def chooseStudyCorpus():
    global study_corpus_file
    study_corpus_file = askopenfilename(filetypes=[('Plain Text Files', '*.txt')])
    if study_corpus_file:
        showinfo("Information", "Study Corpus file selected: {}".format(study_corpus_file))

def chooseReferenceCorpus():
    global reference_corpus_file
    reference_corpus_file = askopenfilename(filetypes=[('Plain Text Files', '*.txt')])
    if reference_corpus_file:
        showinfo("Information", "Reference Corpus file selected: {}".format(reference_corpus_file))

def calcKeyness():
    global study_corpus_file, reference_corpus_file
    if study_corpus_file and reference_corpus_file:
        top_3 = Toplevel(root)
        top_3.title("Keyness")
        top_3.geometry("400x200")

        study_corpus_button = Button(top_3, text='Khetha ikhophasi ehlolwayo', command=chooseStudyCorpus)
        study_corpus_button.pack(pady=10)

        reference_corpus_button = Button(top_3, text='Khetha ikhophasi eyisendlalelo', command=chooseReferenceCorpus)
        reference_corpus_button.pack(pady=10)

        calculate_button = Button(top_3, text='Bala ubungqikithimagama', command=calcKeynessFiles)
        calculate_button.pack(pady=10)
    else:
        showinfo("Error", "Please select both the study corpus and reference corpus files.")

def calcKeynessFiles():
    global study_corpus_file, reference_corpus_file, top_3
    if study_corpus_file and reference_corpus_file:
        try:
            tokenizer = RegexpTokenizer(r'\w+')
            with open(study_corpus_file, 'r', encoding='utf-8') as f_study, open(reference_corpus_file, 'r', encoding='utf-8') as f_reference:
                study_tokens = tokenizer.tokenize(f_study.read())
                reference_tokens = tokenizer.tokenize(f_reference.read())

                study_freq = FreqDist(study_tokens)

                similarity_index = {}
                for token in study_freq:
                    if token in reference_tokens:
                        similarity_index[token] = study_freq[token]
                    else:
                        similarity_index[token] = "Not Found"
                text_box.delete(1.0, "end")
                for token, count in similarity_index.items():
                    text_box.insert("end", "Token: {}\t Count: {}\n".format(token, count))
        except Exception as e:
            showinfo("Error", "An error occurred: {}".format(str(e)))
        finally:
            if top_3:
                top_3.destroy()
    else:
        showinfo("Error", "Please select both the study corpus and reference corpus files.")

root.geometry("1200x800")
root.configure(bg='orange')
root.title('Mthuli Buthelezi')

title = Label(root, bg='orange', fg='#fff',
              text='Uhlelo LwesiZulu lokuHlaziya iKhophasi yesiZulu',
              font=("Helvetica", 12), pady=30)
title.grid(row=0, columnspan=3)

wordlist_button = Button(root, text='UHLUMAGAMA', command=calcWordList)
wordlist_button.grid(row=1, column=0, pady=20)

concord_button = Button(root, text='IMVUMELWANOMAGAMA', command=calcConcord)
concord_button.grid(row=1, column=1, pady=20)

keyness_button = Button(root, text='UBUNGQIKITHIMAGAMA', command=calcKeyness)
keyness_button.grid(row=1, column=2, pady=20)

token_count_button = Button(root, text='BALA AMAGAMA')
token_count_button.grid(row=2, column=0, columnspan=3)

text_box = Text(root, height=20, width=150)
text_box.grid(row=3, column=0, columnspan=3)

root.mainloop()

