from pygame import init,display,image,sprite,fastevent,FINGERDOWN,FINGERMOTION,font,time,gfxdraw,transform,mixer
from random import randint
from math import atan2,degrees
from os import walk
init()
fastevent.init()
#screen setup
Width=1080
Height=2290
screen=display.set_mode((Width,Height))
#color
black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
grey=(50,50,50)
finger_posx,finger_posy=0,0
#sound
laser_sound=mixer.Sound("laser.mp3")
laser_sound.set_volume(0.1)
#font & text
font=font.Font(None,30)
def cre_text(name,x,y):
	t=font.render(str(name),1,red)
	screen.blit(t,(x,y))
#image 
bg=image.load("bg.png").convert()
#sprite
def import_sprites(folder):
	for _,__,img in walk(folder):
		return [image.load(folder+i).convert_alpha() for i in img]
		
explosions=[import_sprites(f"explosions{i+1}/") for i in range(3)]
muzzles=import_sprites("muzzles/")

class Player(sprite.Sprite):
	def __init__(self,img_name):
		super().__init__()
		self.image=image.load(img_name).convert_alpha()
		self.rect=self.image.get_rect()
		self.rect.center=Width/2,2000
		self.is_moving=0
		self.index=0
		self.muzzle=muzzles
		max_size=max(self.image.get_width(),self.image.get_height())
		self.explosion=[transform.scale(i,(max_size,max_size)) for i in explosions[randint(0,2)]]
		self.health=self.image.get_width()
		self.die_index=0
		
	def check_movenment(self,down):
		self.is_moving=1 if down else 0
		
	def update(self,f_px,f_py):
		
		if self.health<=0:
			self.image=transform.scale(self.image,(0,0))
			screen.blit(self.explosion[int(self.die_index)],(self.rect.centerx-self.explosion[0].get_width()/2,self.rect.centery-self.explosion[0].get_height()/2))
			self.die_index+=0.5
			if self.die_index>=len(self.explosion):
				self.die_index=0
				self.kill()
		else:
			gfxdraw.box(screen,(self.rect.centerx-self.image.get_width()/2,self.rect.centery-100,self.health,10),red)
			screen.blit(self.muzzle[self.index],(self.rect.centerx-self.muzzle[self.index].get_width()/2,self.rect.top-50))
			self.index+=1
			if self.index>=len(self.muzzle):
				laser_sound.play()
				bullet=Bullet(player.rect.centerx,player.rect.top)
				bullet_group.add(bullet)
				self.index=0
			if self.is_moving and (f_px>self.rect.left-100 and f_px<self.rect.right+100 and f_py>self.rect.top-100 and f_py<self.rect.bottom+100) :
				self.rect.center=f_px,f_py

player_bullet=import_sprites("bullet/")[(randint(0,14))]
class Bullet(sprite.Sprite):
	def __init__(self,res_posx,res_posy):
		super().__init__()
		self.spreed=randint(-3,3)
		self.image=transform.rotate(player_bullet,degrees(atan2(40-0,self.spreed-0)-3.14159/2))
		self.rect=self.image.get_rect()
		self.rect.center=res_posx,res_posy
		
	def update(self):
		self.rect.centery-=40
		self.rect.centerx+=self.spreed
		if self.rect.centery<=0:
			self.kill()

enemy_imgs=import_sprites("enemys/")
class Enemy(sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image=enemy_imgs[randint(0,15)]
		self.rect=self.image.get_rect()
		self.rect.center=randint(50,1030),randint(-1000,0)
		self.health=self.image.get_width()
		self.speed=randint(2,5)
		self.bullet_time=randint(1500,6000)
		self.muzzle=muzzles
		max_size=max(self.image.get_width(),self.image.get_height())
		self.explosion=[transform.scale(i,(max_size,max_size)) for i in explosions[randint(0,2)]]
		self.index=0
		self.shoot=0
		self.die=0
		self.die_index=0
		
	def update(self,c_time):
		if c_time>self.bullet_time and c_time<self.bullet_time+50:
			self.shoot=1
		if self.shoot==1:
			screen.blit(self.muzzle[self.index],(self.rect.centerx-self.muzzle[self.index].get_width()/2,self.rect.bottom))
			self.index+=1
			if self.index>=len(self.muzzle):
				enemy_b=Enemy_b(self.rect.centerx,self.rect.bottom)
				enemy_b_group.add(enemy_b)
				self.index=0
				self.shoot=0
			
		self.rect.centery+=self.speed
		if self.rect.centery>Height+self.image.get_height() or self.health<=0:
			self.die=1
		if self.die==1:
			self.image=transform.scale(self.image,(0,0))
			screen.blit(self.explosion[int(self.die_index)],(self.rect.centerx-self.explosion[0].get_width()/2,self.rect.centery-self.explosion[0].get_height()/2))
			self.die_index+=0.5
			if self.die_index>=len(self.explosion):
				self.die_index=0
				self.die=0
				self.kill()
				enemy=Enemy()
				enemy_group.add(enemy)
		else:
			gfxdraw.box(screen,(self.rect.centerx-self.image.get_width()/2,self.rect.centery-self.image.get_height()/2,self.health,10),red)

enemy_bullet_imgs=import_sprites("enemys_bullet/")
class Enemy_b(sprite.Sprite):
	def __init__(self,res_posx,res_posy):
		super().__init__()
		self.image=enemy_bullet_imgs[randint(0,14)]
		self.rect=self.image.get_rect()
		self.rect.center=res_posx,res_posy
		self.speed=randint(10,20)
		
	def update(self):
		self.rect.centery+=self.speed
		if self.rect.centery>Height+self.image.get_height():
			self.kill()
			
#player setup
player_group=sprite.Group()		
player=Player("ship.png")
player_group.add(player)

bullet_group=sprite.Group()
#enemy setup
enemy_group=sprite.Group()
enemy_b_group=sprite.Group()

for i in range(15):
	enemy=Enemy()
	enemy_group.add(enemy)
#collision
def bullet_system():
	b_c_e=sprite.groupcollide(enemy_group,bullet_group,0,1)
	if b_c_e:
		for enem in b_c_e:
			enem.health-=50
		
def enemy_bullet_system():
	if sprite.spritecollide(player,enemy_b_group,1):
		player.health-=10
	
clock=time.Clock()
start_time=0
current_time=0

while 1:
	clock.tick(60)
	#fire rate
	current_time=time.get_ticks()-start_time
	if current_time>6050:
		start_time=time.get_ticks()
	#handle event
	for ev in fastevent.get():
		if ev.type==FINGERDOWN or ev.type==FINGERMOTION:
			finger_posx,finger_posy=ev.x*Width,ev.y*Height
		player.check_movenment(ev.type==FINGERDOWN or ev.type==FINGERMOTION)
	#draw
	screen.blit(bg,(0,0))
	player_group.draw(screen)
	bullet_group.draw(screen)
	enemy_group.draw(screen)
	enemy_b_group.draw(screen)
	#update
	player.update(finger_posx,finger_posy)
	bullet_system()
	enemy_bullet_system()
	enemy_group.update(current_time)
	bullet_group.update()
	enemy_b_group.update()
	display.update()