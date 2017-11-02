#!/usr/bin/env python

import sys, pygame, random, time, math, glob
from itertools import repeat
assert sys.version_info >= (3,4), 'This script requires at least Python 3.4'


NORTH = math.pi
NORTHEAST = 5/4*math.pi
EAST = 3/2*math.pi
SOUTHEAST = 7/4*math.pi
SOUTH = 0.0
SOUTHWEST = math.pi/4
WEST = math.pi/2
NORTHWEST = 3/4*math.pi


def addVectors(vect1, vect2):
        """ Returns the sum of two vectors """
        (angle1, length1) = vect1
        (angle2, length2) = vect2
        x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
        y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
        
        angle  = 0.5 * math.pi - math.atan2(y, x)
        length = math.hypot(x, y)

        return (angle, length)

class Game:
        def __init__(self, font, color, points_position, lives_position):
                self.font = font
                self.color = color
                self.points_position = points_position
                self.lives_position = lives_position

        def updateColor(self):
                self.color = (random.randint(30, 255), random.randint(30, 255), random.randint(30, 255))
                
        def draw_points(self,screen,points):
                points = str(points)
                f = self.font.render(points,True,self.color)
                screen.blit(f,points_position)

        def draw_lives(self,screen,lives):
                lives = str(lives)
                f = self.font.render(lives,True,self.color)
                screen.blit(f,lives_position)


