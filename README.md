# charging-station
Comment coder sa politique dans Charging_station.

Vous allez devoir implementer votre politique énergétique dans le code. 

-------------

!!!!!  Tout d'abord vous n'avez qu'une seul fonction à modifier : take_decision(self,time) !!!!!

-------------

Cette fonction doit renvoyer pour le temps time quel charge vous voulez mettre dans chaques voitures.
Votre take decision doit renvoyer un dictionnaire de la forme : {"fast":[load_car_fast_1,load_car_fast_2],"slow":[load_car_slow_1,load_car_slow_2]}

Pour implementer votre politique il faut prendre un certain nombre de choses en compte: 
	-La somme de vos load_cars ne doit pas dépasser la capacité maximum de la station, si non les dernières voiture ne seront pas chargées comme voulu.
	-Les voitures lents peuvent prendre un load max de 3 et les fast de 22
	-Si dans votre politique vous etes amenez à charger une voiture qui n'est pas là, le code corrige et ne vous fera pas payer cette consomation car la voiture n'est pas là pour accepter la charge.
	-Idem si vous voulez charger ou decharger les voitures plus qu'il n'est possible le code corrige également.
	-Vous aurez des penalités si les voitures partent avec moins de 25% de leur batterie.
	-Quand les voitures reviennent elles renviennet avec le stock avec lequel elles sont parties -4.

Pour implementez votre politique, vous pouvez utiliser toutes les variables de la classe.

Si vous voulez comprendre un peu le code :
	La fonction observe nous dit à chaques pas de temps si une voiture est partie ou arrivée, cette fonction est appelée après que l'on appel votre take decision donc vous ne pouvez pas utiliser cette information dans le take_decision.
	La fonction update_battery_stock permet de corriger votre load_battery dans les cas ou il n'y a pas de voitures, où vous voulez charger plus que possible etc...
	La fonction penalty permet de calculer les penalités que vous pourriez avoir.
	La fonction nb_cars permet de savoir quels voitures sont là idem que pour observe vous ne pourrez pas utiliser l'information du temps t mais vous pouvez utiliser celle de t-1
	La fonction compute load fait tourner le code et renvoie au manager les inforamtions necessaires.
	Enfin la fonction reset permet de tout rest à la fin de la journée.

Pour votre politique vous pourrez donc utiliser toutes les variables de la classe (celles avec un self. devant qui sont mis à jour de pas de temps en pas de temps)
Attention les variables self.depart et self.arrival sont des dictionnaires qui retiennent les dates de départ et d'arrivé des véicules, ils sont initié de façons à ce que à t=0 les horaires de départ et d'arrivé des véicules est à 23h et quand une voiture part on remplace ce 23h par l'heure de départ pour la voiture correspondante
Donc vous ne disposez pas des toutes les heures de départ et d'arrivé des véicules, vous disposez seulement des heures de départ et d'arrivé des véicules qui sont déja partis ou déja arrivé.
 
