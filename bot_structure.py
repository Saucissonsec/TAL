import re
import sys
import argparse
class Bot:
    
    def __init__(self):
            self.nom = "Vlad"
            self.memoire = []
            
    def repondre(self, texte):
        reponse = Element_Texte(texte)
        self.memoire.append(reponse)
        return reponse
        
        
class Element_Texte:
    
    def __init__(self, texte):
        self.texte = normalise(texte, "fr")
        self.mot = tokenise_en(self.texte)
        self.wichtig = []
        self.place = 0
        #Element_Texte.place +=1
        
    def initDecision(self):
        
        return 0

class Lemme :
    
    def __init__(self):
        self.mot = LemmeMot()
        
    def read_lemme(self):
        pattern = re.compile(".*(;)")
        #TODO : lit le lemme, associe pour chaque mot ou groupe de mots important les mots qui lui sont associés
        
class LemmeMot :
    
    def __init__(self):
        self.baseWords = list()
        self.associate = list()
        
        
####################################################################


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
    sent = re.sub(",|\.|\!|\?|-|\'|;",r" ", sent)
    sent = sent.split() # split on whitespace
    return sent
       
def main(args):
    return 0

if __name__ == '__main__':
    
    argparser = argparse.ArgumentParser()
    argparser.add_argument('text')
    args = argparser.parse_args()
    
    bot = Bot()
    print(bot.repondre(args.text).mot)
    
    sys.exit(main(sys.argv))