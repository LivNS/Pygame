import pygame, sys, random, os
from pygame.locals import *

pygame.init()
mainClock = pygame.time.Clock()

# definindo a janela
WINDOWWIDTH = 700
WINDOWHEIGHT = 700
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Pygame')

# definindo as cores
PINK = (219, 22, 126)
GREEN = (164, 241, 24)
AQUA = (18, 181, 164)
BLACK = (0, 0, 0)

# definindo o jogador e as "comidas"
foodCounter = 0
NEWFOOD = 40
FOODSIZE = 15
player = pygame.Rect(225, 225, 25, 25)  # tamanho do jogador
foods = []
for i in range(10):
    foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH - FOODSIZE),
                             random.randint(0, WINDOWHEIGHT - FOODSIZE), FOODSIZE, FOODSIZE))

# obstáculos
STONE_SIZE = 25
stones = [
    pygame.Rect(random.randint(0, WINDOWWIDTH - STONE_SIZE), random.randint(0, WINDOWHEIGHT - STONE_SIZE), STONE_SIZE, STONE_SIZE),
    pygame.Rect(random.randint(0, WINDOWWIDTH - STONE_SIZE), random.randint(0, WINDOWHEIGHT - STONE_SIZE), STONE_SIZE, STONE_SIZE)
]

# variáveis de movimento
moveLeft = False
moveRight = False
moveUp = False
moveDown = False

MOVESPEED = 6
score = 0  # variável para armazenar a pontuação

# função para limpar o terminal
def clear_terminal():
    if os.name == 'nt':  # para windows
        os.system('cls')
    else:  # para Linux/MacOS
        os.system('clear')

# função para exibir a pontuação
def display_score():
    clear_terminal()
    print(f"Pontos: {score}") # os pontos são os quadradinhos comidos

# função para exibir Game Over
def game_over():
    clear_terminal()
    print("Game Over")
    print(f"Pontuação final: {score}")
    pygame.quit()
    sys.exit()

# rodando o game
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == K_a:
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT or event.key == K_d:
                moveLeft = False
                moveRight = True
            if event.key == K_UP or event.key == K_w:
                moveDown = False
                moveUp = True
            if event.key == K_DOWN or event.key == K_s:
                moveUp = False
                moveDown = True
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == K_a:
                moveLeft = False
            if event.key == K_RIGHT or event.key == K_d:
                moveRight = False
            if event.key == K_UP or event.key == K_w:
                moveUp = False
            if event.key == K_DOWN or event.key == K_s:
                moveDown = False
            if event.key == K_x:
                player.top = random.randint(0, WINDOWHEIGHT - player.height)
                player.left = random.randint(0, WINDOWWIDTH - player.width)

        if event.type == MOUSEBUTTONUP:
            foods.append(pygame.Rect(event.pos[0], event.pos[1], FOODSIZE, FOODSIZE))

    foodCounter += 1
    if foodCounter >= NEWFOOD:
        foodCounter = 0
        foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH - FOODSIZE),
                                 random.randint(0, WINDOWHEIGHT - FOODSIZE), FOODSIZE, FOODSIZE))

    # movimento do jogador
    if moveDown:
        player.top += MOVESPEED
    if moveUp:
        player.top -= MOVESPEED
    if moveLeft:
        player.left -= MOVESPEED
    if moveRight:
        player.left += MOVESPEED

    # wrap around
    if player.top < 0:
        player.top = WINDOWHEIGHT - player.height
    elif player.bottom > WINDOWHEIGHT:
        player.top = 0
    if player.left < 0:
        player.left = WINDOWWIDTH - player.width
    elif player.right > WINDOWWIDTH:
        player.left = 0

    # não permitir jogador passar sobre as pedras
    playerRect = player.inflate(-5, -5)
    for stone in stones:
        if playerRect.colliderect(stone):
            game_over()  # função game_over quando o jogador encosta em um obstáculo

    # permitir jogador "comer" as peças
    for food in foods[:]:
        if player.colliderect(food):
            foods.remove(food)
            score += 1  # contabilizar a peça comida na pontuação
            display_score() # exibir a pontuação no terminal

            # crescer o jogador
            player.inflate_ip(5, 5)

    # definindo a cor de fundo
    windowSurface.fill(BLACK)


    # desenhando as pedras
    for stone in stones:
        pygame.draw.rect(windowSurface, AQUA, stone)

    # desenhando jogador
    pygame.draw.rect(windowSurface, PINK, player)

    # desenhando comidas
    for i in range(len(foods)):
        pygame.draw.rect(windowSurface, GREEN, foods[i])

    pygame.display.update()
    mainClock.tick(40)
