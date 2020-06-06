
#######################
##PLease access the link: http://www.codeskulptor.org/#user45_z9hrcpf5LO_12.py to see the execution of this game! :) ENJOY!
#######################
# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
my_score = 0;
highest_score = 0;
new_high_score = 0;
lives = 3
time = 0
started = False; # for start screen at the start of game..
FRICTION = 0.015;
ACCL_INC = 0.2;
MSL_INC = 8;
CANNON_TIP = 40;


class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35) #no lifespan
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50) #lifespan = 50
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40) #no lifespan
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True) #lifespan = 24 fps
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.4)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")
explosion_sound.set_volume(0.6)
# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


        
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.forward = [];
        
    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        if(self.thrust == False):
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle);
        else:
            canvas.draw_image(self.image, [self.image_center[0]+90,self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle);
            

    def update(self):
        #update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH;
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT;
        
        #forward vector
        self.forward = angle_to_vector(self.angle);
        
        #update velocity with Friction and acceleration
        self.vel[0] = (1-FRICTION)*self.vel[0];
        self.vel[1] = (1-FRICTION)*self.vel[1];
        
        if(self.thrust == True):
            self.vel[0] += ACCL_INC*self.forward[0];
            self.vel[1] += ACCL_INC*self.forward[1];
                
        #update angle by angular velocity
        self.angle += self.angle_vel;

        
    #update the angular velocity according to user controls       
    def update_angle_vel(self,key):
        self.angle_vel += 0.09;
        if key == simplegui.KEY_MAP["left"]:
            self.angle_vel = -self.angle_vel;

    def reset_angle_vel(self):
        self.angle_vel = 0;

    #update thrust status    
    def set_thrust(self):
        self.thrust = True;
        ship_thrust_sound.rewind()
        ship_thrust_sound.play()        
    
    def reset_thrust(self):
        self.thrust = False;
        ship_thrust_sound.pause()        
        
    ###shoot missiles###            
    def shoot(self):
        global missile_group;
        missile_group.add(Sprite([self.pos[0]+CANNON_TIP*self.forward[0],self.pos[1]+ CANNON_TIP*self.forward[1]], [self.vel[0] + MSL_INC*self.forward[0],self.vel[1] + MSL_INC*self.forward[1]], 0, 0, missile_image, missile_info, missile_sound));
        
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated is False:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle);
        else: #animated explosions            
            canvas.draw_image(self.image, [self.image_center[0] + self.age*self.image_size[0],self.image_center[1]], self.image_size, self.pos, self.image_size); #no angle needed for animation image
    
    def update(self):
        #pos update
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH;
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT;
        
        #angle update
        self.angle += self.angle_vel;
        
        #increment age of the sprite
        self.age += 1;
        if(self.age >= self.lifespan):
            return True;
        else:
            return False;
        

    def collide(self,other_obj):
        #check for sprite colliding with another sprite or the spaceship..rock-ship or rock-missile cases:
        if (dist(self.pos,other_obj.pos) <= (self.radius+ other_obj.radius)):
            return True;
        else:
            return False;
        

        
def draw(canvas):
    global time, started,lives,score,my_score,my_ship;
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    #score and lives text:
    canvas.draw_text("Lives: "+str(lives), [50,50], 20, "White");
    canvas.draw_text("Score: "+ str(score), [WIDTH-150,50], 20, "White");
    canvas.draw_text("Highest_Score: "+ str(highest_score), [WIDTH-150,70], 20, "White");
    
    # draw ship and sprites
    my_ship.draw(canvas)
    
    # update ship and sprites
    my_ship.update()

    #call missiles and rocks group draw function
    process_sprite_group(canvas,rock_group);
    process_sprite_group(canvas,missile_group);
    process_sprite_group(canvas,explosion_group); #for exploding asteroids that have a collision with ship/missile

    #check if rocks have a collision with ship and update lives:
    if (group_collide(rock_group,my_ship)):
        lives -= 1;                
    
    #check if any missile hit a rock and update score:
    if(group_group_collide(missile_group, rock_group)):
        score += 1;
        
    #check game over    
    if(lives == 0): #GAME OVER!!!
        check_score(); #check the current score at the end of the game
        reset(); #start new game..       
       
    # draw splash screen if not started
    if not started:
        ship_thrust_sound.pause(); #stop the thrust sound from running continuosly..        
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        if(new_high_score):
            canvas.draw_text("YOU BEAT THE HIGHEST SCORE of "+ str(highest_score)+"! :)",[150,100],30,"Red");
            canvas.draw_text("Your Score is: "+ str(score),[300,150],30,"White"); 
        else:
            canvas.draw_text("Your Score is: "+ str(score),[300,100],30,"White");
            if(highest_score !=0):
                canvas.draw_text("Highest Score is: "+ str(highest_score),[300,130],25,"White");

                    

            
