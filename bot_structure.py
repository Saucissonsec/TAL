import sqlite3
import re 
import os 
import random
import csv
import sys

def tokenise(sent): # Objectif : une fonction global, permettant de découper la demande au bot en élement primaire pouvant être compris, retourne un tableau
	sent = re.sub("([^ ])\'", r"\1 '", sent) # travail sur les apostrophes
	sent = re.sub(" \'", r" ' ", sent) #Apostrophes
	cannot_precede = ["M", "Prof", "Sgt", "Lt", "Ltd", "co", "etc", "[A-Z]", "[Ii].e", "[eE].g"] # Retrait de terme que l'on considère inutile 
	regex_cannot_precede = "(?:(?<!"+")(?<!".join(cannot_precede)+"))"
	sent = re.sub(regex_cannot_precede+"([\.\,\;\:\)\(\"\?\!]( |$))", r" \1", sent)
	sent = re.sub("((^| )[\.\?\!]) ([\.\?\!]( |$))", r"\1\2", sent) # Evite les doublons de ponctuation
	sent = re.sub(",|\.|\!|\?|-|\'|;",r" ", sent)
	sent = sent.split() # decoupage en element primaire
	return sent

def normalise(sent): #Objectif : eclaisir un texte passer en normalisant son écriture, retourne une string
	sent = re.sub("\'\'", '"', sent) # standardisation des apostrophes
	sent = re.sub("[`‘’]+", r"'", sent) # normalise apostrophes/single quotes
	sent = re.sub("[≪≫“”]", '"', sent) # normalise double quotes
	
	replacements = [("keske", "qu' est -ce que"), ("estke", "est -ce que"), ("bcp", "beaucoup")] # Eviter le langage familier
	for (original, replacement) in replacements:
		sent = re.sub("(^| )"+original+"( |$)", r"\1"+replacement+r"\2", sent)
	return sent


def lemme(sent): #Prend un tableau d'élement primitif et en retourne le tableau de lemme, donnant un sens plus global aux mots
	tab = list()
	for i in sent:
		if(i == "trouver" or i == "trouve" or i == "trouves" or i == "trouvent" or i == "trouvera" or i == "trouveras" or i == "trouverais" or i == "trouvait"):
			tab.append("trouver")
		if(i == "souhaiter" or i == "souhaite" or i == "souhaites" or i == "souhaitent" or i == "souhaitera" or i == "souhaiteras" or i == "souhaiterais" or i == "souhaitait"):
			tab.append("souhaiter")
		elif(i == "chercher" or i == "cherche" or i == "cherches" or i == "cherchent" or i == "cherchera" or i == "chercheras" or i == "chercherais" or i == "cherchait"):
			tab.append("chercher")	
		elif(i == "afficher" or i == "affiche" or i == "affiches" or i == "affichent" or i == "affichera" or i == "afficheras" or i == "afficherais" or i == "affichait"):
			tab.append("afficher")
		elif(i == "lister" or i == "liste" or i == "listes" or i == "listent" or i == "listera" or i == "listeras" or i == "listerais" or i == "listait"):
			tab.append("lister")
		elif(i == "montrer" or i == "montre" or i == "montres" or i == "montrent" or i == "montrera" or i == "montreras" or i == "montrerais" or i == "montrait"):
			tab.append("montrer")
		elif(i == "donner" or i == "donne" or i == "donnes" or i == "donnent" or i == "donnera" or i == "donneras" or i == "donnerais" or i == "donnait"):
			tab.append("donner")
		elif(i == "emmener" or i == "emmene" or i == "emmenes" or i == "emmenent" or i == "emmenera" or i == "emmeneras" or i == "emmenerais" or i == "emmenait"):
			tab.append("emmener")
		elif(i == "aller" or i == "vais" or i == "vas" or i == "va" or i == "vont" or i == "ira" or i == "iras" or i == "irait" or i == "irais"):
			tab.append("aller")
		elif(i == "voulons" or i == "vouloir" or i == "veux" or i == "veut" or i == "veulent" or i == "voudra" or i == "voudras" or i == "voudrais" or i == "voudrait"):
			tab.append("vouloir")
		elif(i == "pouvoir" or i == "peux" or i == "peut" or i == "peuvent" or i == "pourra" or i == "pourras" or i == "pourrais" or i == "pourrait"):
			tab.append("pouvoir")
		elif(i == "alimenter" or i == "manger" or i == "manges" or i == "mange" or i == "mangent" or i == "mangera" or i == "mangeras" or i == "mangerent" or i == "mangerait" or i == "mangerais" or i == "nourrir" or i == "restaurant" or i == "alimentation"):
			tab.append("alimenter")
		elif(i == "regarder" or i == "regarde" or i == "regardes" or i == "regardent" or i == "regardera" or i == "regarderas" or i == "regarderais" or i == "regardait" or i == "voir" or i == "vois" or i == "voit"):
			tab.append("regarder")
		elif(i == "thé"):
			tab.append("thé")
		elif(i == "choucroute"):
			tab.append("choucroute")
		elif(i == "chinois" or i == "asiat" or i == "asiatique"):
			tab.append("restaurant chinois")
		elif(i == "thailandais" or i == "thai" or i == "thaïlandais" or i == "thaï"):
			tab.append("thailandais")
		elif(i == "italien" or i == "pizza" or i == "pates" or i == "pate" or i == "pizzas"):
			tab.append("italien")
		elif(i == "mexicain" or i == "texmex" or i == "tex-mex" or i == "burrito" or i == "chipolte" or i == "tortillas"):
			tab.append("mexicain")
		elif(i == "japonais" or i == "jap" or i == "sushi" or i == "sushis"):
			tab.append("japonais")
		elif(i == "traditionnel" or i == "français"):
			tab.append("traditionnel")
		elif(i == "allemand" or i == "saucisses" or i == "saucisse"):
			tab.append("allemand")
		elif(i == "boulangerie" or i == "patisserie" or i == "pain" or i == "baguette" or i == "gateau" or i == "croissant" or i == "banette"):
			tab.append("boulangerie")
		elif(i == "macdo" or i == "mcdonald's" or i == "mcdo" or i == "macdonalds" or i == "macdonald" or i == "domac"):
			tab.append("macdo")
		elif(i == "kfc" or i == "poulet"):
			tab.append("kfc")
		elif(i == "kebab" or i == "grec" or i == "turc" or i == "kegre"):
			tab.append("kebab")
		elif(i == "boire" or i == "bois" or i == "boit" or i == "verre" or i == "vin" or i =="bière" or i == "biere" or i == "coktail" or i == "mojito" or i == "vodka"):
			tab.append("boire")
		elif(i == "café"):
			tab.append("café")
		elif(i == "gare" or i == "station" or i == "gare" or i == "bus" or i == "train" or i == "taxi" or i == "vélo"):
			tab.append("transport")
		elif(i == "cinéma" or i == "cinema" or i == "théâtre" or i == "théatre" or i == "theatre" or i == "pièce" or i == "opéra" or i == "concert" or i == "comédie" or i == "spectacle"):
			tab.append("spectacle")
		elif(i == "shopping" or i == "vetement" or i == "vêtement" or i == "vetements" or i == "vêtements" or i == "mode" or i == "souvenirs" or i == "souvenir"):
			tab.append("shopping")
		elif(i == "atm" or i == "distributeur" or i == "argent" or i == "banque" or i == "dab"):
			tab.append("retrait")
		elif(i == "soin" or i == "médicaments" or i == "médicament" or i == "hôpital" or i == "hopital" or i == "pharmacie" or i == "garde" or i == "urgence" or i == "pompier" or i == "samu" or i == "police" or i == "gendarmerie"):
			tab.append("urgence")
		elif(i == "dormir" or i == "reposer" or i == "hotel" or i == "hôtel" or i == "chambre"):
				tab.append("dormir")
		else:
			tab.append("null") # null est notre valeur par défaut si le mot n'est pas reconnu et n'a donc pas d'interet
	return tab

	
	
	

