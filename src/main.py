import pygame
import random
import sys
import math

pygame.init()

width = 800
height = 600
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
pygame.display.set_caption("Planet Game")
num_meteor = 5

pygame.font.init()
font = pygame.font.Font("MinecraftRegular.otf",30)
fontBig = pygame.font.Font("MinecraftRegular.otf",100) 
fontMedium = pygame.font.Font("MinecraftRegular.otf",50) 

def draw_rounded_rect(surface, color, rect, radius):
    x, y, width, height = rect

    # Zeichne das mittlere Rechteck
    pygame.draw.rect(surface, color, (x + radius, y, width - 2 * radius, height))
    pygame.draw.rect(surface, color, (x, y + radius, width, height - 2 * radius))

    # Zeichne die vier Ecken als Kreise
    pygame.draw.circle(surface, color, (x + radius, y + radius), radius)  # Oben links
    pygame.draw.circle(surface, color, (x + width - radius, y + radius), radius)  # Oben rechts
    pygame.draw.circle(surface, color, (x + radius, y + height - radius), radius)  # Unten links
    pygame.draw.circle(surface, color, (x + width - radius, y + height - radius), radius)  # Unten rechts



def startMenu():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_mode_textRect.collidepoint(event.pos):
                    run = False

        screen.fill("black")
        mouse_pos = pygame.mouse.get_pos()
        
        easy_mode_textRect = pygame.Rect(100,500,100,100)
        medium_mode_textRect = pygame.Rect(300,500,200,50)
        hard_mode_textRect = pygame.Rect(550,500,100,50)
        
        if easy_mode_textRect.collidepoint(mouse_pos):
            easy_mode_text = fontMedium.render("EASY",False,"green")
        else:
            easy_mode_text = fontMedium.render("EASY",False,"white")

        if medium_mode_textRect.collidepoint(mouse_pos):
            medium_mode_text = fontMedium.render("MEDIUM",False,"green")
        else:
            medium_mode_text = fontMedium.render("MEDIUM",False,"white")

        if hard_mode_textRect.collidepoint(mouse_pos):
            hard_mode_text = fontMedium.render("HARD",False,"red")
        else:
            hard_mode_text = fontMedium.render("HARD",False,"white")
        preview_image = pygame.image.load("preview.png")
        title_image = pygame.image.load("Title.png")
        #screen.blit(preview_image,(0,0))
        #screen.blit(background_image,(0,0))
        draw_rounded_rect(screen, (32, 30, 31), (80,480,150,80), 30)
        draw_rounded_rect(screen, (32,30,31), (285,480,200,80), 30)
        draw_rounded_rect(screen, (32, 30, 31), (531,480,150,80), 30)

        screen.blit(easy_mode_text,(100,500))
        screen.blit(title_image,(0,-200))
        screen.blit(medium_mode_text,(300,500))
        screen.blit(hard_mode_text,(550,500))
        
        clock.tick(60)
        pygame.display.update()

startMenu()

