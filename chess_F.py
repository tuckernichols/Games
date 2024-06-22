import pygame
import os
import time
r_count = 0                         # make a bord of rectangles
WIDTH = 720   # eachsquare is 90 x 90
Window = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("chess")

backround_img = pygame.image.load(os.path.join("chessIMGs/chessBoardBackround.jpg"))
dark_red = pygame.image.load(os.path.join("chessIMGs/darkRedSquare.png"))
dark_red = pygame.transform.scale(dark_red, (91, 91))
dark_gray = pygame.image.load(os.path.join("chessIMGs/graySquare.png"))
dark_gray = pygame.transform.scale(dark_gray, (90, 360))
green_sq = pygame.image.load(os.path.join("chessIMGs/greenSquare.jpg"))
green_sq = pygame.transform.scale(green_sq, (92, 92))

pawn_white = pygame.image.load(os.path.join("chessIMGs/white_pawn.png"))
castle_white = pygame.image.load(os.path.join("chessIMGs/white_castle.png"))
bishop_white = pygame.image.load(os.path.join("chessIMGs/white_bishop.png"))
horse_white = pygame.image.load(os.path.join("chessIMGs/white_horse.png"))
queen_white = pygame.image.load(os.path.join("chessIMGs/white_queen.png"))
k_white_king = pygame.image.load(os.path.join("chessIMGs/white_king.png"))

pawn_black = pygame.image.load(os.path.join("chessIMGs/black_pawn.png"))
castle_black = pygame.image.load(os.path.join("chessIMGs/black_castle.png"))
bishop_black = pygame.image.load(os.path.join("chessIMGs/black_bishop.png"))
horse_black = pygame.image.load(os.path.join("chessIMGs/black_horse.png"))
queen_black = pygame.image.load(os.path.join("chessIMGs/black_queen.png"))
k_black_king = pygame.image.load(os.path.join("chessIMGs/black_king.png"))

select_w_queen = pygame.transform.scale(queen_white, (80, 80))
select_w_caslte = pygame.transform.scale(castle_white, (80, 80))
select_w_bishop = pygame.transform.scale(bishop_white, (80, 80))
select_w_horse = pygame.transform.scale(horse_white, (80, 80))



white_turn = True
Gray_piece = False
check_white = []
check_black = []
king_in_check = False
king_location_white = [3, 5, 'p']
king_location_black = [3, 5, 'p']
run_count = 0
click_crds = [-400, -400]
super_backup_white = []
super_backup_black = []
times = 100
go_red2 = False
selectable_function = True
killed = False
thing = []


class BG:                                             #backround
    def __init__(self,x,y,image,):
        self.image = pygame.transform.scale(image,(WIDTH,WIDTH))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self):
        Window.blit(self.image,(self.rect.x,self.rect.y))


bg = BG(0, 0, backround_img)
selected_peice = False


class Checker():
    def __init__(self, image,):
        self.image = pygame.transform.scale(image, (60,70))

    def draw1(self, x, y):
        Window.blit(self.image, (x, y))
        #print(x,y)



white_chess_super = [[0, 0, 'castle'], [1, 0, 'horse'], [2, 0, 'bishop'], [3, 0, 'queen'], [4, 0, 'king'], [5, 0, 'bishop'], [6, 0, 'horse'], [7, 0, 'castle'], [0, 1, 'p'], [1, 1, 'p'], [2, 1, 'p'], [3, 1, 'p'], [4, 1, 'p'], [5, 1, 'p'], [6, 1, 'p'], [7, 1, 'p']]
#white_chess_super = [[2, 1, 'king'], [0, 2,'queen'], [6, 6, 'p'], [3, 4, 'p']]
black_chess_super = [[0, 7, 'castle'], [1, 7, 'horse'], [2, 7, 'bishop'], [3, 7, 'queen'], [4, 7, 'king'], [5, 7, 'bishop'], [6, 7, 'horse'], [7, 7, 'castle'], [0, 6, 'p'], [1, 6, 'p'], [2, 6, 'p'], [3, 6, 'p'], [4, 6, 'p'], [5, 6, 'p'], [6, 6, 'p'], [7, 6, 'p']]
#black_chess_super = [[2, 4, 'king'], [5, 5,'queen'], [4, 2, 'p'], [3, 3, 'p'], [6, 1, 'p']]
possibles = []
last_10 = tuple((white_chess_super.copy(), black_chess_super.copy()))


