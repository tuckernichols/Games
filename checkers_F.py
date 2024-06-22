import pygame
import os
import time

r_count = 0  # make a bord of rectangles
WIDTH = 720  # eachsquare is 90 x 90
Window = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("checkers")
Window.fill((255, 255, 255))

backround_img = pygame.image.load(os.path.join("chessIMGs/chessBoardBackround.jpg"))

red_img = pygame.image.load(os.path.join("checkersIMGs/redChecker.png"))
gray_img = pygame.image.load(os.path.join("checkersIMGs/grayChecker.png"))
red_king = pygame.image.load(os.path.join("checkersIMGs/kingCheckerRed.png"))
gray_king = pygame.image.load(os.path.join("checkersIMGs/kingCheckerGray.png"))

Gray_piece = False


class BG:  # backround
    def __init__(self, x, y, image, ):
        self.image = pygame.transform.scale(image, (WIDTH, WIDTH))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        Window.blit(self.image, (self.rect.x, self.rect.y))


bg = BG(0, 0, backround_img)
selected_peice = False


class Checker():
    def __init__(self, image, ):
        self.image = pygame.transform.scale(image, (70, 70))

    def draw1(self, x, y):
        Window.blit(self.image, (x, y))
        # print(x,y)


def king_moves(start, color):
    global possibles
    possibles = [[start[0] - 1, start[1] - 1, "k"], [starting_spot[0] + 1, starting_spot[1] - 1, "k"]]
    possibles.append([start[0] - 1, start[1] + 1, "k"])
    possibles.append([starting_spot[0] + 1, starting_spot[1] + 1, "k"])
    if not color:
        print("red king")
        jumps_xx(opposite_checks=gray_checks, start=starting_spot, type='k')
        jumps_xx(opposite_checks=gray_checks, start=starting_spot, type='k')
        jumps_xx(opposite_checks=gray_checks, start=starting_spot, type='k')
        jumps_xx(opposite_checks=gray_checks, start=starting_spot, type='k')
        for r in red_checks:  # remove possible spots if theres a red peice there
            for p in possibles:
                if r[0:2] == p[0:2]:
                    possibles.remove(p)


    if color is True:
        print('gray king')
        jumps_xx(opposite_checks=red_checks, start=starting_spot, type='k')
        jumps_xx(opposite_checks=red_checks, start=starting_spot, type='k')
        jumps_xx(opposite_checks=red_checks, start=starting_spot, type='k')
        jumps_xx(opposite_checks=red_checks, start=starting_spot, type='k')
        for r in gray_checks:  # remove possible spots if theres a gray peice there
            for p in possibles:
                if r[0:2] == p[0:2]:
                    possibles.remove(p)

    possibles.append(start)
    print("king possibles = ", possibles)


red_checks = [[0, 0, "l"], [2, 0, "l"], [4, 0, "l"], [6, 0, "l"], [1, 1, "l"], [3, 1, "l"], [5, 1, "l"],[7, 1, 'l'], [0, 2, 'l'], [2, 2, 'l'],[4, 2, 'l'],[6, 2, 'l']]
gray_checks = [[1, 7, "l"], [3, 7, "l"], [5, 7, "l"], [7, 7, "l"], [0, 6, "l"], [2, 6, "l"], [4, 6, "l"],[6, 6, 'l'], [1, 5, 'l'], [3, 5, 'l'], [5, 5, 'l'],[7, 5, 'l'] ]
possibles = []


