import pygame
pygame.init()

red=(255,0,0)
class Fighter():
    def __init__(self,P,x,y,flip,sheet,data,animation_steps) :
        self.rect=pygame.Rect(x,y,80,180)
        self.size=data[0]
        self.scale=data[1]
        self.offset=data[2]
        self.vel_y=0
        self.jumped=False
        self.health=100
        self.flip=flip
        self.type_attack=0
        self.attacking=False
        self.data=data
        self.animation_list=self.load_images(sheet,animation_steps)
        self.action=0
        self.index_frame=0
        self.image=self.animation_list[self.action][self.index_frame]
        self.update_time=pygame.time.get_ticks()
        self.running=False
        self.hitted=False
        self.alive=True
        self.player=P
        self.attacking_cooldown=0
        
    def load_images(self,sheet,animation_steps):
        animation_list=[]
        y=0
        for animation in animation_steps:
            tmp_list=[]
            for x in range(animation) :
                tmp_img=sheet.subsurface(x*self.size,y*self.size,self.size,self.size)
                tmp_list.append(pygame.transform.scale(tmp_img,(self.size*self.scale,self.size*self.scale)))
            y+=1
            animation_list.append(tmp_list)
        return animation_list
        
    def move(self,screen_width,screen_height,screen,target):
        speed=10
        dx=0
        dy=0
        gravity=2
        self.running=False
        if self.attacking==False and self.alive:
            if self.player==1:
            #getting key presses
                key=pygame.key.get_pressed()
                if key[pygame.K_LEFT]:
                    dx-=speed
                    self.running=True
                if key[pygame.K_RIGHT]:
                    dx+=speed
                    self.running=True
                if key[pygame.K_UP] and not(self.jumped):
                    self.vel_y=-30
                    self.jumped=True
                if key[pygame.K_k] or key[pygame.K_l]:
                    self.attack(screen,target)
                    if key[pygame.K_k]:
                        self.type_attack=1
                    elif key[pygame.K_l]:
                        self.type_attack=2
            elif self.player==2:
                key=pygame.key.get_pressed()
                if key[pygame.K_q]:
                    dx-=speed
                    self.running=True
                if key[pygame.K_d]:
                    dx+=speed
                    self.running=True
                if key[pygame.K_z] and not(self.jumped):
                    self.vel_y=-30
                    self.jumped=True
                if key[pygame.K_x] or key[pygame.K_c]:
                    self.attack(screen,target)
                    if key[pygame.K_x]:
                        self.type_attack=1
                    elif key[pygame.K_c]:
                        self.type_attack=2
                
            
        #check flping
        if self.rect.centerx>target.rect.centerx:
            self.flip=True
        else:
            self.flip=False
        
        #adding gravity
        self.vel_y+=gravity
        dy+=self.vel_y
        
        #check to keep the player in the screen
           # x direction 
        if self.rect.left+dx<0 :
            dx=0-self.rect.left
        elif self.rect.right+dx>screen_width:
            dx=screen_width-self.rect.right
            # y direction
        if self.rect.bottom+dy>screen_height-110:
            dy=screen_height-110-self.rect.bottom
            self.jumped=False
        
        #apply the movement
        self.rect.x+=dx
        self.rect.y+=dy
    
    
    def update(self):
        if self.health<=0:
            self.alive=False
            self.update_action(6)
        elif self.hitted:
            self.update_action(5)
        elif self.attacking:
            if self.type_attack==1:
                self.update_action(3)
            elif self.type_attack==2:
                self.update_action(4)
        elif self.jumped:
            self.update_action(2)
        elif self.running:
            self.update_action(1)
        else:
            self.update_action(0)
        animation_cooldown=50
        if pygame.time.get_ticks()-self.update_time>animation_cooldown:
            self.index_frame+=1
            self.update_time=pygame.time.get_ticks()
        
        if self.attacking_cooldown>0:
            self.attacking_cooldown -=1
        
        if self.index_frame>=len(self.animation_list[self.action]):
            self.index_frame=0
            if self.action==3 or self.action==4:
                self.attacking=False
            elif self.action==5:
                self.hitted=False
            elif self.action==6:
                self.index_frame=len(self.animation_list[self.action])-1
                
            
        
        self.image=self.animation_list[self.action][self.index_frame]
        
    def update_action(self,newaction):
        if newaction!=self.action:
            self.action=newaction
            self.index_frame=0
            self.update_time=pygame.time.get_ticks()
        
    def attack(self,screen,target):
        if self.attacking_cooldown==0:
            self.attacking=True
            attacking_rect=pygame.Rect(self.rect.centerx-250*self.flip,self.rect.y,250,self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health-=10
                target.hitted=True
            self.attacking_cooldown=40
        
        #pygame.draw.rect(screen,(0,255,0),attacking_rect)    
        
            
    def draw(self,screen):
        img=pygame.transform.flip(self.image,self.flip,False)
     #   pygame.draw.rect(screen,red,self.rect)
        screen.blit(img,(self.rect.x-self.offset[0]*self.scale,self.rect.y-self.offset[1]*self.scale))
        