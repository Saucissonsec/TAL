#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import re
import matplotlib.pyplot as plt
import numpy as np

def read_paragraph_file(filename):
    paragraphs = []
    with open(filename, "r") as filepointer:
        for line in filepointer.readlines():
            if line.strip()=="": continue # ignore blank paragraphs
            paragraphs.append(line.strip()) # remove whitespace with strip()
    return paragraphs

def write_paragraph_file(paragraphs, filename):
    with open(filename, "w") as filepointer:
        for paragraph in paragraphs:
            filepointer.write(paragraph+"\n")

def read_word_list_file(filename):
    wordlist = []
    with open(filename, "r") as filepointer:
        for line in filepointer.readlines():
            word = line.strip() # remove whitespace
            if word=="": continue # ignore blank lines
            wordlist.append(word)
    return wordlist

def write_word_list_file(wordlist, filename):
    with open(filename, "w") as filepointer:
        for word in wordlist:
            filepointer.write(word+"\n")    

def read_tab_separated_file(filename):
    rows = []
    with open(filename, "r") as filepointer:
        for line in filepointer.readlines():
            line = line.strip() # strip on whitespace
            if line=="": continue # ignore blank lines
            rows.append(line.split("\t")) # split on tabs
    return rows 

def write_tab_separated_file(rows, filename):
    with open(filename, "w") as filepointer:
        for row in rows:
            filepointer.write("\t".join(row)+"\n") 


def segment_into_sents(paragraph):

    cannot_precede = ["M", "Prof", "Sgt", "Lt", "Ltd", "co", "etc", "[A-Z]", "[Ii].e", "[eE].g"] # non-exhaustive list
    regex_cannot_precede = "(?:(?<!"+")(?<!".join(cannot_precede)+"))"
    
    if "\n" in paragraph: exit("Error in paragraph: paragraph contains \n.")       
    newline_separated = re.sub(regex_cannot_precede+"([\.\!\?]+([\'\’\"\)]*( |$)| [\'\’\"\) ]*))", r"\1\n", paragraph)
    sents = newline_separated.strip().split("\n")
    for s, sent in enumerate(sents):
        sents[s] = sent.strip()
    return sents


def normalise(sent, lang):
    sent = re.sub("\'\'", '"', sent) # two single quotes = double quotes
    sent = re.sub("[`‘’]+", r"'", sent) # normalise apostrophes/single quotes
    sent = re.sub("[≪≫“”]", '"', sent) # normalise double quotes

    if lang=="en":
        sent = re.sub("([a-z]{3,})or", r"\1our", sent) # replace ..or words with ..our words (American versus British)
        sent = re.sub("([a-z]{2,})iz([eai])", r"\1is\2", sent) # replace ize with ise (..ise, ...isation, ..ising)
    if lang=="fr":
        replacements = [("keske", "qu' est -ce que"), ("estke", "est -ce que"), ("bcp", "beaucoup")] # etc.
        for (original, replacement) in replacements:
            sent = re.sub("(^| )"+original+"( |$)", r"\1"+replacement+r"\2", sent)
    return sent
    
def tokenise_en(sent):

    sent = re.sub("([^ ])\'", r"\1 '", sent) # separate apostrophe from preceding word by a space if no space to left
    sent = re.sub(" \'", r" ' ", sent) # separate apostrophe from following word if a space if left

    # separate on punctuation
    cannot_precede = ["M", "Prof", "Sgt", "Lt", "Ltd", "co", "etc", "[A-Z]", "[Ii].e", "[eE].g"] # non-exhaustive list
    regex_cannot_precede = "(?:(?<!"+")(?<!".join(cannot_precede)+"))"
    sent = re.sub(regex_cannot_precede+"([\.\,\;\:\)\(\"\?\!]( |$))", r" \1", sent)
    sent = re.sub("((^| )[\.\?\!]) ([\.\?\!]( |$))", r"\1\2", sent) # then restick several fullstops ... or several ?? or !!
    sent = sent.split() # split on whitespace
    return sent

