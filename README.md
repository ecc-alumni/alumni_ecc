

## 📁 Structure du projet
## scrap.py
Installez une version de chrome divercomppatible avec votre navigateur chrome. allez dans le fichier .env et remplacez les champs MY_EMAIL et MY_PASSWORD par vos identifiants linkedin. Installez les dependances  
`pip install requirements.txt`  
Executez **scrap.py**. Les resultats seront stockés dans **data.html**

## process.py 
Après avoir mis votre clé secrète ghost genius api dans le fichier **.env**, vous executez ce script pour envoyer les liens des qlumni a l'API GHOST GENIUS pour extraire les informations essentielles. Les résultats seront stockés dans **data.json**

## data.py
Si vous voulez stocker les données dans une base de données MYSQL  

<details> <summary><strong>📦 Structure SQL de la table <code>alumni</code></strong></summary>
</details>
```
CREATE TABLE IF NOT EXISTS alumni (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lkdid VARCHAR(60) UNIQUE NOT NULL,
    nom VARCHAR(100) NOT NULL,
    prénoms VARCHAR(100) NOT NULL,
    datediplome DATE,
    profil TEXT,
    bio TEXT,
    skills TEXT NOT NULL,
    location VARCHAR(250),
    url TEXT NOT NULL
);
```

