from abc import ABC, abstractmethod
from tkinter import *
import os.path
import pygame
from random import randint

window = Tk()
window_height = 400
window_width = 600

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

window.geometry("{}x{}+{}+{}".format(window_width,
                window_height, x_cordinate, y_cordinate))
window.title("PONG")
window.resizable(False, False)
window.config(bg='black')


class SpecialError(Exception):
    pass

class DataError(Exception):
    pass

def check_file_exist(filepath):
    if not os.path.isfile(filepath):
        print("{:^40}".format("File does not exist."))
        raise SpecialError

def check_data(text):
    if text == []:
        print("{:^40}".format("File is empty."))
        raise DataError

def setting_recall(pong_setting_object):
    global score_limit
    global ball_x_velocity
    setting_list = ["score_set", "ball_speed"]
    print("{:=^40}".format("<Setting_recall>"))
    try:
        check_file_exist("setting.txt")
        print("{:^40}".format("File found."))
        f = open("setting.txt", "r")
        text = f.readlines()
        f.close()
        # replace "\n" with ""
        try:
            check_data(text)
            for index in range(len(text)):
                if "\n" in text[index]:
                    new_text = text[index].replace("\n", "")
                    text[index] = new_text
            for each_setting in text:
                sub_setting = each_setting.split(" = ")
                if len(sub_setting) != 2 or sub_setting[0] not in setting_list:
                    raise DataError
                if sub_setting[0] == "score_set":
                    score_limit = int(sub_setting[1])
                    if score_limit >= 999:
                        change_textvariable(pong_setting_object.score_selected_var, "Endless")
                    else:
                        change_textvariable(pong_setting_object.score_selected_var, sub_setting[1])
                elif sub_setting[0] == "ball_speed":
                    ball_x_velocity = int(sub_setting[1])
                    if ball_x_velocity == 5:
                        change_textvariable(pong_setting_object.speed_selected_var, "Slow")
                    elif ball_x_velocity == 10:
                        change_textvariable(pong_setting_object.speed_selected_var, "Medium")
                    elif ball_x_velocity == 15:
                        change_textvariable(pong_setting_object.speed_selected_var, "Fast")
                    else:
                        change_textvariable(pong_setting_object.speed_selected_var, "Custom speed: " + sub_setting[1])
            print("{:^40}\n{:=^40}".format("<<<Recalling setting.txt>>>",""))
            # checking data values
            # print(f"Score_set: {score_limit} Max_velocity: {ball_x_velocity}")
        except DataError:
            print("{:^40}".format("Data corrupted."))
            raise SpecialError
            
            
    except SpecialError:
        print("{:^40}\n{:=^40}".format("<<<Initializing new setting.txt>>>",""))
        f = open("setting.txt", "w")
        f.write("score_set = 10\nball_speed = 10")
        f.close()

        f = open("setting.txt", "r")
        text = f.readlines()
        f.close()
        
        # replace "\n" with ""
        for index in range(len(text)):
            if "\n" in text[index]:
                new_text = text[index].replace("\n", "")
                text[index] = new_text
        for each_setting in text:
            sub_setting = each_setting.split(" = ")
            if sub_setting[0] == "score_set":
                score_limit = int(sub_setting[1])
                if int(sub_setting[1]) >= 999:
                    change_textvariable(pong_setting_object.score_selected_var, "Endless")
                else:
                    change_textvariable(pong_setting_object.score_selected_var, sub_setting[1])
            elif sub_setting[0] == "ball_speed":
                ball_x_velocity = int(sub_setting[1])
                if ball_x_velocity == 5:
                    change_textvariable(pong_setting_object.speed_selected_var, "Slow")
                elif ball_x_velocity == 10:
                    change_textvariable(pong_setting_object.speed_selected_var, "Medium")
                elif ball_x_velocity == 15:
                    change_textvariable(pong_setting_object.speed_selected_var, "Fast")
                else:
                    change_textvariable(pong_setting_object.speed_selected_var, "Custom: " + sub_setting[1])
        # checking data values
        # print(f"Score_set: {score_limit} Max_velocity: {ball_x_velocity}")


def change_screen(present_screen, next_screen):
    present_screen.forget_screen()
    next_screen.show_screen()

def change_textvariable(stringvariable, text):
    stringvariable.set(text)