def jumps_xx(opposite_checks, start, type):
    global possibles
    for p in possibles:
        scan_k = [p[0], p[1], 'k']
        scan_l = [p[0], p[1], 'l']
        # print(scan_l,"and ", scan_k)
        if opposite_checks.count(scan_l) == 1 or opposite_checks.count(scan_k) == 1:
            a = p[0] - start[0]
            b = p[1] - start[1]
            if a == -1:
                if b == -1:
                    #print("up left")
                    if opposite_checks.count([scan_l[0] - 1, scan_l[1] - 1, 'l']) or opposite_checks.count([scan_k[0]-1, scan_k[1] - 1, 'k']) == 1:
                        possibles.remove(p)
                    else:
                        possibles.append([scan_k[0] - 1, scan_k[1] - 1, type])
                        possibles.remove(p)
                else:
                    #print("down left")
                    if opposite_checks.count([scan_l[0] - 1, scan_l[1] + 1, 'l']) or opposite_checks.count([scan_k[0]-1, scan_k[1] + 1, 'k']) == 1:
                        possibles.remove(p)
                    else:
                        possibles.append([scan_k[0] - 1, scan_k[1] + 1, type])
                        possibles.remove(p)
            else:
                if b == -1:
                    #print("up right")
                    if opposite_checks.count([scan_l[0] + 1, scan_l[1] - 1, 'l']) or opposite_checks.count([scan_k[0] + 1, scan_k[1] - 1, 'k']):
                        possibles.remove(p)
                    else:
                        possibles.append([scan_k[0] + 1, scan_k[1] - 1, type])
                        possibles.remove(p)
                else:
                    #print("down right")
                    if opposite_checks.count([scan_l[0] + 1, scan_l[1] + 1, 'l']) or opposite_checks.count([scan_k[0] + 1, scan_k[1] + 1, 'k']) == 1:
                        possibles.remove(p)
                    else:
                        possibles.append([scan_k[0] + 1, scan_k[1] + 1, type])
                        possibles.remove(p)


def possible_moves(start, color):
    global possibles
    if not color:
        print("red peice")
        possibles = [[start[0] - 1, start[1] + 1, 'l'], [starting_spot[0] + 1, starting_spot[1] + 1, 'l']]
        jumps_xx(opposite_checks=gray_checks, start=starting_spot, type='l')
        jumps_xx(opposite_checks=gray_checks, start=starting_spot, type='l')


    # for the gray peices    ________________________________________________________________

    elif color:
        print("gray peice")  # the 2 spaces to the left and right in front
        possibles = [[start[0] - 1, start[1] - 1,'l'], [starting_spot[0] + 1, starting_spot[1] - 1,'l']]
        jumps_xx(opposite_checks=red_checks, start=starting_spot, type='l')
        jumps_xx(opposite_checks=red_checks, start=starting_spot, type='l')








        r_count = 0
        for i in possibles:  # get currenty number of possible moves
            r_count += 1

    #for i in possibles:
        #i.append('l')
    possibles.append(starting_spot)         # adds going know where as a possible spot
    print("possible moves =", possibles)


starting_spot = [0, 0]
go_x = 10
go_y = 10
count = 0

run = True  # fhksdfbskjdfhsjofkldhfsljksjdfhgljgsd

