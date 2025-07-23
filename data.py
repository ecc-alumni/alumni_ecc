import pandas as pd
import os
from dotenv import load_dotenv
import time
import json
from process import extract_links_data
import mysql.connector
from datetime import date
import datetime

load_dotenv()


gdata = []
exdata = []
# Connexion à la base de données
connexion = mysql.connector.connect(
    host=os.getenv("SERVER_IP"),       # ou l'IP du serveur MySQL
    user=os.getenv("DB_USER"),
    port=os.getenv("DB_PORT"),
    password=os.getenv("DB_PWD"),
    database=os.getenv("DB_NAME")
)

curseur = connexion.cursor()

# Exemple de données à insérer
sdata = extract_links_data()
# Requête SQL (paramétrée pour éviter les injections SQL)





for stu in sdata :

  id = stu['public_id']
  nom = stu['last_name']
  prénoms = stu['first_name']
  url = stu['url']
  skills = stu['skills']
  skills = json.dumps(skills)
  location = stu['geo']['location']['name']
  if 'summary' not in stu.keys():
      bio = 'Pas de Résume'
  else:
      bio = stu['summary']

  profil = stu['headline']
  edus = stu['educations']
  casa = []
  for edu in edus :
    if edu['school']['id'] == '3747130' :
      casa.append(edu)
  if casa == [] :
    datediplome = "Unknown"
  else:
    cas = casa[0]
    datediplome = cas['end']
    ck = 1
    while cas['end'] is None and ck < len(casa):
      cas = casa[ck]
      datediplome = cas['end']
      ck = ck + 1

  if datediplome is None :
    print(f"{stu['url']}")
    continue
  else:
    if datediplome ==  "Unknown" :
      ddpl = date(datetime.now().year, 1, 1)  # Pour ceux dont la date d;obtention du diplome est inconnue
      gdata.append((id, nom, prénoms, skills, location, bio,ddpl, profil, url))
      
    else:
      datediplome = datediplome.split("-")
      datediplome = date(int(datediplome[0]), int(datediplome[1]), 1)
      gdata.append((id, nom, prénoms, skills, location, bio, datediplome, profil, url))
    if stu['experiences'] == []:
      continue
    else :
      for exp in stu['experiences']:
        if exp is None :
          print(f"Exp nulle pour {stu['url']}")
        alumni_id = stu['public_id']
        #company = exp.get('company')['name'] if exp.get('company') is not None else 'Unknown'
        if exp.get('company') is not None :
          corp = exp['company']
          if corp.get('name') is not None :
            company = corp['name']
          else :
            company = 'Unknown'
        else :
          company = 'Unknown'
        #company = exp.get('company', {}).get('name', 'Unknown')
        position = exp['position']
        employment_type = exp.get('employmentType') if exp.get('employmentType') is not None else 'Unknown'
        if 'description' not in exp.keys():
          description = 'Pas de Description'
        else:
          description = exp['description']
        start = exp['start']
        if start is not None :
          start = start.split("-")
          start = date(int(start[0]), int(start[1]), 1)
        end = exp['end']
        if end is not None and end != 'Present':
          end = end.split("-")
          end = date(int(end[0]), int(end[1]), 1)
          location = exp['location']
          exdata.append((alumni_id, company, position, employment_type, start, end, location, description))
        else :
          end = date(datetime.now().year + 5, 1, 1) # Pour ceux dont la date de fin est inconnue ou n'est pas encore arrivée
          exdata.append((alumni_id, company, position, employment_type, start,end, location, description))
    

requete_alumni = "INSERT INTO alumni (lkdid, nom, prénoms, skills, location, bio, datediplome, profil, url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
requete_experience = "INSERT INTO experiences (alumni_id, company, position, employment_type, start, end, location, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"


curseur.executemany(requete_alumni, gdata)

# Valider les modifications
connexion.commit()
print(f"{curseur.rowcount} lignes d'alumni insérées.")

curseur.executemany(requete_experience, exdata)
# Valider les modifications
connexion.commit()
print(f"{curseur.rowcount} lignes d'expériences insérées.")

# Fermer la connexion
curseur.close()
connexion.close()