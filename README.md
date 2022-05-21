# OpenClassrooms Project 6 - Classifiez automatiquement des biens de consommation

## 1. Introduction
Ce projet a été réalisé pour le [parcours Data Scientist de OpenClassrooms](https://openclassrooms.com/fr/paths/164-data-scientist). <br>
Il s'agit du sixième projet du parcours : [Implémentez un modèle de scoring](https://openclassrooms.com/fr/paths/164/projects/632/assignment).
Ce repos est fait our la partie de l'API et du dashboard. Il y a un autre pour la partie de modelisation.

## 2. Description du Projet
Développer un algorithme de classification pour classifier la demande en crédit accordé ou refusé avec des données déséquilibres. Puis, développer un dashboard interactif pour expliquer de façon la plus transparente possible les décisions d’octroi de crédit.

## 3. Compétences Exigées
- Utiliser un logiciel de version de code pour assurer l’intégration du modèle
- Déployer un modèle via une API dans le Web
- Réaliser un dashboard pour présenter son travail de modélisation
- Rédiger une note méthodologique afin de communiquer sa démarche de modélisation
- Présenter son travail de modélisation à l'oral

## 4. Contenu du Repository
- app.py : comporte les routes de l'application.
- forms.py : comporte la formule qui prend l'ID Client comme input.
- predict_credit_score.py : comporte les fonctions qui prédirent le score crédit et qui plot les graphes pour le dashboard.
- static/ et templates/ : comporte les elements de front-end.

## 4. Données
[Home Credit Default Risk](https://www.kaggle.com/c/home-credit-default-risk/data)