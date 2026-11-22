# ProiePredateur-IA

# Pour installer et lancer le projet 
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python ecosysteme/affichage.py
```

# Meteo :
 1 : pluie, 2 : meteo normale, 3 : secheresse.
- La pluie augmente l'eau et accelere la repousse. 
- La secheresse diminue l'eau, augmente la temperature et ralentit la repousse.
- La vegetation pousse mieux entre 15 et 25 C. Les animaux perdent plus d'energie en dehors de cette plage.
- La végétation s'arrête de pousser en dehors de -5 C et 45 C
- Pour chaque animal, chaque degré au-delà de la zone de confort ajoute 0,05 point à la perte d’énergie par action. À 30 C, un lapin perd donc 2,25 points au lieu de 2, et un renard 1,25 au lieu de 

Résultats : 
- En mode pluie, les lapins ont tendance à survire plus longtemps qu'en méteo normale 
- En mode sécheresse, les lapins meurent plus vite, et les renards restent plus longtemps