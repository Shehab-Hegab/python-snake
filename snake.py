# this program is written for Python2

# imports
import Tkinter
import time
import random
import sys
import math

# create game window
window = Tkinter.Tk()

# create window size and set no-resize option
window_dimensions = [625, 625]
window.geometry(str(window_dimensions[0]) + "x" + str(window_dimensions[1]))
window.resizable(0, 0)

# set window title
window.title("Snake Game")

# close window when OS close button is clicked
window.protocol("WM_DELETE_WINDOW", sys.exit)

# choose fps for game
frames_per_second = 12

# create game canvas
game_canvas = Tkinter.Canvas(window, width=window_dimensions[0], height=window_dimensions[1], bd=0, highlightthickness=0)
game_canvas.pack()

# create game variables
game_scale = 25
game_dimensions = [ window_dimensions[0] / game_scale, window_dimensions[1] / game_scale ]

# center player coordinates (position of snake head), and create player tail array
player_coords = [math.floor(game_dimensions[0] / 2.0), math.floor(game_dimensions[1] / 2.0)]
player_tail = []

# player velocity variable (decides which direction to move every frame)
player_velocity = [1, 0]

# generate new random apple coordinates
def generateAppleCoords():
	# declare global variable(s)
	global player_tail

	# variable for generated random apple coordinates
	generated_apple_coords = [random.randint(0, (game_dimensions[0] - 1)), random.randint(0, (game_dimensions[1] - 1))]

	# loop through tail and check if generated apple coords overlap the tail; if they do, generate again (recursion!)
	for item in player_tail:
		if(item[0] == generated_apple_coords[0] and item[1] == generated_apple_coords[1]):
			return generateAppleCoords()

	# apple coords do not overlap, so return them
	return generated_apple_coords

# apple coordinates
apple_coords = generateAppleCoords()

# create velocity changed variable (used to fix bug in arrow key binds)
velocity_changed_this_frame = False

# function to create grid item of specific game coordinates and bg color
def createGridItem(coords, hexcolor):
	game_canvas.create_rectangle((coords[0]) * game_scale, (coords[1]) * game_scale, (coords[0] + 1) * game_scale, (coords[1] + 1) * game_scale, fill=hexcolor, outline="#222222", width=3)

# gameloop
def gameloop():
	# declare use of global variables
	global frames_per_second
	global velocity_changed_this_frame
	global game_canvas
	global game_dimensions
	global window_dimensions
	global player_tail
	global player_coords
	global player_velocity
	global apple_coords

	# call gameloop again in 100 milleseconds (gameloops is called every 100 MS)
	window.after(1000 / frames_per_second, gameloop)

	# change velocity changed variable back to false
	velocity_changed_this_frame = False

	# clear canvas
	game_canvas.delete("all")
	
	# create dark gray background
	game_canvas.create_rectangle(0, 0, window_dimensions[0], window_dimensions[1], fill="#222222", outline="#222222")

	# add head to tail
	player_tail.append([player_coords[0], player_coords[1]])

	# move player in direction specified in player velocity variable
	player_coords[0] += player_velocity[0]
	player_coords[1] += player_velocity[1]

	# add ability to move through walls
	if(player_coords[0] == game_dimensions[0]):
		player_coords[0] = 0
	elif(player_coords[0] == -1):
		player_coords[0] = game_dimensions[0] - 1
	elif(player_coords[1] == game_dimensions[1]):
		player_coords[1] = 0
	elif(player_coords[1] == -1):
		player_coords[1] = game_dimensions[1] - 1
	

	# loop through tail, display each item in tail, and check if it's colliding w/head: if so, gameover and restart
 	for item in player_tail:
 		# check for collision
 		if(item[0] == player_coords[0] and item[1] == player_coords[1]):
 			# restart game and variables
			player_coords = [math.floor(game_dimensions[0] / 2.0), math.floor(game_dimensions[1] / 2.0)]
			player_tail = []
			player_velocity = [1, 0]
			apple_coords = generateAppleCoords()

 		# display item
		createGridItem(item, "#00ff00")

	# display apple
	createGridItem(apple_coords, "#ff0000")

	# check if player has eaten apple; if yes, add 1 to tail; if not, move as normal
	if(apple_coords[0] == player_coords[0] and apple_coords[1] == player_coords[1]):
		apple_coords = generateAppleCoords()
	else:
		player_tail.pop(0)

# handle arrow keys keydown events
def onKeyDown(e):
	# declare use of global variable(s)
	global player_velocity
	global velocity_changed_this_frame

	# only handle event if velocity has not been changed in current frame
	if(velocity_changed_this_frame == False):
		# set velocity changed variable to true
		velocity_changed_this_frame = True

		# bind arrow keys to specific player velocity directions
		if(e.keysym == "Left" and player_velocity[0] != 1):
			player_velocity = [-1, 0]
		elif(e.keysym == "Right" and player_velocity[0] != -1):
			player_velocity = [1, 0]
		elif(e.keysym == "Up" and player_velocity[1] != 1):
			player_velocity = [0, -1]
		elif(e.keysym == "Down" and player_velocity[1] != -1):
			player_velocity = [0, 1]
		else:
			# if player velocity indeed was not changed, then revert variable back to false
			velocity_changed_this_frame = False

# connect keydown event to function
window.bind("<KeyPress>", onKeyDown)

# call gameloop
gameloop()

# display window and mainloop
window.mainloop()