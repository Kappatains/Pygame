import pygame
from pygame.locals import *
from Button import *
from Label import *
from Wiki import *


class Game:
    def __init__ (self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.buttons = menu_buttons
        self.status = 'menu_home'
        self.game_label_header = None
        self.pages_list = None
        self.current_page_number = 0
        self.url_start = None
        self.url_current = None
        self.url_target = None
        self.score_count = 1200
        self.path = []
        self.path_group = None

    #Fonction de gestion des event dans pygame.
    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    self.running = False
            for rb in self.buttons:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rb.rect.collidepoint(pygame.mouse.get_pos()) and event.button == 1 and rb.type == 'quit':
                         self.running = False
                    if rb.rect.collidepoint(pygame.mouse.get_pos()) and event.button == 1 and rb.type == 'start':
                        self.score_count = 1200
                        self.path = []
                        self.path_group = None
                        self.status = 'menu_game'
                        self.current_page_number = 0
                        self.url_start = get_random_page()
                        self.url_target = get_random_page() #"https://fr.wikipedia.org/wiki/Anglicisme"
                        self.url_current = self.url_start
                        self.pages_list = create_page_list(self.url_start)
                        self.buttons = create_button_page(self.pages_list, self.current_page_number)
                        self.game_group = pygame.sprite.Group(self.buttons)


                        
                    if rb.rect.collidepoint(pygame.mouse.get_pos()) and event.button == 1 and rb.type == 'score':
                        self.status = 'menu_score'
                        self.buttons = score_buttons
                        
                    if rb.rect.collidepoint(pygame.mouse.get_pos()) and event.button == 1 and (rb.type == 'menu'or rb.type == 'reset'):
                        self.status = 'menu_home'
                        self.buttons = menu_buttons

                    if rb.rect.collidepoint(pygame.mouse.get_pos()) and event.button == 1 and rb.type == 'game':
                        self.path.append(rb.text)
                        self.score_count -= 5
                        self.current_page_number = 0
                        if rb.link == self.url_target:
                            self.status = 'menu_win'
                        else:
                            print("you choose the page : ",  rb.link)
                            self.pages_list = create_page_list(rb.link)
                            self.buttons = create_button_page(self.pages_list, self.current_page_number)
                            self.game_group = pygame.sprite.Group(self.buttons)
                            self.url_current = rb.text
                            
                    if rb.rect.collidepoint(pygame.mouse.get_pos()) and event.button == 1 and rb.type == 'next':
                        self.current_page_number += 1
                        self.buttons = create_button_page(self.pages_list, self.current_page_number)
                        self.game_group = pygame.sprite.Group(self.buttons)

                    if rb.rect.collidepoint(pygame.mouse.get_pos()) and event.button == 1 and rb.type == 'previous':
                        self.current_page_number -= 1
                        self.buttons = create_button_page(self.pages_list, self.current_page_number)
                        self.game_group = pygame.sprite.Group(self.buttons)

                    #Si on rappuie dessus => self.path ayant changé => fait planter le jeu
                    if rb.rect.collidepoint(pygame.mouse.get_pos()) and event.button == 1 and rb.type == 'show_path':
                        self.path_object = create_path_label(self.path)
                        self.path_group = pygame.sprite.Group(self.path_object)
                

    #Fonction de gestion des mises à jours de statut dans pygame.                    
    def update(self):
        for rb in self.buttons:
            if rb.rect.collidepoint(pygame.mouse.get_pos()):
                rb.image = rb.hover_image
            else :
                rb.image = rb.button_image
        if self.status == 'menu_game' and self.score_count > 0:
            self.score_count -= (1/60)
        elif self.status == 'menu_game' :
            self.score_count = 0
        if self.score_count <= 0:
            #Devrait amener à menu_lose mais pas de design fait.
            self.status = 'menu_home'

    #Fonction d'affichage dans pygame.
    def display(self):
        self.screen.fill("grey")
        #Si je met cette condition, les textes ne sont plus centré. Je ne comprend pas donc je la retire, ca fait que nous initions 60x par seconde les labels ce qui n'est pas optimisé
        #if self.game_label_header == None :
        self.game_label_header = [
                                    Label(50, 10, x-100, h, 'start', font25, beautify(self.url_start)),
                                    Label(50, 50, x-100, h, 'current', font25, beautify(self.url_current)),
                                    Label(50, 90, x-100, h, 'target', font25, beautify(self.url_target)),
                                    Label(50, 140, x-100, h, 'score_count', font25, str(int("{:.0f}".format(self.score_count))))
                                ]
        header_group = pygame.sprite.Group(self.game_label_header)

        if self.status == 'menu_home':
            menu_group.draw(self.screen)

        if self.status == 'menu_game':
            self.game_group.draw(self.screen)
            header_group.draw(self.screen)

        #Pas de gestion de scoring fait. Mais aurait put être fait avec stockage dans un fichier annexe (Risque de triche, voir pour crypter ce qu'il y a dans le texte)
        if self.status == 'menu_score':
            score_group.draw(self.screen)
            
        #Il manque un menu de defaite
        if self.status == 'menu_lose':
            print("You Lose")

        if self.status == 'menu_win':
            path_group.draw(self.screen)
            pygame.sprite.Group(Label(550, 100, w, h, 'start', font25,'You Win !')).draw(self.screen)
            if self.path_group != None:
                self.path_group.draw(self.screen)
            self.buttons = path_buttons    
        pygame.display.flip()

    #Fonction qui gère le run et l'appel des 3 autres fonctions. Gère aussi les fps (ici 60/sec)
    def run(self):
        while self.running:
            self.handling_events()
            self.update()
            self.display()
            self.clock.tick(60)

#Fonction qui appel la logique du wikigame
def create_page_list(url):
    links_list = get_links(url)
    filtered_links_list = filter_link(links_list)
    return pagination_link(filtered_links_list)

#Fonction qui setup les boutons pour la page de jeu.
def create_button_page(pages_list, current_page):
    print("start : create_button_page")
    print("pages_list len: ", len(pages_list))
    print("current_page number: ", current_page)
    y = 200
    w = 450
    h = 20
    list_buttons =[]
    count = 0
    if len(pages_list) != 0 :
        links_dico = transform_list_to_dico(pages_list[current_page])
        for key, value in links_dico.items():
            if count < 10:
                list_buttons.append(Button(50, y +30*count, w, h, 'game', font20, key, value))
            else :
                list_buttons.append(Button(580, y +30*count - 300, w, h, 'game', font20, key, value))
            count += 1
    if current_page > 0:
        list_buttons.append(Button(175, 600, 200, h, 'previous', font20, 'Previous'))
    if current_page < len(pages_list) -1:
        list_buttons.append(Button(705, 600, 200, h, 'next', font20, 'Next'))
    list_buttons.append(Button(450, 600, 180, h, 'reset', font20, 'Reset to Menu'))
    return list_buttons

#Fonction qui génère les label pour afficher le path final en cas de victoire
def create_path_label(path):
    y = 200
    w = 450
    h = 20
    label_path_list = []
    count = 0
    for item in path:
        label_path_list.append(Label(50, y +30*count, w, h, 'start', font25, str(count+1) + "/ "+ item))
        count += 1
    return label_path_list     

pygame.init()

font25 = pygame.font.SysFont(None, 25)
font20 = pygame.font.SysFont(None, 20)
x = 1080
y = 720
w = 150
h = 20
screen = pygame.display.set_mode((x, y))

#La gestion des boutons et des sprite de pygame. Une partie ce trouve ici par facilité, une autre directement dans les boucles du jeu.
menu_buttons = [
        Button(x/2-w/2, y/2, w, h, 'start', font25, 'Start'),
        Button(x/2-w/2, y/2 + h*2, w, h, 'score', font25, 'Score'),
        Button(x/2-w/2, y/2 + h*4, w, h, 'quit', font25, 'Quit')
        ]
menu_group = pygame.sprite.Group(menu_buttons)

score_buttons = [   
        Button(x/2-w/2, y/2, w, h, 'start', font25, 'Start'),
        Button(x/2-w/2, y/2 + h*2, w, h, 'menu', font25, 'Menu')
        ]
score_group = pygame.sprite.Group(score_buttons)

path_buttons = [   
        Button(50, 100, 100, 20, 'show_path', font25, 'Historic'),
        Button(50, 150, 100, 20, 'menu', font25, 'Menu')
        ]
path_group= pygame.sprite.Group(path_buttons)



game = Game(screen)
game.run()

pygame.quit()
exit()