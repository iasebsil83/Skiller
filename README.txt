Skiller[2.3.0] Role Play Game intégralement développé par I.A. avec Python

YT : www.youtube.com/user/IAsebsil83
 @ : i.a.sebsil83@gmail.com

Ce jeu est un rpg codé en python fonctionnant sur serveur donc nécessite de créer un réseau local




Matériel nécessaire :

	1) Un moyen de connexion en réseau local (Routeur, Serveur, multi-Ethernet, ...)

	2) Un ordinateur qui servira de serveur pour le jeu (possible pour les raspberry pi)

	3) Un ordinateur pour chaque joueur




I] Installation d'un réseau local :

	1) Brancher votre appareil à une prise d'alimentation et assurez vous qu'il est alimenté.

	2) Si vous avez correctement initialisé votre matériel comme indiqué sur la notice,
			votre réseau est prêt à être utilisé.




II] Installation d'un serveur :

	1) Installer "Python" sur l'ordinateur serveur.

	2) Copier le dossier "Server" où vous le souhaitez.

	4) Connecter votre ordinateur à votre réseau local (par wifi ou par câble eternet).

	5) Lancer le serveur "SkillerServer.py".
	   Dès que le message "Server ON" apparaît sur le serveur, le serveur est lancé.




III] Installation individuelle :

	1) Installer "Python" sur votre ordinateur.

	2) Copier le dossier "Client" où vous le souhaitez, c'est votre dossier joueur.

	4) Connecter votre ordinateur à votre réseau local (par wifi ou par câble ethernet).

	5) Pour lancer le jeu, il faut suivre 3 étapes :
	    - Récupérer l'ip du serveur et l'écrire dans "SkillerClient.py"
	    - Même chose pour les ports utilisés, voir dans le fichier du serveur "SkillerServer.py".
	    - Lancer "SkillerClient.py"




/!\ ATTENTION /!\ : Ce jeu a été codé en python et n'est donc pas sécurisé :

	- Merci de ne PAS modifier les fichiers du serveur pendant une partie.

	- Merci de ne PAS modifier le programme SkillerClient.py en cours de route.

	- En cas de crash ou de quelconque problème rencontré sur le serveur,
			déconnecter tous les joueurs du serveur, puis éxécutez le fichier RepairSkiller.py.
			(Prévenir les autres joueurs auparavant à cause du risque de double connexion sur un même compte
			 pouvant entraîner une sursaturation d'informations sur le réseau)




Quelques précisions:

	- Les statistiques des joueurs ne sont pas encore réglées.

	- Il n'y a qu'une seule attaque possible pour l'instant : punch, accessible à la touche 0 du pavé numérique (0 mana consomée, 0 secondes de récupération).

	- Toutes les créatures hostiles ont les mêmes caractéristiques excéptés le niveau mais ont toutes les mêmes textures (Et ce, peu importe les directions).

	- Les touches sont configurables via la touche K.

	- La carte entière du jeu est visible dans chaque dossier joueur maps.jpg.
			(le nom de la map dans laquelle on se trouve s'affiche dans le chat lorsqu'on y arrive.)

	- Les créatures hostiles n'apparaîssent pas dans Skyens (Lobby + périphérie).

	- Casques, armures, armes, pendantifs et anneaux peuvent être équipés (avec une commande).

	- Les commandes existent mais on ne peut y accéder qu'en remplaçant dans la sauvegarde du joueur l'atribut 'False' par 'True'
			(Utiles pour les administrateurs serveur) ou avec une commande s'il y a déjà un administrateur.

	- IL EST POSSIBLE QUE LE JEU NE DEMARE PAS CORRECTEMENT S'IL N'EST PAS DEMARRÉ PAR L'IDLE !

I.A. Let's Code !
