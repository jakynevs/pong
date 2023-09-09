# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [0, 0]
paddle1_pos = 200
paddle2_pos = 200
paddle1_vel = 0
paddle2_vel = 0
vel_increment = 5
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel, score1, score2 # these are vectors stored as lists
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    if direction == RIGHT:
        ball_vel = [random.randrange(1, 4), random.randrange(2, 6)]
        score2 += 1
    elif direction == LEFT:
        ball_vel = [-random.randrange(1, 4), random.randrange(2, 6)]
        score1 += 1
    else:
        ball_vel = [2, -2]


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(ball_vel)
    score1 = 0
    score2 = 0

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    elif ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        if paddle1_pos <= ball_pos[1] < (paddle1_pos + PAD_HEIGHT):
            ball_vel[0] = -ball_vel[0] * 1.2
        else:
            spawn_ball(RIGHT)
    elif ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
        if paddle2_pos <= ball_pos[1] < (paddle2_pos + PAD_HEIGHT):
            ball_vel[0] = -ball_vel[0] * 1.2
        else:
            spawn_ball(LEFT)
            
        
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 5, "White", "Blue")
    
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos + paddle1_vel) >= 0 and (paddle1_pos + paddle1_vel) <= HEIGHT - PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    if (paddle2_pos + paddle2_vel) >= 0 and (paddle2_pos + paddle2_vel) <= HEIGHT - PAD_HEIGHT:
        paddle2_pos += paddle2_vel

    # draw paddles
    canvas.draw_line([0, paddle1_pos], [0, paddle1_pos + PAD_HEIGHT], 
                     PAD_WIDTH, "White")
    canvas.draw_line([WIDTH, paddle2_pos], [WIDTH, paddle2_pos + PAD_HEIGHT], 
                     PAD_WIDTH, "White")
    
    # draw scores
    canvas.draw_text("Pong", [126, 40], 40, "White")
    canvas.draw_text(str(score1), [30, 100], 50, "Blue")
    canvas.draw_text(str(score2), [WIDTH - 50, 100], 50, "Blue")
        
def keydown(key):
    global paddle1_vel, paddle2_vel, vel_increment
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel += vel_increment
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel -= vel_increment
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel -= vel_increment
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel += vel_increment
        
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game)


# start frame
new_game()
frame.start()
