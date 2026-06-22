# 🏠 Airbnb Analytics Platform

Plateforme analytique Airbnb construite avec **DuckDB**, **dbt** et **Streamlit**.


## 📋 Contexte

Ce projet a été réalisé dans le cadre du MBA ESG 2026.  
Il vise à analyser les données Airbnb pour produire des insights business
sur les logements, les hôtes, les avis clients et l'impact des nuits de pleine lune.


## 🏗️ Architecture

```
Sources (S3)
     │
     ▼
Bronze (vues brutes)
     │
     ▼
Silver (tables nettoyées)
     │
     ▼
Gold (tables analytiques)
     │
     ▼
Streamlit (dashboard)
```

## 🛠️ Stack technique

| Outil     | Rôle                             |
| --------- | -------------------------------- |
| DuckDB    | Moteur analytique local          |
| dbt       | Transformations et tests qualité |
| Streamlit | Dashboard interactif             |
| Plotly    | Visualisations                   |
| GitHub    | Versioning et collaboration      |


## 📦 Sources de données

| Fichier                    | Description            | Lignes  |
|----------------------------| ---------------------- | ------- |
| `hosts.csv`                | Données des hôtes      | 14 111  | 
| `listings.csv`             | Données des logements  | 17 499  |
| `reviews.csv`              | Avis clients           | 410 284 |
| `seed_full_moon_dates.csv` | Dates de pleine lune   | ------- |


## 🗂️ Structure du projet

```
airbnb-analytics/
├── models/
│   ├── schema.yml
│   ├── bronze/
│   │   ├── bronze_hosts.sql
│   │   ├── bronze_listings.sql
│   │   └── bronze_reviews.sql
│   ├── silver/
│   │   ├── silver_hosts.sql
│   │   ├── silver_listings.sql
│   │   └── silver_reviews.sql
│   └── gold/
│       ├── gold_listings_analysis.sql
│       ├── gold_hosts_analysis.sql
│       ├── gold_reviews_analysis.sql
│       └── gold_full_moon_impact.sql
├── seeds/
│   └── seed_full_moon_dates.csv
├── streamlit/
│   └── app.py
├── dbt_project.yml
├── profiles.yml
├── requirements.txt
└── README.md
```

## 🚀 Installation et exécution

### 1. Cloner le repo
```bash
git clone https://github.com/SyfaxAcherfouche/airbnb-analytics.git
cd airbnb-analytics
```

### 2. Créer et activer l'environnement virtuel
```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Lancer le pipeline dbt
```bash
dbt seed       # Charge les dates de pleine lune
dbt run        # Exécute tous les modèles Bronze → Silver → Gold
dbt test       # Lance les tests qualité
```

### 5. Lancer le dashboard
```bash
streamlit run streamlit/app.py
```

## 📊 Fonctionnalités du dashboard

- **12 KPIs** : logements, prix moyen/médian, hôtes, superhosts, sentiments
- **Filtres dynamiques** : type de logement, sentiment des avis
- **4 visualisations** :
  - 🏘️ Analyse des logements par type
  - 🏅 Superhosts vs hôtes classiques
  - 📅 Évolution mensuelle des avis
  - 🌕 Impact des nuits de pleine lune


## 🔍 Insights clés

### 🏘️ Analyse des logements
- Le parc analysé compte **17 491 logements** proposés par **14 103 hôtes**
- Le prix moyen est de **74.94 €** avec un prix médian de **55 €**,
  l'écart important entre les deux indique une minorité de logements
  très haut de gamme (jusqu'à **8 000 €**) qui tirent la moyenne vers le haut
- **"Entire home/apt"** est le type le plus répandu (~10 000 logements)
  et le plus abordable (~95 €), tandis que les **"Hotel room"**
  sont les plus chers (~200 €) mais les plus rares
- **"Private room"** est le deuxième segment en volume (~7 500 logements)
  à un prix moyen de ~48 €, ciblant les voyageurs à petit budget

### 🏅 Analyse des hôtes
- Seulement **13.6%** des hôtes ont le statut **Superhost**
  contre **86.4%** d'hôtes classiques
- Les Superhosts affichent un prix moyen de **86.93 €**
  contre ~73 € pour les hôtes classiques, soit environ
  **+15% de revenus** grâce au statut Superhost
- Malgré leur minorité, les Superhosts gèrent une part
  significative des logements, signe d'une plus grande
  professionnalisation de leur activité

### 📅 Analyse des avis clients
- **410 284 avis** analysés sur la période 2009–2022
- Les avis sont majoritairement **positifs (56.7%)**, 
  suivis des neutres et des négatifs **(7.3%)**
- On observe une **croissance exponentielle** des avis 
  entre 2009 et 2019, signe d'une adoption massive de la plateforme
- Un **pic notable** est visible autour de **2019-2020**,
  suivi d'une chute brutale début 2020 correspondant à
  l'impact du **COVID-19** sur le tourisme mondial
- Une **reprise progressive** est visible à partir de fin 2020,
  mais le volume n'a pas encore retrouvé son niveau pré-COVID en 2022

### 🌕 Impact des nuits de pleine lune
- **3.5%** des avis ont été déposés lors d'une nuit de pleine lune,
  soit **14 269 avis** sur 410 284
- La répartition des sentiments est **quasi identique** entre
  les deux types de nuits :
  - Positifs : **~55%** (pleine lune) vs **~55%** (nuit normale)
  - Neutres : **~36%** vs **~36%**
  - Négatifs : **~8%** vs **~8%**
- **Conclusion : la pleine lune n'a aucun impact mesurable**
  sur la satisfaction des voyageurs Airbnb
- Cette absence de corrélation invalide l'idée reçue selon laquelle
  la pleine lune influencerait le comportement humain

## 👥 Équipe

- **ACHERFOUCHE SYFAX** — Travail réalisé en autonomie complète

*MBA ESG 2026 – Évaluation Management Opérationnel*