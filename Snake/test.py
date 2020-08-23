#!pip install pygame
import pygame
import random
import math
import time
'''
The name shall be Jörmungandr
https://en.wikipedia.org/wiki/J%C3%B6rmungandr

By Mark Sicoli, Hithesh Yedlapati, and Saiyam Kothari
'''

pygame.init()
# GLOBAL VARIABLE #


# create screen(width,height)
screen = pygame.display.set_mode((800,600))

# create title and icon
pygame.display.set_caption('Jörmungandr')
icon = pygame.image.load('snake.png')
pygame.display.set_icon(icon)

# background
background = (150,150,150)
screen.fill(background)

# score
value = 0
highscore = 0
speedscore = 0
bombscore = 0
speed = False
bomb = False
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

hightextX = 550
hightextY = 10

modeX = 10
modeY = 70

# movement variables
x = 400
y = 300
x_change = 0
y_change = 0

mode_font = pygame.font.Font('freesansbold.ttf', 24)


def timer_hold (t):

    for i in range(t*100000):
       pass


def show_mode(x,y):
    mode = mode_font.render("Game Modes: Press 1 for Normal, 2 for Insane, 3 for Survival", True, (92,219,207))
    screen.blit(mode, (x,y))

def show_score(x,y,value):
    score = font.render("Score: " + str(value), True, (92,219,207))
    screen.blit(score, (x,y))

def high_score(x,y,value):
    global highscore
    global speedscore
    global bombscore

    if speed:
        speedscore = value if value > speedscore else speedscore
        score = font.render("High Score: " + str(speedscore), True, (92,219,207))
    elif bomb:
        bombscore = value if value > bombscore else bombscore
        score = font.render("High Score: " + str(bombscore), True, (92,219,207))
    else:
        highscore = value if value > highscore else highscore
        score = font.render("High Score: " + str(highscore), True, (92,219,207))
    screen.blit(score, (x,y))

def game_over():
    game_over_text = font.render("GAME OVER, Press 'ENTER' to Play Again", True, (255,0,0))
    screen.blit(game_over_text, (100,250))

def apple(sneke_parts):
        global speed
        if speed:
            left = random.randint(0, 29)
            top = random.randint(0, 23)
        else:
            left = random.randint(0, 38)
            top = random.randint(0, 23)
        while ((101+left*20,111+top*20) in sneke_parts) and speed:
            left = random.randint(0, 29)
            top = random.randint(0, 23)
        while ((11+left*20,111+top*20) in sneke_parts) and not speed:
            left = random.randint(0, 38)
            top = random.randint(0, 23)
        #pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(15 + left * 20, 115 + top * 20, length, width))
        return left,top

def bom(sneke_parts,bomb_parts):
    left = random.randint(0,38)
    top = random.randint(0,23)
    while (11+left*20,111+top*20) in sneke_parts or (20+left*20,120+top*20) in bomb_parts:
        left = random.randint(0,38)
        top = random.randint(0,23)
    return 20+left*20,120+top*20

def main():
    global speed
    global bomb
    t1 = time.time()
    t0 = time.time()
    x_change = 20
    y_change = 0
    count = 0
    value = 0
    bomb_parts = []
    if speed:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(98, 108, 604, 484), 2)
        sneke_parts = [(161, 231), (141, 231), (121, 231)]
    else:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(8, 108, 784, 484), 2)
        sneke_parts = [(131, 231), (111, 231), (91, 231)]
    for x, y in sneke_parts:
        pygame.draw.rect(screen, (0, 255, 0), [x, y, 18, 18])
    if bomb:
        b_left, b_top = bom(sneke_parts,bomb_parts)
        bomb_parts = [(b_left,b_top)]
    else:
        left, top = apple(sneke_parts)
    running = True
    breaking = False
    g_o = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change != 20:
                    x_change = -20
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change != -20:
                    x_change = 20
                    y_change = 0
                elif event.key == pygame.K_UP and y_change != 20:
                    x_change = 0
                    y_change = -20
                elif event.key == pygame.K_DOWN and y_change != -20:
                    x_change = 0
                    y_change = 20
                if event.key == pygame.K_RETURN:
                    main()
                    breaking = True
                if event.key == pygame.K_1:
                    speed = False
                    bomb = False
                    main()
                    breaking = True
                if event.key == pygame.K_2:
                    speed = True
                    bomb = False
                    main()
                    breaking = True
                if event.key == pygame.K_3:
                    speed = False
                    bomb = True
                    main()
                    breaking = True
            break

        if breaking:
            break
        x = sneke_parts[0][0] + x_change
        y = sneke_parts[0][1] + y_change
        if speed and not bomb:
            a_left = 103 + left * 20
            a_top = 113 + top * 20
        elif not bomb:
            a_left = 13 + left * 20
            a_top = 113 + top * 20

        if bomb and (time.time()-t0) > 2 and not g_o:
            b_left, b_top = bom(sneke_parts,bomb_parts)
            bomb_parts.append((b_left, b_top))
            t0 += 2

        screen.fill((150, 150, 150))

        # create boundaries
        if (x < 11 or x > 771 or y < 111 or y > 571) and not speed:
            g_o = True
            # game_over()
        elif (x < 101 or x > 681 or y < 111 or y > 571) and speed:
            g_o = True
        elif (x,y) in sneke_parts:
            g_o = True
            # game_over()
        elif not bomb and x == (a_left - 2) and y == (a_top - 2) and not g_o:
            sneke_parts.insert(0, (x, y))
            left, top = apple(sneke_parts)
            value += 1
        elif (x+9,y+9) in bomb_parts:
            g_o = True
        elif not g_o:
            sneke_parts.pop()
            sneke_parts.insert(0, (x, y))

        if bomb and not g_o:
            value = round(time.time()-t1)

        # outline (play area is 780 x 480)
        if speed:
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(98, 108, 604, 484), 2)
        else:
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(8, 108, 784, 484), 2)

        # pygame.draw.rect(screen, (0, 255, 0), [x, y, 18, 18])

        # pygame.draw.circle(screen, (0,0,0), (400,300), 7)

        if bomb:
            for x,y in bomb_parts:
                pygame.draw.circle(screen, (0,0,0), (x,y), 7)
        else:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(a_left, a_top, 14, 14))

        for x, y in sneke_parts:
            pygame.draw.rect(screen, (0, 255, 0), [x, y, 18, 18])

        show_mode(modeX, modeY)
        show_score(textX, textY, value)
        high_score(hightextX, hightextY , value)

        if g_o:
            game_over()

        pygame.display.update()
        # clock.tick(40)
        if speed:
            pygame.time.wait(50)
        else:
            pygame.time.wait(100)

        #print(time.time() - t0)

main()