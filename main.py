import pygame
from fighter import Fighter
pygame.init()
#screen settings
screen_width=1000
screen_height=600
clock=pygame.time.Clock()
FPS=60
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Brawler')

#colors
red=(255,0,0)
yellow=(255,255,0)


def draw_bg():
    img=pygame.image.load('background.jpg').convert_alpha()
    img=pygame.transform.scale(img,(screen_width,screen_height))
    screen.blit(img,(0,0))

def draw_health_bar(health,x,y):
    ratio=health/100
    pygame.draw.rect(screen,red,(x,y,400,30)) 
    pygame.draw.rect(screen,yellow,(x,y,400*ratio,30)) 

warrior_sheet=pygame.image.load('warrior.png').convert_alpha()
warrior_animation_steps=[10,8,1,7,7,3,7]
warrior_size=162
warrior_scale=4
warrior_offset=(70,56)
warrior_data=[warrior_size,warrior_scale,warrior_offset]
    
wizard_sheet=pygame.image.load('wizard.png').convert_alpha()
wizard_animation_steps= [8,8,1,8,8,3,7] 
wizard_size=250
wizard_scale=3
wizard_offset=(112,107)
wizard_data=[wizard_size,wizard_scale,wizard_offset]


fighter_1=Fighter(200,310,warrior_data,warrior_sheet,warrior_animation_steps)
fighter_2=Fighter(700,310,wizard_data,wizard_sheet,wizard_animation_steps)


run=True
while run:
    clock.tick(FPS)
    draw_bg()
    
    fighter_1.move(screen_width,screen_height,screen,fighter_2)
   # fighter_2.move(screen_width,screen_height,screen,fighter_1)
    draw_health_bar(fighter_1.health,20,20)
    draw_health_bar(fighter_2.health,580,20)
    
    
    fighter_1.update()
    fighter_2.update()
    
    fighter_1.draw(screen)
    fighter_2.draw(screen)
    
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
            

    pygame.display.update()