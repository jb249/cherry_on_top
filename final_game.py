'''
Name: Jack Butler, Hyun Jin Lim
File: final_game.py
'''

import pygame, sys, random
from pygame.locals import *

ORANGE =   (255, 128, 0)
BLUE =     (0,   0,   255)
GREEN =    (0,   128, 0)
PURPLE =   (128, 0,   128)
RED =      (255, 0,   0)
YELLOW =   (255, 255, 0)
NAVYBLUE = (0,   0,   128)
WHITE =    (255, 255, 255)
BLACK =    (0,   0,   0)
SKY =      (135,206,250)
#"The Other RGB Color Chart." TayloredMktg.com. Assistance given to the author,
#online reference table. I used this table to find the RGB values for sky blue.
#West Point, NY. 5 May 2019. <http://www.tayloredmktg.com/rgb/>

def init_main_window(dimensions, caption):
	pygame.init()
	pygame.display.set_caption(caption)
	return pygame.display.set_mode(dimensions)

image_file_type = '.gif'

class Cone (object):
	def __init__ (self, img = 'cone3'+image_file_type):
		self.image = pygame.image.load('gif_images/{}'.format(img))
		self.image  = pygame.transform.scale(self.image,(500,175))
		#"How to Scale Images to Screen Size in pygame." StackOverflow.com.
		#Assistance given to the author, help forum response. I used this help
		#forum to learn how to scale an image in pyGame. West Point, NY. 5 May 2019.
		#<https://stackoverflow.com/questions/20002242/how-to-scale-images-to-screen-size-in-pygame>
		self.rect = self.image.get_rect()
		self.contents = []
	def __repr__ (self):
		return "cone(contents={})".format(self.contents)
	def __str__ (self):
		return "Cone Object"
	def load_image (self):
		return pygame.image.load('gif_images/{}'.format(self.image))
	def add_topping (self,topping):
		self.contents.append(topping)