def possibles_pawn(start, white):
    global possibles
    possibles = []
    if white:
        if check_for.count([start[0],start[1] + 1]) == 0:
            if start[1]== 1:
                possibles.append([start[0],start[1] + 2])
            possibles.append([start[0], start[1] + 1])
        if check_black.count([start[0]-1, start[1] + 1]):
            possibles.append([start[0]-1, start[1] + 1])
        if check_black.count([start[0]+1, start[1] + 1]):
            possibles.append([start[0]+1, start[1] + 1])

    if not white:
        if check_for.count([start[0], start[1] - 1]) == 0:
            if start[1] == 6:                                           # adding first jump and 1 ahead as possibles
                possibles.append([start[0], start[1] - 2])
            possibles.append([start[0], start[1] - 1])
        if check_white.count([start[0] - 1, start[1] - 1]):
            possibles.append([start[0] - 1, start[1] - 1])
        if check_white.count([start[0] + 1, start[1] - 1]):
            possibles.append([start[0] + 1, start[1] - 1])

    #print("pawn: possible moves =",possibles)


def possibles_castle(start, color, queen):
    global possibles
    #print(start)
    if queen == False:
        possibles = []
    hit = False
    count = 1
    x = 0
    while x < 7 and hit == False:
        x = start[0] + count
        if check_for.count([x, start[1]]) == 0:
            possibles.append([x, start[1]])                     # right
        else:
            possibles.append([x, start[1]])
            hit = True
        count += 1
    hit = False
    count = 1
    while x > 0 and hit == False:
        x = start[0] - count
        if check_for.count([x, start[1]]) == 0:                 # left
            possibles.append([x, start[1]])
        else:
            possibles.append([x, start[1]])
            hit = True
        count += 1
    hit = False
    count = 1
    while x < 8 and hit == False:
        x = start[1] + count
        if check_for.count([start[0], x]) == 0:             # up
            possibles.append([start[0], x])
        else:
            possibles.append([start[0], x])
            hit = True
        count += 1
    hit = False
    count = 1
    while x > 0 and hit == False:
        x = start[1] - count
        if check_for.count([start[0], x]) == 0:         # down
            possibles.append([start[0], x])
        else:
            possibles.append([start[0], x])
            hit = True
        count += 1
    #print("castle: possible moves =",possibles)


def possibles_bishop(start, color):
    global possibles
    #print(start)
    possibles = []
    hit = False
    countx = 1
    county = 1
    count = 0
    x = 3
    y = 3
    for i in range(4):
        hit = False
        count  += 1
        if count == 2:
            countx = -1
            county = -1
        if count == 3:
            countx = 1
            county = -1
        if count == 4:
            countx = -1
            county = 1
        x = 3
        y = 3
        while hit == False and x > 0 and y > 0:
            x = start[0] - countx
            y = start[1] - county
            if x > 8 or y > 8 or x < 0 or y < 0:
                hit = True
            elif check_for.count([x,y]) == 0:
                possibles.append([x,y])
            else:
                possibles.append([x,y])
                hit = True
            countx += 1
            county += 1
            if count == 2:
                countx += -2
                county += -2
            if count == 3:
                county += -2
            if count == 4:
                countx += -2
    #print("bishop: possible moves =", possibles)


def possibles_horse(start,color):
    global possibles
    #print(start)
    possibles = []
    w = start[0] - 2
    possibles.append([w, start[1] - 1])   # remove if white_count>count
    possibles.append([w, start[1] + 1])
    w += 4
    possibles.append([w, start[1] - 1])
    possibles.append([w, start[1] + 1])
    w = start[1] - 2
    possibles.append([start[0] - 1, w])
    possibles.append([start[0] + 1, w])
    w += 4
    possibles.append([start[0] - 1, w])
    possibles.append([start[0] + 1, w])

    for i in range(8):
        for p in possibles:
            if color.count(p) == 1:
                possibles.remove(p)
            if p[0] > 7 or p[0] < 0 or p[1] > 7 or p[1] < 0:
                possibles.remove(p)

    #print("horse: possible moves =", possibles)


