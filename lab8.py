import math
from random import choice
import random as ra
import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

gt=-1 #приращение скорости за кадр

class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 20
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
         
        if (self.x < (800 - self.r) and  self.x > self.r):
            self.x += self.vx
            self.vx = self.vx * 0.99
        else:
            self.vx = - self.vx
            self.x = self.x + 2 * self.vx
            
        if (self.y < (600 - self.r) and  self.y > self.r):
            self.y += self.vy
            self.vy = self.vy - gt
            self.vy = self.vy * 0.95
        else:
            self.vy = - 0.9*self.vy
            self.y = self.y + 0.9*self.vy




            
    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 < (self.r + obj.r)**2:
            return True
        else:
            return False
 

class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 20
        self.wigth=6
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = -math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = -math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        """Рисуем пушку. Зависит от положения мыши."""
        pygame.draw.polygon(self.screen, self.color, ([40, 450],
                                                      [40 + self.f2_power * math.cos(self.an), 450 - self.f2_power * math.sin(self.an)],
                                                      [40 + self.f2_power * math.cos(self.an) + self.wigth * math.sin(self.an), 450 - self.f2_power * math.sin(self.an) + self.wigth * math.cos(self.an)],
                                                      [40 + self.wigth * math.sin(self.an), 450 + self.wigth * math.cos(self.an)]))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self, screen):
        
        self.screen = screen
        self.x = ra.randint(600, 780)
        self.y = ra.randint(300, 550)
        self.r = 10
        self.points = 0
        self.live = 1
        self.color = choice(GAME_COLORS)
    
       

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = ra.randint(600, 780)
        y = self.y = ra.randint(300, 550)
        r = self.r = ra.randint(2, 50)
        color = self.color = RED
        self.live = 1
        self.points = 1
        
    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.new_target()
    gun.power_up()
print(self.points)
pygame.quit()