class Ball(pygame.sprite.Sprite):
        def __init__(self,size,position,vector,max_speed,elasticity,color,constraints):
                pygame.sprite.Sprite.__init__(self)
                self.size = size
                (self.angle,self.speed) = self.vector = vector
                self.init_vector = vector
                color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
                self.color = color
                self.constraints = constraints
                self.elasticity = elasticity
                self.image = pygame.Surface((size*2, size*2))
                self.image.fill((0, 0, 0))
                pygame.draw.circle(self.image, color, (size,size), size)
                self.image.set_colorkey((0,0,0))
                self.rect = self.image.get_rect()
                self.init_position = position
                (self.x, self.y) = position
                self.rect.x = int(self.x)
                self.rect.y = int(self.y)
                self.max_speed = max_speed
                self.min_speed = self.speed
                self.dying = False
                self.dead = False

        def update(self,paddles,blocks):
                if self.dying:
                        self.dead = True
                        return
                for s in range(0,int(self.speed)):
                        self.bounce_off_wall()
                        for paddle in paddles:
                                if pygame.sprite.collide_rect(self,paddle):
                                        self.bounce_off_paddle(paddle)
                        for block in blocks:
                                if pygame.sprite.collide_rect(self,block):
                                        self.bounce_off_block(block)
                                        block.dying = True
                        self.check_max_speed()
                        (self.x,self.y) = self.get_next_pos()
                        self.rect.x = int(self.x)
                        self.rect.y = int(self.y)

        def check_max_speed(self):
                (self.angle,self.speed) = self.vector
                if self.speed > self.max_speed:
                        self.speed = self.max_speed
                if self.speed < self.min_speed:
                        self.speed = self.min_speed
                while self.angle < 0:
                        self.angle += 2*math.pi
                while self.angle > 2*math.pi:
                        self.angle -= 2*math.pi

                # try to keep the angle close to multiples of 45 degrees
                if self.angle < math.pi/4:
                        self.angle += math.pi/float(random.randrange(6,12))
                elif self.angle > math.pi/4 and self.angle <= math.pi/2:
                        self.angle -= math.pi/float(random.randrange(6,12))
                elif self.angle > math.pi/2 and self.angle < 3/4*math.pi:
                        self.angle += math.pi/float(random.randrange(6,12))
                elif self.angle > 3/4*math.pi and self.angle <= math.pi:
                        self.angle -= math.pi/float(random.randrange(6,12))
                elif self.angle > math.pi and self.angle < 5/4*math.pi:
                        self.angle += math.pi/float(random.randrange(6,12))
                elif self.angle > 5/4*math.pi and self.angle <= 3/2*math.pi:
                        self.angle -= math.pi/float(random.randrange(6,12))
                elif self.angle > 3/2*math.pi and self.angle < 7/4*math.pi:
                        self.angle += math.pi/float(random.randrange(6,12))
                elif self.angle > 7/4*math.pi and self.angle <= 2*math.pi:
                        self.angle -= math.pi/float(random.randrange(6,12))
                self.vector = (self.angle,self.speed)
                

        def get_next_pos(self):
                x = self.x + math.sin(self.angle)
                y = self.y + math.cos(self.angle)
                return (x,y)
                        
        def bounce_off_wall(self):
                (width,height) = self.constraints
                wall_speed = self.speed*2*self.elasticity
                direction = -1
                if self.rect.right >= width:
                        direction = EAST
                        self.rect.right = width-1
                elif self.rect.left <= 0:
                        direction = WEST
                        self.rect.left = 1
                if self.rect.top <= 0:
                        direction = SOUTH
                        self.rect.top = 1
                elif self.rect.bottom >= height:
                        direction = NORTH
                        self.rect.bottom = height-1
                        self.dying = True
                if direction >= 0:
                        self.vector = addVectors(self.vector,(direction,wall_speed))
                        (self.angle,self.speed) = self.vector

        def bounce_off_paddle(self,paddle):
                pygame.mixer.Sound("cloth1.ogg").play()
                paddle_speed = self.speed*2
                direction = NORTH
                if self.rect.right == paddle.rect.left and self.rect.bottom == paddle.rect.top:
                        direction = NORTHWEST
                elif self.rect.left == paddle.rect.right and self.rect.bottom == paddle.rect.top:
                        direction = NORTHEAST
                elif self.rect.left == paddle.rect.right and self.rect.top == paddle.rect.bottom:
                        direction = SOUTHEAST
                elif self.rect.right == paddle.rect.left and self.rect.top == paddle.rect.bottom:
                        direction = SOUTHWEST
                if self.rect.bottom <= paddle.rect.centery:
                        direction = NORTH
                elif self.rect.top > paddle.rect.centery:
                        direction = SOUTH
                elif self.rect.left > paddle.rect.centerx:
                        direction = WEST
                elif self.rect.right < paddle.rect.centerx:
                        direction = EAST
                else:
                        direction = NORTH
                self.vector = addVectors(self.vector,(direction,paddle_speed))
                (self.angle,self.speed) = self.vector

        def bounce_off_block(self,block):
                block_speed = self.speed*2
                #corners first
                if self.rect.right == block.rect.left and self.rect.bottom == block.rect.top:
                        direction = NORTHWEST
                elif self.rect.left == block.rect.right and self.rect.bottom == block.rect.top:
                        direction = NORTHEAST
                elif self.rect.left == block.rect.right and self.rect.top == block.rect.bottom:
                        direction = SOUTHEAST
                elif self.rect.right == block.rect.left and self.rect.top == block.rect.bottom:
                        direction = SOUTHWEST
                if self.rect.bottom <= block.rect.centery:
                        direction = NORTH
                elif self.rect.top > block.rect.centery:
                        direction = SOUTH
                elif self.rect.left > block.rect.centerx:
                        direction = EAST
                elif self.rect.right < block.rect.centerx:
                        direction = WEST
                else:
                        direction = SOUTH
                self.vector = addVectors(self.vector,(direction,block_speed))
                (self.angle,self.speed) = self.vector

        def set_forces(self,gravity):
                self.gravity = gravity

        def reset(self):
                color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
                self.color = color
                #self.image.fill(color)
                pygame.draw.circle(self.image, color, (self.size,self.size), self.size)
                (self.angle,self.speed) = self.vector = self.init_vector
                (self.x,self.y) = self.position = (random.randint(0, screen_size[0]), self.init_position[1])
                self.rect.x = int(self.x)
                self.rect.y = int(self.y)
                self.dying = False
                self.dead = False

        def draw(self,screen):  
                screen.blit(self.image, (self.rect.x, self.rect.y))
        
