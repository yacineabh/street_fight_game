import pygame
from fighter2 import Fighter
pygame.init()

#screen settings
screen_width=1000
screen_height=600
clock=pygame.time.Clock()
fps=60
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('fight steet game')

red=(255,0,0)
yellow=(255,255,0)

def draw_health_bar(health,color,x,y):
    ratio=health/100
    pygame.draw.rect(screen,color,(x,y,400*ratio,30))

#images
warrior_sheet=pygame.image.load('warrior.png')
warrior_animation_steps=[10,8,1,7,7,3,7]
warrior_size=162
warrior_scale=4
warrior_offset=(70,56)
warrior_data=[warrior_size,warrior_scale,warrior_offset]

wizard_sheet=pygame.image.load('wizard.png')
wizard_animation_steps= [8,8,1,8,8,3,7] 
wizard_size=250
wizard_scale=3
wizard_offset=(112,107)
wizard_data=[wizard_size,wizard_scale,wizard_offset]

#background
bg_image=pygame.image.load('background.jpg')
bg_image=pygame.transform.scale(bg_image,(screen_width,screen_height))


#create objects
fighter1=Fighter(1,200,310,False,warrior_sheet,warrior_data,warrior_animation_steps)
fighter2=Fighter(2,700,310,True,wizard_sheet,wizard_data,wizard_animation_steps)

run=True
while run:
    clock.tick(fps)
    screen.blit(bg_image,(0,0))
    draw_health_bar(100,red,50,50)
    draw_health_bar(fighter1.health,yellow,50,50)
    draw_health_bar(100,red,550,50)
    draw_health_bar(fighter2.health,yellow,550,50)
    
    fighter1.update()
    fighter2.update()
    fighter1.move(screen_width,screen_height,screen,fighter2)
    fighter2.move(screen_width,screen_height,screen,fighter1)
    
    fighter1.draw(screen)
    fighter2.draw(screen)
    
    
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
            
    
    pygame.display.update()