def tokenise(sent, lang):
    if lang=="en":
        return tokenise_en(sent)
    #elif lang=="fr":
     #   return tokenise_fr(sent)
    else:
        exit("Lang: "+str(lang)+" not recognised for tokenisation.\n")

def test_segments_into_sents():

    # basic case
    assert(segment_into_sents("Time flies like an arrow. Fruit flies like a banana.") == ["Time flies like an arrow.", "Fruit flies like a banana."])
    # don't segment on all full stops
    assert(segment_into_sents("M. Dupont est venu nous voir.") == ["M. Dupont est venu nous voir."])
    assert(segment_into_sents("Aux U.S.A. il pleut.") == ["Aux U.S.A. il pleut."])


def get_tok2count(paras):
    tok2count = {}
    for para in paras:
        for sent in para:
            for tok in sent:
                if tok not in tok2count: tok2count[tok] = 0
                tok2count[tok] += 1

    return tok2count

def get_occ2count(tok2count):
    occ2count = {}
    for tok in tok2count:
        if tok2count[tok] not in occ2count: occ2count[tok2count[tok]] = 0
        occ2count[tok2count[tok]] += 1
    return occ2count

def sort_dict_by_value(dict, decroissant=False):
    return sorted(dict, key=dict.get, reverse=decroissant)

def plot_occ2count(occ2count):

    x = sorted(occ2count.keys())
    # print(x)
    
    for occ in x:
        print(occ)
    y = [ occ2count[occ] for occ in x ]

    print(occ2count.values())
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.hist(list(occ2count.values()), bins=400)
    plt.title("Word occurrence distribution")
    plt.xlabel("Number of occurrences of a wordform in a text")
    plt.ylabel("Number of wordforms with that number of occurrences")
    
    # plt.plot(x, y)
    plt.show()
    
def plot_rank2occ(tok2count):
    samplesize = len(tok2count)
    
    x_labels = sort_dict_by_value(tok2count, True)[:samplesize]
    x = [ i for i in range(len(x_labels)) ]
    y = [ tok2count[tok] for tok in x_labels ]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(x, y)
    locs, labels = plt.xticks(x, x_labels)
    plt.setp(labels, rotation=90)

    plt.tick_params(axis='x', which='major', labelsize=5)
    plt.xlabel("Wordforms sorted by frequency rank", fontsize=30)
    plt.ylabel("Number of wordforms with that number of occurrences", fontsize=30)
    fig.set_size_inches(40, 20, forward=True)
    # fig.savefig('outfile.png', dpi=200)
            
    
if __name__=="__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument('textfilefolder')
    args = argparser.parse_args()

    # file locations
    folder = args.textfilefolder
    wordlist_file = folder+"/welsh_places.en.list"
    wordlist_file_copy = folder+"/welsh_places.en.list.copy"
    para_file = folder+"/alice.en.paras"
    para_file_copy = folder+"/alice.en.paras.copy"
    tab_sep_file = folder+"/personal_pronouns.fr.tsv"
    tab_sep_file_copy = folder+"/personal_pronouns.fr.tsv.copy"
    
    # read (and write) file with paragraphs
    paras = read_paragraph_file(para_file)
    write_paragraph_file(paras, para_file_copy)

    # read (and write) word list (places in Wales)
    list_places = read_word_list_file(wordlist_file)
    write_word_list_file(list_places, wordlist_file_copy)

    # read (and write) pronoun information file
    pronoun_info = read_tab_separated_file(tab_sep_file)
    write_tab_separated_file(pronoun_info, tab_sep_file_copy)

    # test segmentation
    test_segments_into_sents()
    
    # preprocess alice in wonderland
    preprocessed = []
    for p, para in enumerate(paras):
        preprocessed_sents = []
        sents = segment_into_sents(para)
        
        for sent in sents:
            sent = normalise(sent, "en")
            sent = tokenise(sent, "en")

            preprocessed_sents.append(sent)
            
        preprocessed.append(preprocessed_sents)
        
    tok2count = get_tok2count(preprocessed)
    print(tok2count)
    occ2count = get_occ2count(tok2count)
    plot_occ2count(tok2count)


    # statistics
    plot_rank2occ(tok2count)
