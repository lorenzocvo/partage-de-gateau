#main

from Graphe import *
from MainWindow import *

if __name__=="__main__":

    print("Debut")
    aleatoire = True

    graph = None
    
    #on test a vec un graphe que l'on crée
    if not aleatoire:
        g = Graphe()
        
        g.ajouter_noeud("A")
        g.ajouter_noeud("B")
        g.ajouter_liste_noeuds(["C","D","E"])
        
        g.ajouter_arc("A", "B")
        g.ajouter_arc("B", "A")
        g.ajouter_liste_arcs([("A","C"),("A","D"),("B","E")])

        #g.afficher_graphe()
        g.partage_aleatoire()
        #g.afficher_graphe()
        
        #g.affiche()
        graph = g

    #on test avec un graphe généré aléatoirement
    else :
        
        g2 = Graphe()
        g2.generer_graphe(6,0.2)
        #g2.afficher_graphe()
        #g2.affiche()
        g2.partage_aleatoire()
        #g2.afficher_graphe()
        graph = g2
        
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.import_graph(graph)
    app.exec_()
    
    print("Fin")