while run:
    time.sleep(0.05)  # 20 fps

    if count > 0:
        time.sleep(.2)
        count = 0

    bg.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    cords = pygame.mouse.get_pos()

    if pygame.mouse.get_pressed()[0] == 1 and selected_peice == True:
        count = 0
        click_crds = []
        xxx = cords[0] // 90
        yyy = cords[1] // 90
        click_crds.append(xxx)
        click_crds.append(yyy)
        click_crds.append(starting_spot[2])  # adds king or l
        print(click_crds)  # go to / move
        if Gray_piece == False:                         # red peices only
            if possibles.count(click_crds) == 1:
                idx = red_checks.index(starting_spot)
                red_checks[idx] = click_crds
                selected_peice = False
                if starting_spot[1] > click_crds[1] + 1:
                    if starting_spot[0] > click_crds[0] + 1:
                        print("jumped up and to left")
                        if gray_checks.count([starting_spot[0] - 1, starting_spot[1] - 1, 'l']) == 1:
                            gray_checks.remove([starting_spot[0] - 1, starting_spot[1] - 1, 'l'])
                        else:
                            gray_checks.remove([starting_spot[0] - 1, starting_spot[1] - 1, 'k'])
                    else:
                        print("jumped up to right")
                        if gray_checks.count([starting_spot[0] + 1, starting_spot[1] - 1, 'l']):
                            gray_checks.remove([starting_spot[0] + 1, starting_spot[1] - 1, 'l'])
                        else:
                            gray_checks.remove([starting_spot[0] + 1, starting_spot[1] - 1, 'k'])
                else:
                    if starting_spot[0] > click_crds[0] + 1:
                        print("jumped down and to left")
                        if gray_checks.count([starting_spot[0] - 1, starting_spot[1] + 1, 'l']) == 1:
                            gray_checks.remove([starting_spot[0] - 1, starting_spot[1] + 1, 'l'])
                        else:
                            gray_checks.remove([starting_spot[0] - 1, starting_spot[1] + 1, 'k'])

                    elif starting_spot[0] + 1 < click_crds[0]:
                        print("jumped down and to right")
                        if gray_checks.count([starting_spot[0] + 1, starting_spot[1] + 1, 'l']) == 1:
                            gray_checks.remove([starting_spot[0] + 1, starting_spot[1] + 1, 'l'])
                        else:
                            gray_checks.remove([starting_spot[0] + 1, starting_spot[1] + 1, 'k'])

        if Gray_piece:
            if possibles.count(click_crds) == 1:
                idx = gray_checks.index(starting_spot)
                gray_checks[idx] = click_crds
                selected_peice = False
                if starting_spot[1] > click_crds[1] + 1:
                    if starting_spot[0] > click_crds[0] + 1:
                        print("jumped up and to left")
                        if red_checks.count([starting_spot[0] - 1, starting_spot[1] - 1, 'l']) == 1:
                            red_checks.remove([starting_spot[0] - 1, starting_spot[1] - 1, 'l'])
                        else:
                            red_checks.remove([starting_spot[0] - 1, starting_spot[1] - 1, 'k'])
                    else:
                        print("jumped up to right")
                        if red_checks.count([starting_spot[0] + 1, starting_spot[1] - 1, 'l']):
                            red_checks.remove([starting_spot[0] + 1, starting_spot[1] - 1, 'l'])
                        else:
                            red_checks.remove([starting_spot[0] + 1, starting_spot[1] - 1, 'k'])
                else:
                    if starting_spot[0] > click_crds[0] + 1:
                        print("jumped down and to left")
                        if red_checks.count([starting_spot[0] - 1, starting_spot[1] + 1, 'l']) == 1:
                            red_checks.remove([starting_spot[0] - 1, starting_spot[1] + 1, 'l'])
                        else:
                            red_checks.remove([starting_spot[0] - 1, starting_spot[1] + 1, 'k'])

                    elif starting_spot[0] + 1 < click_crds[0]:
                        print("jumped down and to right")
                        if red_checks.count([starting_spot[0] + 1, starting_spot[1] + 1, 'l']) == 1:
                            red_checks.remove([starting_spot[0] + 1, starting_spot[1] + 1, 'l'])
                        else:
                            red_checks.remove([starting_spot[0] + 1, starting_spot[1] + 1, 'k'])

        count += 1
        continue

    if pygame.mouse.get_pressed()[0] == 1 and selected_peice == False:
        count = 0
        click_crds = []
        xxx = cords[0] // 90
        yyy = cords[1] // 90
        click_crds.append(xxx)
        click_crds.append(yyy)              # selecting checker
        click_crds.append('l')
        king_cords = click_crds[0:2]
        king_cords.append("k")
        print(king_cords)
        if red_checks.count(click_crds) == 1:
            starting_spot = click_crds                  #red checker
            Gray_piece = False
            selected_peice = True
            possible_moves(start=starting_spot, color=Gray_piece)
        elif red_checks.count(king_cords) == 1:
            print("king status")
            starting_spot = king_cords          # red king
            Gray_piece = False
            selected_peice = True
            king_moves(start=starting_spot, color=Gray_piece)

        if gray_checks.count(click_crds) == 1:
            starting_spot = click_crds
            Gray_piece = True                               # gray checker
            selected_peice = True
            possible_moves(start=starting_spot, color=Gray_piece)
        elif gray_checks.count(king_cords) == 1:
            starting_spot = king_cords
            Gray_piece = True                               # gray king
            selected_peice = True
            king_moves(start=starting_spot, color=Gray_piece)
        count += 1

    checkers_R = []

    for i in red_checks:
        if i[1] == 7:  # changing to king when it get to end
            i[2] = 'k'
        if i[2] == 'k':
            check = Checker(red_king)  # creating red checkers
        else:
            check = Checker(red_img)
        checkers_R.append(check)
    indx = 0

    for enemy in checkers_R[:]:  # blitint red checkers
        enemy.draw1(red_checks[indx][0] * 90 + 10, red_checks[indx][1] * 90 + 10)
        indx += 1

    checkers_G = []
    indx = 0

    for i in gray_checks:
        if i[1] == 0:
            i[2] = 'k'
        if i[2] == 'k':
            check = Checker(gray_king)  # creating gray checkers
        else:
            check = Checker(gray_img)
        checkers_G.append(check)

    for enemy in checkers_G[:]:          # blitint gray checkers
        enemy.draw1(gray_checks[indx][0] * 90 + 10, gray_checks[indx][1] * 90 + 10)
        indx += 1

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        print("no value")

    pygame.display.update()