class Paddle(pygame.sprite.Sprite):
        def __init__(self,size,position,max_speed,color,constraints):
                pygame.sprite.Sprite.__init__(self)
                #color = (random.randint(30, 255), random.randint(30, 255), random.randint(30, 255))
                self.color = color
                self.constraints = constraints
                self.vector = (0.0,0)
                (self.w, self.h) = size
                self.image = pygame.Surface((self.w, self.h))
                self.image.fill(color)
                self.rect = self.image.get_rect()
                (x, y) = position
                self.rect.x = x
                self.rect.y = y
                self.max_speed = max_speed

        def update(self,position):
                (x,y) = position
                (width,height) = self.constraints
                if x + self.w > width:
                        x = width - self.w
                self.position = (x,self.rect.y)
                self.rect.x = x
                self.rect.y = self.rect.y       

        def set_forces(self,gravity):
                self.gravity = gravity

        def draw(self,screen):  
                screen.blit(self.image, (self.rect.x, self.rect.y))

class Block(pygame.sprite.Sprite):
        def __init__(self,size,points,color):
                pygame.sprite.Sprite.__init__(self)
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                self.color = color
                (self.w, self.h) = size
                self.image = pygame.Surface((self.w, self.h))
                self.image.fill(color)
                self.rect = self.image.get_rect()
                self.rect.x = 0
                self.rect.y = -100
                self.points = points
                self.dying = False
                self.dead = False
        
        def move_to(self,origin,size,margin,col,row):
                (o_x,o_y) = origin
                (w,h) = size
                (x,y) = (o_x+col*(w+margin),o_y+row*(h+margin))
                self.rect.x = x
                self.rect.y = y

        def set_forces(self,gravity):
                self.gravity = gravity
        
        def update(self):
                if self.dying:
                        self.dead = True
        
        def draw(self,screen):  
                screen.blit(self.image, (self.rect.x, self.rect.y))

class StaticSprite(pygame.sprite.Sprite):
	def __init__(self, imgTitle, pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(imgTitle)
		self.rect = self.image.get_rect()
		self.rect.center = pos
                
def LerpColour(c1,c2,t):
    return (c1[0]+(c2[0]-c1[0])*t,c1[1]+(c2[1]-c1[1])*t,c1[2]+(c2[2]-c1[2])*t)

# this function creates our shake-generator
# it "moves" the screen to the left and right
# three times by yielding (-5, 0), (-10, 0),
# ... (-20, 0), (-15, 0) ... (20, 0) three times,
# then keeps yieling (0, 0)
def shake():
	s = -1
	for _ in range(0, 3):
		for x in range(0, 20, 5):
			yield (x*s, 0)
		for x in range(20, 0, 5):
			yield (x*s, 0)
		s *= -1
	while True:
		yield (0, 0)

list_of_colors = [(255, 255, 255), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)), (255, 255, 255), (255, 255, 255)]

no_steps = 50

# create a class for Particles derived from pygame.sprite.Sprite
# pygame.sprite.Sprite allows us to collide objects easily
class Particle(pygame.sprite.Sprite):
    # constructor that takes starting x and y positions
    # change in x and y which provides speed and direction of the particle
    # size of the particle
    def __init__(self, x, y, dx, dy, size):
        # create a displayable surface to represent the particle and
        # create a rect object from the image
        self.image = pygame.Surface((size, size))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()

        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.color = color
        self.image.fill(color)
        
        # assign the passed values to the class objects own values
        self.x_velocity = dx
        self.y_velocity = dy
        self.rect.x = x
        self.rect.y = y

        # create gravity effect (optional in the class update function)
        self.gravity = 0.25

    def update(self):
        # add gravity effect (optional but cool)
        self.y_velocity += self.gravity

        # move the rect based on the current velocity of the particle
        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity

    def display(self, main_surface):
        # display the particles image to the main surface at the particles coordinates
        main_surface.blit(self.image, (self.rect.x, self.rect.y))

