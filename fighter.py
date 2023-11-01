import pygame

pygame.init()

class Fighter():
    def __init__(self,x,y,data,sheet,animation_steps) :
        self.size=data[0]
        self.scale=data[1]
        self.offset=data[2]
        self.update_time=pygame.time.get_ticks()     
        self.animation_list=self.load_image(sheet,animation_steps)
        self.action=0 #
        self.frame_index=0
        self.image=self.animation_list[self.action][self.frame_index]
        self.rect=pygame.Rect((x,y,80,180))     
        self.vel_y=0
        self.jumped=False
        self.attack_type=0
        self.attacking=False
        self.attack_cooldown=0
        self.health=100
        self.flip=False
        self.running=False
        self.hitted=False
        self.alive=True
        
        
    def load_image(self,sheet,animation_steps):
        y=0
        animation_list=[]
        for animation in animation_steps:
            tmp_list_img=[]
            for x in range(animation):
                img=sheet.subsurface(x*self.size,y*self.size,self.size,self.size)
                tmp_list_img.append(pygame.transform.scale(img,(self.size*self.scale,self.size*self.scale)))
            animation_list.append(tmp_list_img)
            y+=1
        return animation_list
        
        
    def move(self,screen_width,height_width,screen,target):
        dx=0
        dy=0
        speed=10
        gravity=2
        self.attack_type=0
        self.running=False
        
              
        if not(self.attacking):
            key=pygame.key.get_pressed()
            # get the move 
            if key[pygame.K_RIGHT]:
                dx+=speed
                self.running=True
            if key[pygame.K_LEFT]:
                dx-=speed
                self.running=True
            if key[pygame.K_UP] and not(self.jumped):
                self.vel_y=-30
                self.jumped=True        
            self.vel_y+=gravity
            dy +=self.vel_y
            
            #get the attack
            if key[pygame.K_x] or key[pygame.K_c]:
                self.attack(screen,target)
                if key[pygame.K_x]: self.attack_type=1
                if key[pygame.K_c]:self.attack_type=2
            
            
            #check to keep the player in the screen 
            if self.rect.left+dx<0 :
                dx=-self.rect.left
            elif self.rect.right+dx>screen_width:
                dx=screen_width-self.rect.right
            
            if self.rect.bottom +dy >height_width-110:
                dy=height_width-110-self.rect.bottom
                self.jumped=False
            
            
            #set filp
            if target.rect.centerx> self.rect.centerx :
                self.flip=False
            else:
                self.flip=True
            
            #apply the move 
            self.rect.x +=dx
            self.rect.y +=dy
    
    def update(self):
        if self.health<=0:
            self.health=0
            self.alive=False
            self.update_action(6)
        elif self.hitted:
            self.update_action(5)
        elif self.attacking:
            if self.attack_type==1:
                self.update_action(3)
            elif self.attack_type==2:
                self.update_action(4)      
        elif self.jumped:
            self.update_action(2)
        elif self.running:
            self.update_action(1)
        else :
            self.update_action(0)
        
        animation_cooldown=50
        #reduce the cooldown to make the player able to kick
        if self.attack_cooldown>0:
            self.attack_cooldown -=1
            
            
        self.image=self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks()-self.update_time>animation_cooldown :
            self.frame_index +=1
            self.update_time=pygame.time.get_ticks()
            
        if self.frame_index>=len(self.animation_list[self.action]):
            if self.alive==False:
                self.frame_index=len(self.animation_list[self.action])-1
            else :    
                self.frame_index=0
                if self.action==3 or self.action==4:
                    self.attacking=False
                    self.attack_cooldown=15
                if self.action==5:
                    self.hitted=False
          
    def update_action(self,new_action):
        if new_action!=self.action:
            self.action=new_action
            self.frame_index=0
            self.update_time=pygame.time.get_ticks()
    
    def attack(self,screen,target):
        if self.attack_cooldown==0:
            self.attacking=True
            attacking_rect=pygame.Rect(self.rect.centerx-150*self.flip,self.rect.y,150,180)
            pygame.draw.rect(screen,(255,255,255),attacking_rect)
            if attacking_rect.colliderect(target.rect):
                target.health -=10
                target.hitted =True
        
    def draw(self,screen):
        pygame.draw.rect(screen,(255,0,0),self.rect)
        img=pygame.transform.flip(self.image,self.flip,False)
        screen.blit(img,(self.rect.x-self.offset[0]*self.scale,self.rect.y-self.offset[1]*self.scale))