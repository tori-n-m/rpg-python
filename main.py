import pygame
import random
import button

pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')

#define game variables 
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
potion_effect = 15
clicked = False
game_over = 0


#define fonts
font = pygame.font.SysFont('Times New Roman', 26)

#define colors
red = (255, 0, 0)
green = (0, 255, 0)



#load images
#background image
background_img = pygame.image.load('img/background/background.png').convert_alpha()
#panel image 
panel_img = pygame.image.load('img/icons/panel.png').convert_alpha()
#button images
potion_img = pygame.image.load('img/icons/potion.png').convert_alpha()
restart_img = pygame.image.load('img/icons/restart.png').convert_alpha()
#load victory and defeat images
victory_img = pygame.image.load('img/icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('img/icons/defeat.png').convert_alpha()

#sword image 
sword_img = pygame.image.load('img/icons/sword.png').convert_alpha()


#create function for drawing text
def draw_text(text, font, text_col, x, y):
     img = font.render(text, True, text_col)
     screen.blit(img, (x, y))

#function for drawing background
def draw_bg():
    screen.blit(background_img, (0, 0))


#function for drawing panel
def draw_panel():
        #draw panel rectangle
        screen.blit(panel_img, (0, screen_height - bottom_panel))
        #show knight stats
        draw_text(f'{knight.name} HP: {knight.hp}', font, red, 100, screen_height - bottom_panel + 10)
        for count, i in enumerate(bandit_list):
            #show name and health
            draw_text(f'{i.name} HP: {i.hp}', font, red, 550, (screen_height - bottom_panel + 10) + count * 60)


#fighter class
class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potions):
          self.name = name
          self.max_hp = max_hp
          self.hp = max_hp
          self.strength = strength
          self.start_potions = potions
          self.potions = potions
          self.alive = True
          img = self.image = pygame.image.load(f'img/{self.name}/idle/2.png')
          self.image = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
          self.rect = self.image.get_rect()
          self.rect.center = (x, y)

    def attack(self, target):
         #deal damage to enemy
         rand = random.randint(-5, 5)
         damage = self.strength + rand
         target.hp -= damage
         #check if target has died
         if target.hp < 1:
            target.hp = 0
            target.alive = False
            damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
            damage_text_group.add(damage_text)

    def reset (self):
        self.alive = True
        self.potions = self.start_potions
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0

    def draw(self):
        screen.blit(self.image, self.rect)

class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        #update with new health
        self.hp = hp
        #calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))


class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        #move damage text up
        self.rect.y -= 1
        #delete the text after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()


damage_text_group = pygame.sprite.Group()


knight = Fighter(200, 285, 'knight', 30, 10, 3)
bandit1 = Fighter(550, 285, 'bandit', 20, 6, 1)
bandit2 = Fighter(700, 285, 'bandit', 20, 6, 1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)

knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(550, screen_height - bottom_panel + 40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = HealthBar(550, screen_height - bottom_panel + 100, bandit2.hp, bandit2.max_hp)

#create buttons
potion_button = button.Button(screen, 100, screen_height - bottom_panel + 70, potion_img, 64, 64)
restart_button = button.Button(screen, 330, 275, restart_img, 120, 30)


run = True
while run: 

    clock.tick(fps)

    #draw background
    draw_bg()

    #draw panel 
    draw_panel()
    knight_health_bar.draw(knight.hp)
    bandit1_health_bar.draw(bandit1.hp)
    bandit2_health_bar.draw(bandit2.hp)

    #draw fighters
    knight.draw()
    for bandit in bandit_list:
        bandit.draw()

    #draw the damage text
    damage_text_group.update()
    damage_text_group.draw(screen)

    #control player action
    #reset action variables
    attack = False
    potion = False
    target = None
    #make sure mouse is visible
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, bandit in enumerate(bandit_list):
         if bandit.rect.collidepoint(pos):
              #hide mouse
              pygame.mouse.set_visible(False)
              #show sword in place of mouse cursor
              screen.blit(sword_img, pos)
              if clicked == True:
                   attack = True
                   target = bandit_list[count]
    if potion_button.draw():
         potion = True
    #show number of potions remaining
    draw_text(str(knight.potions), font, red, 150, screen_height - bottom_panel + 70)

    if game_over == 0:

        #player action
        if knight.alive == True:
            if current_fighter == 1:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    #look for player action
                    #attack
                        if attack == True and target != None:
                            knight.attack(target)
                            current_fighter += 1
                            action_cooldown = 0
                        #potion
                        if potion == True:
                            if knight.potions > 0:
                                #check if the potion would heal the player beyond max health
                                if knight.max_hp - knight.hp > potion_effect:
                                    heal_amount = potion_effect
                                else:
                                    heal_amount = knight.max_hp - knight.hp
                                knight.hp += heal_amount
                                knight.potions -= 1
                                damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), green)
                                damage_text_group.add(damage_text)
                                current_fighter += 1
                                action_cooldown = 0

        else:
            game_over = -1

        #enemy action
        for count, bandit in enumerate(bandit_list):
            if current_fighter == 2 + count:
                if bandit.alive == True:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                            #check if bandit needs to heal first
                            if (bandit.hp / bandit.max_hp) < 0.5 and bandit.potions > 0:
                                #check if the potion would heal the player beyond bandit health
                                if bandit.max_hp - bandit.hp > potion_effect:
                                    heal_amount = potion_effect
                                else:
                                    heal_amount = bandit.max_hp - bandit.hp
                                bandit.hp += heal_amount
                                bandit.potions -= 1
                                damage_text = DamageText(bandit.rect.centerx, bandit.rect.y, str(heal_amount), green)
                                damage_text_group.add(damage_text)
                                current_fighter += 1
                                action_cooldown = 0

                        #attack
                            else:
                                bandit.attack(knight)
                                current_fighter += 1
                                action_cooldown = 0

                else:
                    current_fighter += 1

        #if all fighters have had a turn, then reset
        if current_fighter > total_fighters:
            current_fighter = 1

    #check if all bandits are dead
    alive_bandits = 0
    for bandit in bandit_list:
        if bandit.alive == True:
            alive_bandits = 1

    if alive_bandits == 0:
        game_over = 1

    #check if game is over
    if game_over != 0:
        if game_over == 1:
            screen.blit(victory_img, (250, 50))
        if game_over == -1:
            screen.blit(defeat_img, (250, 50))
        if restart_button.draw():
            knight.reset()
            for bandit in bandit_list:
                bandit.reset()
            current_fighter = 1
            action_cooldown
            game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
             clicked = False

    pygame.display.update()

pygame.quit()