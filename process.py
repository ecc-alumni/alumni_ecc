from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import requests
import time
import json

load_dotenv()
def extract_links_data():
    
    with open("data.html", "r", encoding="utf-8") as file:
        content = file.read()
    soup = BeautifulSoup(content,"html.parser")
    org = soup.find_all("div",{"class":"org-people-profile-card__profile-info"})
    org = [og.find("div",{'class':"artdeco-entity-lockup artdeco-entity-lockup--stacked-center artdeco-entity-lockup--size-7 ember-view"}) for og in org]
    org = [og.find("div",{'class':"artdeco-entity-lockup__title ember-view"}) for og in org]

    linkd = []
    k= 1
    for i in range(len(org)):
        case = org[i]
        a = case.find("a")
        print(i)
        if a is None:
            k+=1
            continue
        href = a["href"]
        href = href.split("?")[0]
        noms = a["aria-label"].replace("Voir le profil de ","")
        nom = noms.split(" ")[-1]
        linkd.append(href)
        k +=1


    links = []
    for item in linkd:
        if item not in links:
            links.append(item)



    API_KEY = os.getenv("MY_SECRET_KEY") #Cle GHOST GENIUS API





    sdata = []
    k = 799
    for l in links :
        response = requests.get("https://api.ghostgenius.fr/v2/profile",
            headers={
                "Authorization": f"Bearer {API_KEY}"
            },
            params={
                "url": l
            }
        )
        hk = 0.4
        if response.status_code == 200:
            data = response.json()
            print("======================================")
            sdata.append(data)
            k=k+1
            print(k)
            print(data['full_name'])
            time.sleep(hk)
        else:
            print(f"Erreur {response.status_code} : {response.text}")
        
    return sdata

if __name__ == "__main__":
    sdata = extract_links_data()
    print("Extraction terminée, sauvegarde des données...")
     # Sauvegarder les données dans un fichier JSON
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(sdata, f, ensure_ascii=False, indent=4)
    
   
