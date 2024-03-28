import tkinter
import random

from tile import Tile

# Defining Constants
ROWS = 25
COLS = 25
TILE_SIZE = 25
WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

# Creating Game Window
window = tkinter.Tk()
window.title("Snake Game")
# 625 x 625, non resizable window
window.resizable(False, False)

# Create canvas widget
canvas = tkinter.Canvas(
    window, 
    bg = "black", 
    width= WINDOW_WIDTH, 
    height= WINDOW_HEIGHT,
    borderwidth= 0,
    highlightthickness= 0
)
canvas.pack()
window.update()

# Center Window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x_pos = int((screen_width/2) - (window_width/2))
window_y_pos = int((screen_height/2) - (window_height/2))
window.geometry(f"{window_width}x{window_height}+{window_x_pos}+{window_y_pos}")

# Initialize Game
snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5)
food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
x_velocity = 0
y_velocity = 0
snake_body = []
game_status = False 
score = 0

def draw():
    move_snake()

    canvas.delete("all")

    # Init snake and food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill = "red")
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = "orange")

    # Draw each tile in snake body array
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = "orange")

    if (game_status): 
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2,text = f"Game Over. Your Score Was: {score}", fill = "white")

    # After every 100ms, call draw -> 10 Frames per second
    window.after(100, draw)


def move_snake():
    global game_status, score
    if (game_status):
        return
    
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_status = True
        return
    
    # If snake hits itself
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_status = True
            return
    
    # Check collision
    if (snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        score += 1

    # Update snakes body from the back:
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if (i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            # Update the current tile with the next tile (but in reverse order)
            next_tile = snake_body[i-1]
            tile.x = next_tile.x
            tile.y = next_tile.y

    snake.x += x_velocity * TILE_SIZE 
    snake.y += y_velocity * TILE_SIZE

def direction_manager(e):
    global game_status, x_velocity, y_velocity
    if game_status:
        return
    
    if (e.keysym == "w" and y_velocity != 1):
        x_velocity = 0 
        y_velocity = -1
    elif (e.keysym == "s" and y_velocity != -1):
        x_velocity = 0
        y_velocity = 1
    elif (e.keysym == "a" and x_velocity != 1):
        x_velocity = -1
        y_velocity = 0
    elif (e.keysym == "d" and x_velocity != -1):
        x_velocity = 1
        y_velocity = 0


draw()

# When a key is pressed, call change_direction. 
window.bind("<KeyRelease>", direction_manager)
window.mainloop()
