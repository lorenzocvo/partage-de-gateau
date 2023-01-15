from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *



class ArcDialog(QDialog) :
	
	
	accepted = pyqtSignal(dict)
	
	
	def __init__(self, arc, val1, val2, parent = None):
		print("Debut")
		QDialog.__init__(self, parent)
		self.setWindowTitle("Modification de partage")
		#•message = QLabel("Entrez les nouvelles valeur du partage de l'arc " + str(arc) + " :")
		self.arc = arc
		self.val_noeud1 = QLineEdit(str(val1))
		self.val_noeud2 = QLineEdit(str(val2))
		self.confirm = QPushButton("Confirmer")
		self.confirm.clicked.connect(self.confirmer)
		self.annul = QPushButton("Annuler")
		self.annul.clicked.connect(self.annuler)
		self.suppA = QPushButton("Supprimer Arc")
		self.suppA.clicked.connect(self.supprimerA)
		self.supp = QPushButton("Supprimer Partage")
		self.supp.clicked.connect(self.supprimer)
		
		forma = QFormLayout(self)
		#forma.addRow(message)
		forma.addRow(arc[0], self.val_noeud1)
		forma.addRow(arc[1], self.val_noeud2)
		#Hlay = QVBoxLayout(self)
		#Hlay.addWidget(self.annul)
		#Hlay.addWidget(self.supp)
		#Hlay.addWidget(self.confirm)
		#self.inter = QWidget()
		#self.inter.setLayout(Hlay)
		#format.addRow(self.inter)
		forma.addRow(self.confirm)
		forma.addRow(self.annul)
		forma.addRow(self.suppA)
		forma.addRow(self.supp)
		self.resize(250, 100)
		
	
	
	def confirmer(self):
		text1 = self.val_noeud1.text()
		text2 = self.val_noeud2.text()
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
				valeur = {"val1" : valn1, "val2" : valn2, "arc" : self.arc}
				self.accepted.emit(valeur)
		self.accept()
	
	def supprimer(self):
		valeur = {"val1" : 0, "val2" : 0, "arc" : self.arc}
		self.accepted.emit(valeur)
		self.accept()
	
	def supprimerA(self):
		reponse = QMessageBox.question(self, "Supprimer Arc", "Voulez-vous supprimer définitivement l'arc (" + self.arc[0] + " , " + self.arc[1] + ") ?")
		if reponse == QMessageBox.Yes:
			valeur = {"Supprimer" : True, "arc" : self.arc}
			self.accepted.emit(valeur)
			self.accept()
	
	def annuler(self):
		self.accept()