def create_particles(p_list, position):

    # define an amount of particles to create
    particle_count = random.randint(10, 30)

    # create a range of numbers that exculdes 0, if 0 is included then
    # there is a chance both x and y velocity will be 0 and then the
    # particle will just be stationary
    numbers = list(set(range(-5, 5)) - {0})

    # loop for the particle count
    for i in range(0, particle_count):

        # create a particle using the position passed in the function,
        # random velocity in x and random velocity in y
        # random size from 1 to 5
        p = Particle(position[0], position[1], random.choice(numbers), random.choice(numbers), random.randint(1, 5))

        # add the particle to the list
        p_list.append(p)

    # return the new list
    return p_list

def remove_particles(p_list):
    # loop for the size of the particle list, elements are checked moving backwards through the list size
    # this is because removing an element from a python list just shifts everything back so in a list of
    # [2, 5, 7, 3, 6] lets say elements 0 and 4 need to be removed if element 0 is removed the list
    # becomes [5, 7, 3, 6] now trying to remove element 4 would class as iterating out of range. removing
    # list elements backwards avoids this issue.
    for x in range(0, len(p_list)):
        try:
            # check if the particle is no longer colliding with the screen
            if p_list[len(p_list) - x - 1].rect.y > screen_size[1]:
                # remove the particle from the list
                del p_list[len(p_list) - x - 1]
        except:
            # break in case [len(p_list) - x - 1] is out of range
            # I'm not entirely sure why it gets out of range but maybe one of you
            # could tell me! Please let me know becasue it is bothering me!
            # the missed particle will be removed on the next update anyway
            # because the particle will just get tested next update as it
            # is still in the list
            break

    # return the new list
    return p_list

def update_all(u_list):
    # loop for the length of the list
    for i in range(0, len(u_list)):
        # call the update function of each list element
        u_list[i].update()

def display_all(d_list, main_surface):
    # fill the screen again with black
    #main_s.fill((0, 0, 0))

    # loop for the length of the list
    for i in range(0, len(d_list)):
        # call the display function for each list element and pass the main surface to it
        d_list[i].display(main_surface)

#-------------------------------------------------------------------------------
        
screen_size = (1024,768)
FPS = 60
points_position = (10,10)
lives_position = (990,10)
display_color = (255,255,255)

paddle_pos = (0,700)
paddle_size = (100,15)
paddle_color = (0,0,0)
paddle_max_speed = 60

num_blocks = 50
num_block_rows = 10
block_pos = (40,80)
block_size = (15,15)
block_margin = 4
block_points = 10
block_color = (255,255,255)

ball_pos = (200,300)
ball_size = 10
ball_elasticity = 1
ball_color = (255,255,255)
ball_initial_vector = (7/4*math.pi, 15.0)
ball_max_speed = 15.0

gravity = (math.pi,9.8)