def signification(sent): #regroupe les lemmes en catégorie de signification, associant chaque lemme a un sens plus global, donnant l'orientation de la demande au bot
	tab = list()
	for i in sent:
			if(i == "chercher" or i == "trouver" or i == "afficher" or i == "lister" or i == "montrer" or i == "donner" or i == "vouloir" or i == "pouvoir"):
				tab.append("volonté")
			elif(i == "emmener" or i == "aller"):
				tab.append("deplacement")
			elif(i == "alimenter"):
				tab.append("alimenter")
			elif(i == "regarder"):
				tab.append("regarder")
			elif(i == "choucroute" or i == "restaurant chinois" or i == "thailandais" or i == "italien" or i == "mexicain" or i == "traditionnel" or i == "japonais" or i == "allemand" or i == "boulangerie" or i == "macdo" or i == "kfc" or i == "kebab"):
				tab.append("lieu_manger")
			elif(i == "thé" or i == "boire" or i == "café"):
				tab.append("lieu_boire")
			elif(i == "transport"):
				tab.append("lieu_transport")
			elif(i == "spectacle"):
				tab.append("lieu_spectacle")
			elif(i == "shopping"):
				tab.append("lieu_shopping")
			elif(i == "retrait"):
				tab.append("retrait_argent")
			elif(i == "urgence"):
				tab.append("lieu_urgence")
			elif(i == "dormir"):
				tab.append("lieu_dormir")
			else:
				tab.append(i)
	return tab