# change global variable and also save it to file
def change_global_variable(setting_key, new_value):
    global ball_x_velocity
    global score_limit
    f = open("setting.txt", "w")
    if setting_key == "ball_speed":
        ball_x_velocity = new_value
        f.write(f"score_set = {str(score_limit)}\nball_speed = {str(new_value)}")
    elif setting_key == "score_set":
        score_limit = new_value
        f.write(f"score_set = {str(new_value)}\nball_speed = {str(ball_x_velocity)}")
    f.close()


class Screen(ABC):
    @abstractmethod
    def show_screen(self):
        pass

    @abstractmethod
    def forget_screen(self):
        pass


class PongMenu(Screen):
    def __init__(self, master):
        self.title = Label(master,
                           text="PONG",
                           font=('Georgia 50 bold'),
                           bg='black',
                           fg='white'
                           )
        self.bStart = Button(master,
                             text="Start",
                             font=('Georgia 10 bold'),
                             width=10,
                             height=1,
                             padx=5,
                             pady=5,
                             command=lambda: change_screen(Menu, Pregame)
                             )
        self.bSetting = Button(master,
                               text="Setting",
                               font=('Georgia 10 bold'),
                               width=10,
                               height=1,
                               padx=5,
                               pady=5,
                               command=lambda: change_screen(Menu, Setting)
                               )
        self.bQuit = Button(master,
                            text="Quit",
                            font=('Georgia 10 bold'),
                            width=10,
                            height=1,
                            padx=5,
                            pady=5,
                            command=window.destroy
                            )

    def show_screen(self):
        self.title.pack(padx=200, pady=50)
        self.bStart.pack(padx=200, pady=10)
        self.bSetting.pack(padx=200, pady=10)
        self.bQuit.pack(padx=200, pady=10)

    def forget_screen(self):
        self.title.pack_forget()
        self.bStart.pack_forget()
        self.bSetting.pack_forget()
        self.bQuit.pack_forget()