def main():
        pygame.init()
        font = pygame.font.SysFont("arial",30)
        
        org_screen = pygame.display.set_mode(screen_size)
        screen = org_screen.copy()
        screen_rect = screen.get_rect()
        # 'offset' will be our generator that produces the offset
        # in the beginning of screen shake, we start with a generator that 
        # yields (0, 0) forever
        offset = repeat((0, 0))

        # create an empty list to hold particle objects
        particle_list = []
        
        game = Game(font,display_color,points_position,lives_position)
        clock = pygame.time.Clock()
        
        livesTotal = 25
        lives = livesTotal
        points = 0
        
        balls = pygame.sprite.Group()
        paddles = pygame.sprite.Group()
        blocks = pygame.sprite.Group()
        pos = (0,0)

        if not pygame.mixer:
                pygame.mixer.init(frequency=ogg.info.sample_rate)
        pygame.mixer.stop()
        pygame.mixer.Sound("Thin_Lizzy_-_Jailbreak_minus_.ogg").play(-1)

        gradient = []
        for i in range(len(list_of_colors)-2):
            for j in range(no_steps):
                gradient.append(LerpColour(list_of_colors[i],list_of_colors[i+1],j/no_steps))
        gradient_current = 0
        
        (start_x,start_y) = block_pos
        (block_w,block_h) = block_size
        for r in range(0,num_block_rows):
                for b in range(0,num_blocks):
                        points = block_points*(r+1)
                        block = Block(block_size,points,block_color)
                        block.move_to(block_pos,block_size,block_margin,b,r)
                        blocks.add(block)
        balls.add(Ball(ball_size,ball_pos,ball_initial_vector,ball_max_speed,ball_elasticity,ball_color,screen_size))
        paddles.add(Paddle(paddle_size,paddle_pos,paddle_max_speed,paddle_color,screen_size))
        
        while lives > 0 and len(blocks):
                clock.tick(FPS)
                
                screen.fill(gradient[gradient_current])
                org_screen.fill(gradient[gradient_current])
                if (gradient_current < len(gradient) - 1):
                        gradient_current += 1
                else:
                        gradient_current = 0
                
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit(0)
                        if event.type == pygame.MOUSEMOTION:
                                pos = pygame.mouse.get_pos()
                        if event.type == pygame.MOUSEBUTTONUP:
                                pos = pygame.mouse.get_pos()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                                pos = pygame.mouse.get_pos()
                        if event.type == pygame.KEYDOWN:
                                keys = pygame.key.get_pressed()

                for ball in balls:
                        ball.set_forces(gravity)
                balls.update(paddles,blocks)
                balls.draw(screen)

                for paddle in paddles:
                        paddle.set_forces(gravity)
                paddles.update(pos)
                paddles.draw(screen)

                for block in blocks:
                        block.set_forces(gravity)
                #blocks.update()
                #blocks.draw(screen)
                for block in blocks:
                        if block.dead:
                                points += block.points
                                blocks.remove(block)
                                particle_list = create_particles(particle_list, block.rect) #create particles from the point it was clicked
                                pygame.mixer.Sound("successful_hit.ogg").play()
                blocks.update()
                blocks.draw(screen)
                for ball in balls:
                        if ball.dead:
                                lives -= 1
                                points -= block.points * 5
                                ball.reset()
                                offset = shake() #create a new shake-generator
                                pygame.mixer.Sound("classic_hurt.ogg").play()
                                
                # update and display the particle list
                update_all(particle_list)
                display_all(particle_list, screen)
                # check if any particles need to be removed
                particle_list = remove_particles(particle_list)
                #draw UI
                game.draw_lives(screen,lives)
                game.draw_points(screen,points)
                game.updateColor()
                org_screen.blit(screen, next(offset))
                pygame.display.flip()
        pygame.mixer.stop()
        if (lives > 0):
                pygame.mixer.Sound("Sweet_Victory_Lyrics.ogg").play()
                endingSprite = StaticSprite("victory_logo.gif", (512, 384))
        else:
                pygame.mixer.Sound("You_are_Dead.ogg").play()
                endingSprite = StaticSprite("Game Over.png", (512, 384))
        pygame.sprite.Group(endingSprite).update()
        pygame.sprite.Group(endingSprite).draw(screen)
        pygame.sprite.Group(endingSprite).draw(org_screen)
        #org_screen.blit(screen, next(offset))
        pygame.display.flip()
        #pygame.quit()
        #sys.exit(0)

if __name__ == '__main__':
        playAgain = True
        while True:
                if playAgain:
                        main()
                        playAgain = False
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit(0)
                        if event.type == pygame.MOUSEBUTTONDOWN:
                                playAgain = True
                        if event.type == pygame.KEYDOWN:
                                playAgain = True
