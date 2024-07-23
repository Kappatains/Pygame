from unidecode import  unidecode
from urllib.request import Request, urlopen
from urllib.parse import unquote
from bs4 import BeautifulSoup
import re

def get_random_page():
    req_start_page = Request(
        url="https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard", 
        #url ="https://fr.wikipedia.org/wiki/H%C3%B4tel_de_ville_de_Nusle",
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    webpage = urlopen(req_start_page)
    return webpage.url

#Fonction qui retire les problème de lettre avec accent. => Possible problème de non affichage lorsque nous sommes sur les pages de l'alphabet? 
def beautify(value):
    if value == None:
        return
    better_name = unidecode(unquote(value))
    regex  = "^https://fr.wikipedia.org/wiki/"
    if re.match(regex, better_name):
        better_name = better_name[30:]
    return better_name

#Fonction qui récupère la liste des liens présent dans la page wikipédia (en filtrant sur le corps de l'article). 
#Prend une url en entrée
#Renvoi une liste de string supprimé de tout doublon
def get_links(url):
    list_link_page = []
    webpage = urlopen(url).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    
    content = soup.find(id ='mw-content-text')
    content.find(id='bandeau-portail').clear()
    link_page = content.find_all('a', src= None, attrs={'href': re.compile("^/wiki/")})
    for  link in link_page:
        link_href = link.get('href')
        list_link_page.append(link_href)
    return (set(list_link_page))

#Transforme une liste donnée en dictionnaire contenant 
def transform_list_to_dico(beautiful_list_link):
    link_dico = {}
    for link in beautiful_list_link:
        real_link = "https://fr.wikipedia.org/wiki/" + link
        new_dico = {unidecode(unquote(link)):real_link}
        link_dico.update(new_dico)
    return link_dico

#Fonction qui fait le trie dans les liens pour ne garder que des liens d'article. 
#Prend une liste de string en entrée
#Renvoi une liste de string supprimé de tout les filtre appliqué
def filter_link(list_link):
    beautiful_list_link = []
    for  link in list_link:
        regex1 = "^/wiki/Fichier"
        regex2 = "^/wiki/Sp%C3%A9cial:"
        regex3 = "^/wiki/Mod%C3%A8le:"
        regex4 = "^/wiki/Aide:"
        regex5 = "^/wiki/Projet:"
        regex6 = "^/wiki/Wikip%C3%A9dia:"
        if re.match(regex1, link): 
            pass
        elif re.match(regex2, link): 
            pass
        elif re.match(regex3, link): 
            pass
        elif re.match(regex4, link): 
            pass
        elif re.match(regex5, link): 
            pass
        elif re.match(regex6, link): 
            pass
        else :
        #On retire le /wiki/ pour ne garder que l'information qui nous intéresse
            beautiful_list_link.append(link[6:])
    beautiful_list_link.sort()
#link_dico = transform_list_to_dico(beautiful_list_link)
    return(beautiful_list_link)

#Fonction qui range les liens dans des listes de 20 liens. 
#Prend une liste de string en entrée
#Renvoi une liste de liste de string  avec 20 éléments maximum par sous liste
def pagination_link(beautiful_list_link):
    reworked_list = []
    start_page = 0
    end_page = 20
    while (len(reworked_list)*20) <= len(beautiful_list_link):
        split_list = beautiful_list_link[start_page:end_page]
        reworked_list.append(split_list)
        start_page += 20
        end_page += 20
    return reworked_list