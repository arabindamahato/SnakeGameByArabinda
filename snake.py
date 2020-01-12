import pygame
import random
import os
import pygame

pygame.mixer.init() # for music
pygame.init()


# colors
skyblue = (51, 255, 243)
red = (250, 30, 4)
blue = (7, 11, 91)
pink = (235,135,206)
white = (255, 255, 255)
green = (71, 250, 4 )

# creating game window
screen_width = 850
screen_height = 450
gameWindow = pygame.display.set_mode((screen_width, screen_height))  # display.set_mode() - displays the gamewindow with given height and width


# Background image for game
bgimage = pygame.image.load("blank_border.jpeg")
bgimage = pygame.transform.scale(bgimage, (screen_width, screen_height)).convert_alpha()

# Background image for welcome page
bgimage_welcome = pygame.image.load("wc4.jpeg")
bgimage_welcome = pygame.transform.scale(bgimage_welcome, (screen_width, screen_height)).convert_alpha()

# Background image for gameover
bgimage_gameover = pygame.image.load("gameover.jpeg")
bgimage_gameover = pygame.transform.scale(bgimage_gameover, (screen_width, screen_height)).convert_alpha()



pygame.display.set_caption("SnakesWithArvind")   # set_caption() - set the game name on the caption of window
pygame.display.update() # it sets the background images of window


clock = pygame.time.Clock()

# To display score on the game window
font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(green)
        gameWindow.blit(bgimage_welcome, (0, 0))
        # text_screen("Welcome to Snake Game", pink, 180, 200)
        # text_screen("Press space to play the game", red, 160, 250)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.load('gameplay.mp3')
                    pygame.mixer.music.play()
                    gameloop()
        pygame.display.update()
        clock.tick(60)


# game loop
def gameloop():
    # game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 50
    velocity_x = 0
    velocity_y = 0

    snk_list = []
    snk_lenth = 1
    # check if high score file exist
    if (not os.path.exists("high_score.txt")):
        with open("high_score.txt","w") as f:
            f.write("0")

    with open("high_score.txt", "r") as f:
        high_score = f.read()

    food_x = random.randint(20, screen_height / 2)  # randomly food coms in different positions
    food_y = random.randint(20, screen_width / 2)
    score = 0
    init_velocity = 8
    snake_size = 20
    fps = 15
    while not exit_game:
        if game_over:
            with open("high_score.txt", "w") as f:
                f.write(str(high_score))
            gameWindow.fill(blue)
            gameWindow.blit(bgimage_gameover, (0, 0))
            # text_screen("Game Over ! Press Enter to continue ", red, screen_width/10, screen_width/10)

            for event in pygame.event.get(): #  event.get() - accepets the key board/ mouse event .
                if event.type == pygame.QUIT: # if type of event is == game.QUIT (cross button on window) then game will exit.( When I want to quit event then only it will quit)
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get(): #  event.get() - accepets the key board/ mouse event
                if event.type == pygame.QUIT: # if type of event is == game.QUIT then game will exit.( When I want to quit event then only it will quit)
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                    #chit code
                    if event.key == pygame.K_q:
                        score = score+10


            snake_x += velocity_x
            snake_y += velocity_y

            # snake and food position is same[approx{abs()=absolute value}] then score will increse
            if abs(snake_x - food_x)<15 and abs(snake_y - food_y)<15:
                score+=10
                # print("Score :", score * 10)
                food_x = random.randint(20, screen_height / 2)  # randomly food comes in different positions
                food_y = random.randint(20, screen_width / 2)
                snk_lenth += 5
                if score>int(high_score):
                    high_score = score

            gameWindow.fill(skyblue)
            gameWindow.blit(bgimage, (0, 0))
            text_screen(" Score : " + str(score)+ "  HighScore : " + str(high_score), red, 5, 5)  # displaying the score on game window
            pygame.draw.rect(gameWindow, green, [food_x, food_y, snake_size, snake_size])  # drawing a food with red color


            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            # if snake list is greater than snake length then delete the snake o'th eement
            if len(snk_list)>snk_lenth:
                del snk_list[0]

            if head in snk_list[:-1]: # snk_list means snake body. snk_list[:-1] means all body except head(head is the last element)
                game_over = True
                pygame.mixer.music.load("gameover.mp3")
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load("gameover.mp3")
                pygame.mixer.music.play()

            plot_snake(gameWindow, blue, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps) # fps = frame per second


    pygame.quit()
    quit()
welcome()
# gameloop()