class PongSetting(Screen):
    def __init__(self, master):
        # Score limit
        self.score_limit = Label(master,
                                 text="Score Limit",
                                 font=('Georgia 20 bold'),
                                 bg='black',
                                 fg='white'
                                 )
        self.score_selected_var = StringVar()
        self.score_selected = Label(master,
                                    textvariable=self.score_selected_var,
                                    font=('Georgia 20 bold'),
                                    bg='black',
                                    fg='white'
                                    )
        self.score_select_frame = Frame(master,
                                        bg='black'
                                        )
        self.bScore_limit_5 = Button(self.score_select_frame,
                                     text="5",
                                     font=('Georgia 10 bold'),
                                     width=2,
                                     height=1,
                                     padx=5,
                                     pady=2,
                                     command=lambda: [change_textvariable(self.score_selected_var, "5"), change_global_variable("score_set", 5)]
                                     )
        self.bScore_limit_10 = Button(self.score_select_frame,
                                      text="10",
                                      font=('Georgia 10 bold'),
                                      width=2,
                                      height=1,
                                      padx=5,
                                      pady=2,
                                      command=lambda: [change_textvariable(self.score_selected_var, "10"), change_global_variable("score_set", 10)]
                                      )
        self.bScore_limit_15 = Button(self.score_select_frame,
                                      text="15",
                                      font=('Georgia 10 bold'),
                                      width=2,
                                      height=1,
                                      padx=5,
                                      pady=2,
                                      command=lambda: [change_textvariable(self.score_selected_var, "15"), change_global_variable("score_set", 15)]
                                      )
        self.bScore_limit_20 = Button(self.score_select_frame,
                                      text="20",
                                      font=('Georgia 10 bold'),
                                      width=2,
                                      height=1,
                                      padx=5,
                                      pady=2,
                                      command=lambda: [change_textvariable(self.score_selected_var, "20"), change_global_variable("score_set", 20)]
                                      )
        self.bScore_limit_infinite = Button(self.score_select_frame,
                                            text="Endless",
                                            font=('Georgia 10 bold'),
                                            height=1,
                                            width=6,
                                            padx=5,
                                            pady=2,
                                            command=lambda: [change_textvariable(self.score_selected_var, "Endless"), change_global_variable("score_set", 999)]
                                            )
        # Ball speed
        self.ball_speed = Label(master,
                                text="Ball Speed",
                                font=('Georgia 20 bold'),
                                bg='black',
                                fg='white'
                                )
        self.speed_selected_var = StringVar()
        self.speed_selected = Label(master,
                                    textvariable=self.speed_selected_var,
                                    font=('Georgia 20 bold'),
                                    bg='black',
                                    fg='white'
                                    )
        self.speed_select_frame = Frame(master,
                                        bg='black'
                                        )
        self.bBall_speed_slow = Button(self.speed_select_frame,
                                       text="Slow",
                                       font=('Georgia 10 bold'),
                                       width=10,
                                       height=1,
                                       padx=5,
                                       pady=5,
                                       command=lambda: [change_textvariable(self.speed_selected_var, "Slow"), change_global_variable("ball_speed", 5)]
                                       )
        self.bBall_speed_medium = Button(self.speed_select_frame,
                                         text="Medium",
                                         font=('Georgia 10 bold'),
                                         width=10,
                                         height=1,
                                         padx=5,
                                         pady=5,
                                         command=lambda: [change_textvariable(self.speed_selected_var, "Medium"), change_global_variable("ball_speed", 10)]
                                         )
        self.bBall_speed_fast = Button(self.speed_select_frame,
                                       text="Fast",
                                       font=('Georgia 10 bold'),
                                       width=10,
                                       height=1,
                                       padx=5,
                                       pady=5,
                                       command=lambda: [change_textvariable(self.speed_selected_var, "Fast"), change_global_variable("ball_speed", 15)]
                                       )
        self.bBack = Button(master,
                            text="Back",
                            font=('Georgia 10 bold'),
                            width=7,
                            height=1,
                            padx=5,
                            pady=5,
                            command=lambda: change_screen(Setting, Menu)
                            )

    def show_screen(self):
        # Score limit
        self.score_limit.pack(padx=200, pady=10)
        self.score_selected.pack(pady=5)
        self.score_select_frame.pack()
        self.bScore_limit_5.pack(padx=5, pady=10, side=LEFT)
        self.bScore_limit_10.pack(padx=5, pady=10, side=LEFT)
        self.bScore_limit_15.pack(padx=5, pady=10, side=LEFT)
        self.bScore_limit_20.pack(padx=5, pady=10, side=LEFT)
        self.bScore_limit_infinite.pack(padx=5, pady=10, side=LEFT)
        # Ball speed
        self.ball_speed.pack(padx=200, pady=10)
        self.speed_selected.pack(pady=5)
        self.speed_select_frame.pack()
        self.bBall_speed_slow.pack(padx=5, pady=10, side=LEFT)
        self.bBall_speed_medium.pack(padx=5, pady=10, side=LEFT)
        self.bBall_speed_fast.pack(padx=5, pady=10, side=LEFT)

        self.bBack.pack(padx=200, pady=5)

    def forget_screen(self):
        # Score limit
        self.score_limit.pack_forget()
        self.score_selected.pack_forget()
        self.score_select_frame.pack_forget()
        self.bScore_limit_5.pack_forget()
        self.bScore_limit_10.pack_forget()
        self.bScore_limit_15.pack_forget()
        self.bScore_limit_20.pack_forget()
        self.bScore_limit_infinite.pack_forget()
        # Ball speed
        self.ball_speed.pack_forget()
        self.speed_selected.pack_forget()
        self.speed_select_frame.pack_forget()
        self.bBall_speed_slow.pack_forget()
        self.bBall_speed_medium.pack_forget()
        self.bBall_speed_fast.pack_forget()

        self.bBack.pack_forget()

    def get_score_limit(self):
        return self.score_selected_var.get()

    def get_ball_speed(self):
        return self.speed_selected_var.get()


class PongPregame(Screen):
    def __init__(self, master):
        self.title = Label(master,
                           text="PONG",
                           font=('Georgia 50 bold'),
                           bg='black',
                           fg='white'
                           )
        self.bSingleplayer = Button(master,
                                    text="Singleplayer",
                                    font=('Georgia 10 bold'),
                                    width=20,
                                    height=1,
                                    padx=5,
                                    pady=5,
                                    command=lambda: [window.withdraw(), start_game("Singleplayer")]
                                    )
        self.bMultiplayer = Button(master,
                                   text="Multiplayer",
                                   font=('Georgia 10 bold'),
                                   width=20,
                                   height=1,
                                   padx=5,
                                   pady=5,
                                   command=lambda: [window.withdraw(), start_game("Multiplayer")]
                                   )
        self.bBack = Button(master,
                            text="Back",
                            font=('Georgia 10 bold'),
                            width=7,
                            height=1,
                            padx=5,
                            pady=5,
                            command=lambda: change_screen(Pregame, Menu)
                            )

    def show_screen(self):
        self.title.pack(padx=200, pady=50)
        self.bSingleplayer.pack(padx=200, pady=10)
        self.bMultiplayer.pack(padx=200, pady=10)
        self.bBack.pack(padx=200, pady=5)

    def forget_screen(self):
        self.title.pack_forget()
        self.bSingleplayer.pack_forget()
        self.bMultiplayer.pack_forget()
        self.bBack.pack_forget()