def possibles_king(start,color):
    global possibles
    possibles = []
    possibles.append([start[0], start[1] -1])
    possibles.append([start[0], start[1] + 1])
    possibles.append([start[0]-1, start[1]])
    possibles.append([start[0]+1, start[1]])

    possibles.append([start[0] - 1, start[1]-1])
    possibles.append([start[0] + 1, start[1]-1])
    possibles.append([start[0] - 1, start[1] + 1])
    possibles.append([start[0] + 1, start[1] + 1])

    for i in range(8):
        for p in possibles:
            if color.count(p) ==1:
                possibles.remove(p)
            if p[0] > 7 or p[0] < 0 or p[1] > 7 or p[1] < 0:
                possibles.remove(p)

    #print("king: possible moves =", possibles)


def check_in(current_king_cords, check_self, check_oposite, self_super, oposite_super, white):
    global king_in_check
    king_in_check = False

    possibles_bishop(current_king_cords, check_self)
    ggg = possibles
    #print('bishops / queens',ggg)
    for g in ggg:
        if check_oposite.count(g) ==1:
            ii = check_oposite.index(g)
            #print(ii)
            #print(oposite_super)
            #print(oposite_super[ii][2],'shfjsjfdhs')
            if oposite_super[ii][2] == 'queen' or oposite_super[ii][2] =='bishop':
                print("in check")
                king_in_check = True
    possibles_castle(current_king_cords, white_chess_super, queen=False)
    ggg = possibles
    #print('castles / queens', ggg)
    for g in ggg:
        if check_oposite.count(g) ==1:
            ii = check_oposite.index(g)
            #print(oposite_super[ii][2],'shfjsjfdhs')
            if oposite_super[ii][2] == 'queen' or oposite_super[ii][2] =='castle':
                print("in check")
                king_in_check = True

    possibles_horse(start=current_king_cords, color=check_self)
    ggg = possibles
    for g in ggg:
        if check_oposite.count(g) ==1:
            ii = check_oposite.index(g)
            if oposite_super[ii][2] == 'horse':
                king_in_check = True

    if white:                                                                                       # pawn
        if check_black.count([current_king_cords[0] - 1, current_king_cords[1] + 1]) ==1:
            idxx = check_black.index([current_king_cords[0] - 1, current_king_cords[1] + 1])
            print(black_chess_super[idxx][2])
            if black_chess_super[idxx][2] == 'p':
                king_in_check = True
        if check_black.count([current_king_cords[0] + 1, current_king_cords[1] + 1]) == 1:
            idxx = check_black.index([current_king_cords[0] + 1, current_king_cords[1] + 1])
            print(black_chess_super[idxx][2])
            if black_chess_super[idxx][2] == 'p':
                king_in_check = True
    if not white:    # black
        if check_white.count([current_king_cords[0] - 1, current_king_cords[1] - 1]) ==1:
            idxx = check_white.index([current_king_cords[0] - 1, current_king_cords[1] - 1])
            if white_chess_super[idxx][2] == 'p':
                king_in_check = True
        if check_white.count([current_king_cords[0] + 1, current_king_cords[1] - 1]) == 1:
            idxx = check_white.index([current_king_cords[0] + 1, current_king_cords[1] - 1])
            if white_chess_super[idxx][2] == 'p':
                king_in_check = True

    if king_in_check and white:
        print('white king in check')
    elif king_in_check and not white:
        print('black king in check')
    else:
        print('not in check')
    #print("king in check = ", king_in_check , " /and white peice = ", white)


starting_spot = [0,0]
go_x = 10
go_y = 10                             # fhksdfbskjdfhsjofkldhfsljksjdfhgljgsdaskjhfsalfjhaszflsjhfslfhslfhslfhw
count = 0

run = True                           # fhksdfbskjdfhsjofkldhfsljksjdfhgljgsdaskjhfsalfjhaszflsjhfslfhslfhslfhw
go_red = False                  # to do:  pawn to end black

