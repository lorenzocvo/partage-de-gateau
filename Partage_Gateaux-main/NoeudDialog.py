from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *



class NoeudDialog(QDialog) :
	
	
	accepted = pyqtSignal(dict)
	
	
	def __init__(self, nomA, parent = None):
		QDialog.__init__(self, parent)
		self.setWindowTitle("Modification de Noeud")
		message = QLabel("Entrez le nouveau nom du noeud " + nomA + " :")
		self.ancNom = nomA
		self.nouvNom = QLineEdit(nomA)
		self.confirm = QPushButton("Confirmer")
		self.confirm.clicked.connect(self.confirmer)
		self.annul = QPushButton("Annuler")
		self.annul.clicked.connect(self.annuler)
		self.suppN = QPushButton("Supprimer Noeud")
		self.suppN.clicked.connect(self.supprimerN)
		
		forma = QFormLayout(self)
		forma.addRow(message)
		forma.addRow("Nouveau nom :", self.nouvNom)
		#Hlay = QVBoxLayout(self)
		#Hlay.addWidget(self.annul)
		#Hlay.addWidget(self.supp)
		#Hlay.addWidget(self.confirm)
		#self.inter = QWidget()
		#self.inter.setLayout(Hlay)
		#format.addRow(self.inter)
		forma.addRow(self.confirm)
		forma.addRow(self.annul)
		forma.addRow(self.suppN)
		self.resize(250, 100)
		
	
	
	def confirmer(self):
		nouv = self.nouvNom.text()
		#annulation = False :
		if (',' not in nouv) and (' ' not in nouv) :
			valeur = {"NouvNom" : nouv, "AncNom" : self.ancNom}
			self.accepted.emit(valeur)
		self.accept()

	def supprimerN(self):
		reponse = QMessageBox.question(self, "Supprimer Noeud", "Voulez-vous supprimer définitivement le noeud " + self.ancNom + " ?")
		if reponse == QMessageBox.Yes:
			valeur = {"Supprimer" : True, "AncNom" : self.ancNom}
			self.accepted.emit(valeur)
			self.accept()
	
	def annuler(self):
		self.accept()