class Bot: #Contient une mémoire et son nom, regroupe le fonctionnement global du bot 
	def __init__(self):
		self.nom = "Vladimir"
		self.memoire = list("null")
	
	def start(self): #Début de l'interaction avec l'utilisateur
		print("Bonjour, je suis " + self.nom + ", et je suis à votre service pour rendre votre voyage à Strasbourg le plus agréable possible. En quoi puis-je vous aidé ? \n")
		
		while (1 == 1):
			self.repondre() # On boucle sur les réponses tant que l'utilsateur pose une question
				
	def repondre(self): #Répond a une question
		inp = input() #Saisi
		reponse = Element_Texte(inp)
		self.memoire.append(reponse)
		phrase = ""
		tab_desir = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #Une table qui contient l'ensemble des significations de la phrase passée, chaque ligne étant une catégorie, permettant de comprendre les besoins de l'utilisateur
		
		for i in reponse.signification: #Remplir la tab desir
			if(i == "volonté"):
				tab_desir[0] = tab_desir[0] + 1
			if(i == "deplacement"):
				tab_desir[1] = tab_desir[1] + 1
			if(i == "alimenter"):
				tab_desir[2] = tab_desir[2] + 1
			if(i == "regarder"):
				tab_desir[3] = tab_desir[3] + 1
			if(i == "lieu_manger"):
				tab_desir[4] = tab_desir[4] + 1
			if(i == "lieu_boire"):
				tab_desir[5] = tab_desir[5] + 1
			if(i == "lieu_transport"):
				tab_desir[6] = tab_desir[6] + 1
			if(i == "lieu_spectacle"):
				tab_desir[7] = tab_desir[7] + 1
			if(i == "lieu_shopping"):
				tab_desir[8] = tab_desir[8] + 1
			if(i == "retrait_argent"):
				tab_desir[9] = tab_desir[9] + 1
			if(i == "lieu_urgence"):
				tab_desir[10] = tab_desir[10] + 1
			if(i == "lieu_dormir"):
				tab_desir[11] = tab_desir[11] + 1
		print(tab_desir)
		
		#On analyse la table des désir pour comprend la demande, en récupérant les lieux dans les lemmes et le desir dans les signification de la table
		if(tab_desir[0] > 0):
			phrase = phrase + "Vous désirez"
		else:
			print("Je ne comprends pas le but de votre demande, merci de la reformuler")
			return 0
		if(tab_desir[1] > 0):
			phrase = phrase + " aller"
		else:
			phrase = phrase
			
		if(tab_desir[2] > 0 and tab_desir[4] == 0):
			phrase = phrase + "manger dans la ville, mais je ne sais pas dans quel type de restaurant"
			print(phrase)
			return 0
		if(tab_desir[3] > 0 and tab_desir[7] == 0):
			phrase = phrase + "vous divertir dans la ville, mais je ne sais pas dans quel d'établissement"
			print(phrase)
			return 0
		if(tab_desir[4] > 0):
			phrase = phrase + " manger dans un restaurant. Je vous indique sur votre carte le plus proche."
			print(phrase)
			print("Le " + reponse.retour_lieu("lieu_manger") + " le plus proche est a *** m")
			return 1
		if(tab_desir[5] > 0):
			phrase = phrase + " boire. Je vous indique sur votre carte le lieu le plus proche."
			print(phrase)
			print("Le " + reponse.retour_lieu("lieu_boire") + " le plus proche est a *** m")
			return 1
		if(tab_desir[6] > 0):
			phrase = phrase + " vous déplacer. Je vous indique sur votre carte le moyen de transport le plus proche."
			print(phrase)
			print("Le " + reponse.retour_lieu("lieu_transport") + " le plus proche est a *** m")
			return 1
		if(tab_desir[7] > 0):
			phrase = phrase + " vous divertir. Je vous indique sur votre carte le lieu plus proche."
			print(phrase)
			print("Le " + reponse.retour_lieu("lieu_spectacle") + " le plus proche est a *** m")
			return 1
		if(tab_desir[8] > 0):
			phrase = phrase + " faire des achats. Je vous indique sur votre carte les magasins les plus proche."
			print(phrase)
			print("Le " + reponse.retour_lieu("lieu_shopping") + " le plus proche est a *** m")
			return 1
		if(tab_desir[9] > 0):
			phrase = phrase + " retirer de l'argent. Je vous indique sur votre carte le point le plus proche."
			print(phrase)
			return 1
		if(tab_desir[10] > 0):
			phrase = phrase + " vous dirigez vers un lieu de prise en charge d'urgence. Je vous indique sur votre carte le plus proche."
			print(phrase)
			print("Le " + reponse.retour_lieu("lieu_urgence") + " le plus proche est a *** m")
			return 1
		if(tab_desir[11] > 0):
			phrase = phrase + " dormir. Je vous indique sur votre carte le lieu le plus proche."
			print(phrase)
			return 1
		print("Je ne comprends pas où vous voulez aller")
class Element_Texte: 
	def __init__(self, texte):	# Un élement texte est standardisé par nos fonctions global, nous donnant un élement de texte enrichi par des signification plus profonde
		self.texte = normalise(texte.lower())
		self.mot = tokenise(self.texte)
		self.lemme = lemme(self.mot)
		self.signification = signification(self.lemme)
		
		
	
	def retour_lemme(self): #Verifie les lemmes d'un Element texte, pour le test
		return self.lemme
	
	def retour_signification(self): # Vérifie la signification, test
		return self.signification
	def retour_lieu(self, lieu): #Retourne le lieu en rapport avec la signification voulue
		j = 0
		for i in self.signification:
			if(i == lieu):
				return self.lemme[j]
			j = j + 1

Vlad = Bot()
Vlad.start()	

