

#######################
##PLease access the link: http://www.codeskulptor.org/#user45_AQAsRbCSqp_16.py to see the execution of this game! :) ENJOY!
#######################

# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles

#paddle values
WIDTH = 600
HEIGHT = 400       
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
PAD_DELTA = HEIGHT/2 - HALF_PAD_HEIGHT
LEFT = False
RIGHT = True
paddle1_won = 0;
paddle2_won = 0;
paddle1_pos = PAD_DELTA;
paddle2_pos = PAD_DELTA;
paddle1_vel = 0;
paddle2_vel = 0;
pad_vel_const = 4;
paddle1_score = 0;
paddle2_score = 0;
win = False;
#ball values
BALL_RADIUS = 15
ball_vel = [0,0];
ball_vel_inc = 0.1;#10% increment in ball velocity as game progresses
ball_pos = [WIDTH/2,HEIGHT/2];
dir = RIGHT;

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_vel,ball_pos,paddle1_pos,paddle2_pos;
    #Ball details
    ball_pos = [WIDTH/2,HEIGHT/2];
    ball_vel[0] = random.randrange(120,240)/60;
    ball_vel[1] = random.randrange(60,180)/60;    
    if(direction==RIGHT):
        ball_vel[1] = -ball_vel[1];
    elif(direction==LEFT):
        ball_vel[0] = -ball_vel[0];
        ball_vel[1] = -ball_vel[1];
        
    #Paddle details
    paddle1_pos = PAD_DELTA;
    paddle2_pos = PAD_DELTA;
    
    
# define event handlers
def new_game():
    global dir,paddle1_score,paddle2_score,win;
    win = False;
    paddle1_score = 0;#reset scores
    paddle2_score = 0;#reset scores
    dir = RIGHT; #default right direction chosen
    spawn_ball(dir);#spawn the ball

def draw(canvas):
    global ball_pos,ball_vel,dir,paddle1_won,paddle2_won,paddle1_pos,paddle2_pos,paddle1_score,paddle2_score          
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
                
    # update ball
    if(win!=True):
        ball_pos[0] += ball_vel[0];
        ball_pos[1] += ball_vel[1];
        # determine whether paddle and ball collide    
        if(ball_pos[0] <= (PAD_WIDTH+BALL_RADIUS) or ball_pos[0] >= (WIDTH-PAD_WIDTH-BALL_RADIUS)):
        
            if(ball_pos[0]<WIDTH/2): #direction left
            #if(dir == LEFT):    
                if(ball_pos[1]>=paddle1_pos and ball_pos[1]<= (paddle1_pos+PAD_HEIGHT)):
                    ball_vel[0] += ball_vel_inc*ball_vel[0];
                    ball_vel[0] = -ball_vel[0];
                #gutter case and other player gets a point and loser serves the ball..
                else:
                    paddle2_score += 1;
                    win_check();
                    dir = RIGHT;
                    if(win!=True):
                        spawn_ball(dir);
                    else:
                        ball_pos = [WIDTH/2,HEIGHT/2];
        
            #if(dir==RIGHT):
            else: #direction right
                if(ball_pos[1]>=paddle2_pos and ball_pos[1]<= (paddle2_pos+PAD_HEIGHT)):
                    ball_vel[0] += ball_vel_inc*ball_vel[0];
                    ball_vel[0] = -ball_vel[0];
                #gutter case and other player gets a point and loser serves the ball..
                else:
                    paddle1_score += 1;
                    win_check();
                    dir = LEFT;
                    if(win!=True):
                        spawn_ball(dir);
                    else:
                        ball_pos = [WIDTH/2,HEIGHT/2];
                   
        if((ball_pos[1]<=BALL_RADIUS) or (ball_pos[1]>=(HEIGHT-BALL_RADIUS))):
            ball_vel[1] = -ball_vel[1];#bounce ball off the top/bottom  
        
    
    # draw ball
    canvas.draw_circle(ball_pos,BALL_RADIUS,1,"white","orange");        
    
    # update paddle's vertical position, keep paddle on the screen
    if(not((paddle1_pos + paddle1_vel)<=0  or (paddle1_pos+paddle1_vel)>= HEIGHT-PAD_HEIGHT)):    
        paddle1_pos += paddle1_vel;
    if(not((paddle2_pos + paddle2_vel)<=0  or (paddle2_pos+paddle2_vel)>= HEIGHT-PAD_HEIGHT)):        
        paddle2_pos += paddle2_vel;
    # draw paddles
    canvas.draw_polygon([[0,paddle1_pos],[PAD_WIDTH,paddle1_pos],[PAD_WIDTH,paddle1_pos+PAD_HEIGHT],[0,paddle1_pos+PAD_HEIGHT]],1,"white","white");
    canvas.draw_polygon([[WIDTH,paddle2_pos],[WIDTH-PAD_WIDTH,paddle2_pos],[WIDTH-PAD_WIDTH,paddle2_pos+PAD_HEIGHT],[WIDTH,paddle2_pos+PAD_HEIGHT]],1,"white","white");
    
    # draw scores
    canvas.draw_text(str(paddle1_score),[150,50],20,"white");
    canvas.draw_text(str(paddle2_score),[450,50],20,"white");
    if(win==True):
        canvas.draw_text(result,[140,150],30,"white");

           
def win_check():
    global win,result;
    if(paddle1_score + paddle2_score == 7):
        win = True;        
        if(paddle1_score> paddle2_score):
            result = "PLAYER 1 WINS the game! :)";
        elif(paddle1_score<paddle2_score):
            result = "PLAYER 2 WINS the game! :)";
    
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if(key == simplegui.KEY_MAP["w"]):
        paddle1_vel = -pad_vel_const;
    elif(key == simplegui.KEY_MAP["s"]):
        paddle1_vel = pad_vel_const;
    elif(key == simplegui.KEY_MAP["up"]):
        paddle2_vel = -pad_vel_const;
    elif(key == simplegui.KEY_MAP["down"]):
        paddle2_vel = pad_vel_const;
            
def keyup(key):
    global paddle1_vel, paddle2_vel
    if(key == simplegui.KEY_MAP['w'] or key == simplegui.KEY_MAP['s']):
        paddle1_vel = 0;
    elif(key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]):
        paddle2_vel = 0;

        
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_canvas_background("green")
label = frame.add_label("***7 Points to win a game of PONG!***")
label2 = frame.add_label("W,S controls paddle for player 1 and up/down arrows for player 2")
frame.add_button("RESTART",new_game,70)



# start frame
new_game()
frame.start()
