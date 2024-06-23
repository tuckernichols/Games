import pygame
import os
import random          #bugs  while loading new level
#import time
FPS = 30                    # this was built using a tutorial by tec with tim on youtube
enemy_shoots = 1            # i edited it in my own way in spots to show my understaning of the code
colly_w_enemy = 1
lifes = 1
pygame.font.init()      # need
WIDTH = 750
HEIGHT = 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooters")

#load images     constants are all caps
RED_SPACE_SHIP = pygame.image.load(os.path.join("spaceShootersIMGs", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("spaceShootersIMGs", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("spaceShootersIMGs", "pixel_ship_blue_small.png"))

#main player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("spaceShootersIMGs", "pixel_ship_yellow.png"))

#lasers
RED_LASER = pygame.image.load(os.path.join("spaceShootersIMGs", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("spaceShootersIMGs", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("spaceShootersIMGs", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("spaceShootersIMGs", "pixel_laser_yellow.png"))

BG = pygame.transform.scale(pygame.image.load(os.path.join("spaceShootersIMGs", "background-black.png")), (WIDTH, HEIGHT))


class Laser:
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self,window,):
        window.blit(self.img,(self.x,self.y))

    def move(self,vel):
        self.y += vel

    def off_screen(self,height):
        return not self.y <= height + 5 and self.y >= -10      # 46 46 46 46

    def collision(self,obj):
        return collide(self, obj)


class Ship:
    COOLDOWN = FPS/3

    def __init__(self, x,y ,health=113):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self,window):
        window.blit(self.ship_img , (self.x,self.y))
        for laser in self.lasers:
            laser.draw(window)



    def move_lasers(self,vel,obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):

                obj.health -=14
                if laser in self.lasers:
                    self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x ,self.y ,self.laser_img)         #
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self,x,y,health=115):
        super().__init__(x,y,health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self,vel,objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        try:
                            self.lasers.remove(laser)
                        except: print("oh no ")




    def draw(self,window):       # drawing health bar
        super().draw(window)
        self.health_bar(window)

    def health_bar(self,window):         #defing health bar
        pygame.draw.rect(window,(255,0,0),(self.x,self.y + self.ship_img.get_height() + 5, self.ship_img.get_width(),10))
        pygame.draw.rect(window,(0,255,0),(self.x,self.y + self.ship_img.get_height() + 5, self.ship_img.get_width() * (self.health / self.max_health) ,10))

class Enemy(Ship):
    COLOR_MAP = {
                 "red":(RED_SPACE_SHIP,RED_LASER),
                 "green":(GREEN_SPACE_SHIP,GREEN_LASER),
                 "blue":(BLUE_SPACE_SHIP,BLUE_LASER)
                 }
    def __init__(self,x,y,color,health=100):
        super().__init__(x,y,health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self,vel):
        self.y += vel




def collide(obj1,obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask,(offset_x,offset_y)) != None

def main():
    run = True
    FPS = 30
    level = 0
    lives = lifes
    main_font = pygame.font.SysFont("comic sans", 25)
    lost_font = pygame.font.SysFont("comic sans", 75,(255,0,0))


    enemies = []
    wave_length = 6
    enemy_vel = 2
    laser_vel = 15
    en_las_vel = 8

    player_vel = 10  # if FPS is low this is high and VV

    lost = False
    lost_count = 0
    player = Player(300,600)

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG,(0,0))
        #draw text    1 make lebel    2 blit it to screen
        lives_label = main_font.render(f"lives: {lives}", True,(255,0,0))         # Ture ws 1
        level_label = main_font.render(f"level: {level}",True,(0,255,0))
        #step 2
        WIN.blit(lives_label,(10,10))
        WIN.blit(level_label,(WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(window=WIN)
        if lost is True:
            lost_label = lost_font.render("GAME OVER",True,(255,0,0))
            WIN.blit(lost_label,(WIDTH/2 - lost_label.get_width()/2,HEIGHT/3 ))


        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if len(enemies) == 0:            # spanwing emilemes
            level += 1
            if player.health < 100:
                player.health += 14              # adding health after waves
                if player.health < 44:
                    player.health += 14

            wave_length += 4
            val_xs = []
            val_Ys = []
            start_spot = 0
            for i in range(wave_length):
                ennemy_x = random.randrange(50, WIDTH - 50)
                val_xs.append(ennemy_x)
            for i in range(wave_length):
                ennemy_y = random.randrange(-500 + level * -120, -300)
                val_Ys.append(ennemy_y)

            for xv in val_xs:
                start_spot += 1
                pizza_counter = 0
                for xv2 in val_xs[start_spot:]:
                    pizza_counter += 1
                    if -30 <= xv - xv2 <= 30:
                       # print("problem ", val_xs[start_spot - 1: start_spot])
                        #print("has problem with ", val_xs[start_spot - 1 + pizza_counter: start_spot + pizza_counter])
                        #print("matching y values")
                       # print(val_Ys[start_spot - 1: start_spot])
                        #print(val_Ys[start_spot - 1 + pizza_counter: start_spot + pizza_counter])
                        st = val_Ys[start_spot - 1: start_spot]
                        nd = val_Ys[start_spot - 1 + pizza_counter: start_spot + pizza_counter]
                        for lll in st:
                            count_ffff = 0
                            for kkk in nd:
                                count_ffff += 1
                                print("final ", lll - kkk)
                                if -80 <= lll - kkk <= 80:
                                    print("removed ", kkk)
                                    #print(val_Ys[ start_spot + pizza_counter - 1])
                                    print(pizza_counter + start_spot)
                                    kkk += 1
                                    #print(int(nd) * 2)
                                    #sval_Ys.remove(int(kkk + 1))





            print(val_xs)
            print(val_Ys)

            indx = 0

            for i in range(wave_length):               # placeing spawed eneimes
                enemy = Enemy(val_xs[indx],val_Ys[indx],random.choice(["red","blue","green"]))
                enemies.append(enemy)
                indx+=1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if player.health <= 0:
            lives -= 1
            player.health = 100

        if lives <= 0:
            lost = True

        if lost:
            lost_count += 1
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if player.x + player_vel > -25:
                player.x -= player_vel
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if player.x + player_vel < WIDTH - 40:
                player.x += player_vel

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if player.y - player_vel > HEIGHT/2:
                player.y -= player_vel                          # nocite - for up bc top is y = 0
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  #D
            if player.y + player_vel + 25 < HEIGHT:
                player.y += player_vel

        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(en_las_vel,player)

            if random.randrange(0,5 * FPS) == 1 and  enemy_shoots == 1:         # 100% chance of shooting per second = 1 x fps
                if enemy.y > -75:
                    enemy.shoot()

            if colly_w_enemy == 1:
                if collide(enemy,player):
                    player.health -= 28
                    enemies.remove(enemy)

            if enemy.y + enemy.get_height() > HEIGHT:
                player.health -= 28
                enemies.remove(enemy)



        player.move_lasers(- laser_vel,enemies)



#    if it stops working 51:24

main()





