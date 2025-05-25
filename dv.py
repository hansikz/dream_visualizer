import turtle
import random
import pygame
import threading
import time

# Initialize pygame mixer for sounds
pygame.mixer.init()

# Local Sound files
SOUNDS = {
    "cosmic": "sounds/custom.wav",
    "forest": "sounds/forest.wav",
    "galaxy": "sounds/custom.wav",
    "custom": "sounds/custom.wav"
}

def play_sound_loop(scene):
    try:
        sound_file = SOUNDS.get(scene, SOUNDS['custom'])
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely
    except Exception as e:
        print(f"Error playing sound: {e}")

# Shape drawing functions
def draw_star(pen, x, y, size, color):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.color(color)
    pen.begin_fill()
    for _ in range(5):
        pen.forward(size)
        pen.right(144)
    pen.end_fill()

def draw_circle(pen, x, y, size, color):
    pen.penup()
    pen.goto(x, y - size)
    pen.pendown()
    pen.color(color)
    pen.begin_fill()
    pen.circle(size)
    pen.end_fill()

def draw_square(pen, x, y, size, color):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.color(color)
    pen.begin_fill()
    for _ in range(4):
        pen.forward(size)
        pen.right(90)
    pen.end_fill()

def draw_triangle(pen, x, y, size, color):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.color(color)
    pen.begin_fill()
    for _ in range(3):
        pen.forward(size)
        pen.left(120)
    pen.end_fill()

def draw_spiral(pen, x, y, color):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.color(color)
    pen.width(2)
    pen.setheading(0)
    for i in range(30):
        pen.forward(i * 2)
        pen.right(45)

# Animated twinkling star
def twinkle_star(pen, x, y, size, colors, delay=1000):
    def twinkle():
        while True:
            for c in colors:
                pen.penup()
                pen.goto(x, y)
                pen.pendown()
                pen.color(c)
                pen.begin_fill()
                for _ in range(5):
                    pen.forward(size)
                    pen.right(144)
                pen.end_fill()
                time.sleep(delay / 1000)
    threading.Thread(target=twinkle, daemon=True).start()

# Scenery Functions
def cosmic_dreamscape(pen, width, height):
    colors = ["white", "lightblue", "violet", "pink"]
    for _ in range(50):
        x = random.randint(-width//2, width//2)
        y = random.randint(-height//2, height//2)
        size = random.randint(10, 25)
        color = random.choice(colors)
        draw_star(pen, x, y, size, color)

def forest_realm(pen, width, height):
    colors = ["darkgreen", "forestgreen", "yellow"]
    for _ in range(30):
        x = random.randint(-width//2, width//2)
        y = random.randint(-height//2, height//2)
        size = random.randint(30, 60)
        draw_triangle(pen, x, y, size, random.choice(colors))
    for _ in range(40):
        x = random.randint(-width//2, width//2)
        y = random.randint(-height//2, height//2)
        draw_circle(pen, x, y, random.randint(5, 10), "yellow")

def galaxy_pattern(pen, width, height):
    colors = ["white", "purple", "cyan", "blue"]
    for _ in range(20):
        x = random.randint(-width//2, width//2)
        y = random.randint(-height//2, height//2)
        draw_spiral(pen, x, y, random.choice(colors))

# Map shape names to functions
shape_functions = {
    'star': draw_star,
    'circle': draw_circle,
    'square': draw_square,
    'triangle': draw_triangle,
    'spiral': draw_spiral
}

def main():
    screen = turtle.Screen()
    screen.title("Ultimate Dream Visualizer")
    width, height = 800, 700
    screen.setup(width, height)

    scene = screen.textinput("Scene Choice", "Choose your dream scene (custom / cosmic / forest / galaxy):")
    if not scene:
        screen.bye()
        return
    bg_color = screen.textinput("Background Color", "Choose background color (e.g. black, navy, lightblue):")
    if not bg_color:
        screen.bye()
        return
    screen.bgcolor(bg_color)

    # Start sound in background thread
    threading.Thread(target=lambda: play_sound_loop(scene.lower()), daemon=True).start()

    pen = turtle.Turtle()
    pen.speed(0)
    pen.hideturtle()

    if scene.lower() == 'custom':
        num_shapes = screen.numinput("Number of Shape Types", "How many different shapes do you want? (0-5)", 0, 0, 5)
        if num_shapes is None:
            screen.bye()
            return
        num_shapes = int(num_shapes)

        selected_shapes = []
        shape_quantities = {}
        for i in range(num_shapes):
            shape_choice = screen.textinput(f"Shape {i+1}", f"Enter your {i+1} shape from: {list(shape_functions.keys())}")
            if shape_choice is None or shape_choice.lower() not in shape_functions:
                screen.textinput("Invalid", "Invalid shape name, closing program.")
                screen.bye()
                return
            quantity = screen.numinput("Quantity", f"How many {shape_choice.lower()}s? (1-200)", 1, 1, 200)
            if quantity is None:
                screen.bye()
                return
            quantity = int(quantity)
            selected_shapes.append(shape_choice.lower())
            shape_quantities[shape_choice.lower()] = quantity

        for shape in selected_shapes:
            for _ in range(shape_quantities[shape]):
                x = random.randint(-width//2, width//2)
                y = random.randint(-height//2, height//2)
                size = random.randint(20, 60)
                color = random.choice(["white", "pink", "cyan", "yellow", "orange", "purple"])
                if shape != 'spiral':
                    shape_functions[shape](pen, x, y, size, color)
                else:
                    shape_functions[shape](pen, x, y, color)

    elif scene.lower() == 'cosmic':
        cosmic_dreamscape(pen, width, height)

    elif scene.lower() == 'forest':
        forest_realm(pen, width, height)

    elif scene.lower() == 'galaxy':
        galaxy_pattern(pen, width, height)

    else:
        screen.textinput("Error", "Invalid scene selected. Close and restart.")
        screen.bye()
        return

    text_choice = screen.textinput("Add Text?", "Do you want to display a message? (yes/no)")
    if text_choice and text_choice.lower() == 'yes':
        dream_text = screen.textinput("Your Dream Message", "Write your message:")
        if dream_text:
            text_color = screen.textinput("Text Color", "Choose text color (like white, yellow, pink):")
            if not text_color:
                text_color = "white"
            pen.penup()
            pen.goto(0, -height//2 + 50)
            pen.color(text_color)
            pen.write(dream_text, align="center", font=("Courier", 18, "bold"))

    screen.exitonclick()
    pygame.mixer.music.stop()

if __name__ == "__main__":
    main()
