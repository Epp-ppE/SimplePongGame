import pygame
pygame.init()

WIDTH = 700
HEIGHT = 500
FPS = 60
window2 = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong_Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100

BALL_RADIUS = 5

MIDDLE_LINE_WIDTH = 10
MIDDLE_LINE_HEIGHT = 25

score_limit = 5

max_velocity = 10
# x move constanly
ball_x_velocity = max_velocity
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
		pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

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


def paddle_movement(keys, paddle, up_key, down_key):
	if keys[up_key] and paddle.y-paddle.velocity > 0:
		paddle.move(True)
	if keys[down_key] and paddle.y+paddle.height+paddle.velocity < HEIGHT:
		paddle.move(False)

def ball_movement(ball, left_paddle, right_paddle):
	# handle collision
	if ball.y-ball.radius <= 0 or ball.y+ball.radius >= HEIGHT:
		ball.y_velocity *= -1
	if ball.x_velocity > 0:
		if right_paddle.x+PADDLE_WIDTH >= ball.x+ball.radius >= right_paddle.x:
			if right_paddle.y <= ball.y <= right_paddle.y+PADDLE_HEIGHT:
				# collide with right paddle
				ball.x_velocity *= -1
				ball.y_velocity = (ball.y - right_paddle.y - PADDLE_HEIGHT//2)/(PADDLE_HEIGHT//2) * max_velocity
	else:
		if left_paddle.x <= ball.x-ball.radius <= left_paddle.x+PADDLE_WIDTH:
			if left_paddle.y <= ball.y <= left_paddle.y+PADDLE_HEIGHT:
				# collide with right paddle
				ball.x_velocity *= -1
				ball.y_velocity = (ball.y - left_paddle.y - PADDLE_HEIGHT//2)/(PADDLE_HEIGHT//2) * max_velocity
	
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
		pygame.draw.rect(window, WHITE, (WIDTH//2 - MIDDLE_LINE_WIDTH//2, y, MIDDLE_LINE_WIDTH, MIDDLE_LINE_HEIGHT))

	pygame.display.update()

def check_winner(left_score, right_score):
	if left_score.score == score_limit:
		return "Left Player"
	elif right_score.score == score_limit:
		return "Right Player"
	return None

def pause(window):
	window.fill(BLACK)
	pause_font = pygame.font.SysFont("system", 60)
	discription_font = pygame.font.SysFont("system", 30)
	text1 = pause_font.render("PAUSE", 1, WHITE)
	text2 = discription_font.render("Press ESC to continue / Press m to MENU / Press q to quit", 1, WHITE)
	window.blit(text1, (WIDTH//2-70, HEIGHT//2-50))
	window.blit(text2, (WIDTH//2-270, HEIGHT//2+50))
	pygame.display.update()

	pause = True
	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if pygame.key.name(event.key) == "q":
					pygame.quit()
					quit()
				if pygame.key.name(event.key) == "escape":
					pause = False
				if pygame.key.name(event.key) == "m":
					pygame.quit()
					# Menu.show_screen()
    				# window.mainloop()
	
def result_screen(window, winner):
	window.fill(BLACK)
	win_font = pygame.font.SysFont("system", 60)
	discription_font = pygame.font.SysFont("system", 30)
	text1 = win_font.render("WINNER", 1, WHITE)
	text2 = discription_font.render("{} won the game".format(winner), 1, WHITE)
	text3 = discription_font.render("Press m to MENU / Press q to quit", 1, WHITE)
	window.blit(text1, (WIDTH//2-85, HEIGHT//2-60))
	window.blit(text2, (WIDTH//2-125, HEIGHT//2+10))
	window.blit(text3, (WIDTH//2-160, HEIGHT//2+50))
	pygame.display.update()

	pause = True
	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if pygame.key.name(event.key) == "q":
					pygame.quit()
					quit()
				if pygame.key.name(event.key) == "m":
					pygame.quit()
					# Menu.show_screen()
					# window.mainloop()

def main():
	run = True
	clock = pygame.time.Clock()

	left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
	right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
	ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)
	left_score = Score(WIDTH//2 - 70, 50)
	right_score = Score(WIDTH//2 + 50, 50)

	while run:
		draw(window2, [left_paddle, right_paddle, ball, left_score, right_score])
		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				break
			if event.type == pygame.KEYDOWN:
				if pygame.key.name(event.key) == "escape":
					pause(window2)
		
		# Define the keys for each paddle
		keys = pygame.key.get_pressed()
		
		paddle_movement(keys, left_paddle, pygame.K_w, pygame.K_s)
		paddle_movement(keys, right_paddle, pygame.K_UP, pygame.K_DOWN)
		ball_movement(ball, left_paddle, right_paddle)

		if goal(ball, left_score, right_score):
			reset_ball(ball)
		
		# Check if someone won
		if check_winner(left_score, right_score) == "Left Player" or check_winner(left_score, right_score) == "Right Player":
			winner = check_winner(left_score, right_score)
			result_screen(window2, winner)

	pygame.quit()




if __name__ == "__main__":
	main()