while run:
    if run_count > 1:
        time.sleep(0.1)
        run_count = 0
    time.sleep(0.05)    # 20 fps

    cords = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] == 1:
        print(cords)


    if count > 0:
        time.sleep(.1)
        count = 0

    bg.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    cords = pygame.mouse.get_pos()

    if pygame.mouse.get_pressed()[0] == 1 and selected_peice and selectable_function:


        count = 0
        click_crds = []
        xxx = cords[0] // 90
        yyy = cords[1] // 90
        click_crds.append(xxx)
        click_crds.append(yyy)
        #print(click_crds, " go to / move")
        #print(starting_spot, 'start')
        if possibles.count(click_crds) == 1:
            #print("aproved move")
            if white_turn:                  # WHITE



                if check_black.count(click_crds) == 1:
                    kill = check_black.index(click_crds)                    # KILLING black peices
                    print(black_chess_super[kill][2])
                    thing = black_chess_super[kill][2]
                    black_chess_super.remove([click_crds[0], click_crds[1], thing])
                    killed = True
                www = check_white.index(starting_spot)
                white_chess_super[www][0] = click_crds[0]                   # moving white peices
                white_chess_super[www][1] = click_crds[1]
                if click_crds == starting_spot:
                    print(" didnt moved")
                else:
                    white_turn = False
                    check_white = []
                    check_black = []
                    check_for = []

                    for g in white_chess_super:  # check for
                        check_white.append([g[0], g[1]])
                        check_for.append([g[0], g[1]])  # list of first 2 digits
                    for g in black_chess_super:
                        check_black.append([g[0], g[1]])
                        check_for.append([g[0], g[1]])

                    check_in(king_location_white, check_white, check_black, white_chess_super, black_chess_super, white=True)

                    if king_in_check:
                        white_chess_super[www][0] = starting_spot[0]  # moving white peices
                        white_chess_super[www][1] = starting_spot[1]
                        white_turn = True
                        go_red = True
                        times = 10
                        if killed and thing != []:  # so king cant kill and peice and then be bumped back
                            black_chess_super.append([click_crds[0], click_crds[1], thing])
                            killed = False
                        else:
                            killed = False

                #last_10.append(white_chess_super)

            elif not white_turn:

                #last_10.append([white_chess_super, black_chess_super])

                if check_white.count(click_crds) == 1:
                    kill = check_white.index(click_crds)
                    print(white_chess_super[kill][2])               # killing white peices
                    thing = white_chess_super[kill][2]
                    white_chess_super.remove([click_crds[0], click_crds[1], thing])
                    print([click_crds[0], click_crds[1], thing], 'removed')
                    killed = True
                www = check_black.index(starting_spot)
                black_chess_super[www][0] = click_crds[0]                    # moving black peices
                black_chess_super[www][1] = click_crds[1]
                if click_crds == starting_spot:
                    print("didnt moved")
                else:
                    white_turn = True
                    check_white = []
                    check_black = []
                    check_for = []

                    for g in white_chess_super:  # check for
                        check_white.append([g[0], g[1]])
                        check_for.append([g[0], g[1]])  # list of first 2 digits
                    for g in black_chess_super:
                        check_black.append([g[0], g[1]])
                        check_for.append([g[0], g[1]])

                    check_in(king_location_black, check_black, check_white, black_chess_super, white_chess_super,white=False)  # 333
                    if king_in_check:
                        #print(click_crds,'go')
                        #print(starting_spot,'back')
                        black_chess_super[www][0] = starting_spot[0]  # moving black peices
                        black_chess_super[www][1] = starting_spot[1]
                        white_turn = False
                        go_red2 = True
                        times = 10
                        if killed and thing != []:          # so king cant kill and peice and then be bumped back
                            white_chess_super.append([click_crds[0], click_crds[1], thing])
                            killed = False
                        else:
                            killed = False

                    check_in(king_location_black, check_black, check_white, black_chess_super, white_chess_super,white=False)  # 333
                    #last_10.append(black_chess_super)

            selected_peice = False
            time.sleep(.05)
            continue

    if pygame.mouse.get_pressed()[0] == 1 and selected_peice == False and selectable_function:
        count = 0
        click_crds = []
        xxx = cords[0] // 90
        yyy = cords[1] // 90
        click_crds.append(xxx)
        click_crds.append(yyy)                            # selecting peice
        print(click_crds)
        starting_spot = click_crds
        check_for = []
        check_white = []
        check_black = []
        for g in white_chess_super:                     # check for
            check_white.append([g[0], g[1]])
            check_for.append([g[0], g[1]])              # list of first 2 digits
        for g in black_chess_super:
            check_black.append([g[0], g[1]])
            check_for.append([g[0], g[1]])

        for i in white_chess_super:
            if i[0] == click_crds[0] and i[1] == click_crds[1] and white_turn == True:                     # seeing if theres a white peice there
                print("white selected")
                #check_in(king_location_white, check_white, check_black, white_chess_super, black_chess_super)
                if i[2] == 'castle':
                    possibles_castle(start=click_crds, color=white_chess_super, queen= False)
                elif i[2] == 'horse':
                    possibles_horse(start=click_crds, color=check_white)
                elif i[2] == 'bishop':
                    possibles_bishop(start=click_crds, color=white_chess_super)
                elif i[2] == 'queen':
                    possibles_bishop(start=click_crds, color=white_chess_super)
                    possibles_castle(start=click_crds, color=white_chess_super, queen=True)
                elif i[2] == 'king':
                    #check_in(start_king=click_crds, check_self=check_white, check_oposite=check_black, self_super=white_chess_super, oposite_super=black_chess_super)
                    possibles_king(start=click_crds,color=check_white)
                else:
                    possibles_pawn(start=click_crds, white=True)
                for h in range(8):
                    for p in possibles:
                        if check_white.count(p) == 1:
                            possibles.remove(p)
                        if p[0] > 7 or p[0] < 0 or p[1] > 7 or p[1]< 0:
                            possibles.remove(p)
                possibles.append(click_crds)
                print('possibles final = ' ,possibles, "FINAL")
                #check_in(king_location_white, check_white, check_black, white_chess_super, black_chess_super)

                selected_peice = True


        for c in black_chess_super:
            if c[0] == click_crds[0] and c[1] == click_crds[1] and not white_turn:                     # seeing if theres a black peice there
                print("black peice selected")
                if c[2] == 'castle':
                    possibles_castle(start=click_crds, color=black_chess_super, queen=False)
                elif c[2] == 'horse':
                    possibles_horse(start=click_crds, color=check_black)
                elif c[2] == 'bishop':
                    possibles_bishop(start=click_crds, color=black_chess_super)
                elif c[2] == 'queen':
                    possibles_bishop(start=click_crds, color=black_chess_super)
                    possibles_castle(start=click_crds, color=black_chess_super, queen=True)
                elif c[2] == 'king':
                    possibles_king(start=click_crds, color=check_black)
                else:
                    possibles_pawn(start=click_crds, white=False)
                for h in range(8):
                    for p in possibles:
                        if check_black.count(p) == 1:
                            possibles.remove(p)
                        if p[0] > 7 or p[0] < 0 or p[1] > 7 or p[1]< 0:
                            possibles.remove(p)
                possibles.append(click_crds)
                print('possibles final = ', possibles, 'FINAL')
                #print("sfmbskfm,gbf")
                selected_peice = True

        count += 1

    if selected_peice:
        Window.blit(green_sq, (starting_spot[0] * 90, starting_spot[1] * 90))                # green select square

    if go_red:
        Window.blit(dark_red, (king_location_white[0] * 90, king_location_white[1] * 90))
        times -= 1
        if times == 0:
            go_red = False

    if go_red2:
        Window.blit(dark_red, (king_location_black[0] * 90, king_location_black[1] * 90))
        times -= 1
        if times == 0:
            go_red2 = False

    #Window.blit(dark_red, (king_location_white[0] * 90, king_location_white[1] * 90))

    checkers_R = []

    indx = 0

    for i in white_chess_super:
        if i[2] == 'castle':
            check = Checker(castle_white)
        elif i[2] == 'horse':
            check = Checker(horse_white)
        elif i[2] == 'bishop':
            check = Checker(bishop_white)                       # creating peices and what they are
        elif i[2] == 'queen':
            check = Checker(queen_white)
        elif i[2] == 'king':
            check = Checker(k_white_king)
            king_location_white = i
        else:
            check = Checker(pawn_white)
        checkers_R.append(check)                                    # bliting peices

    for enemy in checkers_R[:]:
        enemy.draw1(white_chess_super[indx][0] * 90 + 15, white_chess_super[indx][1] * 90 + 10)
        indx +=1

    checkers_G = []
    indx = 0

    for i in black_chess_super:
        if i[2] == 'castle':
            check = Checker(castle_black)
        elif i[2] == 'horse':
            check = Checker(horse_black)
        elif i[2] == 'bishop':
            check = Checker(bishop_black)
        elif i[2] == 'queen':
            check = Checker(queen_black)
        elif i[2] == 'king':
            check = Checker(k_black_king)
            king_location_black = i
        else:
            check = Checker(pawn_black)
        checkers_G.append(check)

    for enemy in checkers_G[:]:  # blitint checkers
        enemy.draw1(black_chess_super[indx][0] * 90 + 15, black_chess_super[indx][1] * 90 + 10)
        indx += 1

    for p in white_chess_super:
        if p[1] == 7 and p[2] == 'p':
            #print("update pawn skdjfh")
            Window.blit(dark_gray, (p[0] * 90, 360))
            Window.blit(select_w_queen, (p[0] * 90 + 5, 635))
            Window.blit(select_w_caslte, (p[0] * 90 + 5, 545))
            Window.blit(select_w_bishop, (p[0] * 90 + 5, 455))
            Window.blit(select_w_horse, (p[0] * 90 + 5, 365))
            selectable_function = False
            if pygame.mouse.get_pressed()[0] == 1:
                print(cords)
                print(cords[1] // 90)
                ffff = cords[1] // 90
                if ffff == 7:
                    p[2] = 'queen'
                elif ffff == 6:
                    p[2] = 'castle'
                elif ffff == 5:
                    p[2] = 'bishop'
                elif ffff == 4:
                    p[2] = 'horse'
                selectable_function = True

    for p in black_chess_super:
        if p[1] == 0 and p[2] == 'p':
            #print("update pawn skdjfh")
            Window.blit(dark_gray, (p[0] * 90, 0))
            Window.blit(select_w_queen, (p[0] * 90 + 5, 5))
            Window.blit(select_w_caslte, (p[0] * 90 + 5, 95))
            Window.blit(select_w_bishop, (p[0] * 90 + 5, 185))
            Window.blit(select_w_horse, (p[0] * 90 + 5, 275))
            selectable_function = False
            time.sleep(0.1)
            if pygame.mouse.get_pressed()[0] == 1:
                print(cords)
                print(cords[1] // 90)
                ffff = cords[1] // 90
                if ffff == 0:
                    p[2] = 'queen'
                elif ffff == 1:
                    p[2] = 'castle'
                elif ffff == 2:
                    p[2] = 'bishop'
                elif ffff == 3:
                    p[2] = 'horse'
                selectable_function = True



    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        print(white_chess_super)
        print(black_chess_super)
    if keys[pygame.K_q]:
        run = False

    if keys[pygame.K_LEFT]:
        print(last_10)
        #print(last_10[0][0])  # the first board
        #print(last_10[1])  # first move
    if keys[pygame.K_r]:
        white_chess_super = [[0, 0, 'castle'], [1, 0, 'horse'], [2, 0, 'bishop'], [3, 0, 'queen'], [4, 0, 'king'],
                             [5, 0, 'bishop'], [6, 0, 'horse'], [7, 0, 'castle'], [0, 1, 'p'], [1, 1, 'p'], [2, 1, 'p'],
                             [3, 1, 'p'], [4, 1, 'p'], [5, 1, 'p'], [6, 1, 'p'], [7, 1, 'p']]
        black_chess_super = [[0, 7, 'castle'], [1, 7, 'horse'], [2, 7, 'bishop'], [3, 7, 'queen'], [4, 7, 'king'],
                             [5, 7, 'bishop'], [6, 7, 'horse'], [7, 7, 'castle'], [0, 6, 'p'], [1, 6, 'p'], [2, 6, 'p'],
                             [3, 6, 'p'], [4, 6, 'p'], [5, 6, 'p'], [6, 6, 'p'], [7, 6, 'p']]
        white_turn = True
        selected_peice = False

    thing = []
    run_count += 1
    pygame.display.update()