##RESET FUNCTION TO START OVER##
def reset():
    global started,rock_group,missile_group,my_ship,explosion_group;
    started = False;
    rock_group = set([]); #clear all rocks. set of rocks spawned
    missile_group = set([]); #clear all missiles. set of missiles launched
    explosion_group = set([]);#clear all explosions.
    my_ship = Ship([WIDTH/2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info); #reset ship to center of the canvas to start a new game
    timer.stop();
    soundtrack.set_volume(0.3); #reset volume back to 0.3
    soundtrack.play();
    
#check high score:
def check_score():
    global new_high_score;        
    if(score > highest_score and highest_score!=0):
        new_high_score = 1;            
        
                
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started,new_high_score,lives,score,highest_score;
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3;
        if(score > highest_score):
            highest_score = int(score);
        score = 0;
        new_high_score = 0; #reset the new high score flag since new game has started
        timer.start(); #start the rock_spawn timer..
        soundtrack.rewind();
        soundtrack.play();
        soundtrack.set_volume(0.1); #reduce background volume once the game starts
                             
        
        
#keydown handler    
def keydown(key):
    global my_ship,started;
    if(started):
        if key == simplegui.KEY_MAP["left"] or key== simplegui.KEY_MAP["right"]:
            my_ship.update_angle_vel(key);
        if key == simplegui.KEY_MAP["up"]:
            my_ship.set_thrust();
            ship_thrust_sound.play();
        if key == simplegui.KEY_MAP["space"]:
            my_ship.shoot();
    else:
        my_ship.reset_thrust();
        

#keyup handler
def keyup(key):
    global my_ship,started;
    if (started):
        if key == simplegui.KEY_MAP["left"] or key== simplegui.KEY_MAP["right"]:
            my_ship.reset_angle_vel();
        if key == simplegui.KEY_MAP["up"]:
            my_ship.reset_thrust();
            ship_thrust_sound.rewind();
        

        
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group;
    #random sprite attributes:
    sprite_rand_angle_vel = random.choice([-0.15, 0.15]);
    lower = -2 - 0.1*score;
    upper = 2 + 0.1*score;
    sprite_rand_vel = [lower + random.random() * (upper-lower),lower + random.random() * (upper-lower)]; # generating velocity values between 0.1 to 1
    sprite_rand_pos = [random.random() * WIDTH, random.random() * HEIGHT];
    #add this new rock to the rock_Group everytime we call rock_spawner. only add upto 10 rocks..
    if(len(rock_group) < 12):
        sprite = Sprite(sprite_rand_pos, sprite_rand_vel, 0, sprite_rand_angle_vel, asteroid_image, asteroid_info);
        if(dist(sprite.pos,my_ship.pos) > (4*sprite.radius + my_ship.radius)):
            rock_group.add(sprite);

# process_sprite_group function
def process_sprite_group(canvas, group):
    for sprite in list(group): #drawing and updating positions for all sprites in the group
        sprite.draw(canvas);
        if(sprite.update()): #age is more than lifespan for this sprite so remove it from the group
            group.remove(sprite);
            

#check collision between ship/missile and a rock from rock_group        
def group_collide(group, obj):
    global explosion_group;
    for sprite in list(group):
        if(sprite.collide(obj)):
            group.remove(sprite); #remove that sprite (rock) from that group
            explosion_group.add(Sprite(sprite.pos,[0,0],0,0,explosion_image,explosion_info,explosion_sound));
            return True; #yes there was a collision with one of the sprites in the group
    return False; # no there was no collision   


#check collision between a missile from missile_group and a rock from rock_group  
def group_group_collide(group_m, group_r):
    for missile in list(group_m):
        if (group_collide(group_r, missile)):
            group_m.remove(missile);
            return True; #yes missile hit a rock
    return False;# no missile did not hit a rock    



##############################        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown);
frame.set_keyup_handler(keyup);
frame.set_mouseclick_handler(click)
label_1 =frame.add_label("GAME CONTROLS:");
label_space1 = frame.add_label("\n");
label_2 =frame.add_label("'UP' ---> thrust");
label_space3 = frame.add_label("\n");
label_x =frame.add_label("'LEFT/RIGHT' --> orientation");
label_space4 = frame.add_label("\n");
label_3 =frame.add_label("'SPACE' --> shoot missiles!!..");
label_space5 = frame.add_label("\n");
label_space6 = frame.add_label("\n");
label_4 =frame.add_label("You have 3 LIVES. Enjoy!! :)");
#rock spawner timer
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
reset(); # initialize ship and two sprites
frame.start()