class Player(object):
    def __init__(self,speed):
        self.speed = speed
        self.center = [100,300]
        self.relative_points = [(-20, -10), (0, 0), (-20, 10)]
        self.player_live = 3

        self.explosion_size = 20
        self.coll = False

        self.angle = 0

    def DeathScreen(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        run = False
                        sys.exit(0)
                    elif event.key == pygame.K_r:
                        run = False
                        reset_game()

            screen.fill("black")
            self.death_text = fontBig.render("YOU DIED",False,"red")
            self.end_score = fontMedium.render(f"SCORE {me.score}",False,"green")
            self.retry_text = fontMedium.render("Press 'r' to restart",False,"green")
            screen.blit(self.death_text,(170,50))
            screen.blit(self.end_score,(280,200))
            screen.blit(self.retry_text,(150,300))

            pygame.display.update()
            clock.tick(60)

    def gameOver(self):

        while self.explosion_size < 50:
            screen.fill("black")

            #self.expl = pygame.draw.rect(screen,"red",(self.center[0] - 35,self.center[1] - 25,self.explosion_size,self.explosion_size),1)
            self.expl = pygame.draw.circle(screen,"red",(self.center[0],self.center[1]),self.explosion_size,1)
            pygame.display.update()
            self.explosion_size += 5
            pygame.time.delay(100)
        self.DeathScreen()


    def update(self):

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_d]:
            self.center[0] += self.speed
            self.angle += 1
        elif pressed[pygame.K_s]:
            self.center[1] += self.speed
            self.angle -= 1
        elif pressed[pygame.K_w]:
            self.center[1] -= self.speed
            self.angle += 1
        elif pressed[pygame.K_a]:
            self.center[0] -= self.speed
            self.angle -= 1
        else:
            self.speed = 5

        if pressed[pygame.K_d] and pressed[pygame.K_w]:
            self.speed = 3
            self.center[0] += self.speed
            self.center[1] -= self.speed
        elif pressed[pygame.K_a] and pressed[pygame.K_w]:
            self.speed = 3
            self.center[0] -= self.speed
            self.center[1] -= self.speed
        elif pressed[pygame.K_d] and pressed[pygame.K_s]:
            self.speed = 3
            self.center[0] += self.speed
            self.center[1] += self.speed
        elif pressed[pygame.K_a] and pressed[pygame.K_s]:
            self.speed = 3
            self.center[0] -= self.speed
            self.center[1] += self.speed
        else:
            self.speed = 5



        if self.center[0] < 30:
            self.center[0] = 30
        elif self.center[0] > width - 10:
            self.center[0] = width - 10

        if self.center[1] < 30:
            self.center[1] = 30
        elif self.center[1] > height - 10:
            self.center[1] = height - 13
        
        self.points =  [(self.center[0] + x, self.center[1] + y) for x, y in self.relative_points]

        self.player = pygame.draw.polygon(screen, "white", self.points, 1)
        self.player_health_text = font.render(f"HEALTH {self.player_live}",False,"white")
        screen.blit(self.player_health_text,(10,40))

        for m in meteor:
            if self.player.colliderect(m.meteorRect):
                self.player_live -= 0.1

        if self.player_live <= 0:
            self.player_live = 0
            self.gameOver()
        self.player_live = round(self.player_live,2)

class Meteor(object):
    def __init__(self,x,y,speed,size):
        self.speed = speed
        self.meteor_x = x
        self.meteor_y = y
        self.max_meteor = 50
        self.meteor_size = size

        self.pos = (self.meteor_x,self.meteor_y)
        self.unique = []
        self.timer = pygame.time.get_ticks()
        self.timerDuration = 500
        self.meteorRect = pygame.Rect(self.meteor_x,self.meteor_y,self.meteor_size,self.meteor_size)

        self.score = 0
    def debug_info(self,font):
        self.score_text = font.render(f"SCORE {self.score}",False,"white")
        screen.blit(self.score_text,(10,0))
    
    def friendlyfire(self,new_meteor):
        # meteoriten kollidieren miteinander
        for m in meteor:
            if new_meteor.meteorRect.colliderect(m.meteorRect):
                return True
        return False

    def spawn_meteor(self):
        self.elapsedTime = pygame.time.get_ticks() - self.timer
        if self.elapsedTime >= self.timerDuration:
            self.timer = pygame.time.get_ticks()
            self.score += 0.5
            
            for _ in range(5):
                new_x = random.randint(500,width)
                new_y = random.randint(0,height)
                new_size = random.randint(10,20)
                new_meteor = Meteor(new_x,new_y,3,new_size)

                if not self.friendlyfire(new_meteor,):
                    meteor.append(new_meteor)
                    break
                

    def faster_meteor(self):
        self.elapsedTime = pygame.time.get_ticks() - self.timer
        if self.elapsedTime >= 1000:
            self.current = pygame.time.get_ticks()
            self.speed += 1
        print(self.elapsedTime)


    def update(self):
        global num_meteor
        #self.faster_meteor()
        self.meteor = pygame.draw.circle(screen,"white",self.pos,self.meteor_size,1)
        self.meteorRect = pygame.Rect(self.meteor_x - 20,self.meteor_y - 25,50,50)
        self.pos = (self.meteor_x,self.meteor_y)
        
        for i,_ in enumerate(meteor):
            if i > 50:
                if self in meteor:
                    meteor.remove(self)
        
        self.meteor_x -= self.speed

        if self.meteor_x <= 1:
            if self in meteor:
                meteor.remove(self)

def reset_game():
    global p,meteor,num_meteor
    p = Player(5)
    #meteor = []
    for m in meteor:
        meteor.remove(m)
    me.score = -1

    


meteor = [Meteor(random.randint(300,width),random.randint(0,height), random.randint(10,20),3) for _ in range(num_meteor)]
p = Player(5)

me = Meteor(random.randint(300,width),random.randint(0,height), random.randint(10,20),3) 
def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_ESCAPE:
                    startMenu()

        screen.fill("black")
        
        me.debug_info(font)
        for m in meteor:
            m.update()
        me.update()
        me.spawn_meteor()
        p.update()
    
    
        clock.tick(60)
        pygame.display.update()

main()