Menu = PongMenu(window)
Setting = PongSetting(window)
Pregame = PongPregame(window)


# Pong game
# constant values

WIDTH = 700
HEIGHT = 500
FPS = 60

pygame.display.set_caption("Pong_Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100

BALL_RADIUS = 5

MIDDLE_LINE_WIDTH = 10
MIDDLE_LINE_HEIGHT = 25

score_limit = 10

# x move constanly and represent the max speed of the ball
ball_x_velocity = 5
# y move constanly only before the collision
ball_y_velovity = 0


class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = WHITE
        self.velocity = 5

    def draw(self, window):
        pygame.draw.rect(window, self.color,
                         (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.velocity
        else:
            self.y += self.velocity


class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = WHITE
        self.x_velocity = ball_x_velocity
        self.y_velocity = ball_y_velovity

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
        

class Score:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = WHITE
        self.score = 0
        self.font = pygame.font.SysFont("system", 40)

    def draw(self, window):
        text = self.font.render(str(self.score), 1, self.color)
        window.blit(text, (self.x, self.y))

    def increase(self):
        self.score += 1

    def reset(self):
        self.score = 0


# Movement functions

# paddle movement
def paddle_movement(keys, paddle, up_key, down_key):
    if keys[up_key] and paddle.y-paddle.velocity > 0:
        paddle.move(True)
    if keys[down_key] and paddle.y+paddle.height+paddle.velocity < HEIGHT:
        paddle.move(False)

# Dumb AI movement (follow ball.y)
def paddle_AI_movement1(ball, paddle):
    if ball.x_velocity > 0:
        if paddle.y+paddle.height//2 > ball.y+(2*paddle.velocity) and paddle.y-paddle.velocity > 0:
            paddle.move(True)
        elif paddle.y+paddle.height//2 < ball.y-(2*paddle.velocity) and paddle.y+paddle.height+paddle.velocity < HEIGHT:
            paddle.move(False)
    elif ball.x_velocity < 0:
        if paddle.y+paddle.height//2 > HEIGHT//2:
            paddle.move(True)
        elif paddle.y+paddle.height//2 < HEIGHT//2:
            paddle.move(False)

# Unbeatable AI movement (predict ball.y at the their paddle.x)
def paddle_AI_movement2(ball, paddle):
    if ball.x_velocity > 0:
        time = (paddle.x-ball.x)//ball.x_velocity + 1
        ball_temp = ball.y
        ball_v_temp = ball.y_velocity
        for i in range(time):
            ball_temp += ball_v_temp
            if ball_temp-ball.radius <= 0 or ball_temp+ball.radius >= HEIGHT:
                ball_v_temp *= -1
        if paddle.y+paddle.height//2 > ball_temp+(2*paddle.velocity) and paddle.y-paddle.velocity > 0:
            paddle.move(True)
        elif paddle.y+paddle.height//2 < ball_temp-(2*paddle.velocity) and paddle.y+paddle.height+paddle.velocity < HEIGHT:
            paddle.move(False)
    elif ball.x_velocity < 0:
        if paddle.y+paddle.height//2 > HEIGHT//2:
            paddle.move(True)
        elif paddle.y+paddle.height//2 < HEIGHT//2:
            paddle.move(False)

# Difficulty adjustable AI movement (hyprid of Dumb and Unbeatable AI)
AIMM3_back_to_middle = True
def paddle_AI_movement3(ball, paddle, difficulty):
    # difficulty max: 100, min: 0
    global AIMM3_back_to_middle
    if ball.x_velocity > 0:
        AIMM3_back_to_middle = 50 < randint(0, difficulty)
        if ball.x > HEIGHT - (difficulty/100)*HEIGHT:
            frames = (paddle.x-ball.x)//ball.x_velocity + 1
            ball_temp = ball.y
            ball_v_temp = ball.y_velocity
            for _ in range(frames):
                ball_temp += ball_v_temp
                if ball_temp-ball.radius <= 0 or ball_temp+ball.radius >= HEIGHT:
                    ball_v_temp *= -1
            if paddle.y+paddle.height//2 > ball_temp+(2*paddle.velocity) and paddle.y-paddle.velocity > 0:
                paddle.move(True)
            elif paddle.y+paddle.height//2 < ball_temp-(2*paddle.velocity) and paddle.y+paddle.height+paddle.velocity < HEIGHT:
                paddle.move(False)
        else:
            if paddle.y+paddle.height//2 > ball.y+(2*paddle.velocity) and paddle.y-paddle.velocity > 0:
                paddle.move(True)
            elif paddle.y+paddle.height//2 < ball.y-(2*paddle.velocity) and paddle.y+paddle.height+paddle.velocity < HEIGHT:
                paddle.move(False)
    elif ball.x_velocity < 0:
        if AIMM3_back_to_middle:
            if paddle.y+paddle.height//2 > HEIGHT//2:
                paddle.move(True)
            elif paddle.y+paddle.height//2 < HEIGHT//2:
                paddle.move(False)
        pass

# ball movement
def ball_movement(ball, left_paddle, right_paddle):
    # handle collision
    if ball.y-ball.radius <= 0 or ball.y+ball.radius >= HEIGHT:
        ball.y_velocity *= -1
    if ball.x_velocity > 0:
        if right_paddle.x+PADDLE_WIDTH >= ball.x+ball.radius >= right_paddle.x:
            if right_paddle.y <= ball.y <= right_paddle.y+PADDLE_HEIGHT:
                # collide with right paddle
                ball.x_velocity *= -1
                ball.y_velocity = (ball.y - right_paddle.y - PADDLE_HEIGHT//2)/(PADDLE_HEIGHT//2) * ball_x_velocity
    else:
        if left_paddle.x <= ball.x-ball.radius <= left_paddle.x+PADDLE_WIDTH:
            if left_paddle.y <= ball.y <= left_paddle.y+PADDLE_HEIGHT:
                # collide with right paddle
                ball.x_velocity *= -1
                ball.y_velocity = (ball.y - left_paddle.y - PADDLE_HEIGHT//2)/(PADDLE_HEIGHT//2) * ball_x_velocity

    ball.move()


def goal(ball, left_score, right_score):
    if ball.x+ball.radius < 0:
        right_score.increase()
        return True
    elif ball.x-ball.radius > WIDTH:
        left_score.increase()
        return True
    return False


def reset_ball(ball):
    ball.x = WIDTH//2
    ball.y = HEIGHT//2
    # ball.x_velocity doesn't change
    ball.y_velocity = ball_y_velovity


def draw(window, objects_list):
    window.fill(BLACK)

    # Draw paddles
    for object in objects_list:
        object.draw(window)

    # Draw the middle line
    for y in range(0, HEIGHT, 40):
        pygame.draw.rect(window, WHITE, (WIDTH//2 - MIDDLE_LINE_WIDTH //
                         2, y, MIDDLE_LINE_WIDTH, MIDDLE_LINE_HEIGHT))

    pygame.display.update()


def check_winner(left_score, right_score, gamemode):
    if gamemode == "Singleplayer":
        if left_score.score == score_limit:
            return "Player"
        elif right_score.score == score_limit:
            return "CPU"
    elif gamemode == "Multiplayer":
        if left_score.score == score_limit:
            return "Left Player"
        elif right_score.score == score_limit:
            return "Right Player"
    return



def pause(window2, left_score, right_score, window):
    window2.fill(BLACK)
    pause_font = pygame.font.SysFont("system", 60)
    discription_font = pygame.font.SysFont("system", 30)
    text1 = pause_font.render("PAUSE", 1, WHITE)
    text2 = discription_font.render(
        "Press ESC to continue / Press m to MENU / Press q to quit", 1, WHITE)
    window2.blit(text1, (WIDTH//2-70, HEIGHT//2-50))
    window2.blit(text2, (WIDTH//2-270, HEIGHT//2+50))
    pygame.display.update()

    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("{:^40}".format("No contest!\n"))
                left_score.reset()
                right_score.reset()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == "q":
                    print("{:^40}".format("No contest!\n"))
                    left_score.reset()
                    right_score.reset()
                    pygame.quit()
                    exit()
                if pygame.key.name(event.key) == "escape":
                    pause = False
                    return False
                if pygame.key.name(event.key) == "m":
                    print("{:^40}".format("No contest!\n"))
                    left_score.reset()
                    right_score.reset()
                    pygame.quit()
                    window.deiconify()
                    return True


def result_screen(window2, winner, window):
    window2.fill(BLACK)
    win_font = pygame.font.SysFont("system", 60)
    discription_font = pygame.font.SysFont("system", 30)
    text1 = win_font.render("WINNER", 1, WHITE)
    text2 = discription_font.render("{:^11} won the game".format(winner), 1, WHITE)
    text3 = discription_font.render(
        "Press m to MENU / Press q to quit", 1, WHITE)
    window2.blit(text1, (WIDTH//2-85, HEIGHT//2-60))
    window2.blit(text2, (WIDTH//2-125, HEIGHT//2+10))
    window2.blit(text3, (WIDTH//2-160, HEIGHT//2+50))
    pygame.display.update()

    result_screen = True
    while result_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                window.destroy()
                exit()
            if event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == "q":
                    pygame.quit()
                    window.destroy()
                    exit()
                if pygame.key.name(event.key) == "m":
                    pygame.quit()
                    window.deiconify()
                    return True


def start_game(gamemode):
    pygame.init()
    window2 = pygame.display.set_mode((WIDTH, HEIGHT))
    run = True
    clock = pygame.time.Clock()

    if gamemode == "Multiplayer":
        print("{:^40}".format("GameMode: " + str(gamemode)))

        left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT //2, PADDLE_WIDTH, PADDLE_HEIGHT)
        right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT //2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
        ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)
        left_score = Score(WIDTH//2 - 70, 50)
        right_score = Score(WIDTH//2 + 50, 50)

        while run:
            draw(window2, [left_paddle, right_paddle,
                ball, left_score, right_score])
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("{:^40}".format("No contest!\n"))
                    left_score.reset()
                    right_score.reset()
                    run = False
                    window.destroy()
                    break
                if event.type == pygame.KEYDOWN:
                    if pygame.key.name(event.key) == "escape":
                        if pause(window2, left_score, right_score, window):
                            return

                    # Define the keys for each paddle
            keys = pygame.key.get_pressed()

            paddle_movement(keys, left_paddle, pygame.K_w, pygame.K_s)
            paddle_movement(keys, right_paddle, pygame.K_UP, pygame.K_DOWN)
            ball_movement(ball, left_paddle, right_paddle)

            if goal(ball, left_score, right_score):
                reset_ball(ball)

                # Check if someone won
            if check_winner(left_score, right_score, gamemode) == "Left Player" or check_winner(left_score, right_score, gamemode) == "Right Player":
                winner = check_winner(left_score, right_score, gamemode)
                left_score.reset()
                right_score.reset()
                print("{:^40}".format(f"Winner<{winner}>\n"))
                if result_screen(window2, winner, window):
                    return

    elif gamemode == "Singleplayer":
        print("{:^40}".format("GameMode: " + str(gamemode)))

        left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT //2, PADDLE_WIDTH, PADDLE_HEIGHT)
        right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT //2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
        ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)
        left_score = Score(WIDTH//2 - 70, 50)
        right_score = Score(WIDTH//2 + 50, 50)

        while run:
            draw(window2, [left_paddle, right_paddle,
                ball, left_score, right_score])
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    left_score.reset()
                    right_score.reset()
                    run = False
                    window.destroy()
                    break
                if event.type == pygame.KEYDOWN:
                    if pygame.key.name(event.key) == "escape":
                        if pause(window2, left_score, right_score, window):
                            return

                    # Define the keys for each paddle
            keys = pygame.key.get_pressed()

            paddle_movement(keys, left_paddle, pygame.K_w, pygame.K_s)
            paddle_AI_movement2(ball, right_paddle)
            ball_movement(ball, left_paddle, right_paddle)

            if goal(ball, left_score, right_score):
                reset_ball(ball)

                # Check if someone won
            if check_winner(left_score, right_score, gamemode) == "Player" or check_winner(left_score, right_score, gamemode) == "CPU":
                winner = check_winner(left_score, right_score, gamemode)
                left_score.reset()
                right_score.reset()
                print("{:^40}".format(f"Winner<{winner}>\n"))
                if result_screen(window2, winner, window):
                    return
                    
    else:
        print("Invalid gamemode")
    
    pygame.quit()


def main():
    Menu.show_screen()
    setting_recall(Setting)
    window.mainloop()


if __name__ == "__main__":
    main()
