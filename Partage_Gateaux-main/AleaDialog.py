from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *



class AleaDialog(QDialog) :
	
	
	accepted = pyqtSignal(dict)
	
	
	def __init__(self,n,p, parent = None):
		#print("Debut")
		QDialog.__init__(self, parent)
		self.setWindowTitle("Paramètres pour graphe aléatoire")
		self.nbNoeuds = QLineEdit(str(n))
		self.probaArc = QLineEdit(str(p))
		self.confirm = QPushButton("Confirmer")
		self.confirm.clicked.connect(self.confirmer)
		self.annul = QPushButton("Annuler")
		self.annul.clicked.connect(self.annuler)
		
		forma = QFormLayout(self)
		forma.addRow('Nombre de noeuds', self.nbNoeuds)
		forma.addRow('Probabilité arc (entre 0 et 1)', self.probaArc)
		forma.addRow(self.confirm)
		forma.addRow(self.annul)
		self.resize(250, 100)
		
	
	
	def confirmer(self):
		text1 = self.nbNoeuds.text()
		text2 = self.probaArc.text()
		valn1 = 0
		valn2 = 0
		entier = ""
		ent = True
		div = False
		flotant = ""
		list_int = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		annuler = False
		if (text1 != "") and (text2 != "") :
			for i in text1 :
				if i in list_int :
					if ent :
						entier += i
					else :
						flotant += i
				elif ent and (i == ',' or i == '.') :
					ent = False
				elif ent and (i == '/') :
					div = True
					ent = False
				else :
					annuler = True
					break
			if div :
				if flotant != "":
					valn1 = int(entier) / int(flotant)
				else :
					annuler = True
			else :
				if flotant != "":
					valn1 = int(entier) + (int(flotant) / (10 ** len(flotant)))
				else :
					valn1 = int(entier)
			ent = True
			div = False
			entier = ""
			flotant = ""
			for i in text2 :
				if i in list_int :
					if ent :
						entier += i
					else :
						flotant += i
				elif ent and (i == ',' or i == '.') :
					ent = False
				elif ent and (i == '/') :
					div = True
					ent = False
				else :
					annuler = True
					break
			if div :
				if flotant != "":
					valn2 = int(entier) / int(flotant)
				else :
					annuler = True
			else :
				if flotant != "":
					valn2 = int(entier) + (int(flotant) / (10 ** len(flotant)))
				else :
					valn2 = int(entier)
			if not annuler :
				valeur = {"nbNoeuds" : int(valn1), "probaArc" : valn2}
				self.accepted.emit(valeur)
		self.accept()
	

	def annuler(self):
		self.accept()