class Topping (object):
	def __init__ (self, type = 'V'):
		self.type = type
		#Menu dictionary contains the name, image file name, and value of each topping.
		self.menu = {'V':('Vanilla','vanilla',1.00),'C':('Chocolate','chocolate',1.00),'S':('Strawberry','strawberry',1.00),'L':('Lemon','lemon',1.00),'W':('Watermelon','watermelon',1.00),'M':('Mint','mint',1.00),'Ch':('Cherry','cherry2',2.00)}
		self.name = self.menu[self.type][0]
		self.image = pygame.image.load('gif_images/{}{}'.format(self.menu[self.type][1],image_file_type))
		if self.type != 'Ch':
			self.image  = pygame.transform.scale(self.image,(140,100))
		self.value = self.menu[self.type][2]
		self.rect = self.image.get_rect()
		#Kenlon, Seth. "What's a Hero Without a Villain? How to add one to your
		#Python Game." Assistance given to the author, tutorial article from OpenSource.com.
		#I took some ideas from this pygame tutorial to improve the class initialization.
		#This tutorial showed how to simplify the use of a class by defining additional
		#self attributes, such as the self.rect, self.image, and self.name attributes.
		#West Point, NY. 23 Apr. 2019. <https://opensource.com/article/18/5/pygame-enemy>

	def __repr__ (self):
		return "topping(type='{}', name='{}', image='{}',value = ${})".format(self.type, self.name, self.image, self.value)

	def __str__ (self):
		return "Topping: {}".format(self.name)

	def move (self, level):
		speed = 8*(level//5+1)
		self.rect.y += speed
		return self.rect.y

#Generates a dictionary with topping names as keys and quantities of toppings as values
def generate_order(toppings,level):
	order = {}
	for i in range(level+2):
		random_type = toppings[random.randrange(len(toppings)-1)]
		topping = Topping(random_type)
		if topping.name not in order.keys():
			order[topping.name] = 1
		else:
			order[topping.name] += 1
	return order

#Return True when topping hits the ground
def splat (topping,disp):
	if topping.rect.y >= disp.get_height():
		return True
	return False

#Check order completion status. Return True if order is incomplete.
def check_order (order):
	completed_toppings = 0
	for topping in order.keys():
		if order[topping] == 0:
			completed_toppings += 1
	if completed_toppings < len(order):
		return True
	return False

def draw_text(text, font, surface, x, y):
	textObj = font.render(text, 2, BLACK)
	textrect = textObj.get_rect()
	textrect.topleft = (x,y)
	surface.blit(textObj, textrect)

def terminate():
	pygame.quit()
	sys.exit()

#3 Main game loop
#3a. Check for events
#3b. Do calculations
#3c. Display result

def game_intro():
	#Set initial conditions
	DISPLAYSURF = init_main_window((400,750),"Cherry on Top")
	fps_clock = pygame.time.Clock()
	FPS = 15

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					play_game()

		title_image = pygame.image.load('gif_images/title_screen'+image_file_type)
		title_image = title_image.convert()
		title = title_image.get_rect()
		title.center = (DISPLAYSURF.get_width()/2,DISPLAYSURF.get_height()/2)

		#Display background
		DISPLAYSURF.fill(SKY)

		#Display title screen image
		DISPLAYSURF.blit(title_image,title)

		#Update the display
		fps_clock.tick(15)
		pygame.display.update()

    #Harrison. Assistance given to the author, code example. We copied Harrison's
    #code example for a game intro from PythonProgramming.net. We used these same
	#concepts for the level intro and game over screens as well. West Point, NY.
    #10 Apr. 2019. <https://PythonProgramming.net/pygame-start-menu-tutorial/>.

def level_intro(level,total_score,order):
	#Set initial conditions
	DISPLAYSURF = init_main_window((400,750),"Cherry on Top")
	fps_clock = pygame.time.Clock()
	FPS = 15
	font1 = pygame.font.SysFont(None,80)
	font2 = pygame.font.SysFont(None,40)

	while True:
		for event in pygame.event.get():
			print(event)
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					return

		#Display the background
		DISPLAYSURF.fill(SKY)

		#Display a cherry at the top of the screen
		cherry_image = pygame.image.load('gif_images/cherry'+image_file_type)
		cherry = cherry_image.get_rect()
		cherry.y = 40
		cherry.centerx = DISPLAYSURF.get_width()/2
		DISPLAYSURF.blit(cherry_image,cherry)

		#Display the level number
		draw_text("Level {}".format(level), font1, DISPLAYSURF, 90, 200)

		draw_text("Upcoming Order:", font2, DISPLAYSURF, 90, 275)

		#Display the ingredients of the upcoming order, which have been randomly
		#generated with the play_game function prior to calling level_intro.
		text_pos = 325
		for k,v in order.items():
			draw_text("{}: {}".format(k,v), font2, DISPLAYSURF, 100, text_pos)
			text_pos+=40

		#Update the display
		fps_clock.tick(15)
		pygame.display.update()

#Displays screen indicating that the player has lost the level and the game is over.
def game_over(total_score):
	#Set initial conditions
	DISPLAYSURF = init_main_window((400,750),"Cherry on Top")
	fps_clock = pygame.time.Clock()
	FPS = 15
	font = pygame.font.SysFont(None,40)

	while True:
		for event in pygame.event.get():
			print(event)
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					play_game()

		#Display the background
		DISPLAYSURF.fill(SKY)

		title_image = pygame.image.load('gif_images/game_over'+image_file_type)
		title = title_image.get_rect()
		title.center = (DISPLAYSURF.get_width()/2-10,DISPLAYSURF.get_height()/2)

		#Display Game Over screen image
		DISPLAYSURF.blit(title_image,title)

		draw_text("Final Score: $"+str(total_score), font, DISPLAYSURF, 90, (3/4)*DISPLAYSURF.get_height())

		#Update the display
		fps_clock.tick(15)
		pygame.display.update()

def play_game(level=1,total_score=0):

	score = 1
	tip = 0

	toppings = ['V','C','S','W','M','L','Ch']
	#V for Vanilla
	#C for Chocolate
	#S for Strawberry
	#W for Watermelon
	#M for Mint
	#L for lemon
	#Ch for Cherry

	#Create Order
	order = generate_order(toppings,level)

	#Create cone
	cone = Cone()

	#Bring up the level intro screen with the upcoming order
	level_intro(level,total_score,order)

	#Display the window
	DISPLAYSURF = init_main_window((400,750),"Cherry on Top")
	#game_intro()

	#Create initial topping and enable topping objects to move
	topping = Topping(toppings[random.randrange(len(toppings))])
	topping.rect.move_ip(100,10)

	FPS = 15
	fps_clock = pygame.time.Clock()
	font = pygame.font.SysFont(None,25)

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					terminate()
			elif event.type == MOUSEMOTION:
				cone.rect.x = event.pos[0]-53

		#clear the background
		DISPLAYSURF.fill(SKY)

		#Display the Topping
		DISPLAYSURF.blit(topping.image,topping.rect)

		#Move the topping. Topping fall speed depends on level.
		topping.move(level)


		height_above = 0
		#Display caught toppings on top of the cone
		for item in cone.contents:
			item.rect.centerx = cone.rect.x + 63
			item.rect.y = cone.rect.y - item.image.get_height() - height_above
			DISPLAYSURF.blit(item.image,item.rect)
			height_above += 75

		#Position of the top of the stack
		if len(cone.contents) > 0:
			top_height = cone.rect.y - height_above
		else:
			top_height = DISPLAYSURF.get_height() - cone.image.get_height()

		#Display the Cone
		DISPLAYSURF.blit(cone.image,cone.rect)
		if len(cone.contents) > 4:
			cone.rect.y = DISPLAYSURF.get_height() - cone.image.get_height() + 75*len(cone.contents[:-3])
		else:
			cone.rect.y = DISPLAYSURF.get_height() - cone.image.get_height()

		#Catch topping if topping makes contact with top of cone and is within certain range laterally from center of cone.
		#Cherry is a special situation. It is harder to catch, so it needs a wider range to make the game playable.
		if abs(topping.rect.y - top_height + 75) <= 4:
			if abs(topping.rect.x - (cone.rect.x)) <= 50 and topping.name == 'Cherry':
			#Check if topping caught was a cherry, which determines Game Over or Level Complete.
				#If order is incomplete when cherry is caught, Game Over.
				if check_order(order):
					game_over(total_score)
				#If order is complete, continue. End level after score is finalized in the lines below.
				else:
					level +=1
					total_score += score*(1+tip/100)
					play_game(level,total_score)
				#If caught, take off one from remaining order and increase score and tip.

		#Catch all other non-cherry toppings.
		if abs(topping.rect.y - top_height + 75) <= 10:
			if abs(topping.rect.x - (cone.rect.x)) <= 20:
				if topping.name in order.keys() and order[topping.name] > 0:
					order[topping.name] -= 1
					score += topping.value
					tip += 1
				#If incorrect topping caught, decrease tip.
				elif tip >= 1:
					tip -= 1
				#Stick to top of cone
				cone.add_topping(topping)
				#Generate new topping
				topping = Topping(toppings[random.randrange(len(toppings))])
				topping.rect.y = 0
				topping.rect.x = random.randrange(DISPLAYSURF.get_width()-topping.image.get_width())

		#Generate new topping when topping hits the ground
		if splat (topping,DISPLAYSURF):
			topping = Topping(toppings[random.randrange(len(toppings))])
			topping.rect.y = 0
			topping.rect.x = random.randrange(DISPLAYSURF.get_width()-topping.image.get_width())

		#Display the score and the order
		draw_text("Level: {}".format(level), font, DISPLAYSURF, 10, 0)
		draw_text("Score: ${:.2f}".format(score), font, DISPLAYSURF, 10, 14)
		draw_text("Tip: {:.2f}%".format(tip), font, DISPLAYSURF, 10, 28)
		text_pos = 50

		#Display remaining order totals if order is not yet complete.
		if check_order(order):
			for k,v in order.items():
				draw_text("{}: {}".format(k,v), font, DISPLAYSURF, 10, text_pos)
				text_pos+=14
		#If order is complete, let the player know that they need to catch a cherry
		#to finish the level.
		else:
			draw_text("Order Complete!", font, DISPLAYSURF, 10, text_pos)
			draw_text("Catch the cherry on top!", font, DISPLAYSURF, 10, text_pos+14)

		fps_clock.tick(FPS)

		#update the display
		pygame.display.update()


if __name__=='__main__':
	game_intro()
