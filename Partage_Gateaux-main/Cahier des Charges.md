# Cahier des charges

Le logiciel concerne les partages de gâteaux entre plusieurs noeuds d'un graphe (non orienté). Ces graphes permettent de modéliser les forces de négociations entre plusieurs agents au sein d'un réseau. Dans un graphe, un partage ne peut avoir lieu qu'entre 2 agents et chaque agent ne peut partager qu'avec un seul autre agent à la fois, le partage est représenté par la proportion du gâteau que chacun des deux agents obtient (donc pour un partage entre 2 agents, deux nombres dont la somme est égale à 1). Le but est d'abord de déterminer si un graphe avec un partage donné est stable, c'est à dire que parmis les couples d'agents, aucun n'a d'intérêt à rompre son accord actuel pour réaliser un partage avec un autre agent. Le logiciel s'ouvre dans une fenêtre, il permet de visualiser au moins un graphe et possède des boutons afin d'agir sur ce dernier et d'appeler les différentes fonctionnalités.
Les différentes fonctionnalités qui sont appelables à partir du logiciel sont :

- Créer un graphe (noeuds et arcs)

- Enregistrer un graphe (et son partage actuel) sous forme de fichier texte

- Ouvrir un graphe à partir d'un fichier texte

- Permettre à l'utilisateur de proposer un partage entre les différents agents du graphe ouvert (placer sur les arcs une pondération)

- Vérifier si le partage d'un graphe est stable (vérification automatique ou bien vérification suite à l'appel de la fonctionnalité par l'utilisateur)

- Permettre à l'utilisateur de zoomer sur le graphe

- Calcul du balanced outcome à l'aide de la méthode Edge balacing Dynamics (https://www.nikhildevanur.com/pubs/edgebalancing.pdf)

- Avoir des graphes de bases pour permettre de tester et prendre en main directement l'application à son lancement

Secondaire :

- Permettre à l'utilisateur de réorganiser les noeuds dans l'espace afin de rendre le graphe plus facile à lire

- Générer un partage stable à partir du partage actuel s'il n'est pas stable

- Permettre de voir l'évolution étape par étape du partage non stable vers le partage stable lorsqu'on demande une génération de partage stable

- Vérifier si un partage est un balanced outcome

- Générer le balanced outcome d'un graphe

- Permettre de voir l'évolution du partage jusqu'à obtenir le balanced outcome d'un graphe lorsque qu'il est généré

