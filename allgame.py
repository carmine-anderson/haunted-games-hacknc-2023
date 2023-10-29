game_selection = 0

while game_selection not in [1, 2, 3]:
    try:
        game_selection = int(input("Choose a game to play by typing in the number associated with the game: (1) Haunted Flappy Bird, (2) Haunted Snake Game, (3) Pumpkin Decorating: "))
    except ValueError:
        print("That was not a valid number. Please choose from the following: (1) Haunted Flappy Bird, (2) Haunted Snake Game, (3) Pumpkin Decorating")


if game_selection == 1:
    import pygame
    import sys
    import time
    import random
    import pygame.mixer

    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()

    js = False
    momo = pygame.image.load("momo2.png")

    js_sound = pygame.mixer.Sound("jumpscare_sound.mp3")
    fb_bg = pygame.mixer.Sound("flappybird.mp3")

    def display_jumpscare():
        screen.blit(momo, (0, 0))
        pygame.display.update()
        time.sleep(0.5)

    def draw_floor():
        screen.blit(floor_img, (floor_x, 520))
        screen.blit(floor_img, (floor_x + 448, 520))
    def create_pipes():
        pipe_y = random.choice(pipe_height)
        top_pipe = pipe_img.get_rect(midbottom=(467, pipe_y - 300))
        bottom_pipe = pipe_img.get_rect(midtop=(467, pipe_y))
        return top_pipe, bottom_pipe
    def pipe_animation():
        global game_over, score_time
        for pipe in pipes:
            if pipe.top < 0:
                flipped_pipe = pygame.transform.flip(pipe_img, False, True)
                screen.blit(flipped_pipe, pipe)
            else:
                screen.blit(pipe_img, pipe)
            pipe.centerx -= 3
            if pipe.right < 0:
                pipes.remove(pipe)
            if bird_rect.colliderect(pipe):
                game_over = True

    # Function to draw score
    def draw_score(game_state):
        if game_state == "game_on":
            score_text = score_font.render(str(score), True, (255, 255, 255))
            score_rect = score_text.get_rect(center = (width // 2, 66))
            screen.blit(score_text, score_rect)
        elif game_state == "game_over":
            score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
            score_rect = score_text.get_rect(center = (width // 2, 66))
            screen.blit(score_text, score_rect)

            high_score_text = score_font.render(f"High Score: {high_score}",
                                                True, (255, 255, 255))
            high_score_rect = high_score_text.get_rect(center = (width // 2, 506))
            screen.blit(high_score_text, high_score_rect)

    # Function to update the score
    def score_update():
        global score, score_time, high_score
        if pipes:
            for pipe in pipes:
                if 65 < pipe.centerx < 69 and score_time:
                    score += 1
                    score_time = False
                if pipe.left <= 0: 
                    score_time = True

        if score > high_score:
            high_score = score

    # Game window

    width, height = 350, 622
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Spooky Flappy Bird")

    # Setting background and base image
    back_img = pygame.image.load("halloween_fb.png")
    floor_img = pygame.image.load("halloween_fb_floor.png")
    floor_x = 0

    # Different stages of bird
    bird_up = pygame.image.load("fb_up_rs.png")
    bird_down = pygame.image.load("fb_down_rs.png")
    bird_mid = pygame.image.load("fb_mid_rs.png")
    birds = [bird_up, bird_mid, bird_down]
    bird_index = 0
    bird_flap = pygame.USEREVENT
    pygame.time.set_timer(bird_flap, 200)
    bird_img = birds[bird_index]
    bird_rect = bird_img.get_rect(center = (67, 622 // 2))
    bird_movement = 0
    gravity = 0.15

    # Loading pipe image
    pipe_img = pygame.image.load("new_pipe.png")
    pipe_height = [400, 350, 456, 490]

    # For the pipes to appear
    pipes = []
    create_pipe = pygame.USEREVENT + 12
    pygame.time.set_timer(create_pipe, 1200)

    # Displaying game over image
    game_over = False
    over_img = pygame.image.load("fb_gameover.png").convert_alpha()
    over_rect = over_img.get_rect(center = (width // 2, height // 2))

    # Setting variables and font for score
    score = 0
    high_score = 0
    score_time = True
    score_font = pygame.font.Font("freesansbold.ttf", 27)

    # Loop of the game
    running = True
    fb_bg.play()
    while running:
        clock.tick(120)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird_movement = 0
                    bird_movement = -6

                if event.key == pygame.K_SPACE and game_over:
                    game_over = False
                    pipes = []
                    bird_movement = 0 
                    bird_rect = bird_img.get_rect(center = (67, 622 // 2))
                    score_time = True
                    score = 0

            if event.type == bird_flap:
                bird_index += 1

                if bird_index > 2:
                    bird_index = 0

                bird_img = birds[bird_index]
                bird_rect = bird_up.get_rect(center = bird_rect.center)

            # Adding pipes
            if event.type == create_pipe:
                pipes.extend(create_pipes())


        screen.blit(floor_img, (floor_x, 550))
        screen.blit(back_img, (0, 0))

        # when the game completes
        if not game_over:
            bird_movement += gravity
            bird_rect.centery += bird_movement
            rotated_bird = pygame.transform.rotozoom(bird_img, bird_movement * -6, 1)

            if bird_rect.top < 5 or bird_rect.bottom >= 550:
                game_over = True
            
            screen.blit(rotated_bird, bird_rect)
            pipe_animation()
            score_update()
            draw_score("game_on")

            if score > 2 and not js:
                js_sound.play()
                display_jumpscare()
                js = True
        elif game_over:
            screen.blit(over_img, over_rect)
            draw_score("game_over")

        floor_x -= 1
        if floor_x < -448:
            floor_x = 0
        
        draw_floor()

        pygame.display.update()

    pygame.quit()
    sys.exit()

if game_selection == 2:
    """Snake Game :)"""

    import pygame
    import time
    import random
    import pygame.mixer

    pygame.mixer.init()
    pygame.init()
    white = (255, 255, 255)
    yellow = (255, 255, 255)
    black = (0, 0, 0)
    red = (213, 50, 80)
    green = (0, 255, 0)
    blue = (50, 153, 213)
    orange = (255, 172, 28)

    jumpscare_display = False

    dis_width = 700
    dis_height = 500

    dis = pygame.display.set_mode((dis_width, dis_height))
    pygame.display.set_caption('Haunted Snake Game by Carmine')

    clock = pygame.time.Clock()

    snake_block = 10
    snake_speed = 15

    font_style = pygame.font.SysFont("bahnschrift", 25)
    score_font = pygame.font.SysFont("comicsansms", 25)

    background_image = pygame.image.load("halloween2.jpeg")
    background_image2 = pygame.image.load("starter_backgroung.jpeg")
    momo = pygame.image.load("momo.png")

    eat_sound = pygame.mixer.Sound("eating_sound.mp3")
    jumpscare_sound = pygame.mixer.Sound("jumpscare_sound.mp3")
    bg_music = pygame.mixer.Sound("horror.mp3")
    dc_join = pygame.mixer.Sound("discord.mp3")

    # new_width = 10
    # new_height = 8
    # resized_ghost = ghost_image.resize((new_width, new_height))

    dis.blit(background_image2, (0, 0))
    pygame.display.update()

    # Jumpscare
    def display_jumpscare():
        dis.blit(momo, (0, 0))
        pygame.display.update()
        time.sleep(1)

    def Your_score(score):
        value = score_font.render("Your score: " + str(score), True, yellow)
        dis.blit(value, [0, 0])

    def our_snake(snake_block, snake_list):
        for x in snake_list:
            # if x == snake_list[0]:  # Draw the ghost image as the snake head
            #     dis.blit(ghost_image, (x[0], x[1]))
            # else:
            #     pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

            # dis.blit(ghost_image, (x[0], x[1]))
            # pygame.display.update()

            pygame.draw.rect(dis, white, [x[0], x[1], snake_block, snake_block])

    def message(msg, color):
        mesg = font_style.render(msg, True, color)
        dis.blit(mesg, [dis_width / 6, dis_height / 3])

    bg_music.play()
    def gameLoop():
        game_over = False
        game_close = False

        x1 = dis_width / 2
        y1 = dis_height / 2

        x1_change = 0 
        y1_change = 0

        snake_List = []
        Length_of_snake = 1

        foodx = round(random.randrange(0, dis_width - snake_block) / 10,0) * 10.0
        foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

        while not game_over:
            dis.blit(background_image2, (0, 0))
            pygame.display.update()

            while game_close == True:
                if Length_of_snake < 2:
                    dis.blit(background_image, (0, 0))
                    message("Don't play if you do not want to play..", white)
                    pygame.display.update()
                    time.sleep(3)
                    game_over = True
                    game_close = False

                elif jumpscare_display:
                    jumpscare_sound.play()
                    display_jumpscare()
                    jumpscare_display = False
                dis.blit(background_image, (0, 0))
                message("You Lost! Press C-Play Again or Q-Quit", white)
                Your_score(Length_of_snake - 1)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            gameLoop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x1_change = -snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        y1_change = -snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        y1_change = snake_block
                        x1_change = 0

            

            if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
                game_close = True
                dc_join.play()
            x1 += x1_change
            y1 += y1_change
            dis.fill(black)
            pygame.draw.rect(dis, orange, [foodx, foody, snake_block, snake_block])
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True
            
            our_snake(snake_block, snake_List)
            Your_score(Length_of_snake - 1)

        
            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                Length_of_snake += 1
                jumpscare_display = True
                eat_sound.play()
            
            clock.tick(snake_speed)

        pygame.mixer.quit()
        pygame.quit()
        quit()


    gameLoop()

if game_selection == 3:
    """Carve your own jack-o-lantern, by Em and Riley."""

    import pygame
    
    pygame.init()   

    # setting the screen, the title, and the pumpkin
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    bg_image = pygame.image.load("hall_ween.jpeg")
    bg_image = pygame.transform.scale(bg_image,(SCREEN_WIDTH, SCREEN_HEIGHT))
    text_font = pygame.font.Font(None, 50)
    instructions_font = pygame.font.Font(None, 25)
    title = text_font.render(("Decorate Your Own Pumpkin!"), True, "#000000" )
    instructions = instructions_font.render(("Click on the object to decorate your pumpkin"), True, "#000000")
    pumpkin = pygame.image.load("pumpkin.png")
    pumpkin = pygame.transform.scale(pumpkin, (300, 300))


    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # creates the screen
    # loading button images
    witch = pygame.image.load("witch_hat.png").convert_alpha()
    witch_on_pumpkin = pygame.transform.scale(witch, (150,150))
    party = pygame.image.load("party.png").convert_alpha()
    party_on_pumpkin = pygame.transform.scale(party, (150,150))
    devil = pygame.image.load("devil.png").convert_alpha()
    devil_on_pumpkin = pygame.transform.scale(devil, (250,250))
    triangle = pygame.image.load("triangle.png").convert_alpha()
    triangle_on_pumpkin = pygame.transform.scale(triangle, (150,100))
    cute = pygame.image.load("cute.png").convert_alpha()
    cute_on_pumpkin = pygame.transform.scale(cute, (150, 90))
    evil = pygame.image.load("evil.png").convert_alpha()
    evil_on_pumpkin = pygame.transform.scale(evil, (150, 100))
    surpise = pygame.image.load("surpise.png").convert_alpha()
    surpise_on_pumpkin = pygame.transform.scale(surpise, (125, 75))
    goofy = pygame.image.load("goofy.png").convert_alpha()
    goofy_on_pumpkin = pygame.transform.scale(goofy, (125, 75))
    fangs = pygame.image.load("fangs.png").convert_alpha()
    fangs_on_pumpkin = pygame.transform.scale(fangs, (125, 75))



    # button class
    class Button():
        def __init__(self, x, y, image, scale):
            width = image.get_width()
            height = image.get_height()
            self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
            self.rect = self.image.get_rect()
            self.rect.topleft = (x,y)
            self.clicked = False
        def draw(self):
            action = False
            #get mouse position
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    action = True
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False
            
            screen.blit(self.image, (self.rect.x, self.rect.y))

            return action

    # creating button instances

    # hat buttons
    witch_button = Button(100, 350, witch, 0.2 )
    witch_visible = False
    party_button = Button(300, 390, party, 0.4)
    party_visible = False
    devil_button = Button(500, 350, devil, 0.2)
    devil_visible = False

    # eye buttons
    triangle_button = Button(40, 140, triangle, 0.35)
    triangle_visible = False
    cute_button = Button(40, 217, cute, 0.15)
    cute_visible = False
    evil_button = Button(40, 260, evil, 0.15)
    evil_visible = False

    # mouth buttons
    surpise_button = Button(600, 150, surpise, 0.17)
    surpise_visible = False
    goofy_button = Button(600, 225, goofy, 0.13)
    goofy_visible = False
    fangs_button = Button(600, 300, fangs, 0.13)
    fangs_visible = False

    run = True 
    while run: 
        screen.blit(bg_image,(0,0))
        screen.blit(title, (150,40))
        screen.blit(instructions, (220, 75))
        screen.blit(pumpkin, (250, 100))
        # running the hats
        if witch_button.draw():
            devil_visible = False
            party_visible = False
            witch_visible = True
        if witch_visible == True:
            screen.blit(witch_on_pumpkin, (325, 75))
        if party_button.draw():
            devil_visible = False
            witch_visible = False
            party_visible = True
        if party_visible == True:
            screen.blit(party_on_pumpkin, (250, 75))
        if devil_button.draw():
            witch_visible = False
            party_visible = False
            devil_visible = True
        if devil_visible == True:
            screen.blit(devil_on_pumpkin, (270, 45))
        
        # running the eyes
        if triangle_button.draw():
            evil_visible = False
            cute_visible = False
            triangle_visible = True
        if triangle_visible == True:
            screen.blit(triangle_on_pumpkin, (315, 200))
        if cute_button.draw():
            evil_visible = False
            triangle_visible = False
            cute_visible = True
        if cute_visible == True:
            screen.blit(cute_on_pumpkin, (315, 225))
        if evil_button.draw():
            cute_visible = False
            triangle_visible = False
            evil_visible = True
        if evil_visible == True:
            screen.blit(evil_on_pumpkin, (315, 220))

        # running the mouth
        if surpise_button.draw():
            goofy_visible = False
            fangs_visible = False
            surpise_visible = True
        if surpise_visible == True:
            screen.blit(surpise_on_pumpkin, (330, 280))
        if goofy_button.draw():
            fangs_visible = False
            surpise_visible = False
            goofy_visible = True
        if goofy_visible == True:
            screen.blit(goofy_on_pumpkin, (330, 280))
        if fangs_button.draw():
            surpise_visible = False
            goofy_visible = False
            fangs_visible = True
        if fangs_visible == True:
            screen.blit(fangs_on_pumpkin, (335, 280))
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
        
    pygame.quit()