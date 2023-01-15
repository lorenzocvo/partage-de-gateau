from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Graphe import *
from ArcDialog import *
from NoeudDialog import *
import math


class Canvas(QWidget):
	
	
	
	def __init__(self, parent = None):
		print("class Canvas")
		QWidget.__init__(self, parent)
		
		self.dicNoeuds = {}
		self.dicLigne = {}
		self.arCurseur = {}
		self.graphe = None
		self.pointer = None
        
		self.setMinimumSize(800, 500)
		self.posCanvas = (300, 150)
		self.cursorPosPress = None
		self.cursorPosRelease = None
		self.mode = "Move"              # mode 
		self.listSelected = []          # liste des elements selectionnes
		self.tailleNoeud = 35
		self.taillePointeur = 5
		self.constructArc = None
	
		self.unstable =[]
	
	
	def get_listElem(self):
		return self.listElem
	
	
	
	def reset(self):
		print("reset")
	
	
	
	def imp_g(self, graphe):
		self.graphe = graphe
		self.dicNoeuds = {}
		self.dicLigne = {}
		for i in self.graphe.noeuds :
			self.dicNoeuds[i[0]] = QPoint(0, 0)
		for n1,n2 in self.graphe.arcs :
			if ((n1,n2) in self.graphe.partage) or ((n2,n1) in self.graphe.partage):
				self.dicLigne[(n1,n2)] = 1
				self.arCurseur[(n1,n2)] = QPoint(0, 0)
			else :
				self.dicLigne[(n1,n2)] = 0
		repartieAuto = True
		if repartieAuto :
			roue = 0
			for cle, val in self.dicNoeuds.items() :
				if roue > 7 :
					roue = 0
				bouge = 1
				while bouge == 1 :
					bouge = 0
					for cle2, val2 in self.dicNoeuds.items() :
						if cle2 != cle and math.sqrt(((self.dicNoeuds[cle].x() - val2.x()) ** 2) + ((self.dicNoeuds[cle].y() - val2.y()) ** 2)) < 150:
							#print(math.sqrt(((val.x() - val2.x()) ** 2) + ((val.y() - val2.y()) ** 2)))
							bouge = 1
					if bouge == 1:
						if roue == 0:
							pos = self.dicNoeuds[cle]
							self.dicNoeuds[cle] = QPoint(pos.x() + 10, pos.y())
						elif roue == 1:
							pos = self.dicNoeuds[cle]
							self.dicNoeuds[cle] = QPoint(pos.x() + 10, pos.y() + 10)
						elif roue == 2:
							pos = self.dicNoeuds[cle]
							self.dicNoeuds[cle] = QPoint(pos.x(), pos.y() + 10)
						elif roue == 3:
							pos = self.dicNoeuds[cle]
							self.dicNoeuds[cle] = QPoint(pos.x() - 10, pos.y() + 10)
						elif roue == 4:
							pos = self.dicNoeuds[cle]
							self.dicNoeuds[cle] = QPoint(pos.x() - 10, pos.y())
						elif roue == 5:
							pos = self.dicNoeuds[cle]
							self.dicNoeuds[cle] = QPoint(pos.x() - 10, pos.y() - 10)
						elif roue == 6:
							pos = self.dicNoeuds[cle]
							self.dicNoeuds[cle] = QPoint(pos.x(), pos.y() - 10)
						elif roue == 7:
							pos = self.dicNoeuds[cle]
							self.dicNoeuds[cle] = QPoint(pos.x() + 10, pos.y() - 10)
				roue += 1
			self.maj_arcurseur()
		self.update()
	
	
	
	def maj_graph(self, graph):
		self.graphe = graph
		for i in self.graphe.noeuds :
			nom, val = i
			if nom not in self.dicNoeuds :
				self.dicNoeuds[nom] = QPoint(0, 0)
		for i in self.graphe.arcs :
			n1, n2 = i
			if ((n1, n2) in self.graphe.partage) or ((n2, n1) in self.graphe.partage) :
				self.dicLigne[i] = 1
			else :
				self.dicLigne[i] = 0
		self.maj_arcurseur()
		#print("Sature : " + str(self.graphe.partage_sature(("A", "B"))))
		#print("Quasi-Balanced : " + str(self.graphe.quasi_balanced(("A", "B"))))
		self.update()
	
	
	
	def maj_arcurseur(self, cur = None) :
		if cur == None :
			self.arCurseur = {}
			for cle, val in self.dicLigne.items() :
				if val == 1:
					n1, n2 = cle
					posN1 = (self.dicNoeuds[n1].x() + int(self.tailleNoeud / 2), self.dicNoeuds[n1].y() + int(self.tailleNoeud / 2))
					posN2 = (self.dicNoeuds[n2].x() + int(self.tailleNoeud / 2), self.dicNoeuds[n2].y() + int(self.tailleNoeud / 2))
					valN1 = self.graphe.get_val_noeud(n1)
					vecN1N2 = (posN2[0] - posN1[0], posN2[1] - posN1[1])
					
					if abs(vecN1N2[0]) + abs(vecN1N2[1]) != 0 :
						maxi = max(abs(vecN1N2[0]), abs(vecN1N2[1]))
						vecNorm = (vecN1N2[0] / (maxi), vecN1N2[1] / (maxi))
						posN1 = (posN1[0] + int((self.tailleNoeud / 2) * vecNorm[0]), posN1[1] + int((self.tailleNoeud / 2) * vecNorm[1]))
						posN2 = (posN2[0] - int((self.tailleNoeud / 2) * vecNorm[0]), posN2[1] - int((self.tailleNoeud / 2) * vecNorm[1]))
						vecN1N2 =(posN2[0] - posN1[0], posN2[1] - posN1[1])
					vecAdap = (int(vecN1N2[0] * valN1), int(vecN1N2[1] * valN1))
					self.arCurseur[cle] = QPoint(posN1[0] + vecAdap[0], posN1[1] + vecAdap[1])
		else :
			for i in cur :
				n1, n2 = i
				posN1 = (self.dicNoeuds[n1].x() + int(self.tailleNoeud / 2), self.dicNoeuds[n1].y() + int(self.tailleNoeud / 2))
				posN2 = (self.dicNoeuds[n2].x() + int(self.tailleNoeud / 2), self.dicNoeuds[n2].y() + int(self.tailleNoeud / 2))
				valN1 = self.graphe.get_val_noeud(n1)
				vecN1N2 = (posN2[0] - posN1[0], posN2[1] - posN1[1])
				
				if abs(vecN1N2[0]) + abs(vecN1N2[1]) != 0 :
					maxi = max(abs(vecN1N2[0]), abs(vecN1N2[1]))
					vecNorm = (vecN1N2[0] / (maxi), vecN1N2[1] / (maxi))
					posN1 = (posN1[0] + int((self.tailleNoeud / 2) * vecNorm[0]), posN1[1] + int((self.tailleNoeud / 2) * vecNorm[1]))
					posN2 = (posN2[0] - int((self.tailleNoeud / 2) * vecNorm[0]), posN2[1] - int((self.tailleNoeud / 2) * vecNorm[1]))
					vecN1N2 = vecN1N2 = (posN2[0] - posN1[0], posN2[1] - posN1[1])
				vecAdap = (int(vecN1N2[0] * valN1), int(vecN1N2[1] * valN1))
				if i in self.arCurseur :
					self.arCurseur[i] = QPoint(posN1[0] + vecAdap[0], posN1[1] + vecAdap[1])
				else :
					self.arCurseur[(n2, n1)] = QPoint(posN1[0] + vecAdap[0], posN1[1] + vecAdap[1])
	
	

	def supprimer_arc(self, arc) :
		n1, n2 = arc
		suppr = False
		if (n1, n2) in self.dicLigne :
			self.dicLigne.pop((n1, n2))
			suppr = True
		if (n2, n1) in self.dicLigne :
			self.dicLigne.pop((n2, n1))
			suppr = True
		if suppr :
			self.graphe.supprimer_arc(arc)
			self.maj_graph(self.graphe)
	
	
	
	def select_arc(self, arc) :
		val_noeud1 = self.graphe.get_valeur(arc[0])
		val_noeud2 = self.graphe.get_valeur(arc[1])
		dialo = ArcDialog(arc, val_noeud1, val_noeud2, parent = self)
		dialo.accepted.connect(self.arcDialogAccepted)
		dialo.exec_()
	
	
	
	def arcDialogAccepted(self, valeur) :
		#print("pouaf")
		#print(int(valeur["val1"]) + int(valeur["val2"]))
		#print(valeur["arc"])
		if "Supprimer" in valeur :
			if valeur["Supprimer"] :
				self.supprimer_arc(valeur["arc"])
		else :
			if (((valeur["val1"]) + (valeur["val2"])) > 0) :
				self.graphe.modifier_partage(valeur["arc"], float(valeur["val1"]), float(valeur["val2"]))
			else :
				self.graphe.supprimer_partage(valeur["arc"])
			self.maj_graph(self.graphe)
	
	
	
	def ajouterArc(self, arc) :
		self.graphe.ajouter_arc(arc[0], arc[1])
		self.maj_graph(self.graphe)
	
	
	
	def nouv_noeud(self, position) :
		nom = ""
		alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
		indiceLettre = 0
		for i in alphabet :
			nom = i
			if nom not in self.dicNoeuds :
				break
		self.graphe.ajouter_noeud(nom)
		if position == None :
			self.dicNoeuds[nom] = QPoint(0, 0)
		else :
			self.dicNoeuds[nom] = QPoint(position.x() - int(self.tailleNoeud / 2), position.y() - int(self.tailleNoeud / 2))
		self.maj_graph(self.graphe)
	
	
	
	def changer_noeud_nom(self, nom, nouv_nom) :
		if (nom != nouv_nom) and (nouv_nom != ""):
			if (nom in self.dicNoeuds) and (nouv_nom not in self.dicNoeuds) :
					pos = self.dicNoeuds[nom]
					self.dicNoeuds[nouv_nom] = pos
					self.dicNoeuds.pop(nom)
					listSuppr = []
					for cle, val in self.dicLigne.items() :
						n1, n2 = cle
						if n1 == nom :
							listSuppr.append(cle)
						elif n2 == nom :
							listSuppr.append(cle)
					for i in listSuppr :
						val = self.dicLigne[i]
						n1, n2 = i
						if n1 == nom :
							self.dicLigne[(nouv_nom, n2)] = val
						else :
							self.dicLigne[(n1, nouv_nom)] = val
						self.dicLigne.pop(i)
					self.graphe.changer_nom_noeud(nom, nouv_nom)
					self.maj_graph(self.graphe)
	
	
	
	def supprimer_noeud(self, nom) :
		if nom in self.dicNoeuds :
			self.dicNoeuds.pop(nom)
			listSuppr = []
			for cle, val in self.dicLigne.items() :
				n1, n2 = cle
				if n1 == nom :
					listSuppr.append(cle)
				elif n2 == nom :
					listSuppr.append(cle)
			for i in listSuppr :
				self.dicLigne.pop(i)
			self.graphe.supprimer_noeud(nom)
			self.maj_graph(self.graphe)
	
	
	
	def select_noeud(self, nom) :
		dialo = NoeudDialog(nom, parent = self)
		dialo.accepted.connect(self.noeudDialogAccepted)
		dialo.exec_()
	
	
	
	def noeudDialogAccepted(self, valeur) :
		if ("NouvNom" in valeur) and ("AncNom" in valeur) :
			self.changer_noeud_nom(valeur["AncNom"], valeur["NouvNom"])
		elif "Supprimer" in valeur :
			self.supprimer_noeud(valeur["AncNom"])
			
	
	
	
	def set_mode(self, mode):
		self.mode = mode
	
	
	
	def mousePressEvent(self, event):
		pointpress = event.pos()
		if self.mode == "Select" :
			self.cursorPosPress = QPoint(pointpress.x() - self.posCanvas[0], pointpress.y() - self.posCanvas[1])
			self.pointer = (QLineF(self.cursorPosPress.x() - self.taillePointeur, self.cursorPosPress.y(), self.cursorPosPress.x() + self.taillePointeur, self.cursorPosPress.y()), QLineF(self.cursorPosPress.x(), self.cursorPosPress.y() - self.taillePointeur, self.cursorPosPress.x(), self.cursorPosPress.y() + self.taillePointeur))
		#elif self.mode == "Move" :
		#	self.cursorPosPress = QPoint(pointpress.x() - self.posCanvas[0], pointpress.y() - self.posCanvas[1])
		#	self.cursorPosRelease = self.cursorPosPress
		elif (self.mode == "Move") or (self.mode == "Calcul") :
			self.listSelected = []
			self.cursorPosPress = QPoint(pointpress.x() - self.posCanvas[0], pointpress.y() - self.posCanvas[1])
			self.cursorPosRelease = self.cursorPosPress
			if self.dicNoeuds != {} :
				for cle, valeur in self.dicNoeuds.items():
					rec = QRect(valeur.x(), valeur.y(), self.tailleNoeud, self.tailleNoeud)
					if rec.contains(self.cursorPosPress.x(), self.cursorPosPress.y()) :
						self.listSelected.append(cle)
						break
		elif self.mode == "Draw" :
			self.constructArc = None
			self.cursorPosPress = QPoint(pointpress.x() - self.posCanvas[0], pointpress.y() - self.posCanvas[1])
			self.cursorPosRelease = self.cursorPosPress
			if self.dicNoeuds != {} :
				for cle, valeur in self.dicNoeuds.items():
					rec = QRect(valeur.x(), valeur.y(), self.tailleNoeud, self.tailleNoeud)
					if rec.contains(self.cursorPosPress.x(), self.cursorPosPress.y()) :
						self.constructArc = (cle, QPoint(valeur.x() + int(self.tailleNoeud / 2), valeur.y() + int(self.tailleNoeud / 2)))
						break
		self.update()
	
	
	
	def mouseReleaseEvent(self, event):
		pointrelease = event.pos()
		if self.mode == "Select" :
			self.cursorPosRelease = QPoint(pointrelease.x() - self.posCanvas[0], pointrelease.y() - self.posCanvas[1])
			change = False
			if self.dicNoeuds != {} :
					noeud = "."
					for cle, valeur in self.dicNoeuds.items():
						rec = QRect(valeur.x(), valeur.y(), self.tailleNoeud, self.tailleNoeud)
						if rec.contains(self.cursorPosRelease.x(), self.cursorPosRelease.y()) :
							noeud = cle
							break
					if noeud != "." :
						#print(noeud)
						self.select_noeud(noeud)
						change = True
			if not change :
				self.pointer = (QLineF(self.cursorPosRelease.x() - self.taillePointeur, self.cursorPosRelease.y(), self.cursorPosRelease.x() + self.taillePointeur, self.cursorPosRelease.y()), QLineF(self.cursorPosRelease.x(), self.cursorPosRelease.y() - self.taillePointeur, self.cursorPosRelease.x(), self.cursorPosRelease.y() + self.taillePointeur))
				intersection = QPointF(0, 0)
				arc = (".", ".")
				for cle, valeur in self.dicLigne.items():
					n1, n2 = cle
					ligne = QLineF(QPoint(self.dicNoeuds[n1].x() + int(self.tailleNoeud / 2), self.dicNoeuds[n1].y() + int(self.tailleNoeud / 2)), QPoint(self.dicNoeuds[n2].x() + int(self.tailleNoeud / 2), self.dicNoeuds[n2].y() + int(self.tailleNoeud / 2)))
					if (ligne.intersect(self.pointer[0], intersection) == 1) or (ligne.intersect(self.pointer[1], intersection) == 1) :
						#print(cle)
						arc = cle
						break
						#print("INTERSECTION :(", intersection.x()," , ", intersection.y(), ")")
						#print("POINTEUR :(", self.cursorPosRelease.x()," , ", self.cursorPosRelease.y(), ")")
				if arc != (".", ".") :
					self.select_arc(arc)
				
				#print("Fin 2")
			#self.pointer = None
		#elif self.mode == "Move" :
		#	self.cursorPosRelease = QPoint(pointrelease.x() - self.posCanvas[0], pointrelease.y() - self.posCanvas[1])
		#	self.posCanvas = (self.posCanvas[0] + self.cursorPosRelease.x() - self.cursorPosPress.x(), self.posCanvas[1] + self.cursorPosRelease.y() - self.cursorPosPress.y())
		elif (self.mode == "Move") or (self.mode == "Calcul") :
			self.cursorPosRelease = QPoint(pointrelease.x() - self.posCanvas[0], pointrelease.y() - self.posCanvas[1])
			self.listSelected = []
		elif self.mode == "Draw" :
			self.cursorPosRelease = QPoint(pointrelease.x() - self.posCanvas[0], pointrelease.y() - self.posCanvas[1])
			if self.constructArc != None :
				arc = ("", "")
				if self.dicNoeuds != {} :
					for cle, valeur in self.dicNoeuds.items():
						rec = QRect(valeur.x(), valeur.y(), self.tailleNoeud, self.tailleNoeud)
						if rec.contains(self.cursorPosRelease.x(), self.cursorPosRelease.y()) :
							arc = (self.constructArc[0], cle)
							self.ajouterArc(arc)
							break
				self.constructArc = None
			else :
				self.nouv_noeud(self.cursorPosRelease)
		self.update()
	
	
	
	def mouseMoveEvent(self, event):
		pointrelease = event.pos()
		if self.mode == "Select" :
			self.cursorPosRelease = QPoint(pointrelease.x() - self.posCanvas[0], pointrelease.y() - self.posCanvas[1])
			self.pointer = (QLineF(self.cursorPosRelease.x() - self.taillePointeur, self.cursorPosRelease.y(), self.cursorPosRelease.x() + self.taillePointeur, self.cursorPosRelease.y()), QLineF(self.cursorPosRelease.x(), self.cursorPosRelease.y() - self.taillePointeur, self.cursorPosRelease.x(), self.cursorPosRelease.y() + self.taillePointeur))

		#elif self.mode == "Move" :
		#	self.cursorPosRelease = QPoint(pointrelease.x() - self.posCanvas[0], pointrelease.y() - self.posCanvas[1])
		#	self.posCanvas = (self.posCanvas[0] + self.cursorPosRelease.x() - self.cursorPosPress.x(), self.posCanvas[1] + self.cursorPosRelease.y() - self.cursorPosPress.y())
		elif (self.mode == "Move") or (self.mode == "Calcul") :
			ancienPos = self.cursorPosRelease
			self.cursorPosRelease = QPoint(pointrelease.x() - self.posCanvas[0], pointrelease.y() - self.posCanvas[1])
			if self.listSelected != []:
				for i in self.listSelected :
					pos = self.dicNoeuds[i]
					self.dicNoeuds[i] = QPoint(pos.x() + self.cursorPosRelease.x() - ancienPos.x(), pos.y() + self.cursorPosRelease.y() - ancienPos.y())
					listCurs = []
					for y, z in self.dicLigne.items() :
						n1, n2 = y
						if ((y[0] == i) or (y[1] == i)) and (z == 1) :
							listCurs.append(y)
					self.maj_arcurseur(listCurs)
			else :
				self.posCanvas = (self.posCanvas[0] + self.cursorPosRelease.x() - self.cursorPosPress.x(), self.posCanvas[1] + self.cursorPosRelease.y() - self.cursorPosPress.y())
		elif self.mode == "Draw" :
			self.cursorPosRelease = QPoint(pointrelease.x() - self.posCanvas[0], pointrelease.y() - self.posCanvas[1])
			if self.constructArc != None :
				dep = self.constructArc[0]
				self.constructArc = (dep, self.cursorPosRelease)
		self.update()
	
	
	
	def paintEvent(self, event):
		painter = QPainter(self)
		painter.translate(QPoint(self.posCanvas[0], self.posCanvas[1]))
		pen = QPen(Qt.black)
		pen.setWidth(3)
		painter.setPen(pen)
		for cle, valeur in self.dicLigne.items() :
			if cle != None or valeur != None :
				n1, n2 = cle 
				if valeur == 1 :
					pen2 = QPen(Qt.red)
					pen2.setWidth(3)
					painter.setPen(pen2)
				painter.drawLine(QPoint(self.dicNoeuds[n1].x() + int(self.tailleNoeud / 2), self.dicNoeuds[n1].y() + int(self.tailleNoeud / 2)), QPoint(self.dicNoeuds[n2].x() + int(self.tailleNoeud / 2), self.dicNoeuds[n2].y() + int(self.tailleNoeud / 2)))
				if valeur == 1 :
					pen = QPen(Qt.black)
					pen.setWidth(3)
					painter.setPen(pen)
		if self.mode == "Draw" :
			if self.constructArc != None :
				pen = QPen(Qt.blue)
				pen.setWidth(3)
				painter.setPen(pen)
				painter.drawLine(QPoint(self.dicNoeuds[self.constructArc[0]].x() + int(self.tailleNoeud / 2), self.dicNoeuds[self.constructArc[0]].y() + int(self.tailleNoeud / 2)), self.constructArc[1])
				#pen = QPen(Qt.black)
				#pen.setWidth(3)
				#painter.setPen(pen)
		for cle, val in self.arCurseur.items() :
			pen = QPen(Qt.red)
			pen.setWidth(3)
			painter.setPen(pen)
			painter.setBrush(Qt.black)
			painter.drawEllipse(val.x() - 3, val.y() - 3, 9, 9)
		pen = QPen(Qt.black)
		pen.setWidth(3)
		painter.setPen(pen)
		for cle, valeur in self.dicNoeuds.items() :
			painter.setBrush(Qt.white)
			if cle != None or valeur != None :
				if cle in self.unstable:
					painter.setBrush(Qt.gray)
				painter.drawEllipse(valeur.x(), valeur.y(), self.tailleNoeud, self.tailleNoeud)
				painter.drawText(valeur.x(), valeur.y(), self.tailleNoeud, self.tailleNoeud, Qt.AlignCenter, cle)
				val = self.graphe.get_val_noeud(cle)
				pen2 = QPen(Qt.red)
				pen2.setWidth(3)
				painter.setPen(pen2)
				if len(str(val)) > 10:
					painter.drawText(valeur.x() - self.tailleNoeud, valeur.y() - 15, 3 * self.tailleNoeud, 15, Qt.AlignLeft, str(val))
				else :
					painter.drawText(valeur.x() - self.tailleNoeud, valeur.y() - 15, 3 * self.tailleNoeud, 15, Qt.AlignCenter, str(val))
				pen = QPen(Qt.black)
				pen.setWidth(3)
				painter.setPen(pen)
		"""if self.mode == "Draw" :
			painter.drawLine(self.pointer[0])
			painter.drawLine(self.pointer[1])"""
					




