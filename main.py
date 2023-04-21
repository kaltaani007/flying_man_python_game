import pygame
from pygame.locals import *

import random

pygame.init()

clock = pygame.time.Clock()
fps = 50

s_width = 800
s_height = 650

flying = False
gameOver = False


pass_pipe = False
score = 0


screen = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("flappy Bird")

# background image
bg = pygame.image.load("./img/bg.png")
ground_img = pygame.image.load("./img/ground.png")
button_img = pygame.image.load("./img/restart.png")

class Button():
    def __init__(self , x , y , img ):
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        screen.blit(self.image, (self.rect.x, self.rect.y))


    def draw(self):

        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):

            if pygame.mouse.get_pressed()[0] == 1:

                action = True


        screen.blit(self.image , (self.rect.x , self.rect.y))

        return action

btn = Button ( int(s_width / 2)  -50 , int(s_height / 2 ) - 50 , button_img )


# resetting the whole view






# variables
ground_pos = 0
rate_ground = 4

# TExt box
font = pygame.font.SysFont("Bauhaus 93" , 60 )

#color
white = ( 255 , 255, 255)

pipe_gap = 200
pipe_frq = 1500 #ms
last_pipe = pygame.time.get_ticks()


def draw_text (text , font , color , x , y ):
    img = font.render( text , True , color )
    screen.blit(img , (x, y))


class Man(pygame.sprite.Sprite):

    def __init__(self , x, y):
        pygame.sprite.Sprite.__init__(self)

        self.images = []

        for num in range (1 , 4):
            img = pygame.image.load(f'./img/man{num}.png')
            self.images.append(img)

        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False

    def update(self):

        if flying == True :

            self.vel += 0.5

            if self.vel > 8:
                self.vel = 8

            if self.rect.bottom > 520:
                self.vel = -15

            self.rect.y += int(self.vel)

            # Clicked event in python
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.vel = -10
                self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False



        if gameOver == False:

            self.counter += 1
            flapper = 40

            if self.counter > flapper:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0

            self.image = self.images[self.index]
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)


        else:

            self.image = pygame.transform.rotate(self.images[self.index], -90)

    def destroy(self):
        if self.rect.y > 500 or self.rect.y < 0 :
            self.kill()

class Pipes(pygame.sprite.Sprite):
    def __init__(self, x, y  , position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("./img/pipe.png")
        self.rect = self.image.get_rect()

        if position == 1:
            self.image = pygame.transform.flip(self.image , False , True )
            self.bottomleft = [x , y ]
        if position == -1 :
            #self.image = pygame.transform.flip(self.image, False, True)
            self.topleft = [x, y]



        self.rect.topleft = [x,y]

    def update(self):

        self.rect.x -= rate_ground
        if self.rect.x < 0:
            self.kill()


man_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flap = Man(100  , 170)

man_group.add(flap)


def reset_game():
    pipe_group.empty()
    #birds_group.empty()
    flap.rect.x = 100
    flap.rect.y = 150
    score = 0

    return score







run = True
while run:

    clock.tick(fps)

    screen.blit(bg, (0, 0))


    man_group.draw(screen)
    man_group.update()

    pipe_group.draw(screen)



    if len(pipe_group) > 0 :


        #print(right)


        if man_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and man_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and pass_pipe == False:

            pass_pipe = True
            #print(score)
            #print(pass_pipe)
            #print("pass")

        #man code
        if man_group.sprites()[0].rect.right - pipe_group.sprites()[0].rect.left == 230  and pass_pipe == False:

            pass_pipe = True
            #print(score)
            #print(pass_pipe)
            #print("pass")

        if pass_pipe == True :

            #print(birds_group.sprites()[0].rect.left)
            #print(pipe_group.sprites()[0].rect.right)

            if man_group.sprites()[0].rect.left  -   pipe_group.sprites()[0].rect.right > 0  :
                score += 1
                #print("cross")
                #print(score)
                pass_pipe = False

        #print(score)
        draw_text(str(score) , font , white , int (s_width/2) , 50)






    screen.blit(ground_img, (ground_pos, 530))


    # check for the conclusion
    if pygame.sprite.groupcollide(man_group , pipe_group , False , False ) or flap.rect.y < 0 :
        gameOver = True

    if flap.rect.bottom > 520 :
        gameOver = True

    if gameOver == True:

        #birds_group.empty()

        btn.draw()
        check = btn.draw()

        if check == True:
            gameOver = False

            #draw_text(str(score), font, white, int(s_width / 2), 50)
            score = reset_game()




    if gameOver == False and flying == True :

        time_now = pygame.time.get_ticks()

        if time_now - last_pipe > pipe_frq:

            pipe_height = random.randint(-100, 50 )



            btm_pipe = Pipes( s_width, int(s_height / 2) + pipe_height , -1)
            top_pipe = Pipes( s_width , int(s_height / 2) - 800 + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)

            last_pipe = time_now

        ground_pos -= rate_ground

        if abs(ground_pos) > 23:
            ground_pos = 0

        pipe_group.update()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and gameOver == False :
            flying = True

    pygame.display.update()



pygame.quit()



