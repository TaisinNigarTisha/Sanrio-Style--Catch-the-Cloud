# ============================================================
# 🌈 Sanrio-Style: Catch the Cloud
# ------------------------------------------------------------
# A dreamy pastel arcade game made with Python Turtle Graphics
# ------------------------------------------------------------
# Controls:
#   ← / →  : Move
#   P      : Pause
#   SPACE  : Start / Restart
#   ESC    : Quit
# ============================================================

import turtle
import random
import math
import time

# ============================================================
# SCREEN SETUP
# ============================================================

WIDTH = 900
HEIGHT = 700

screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("☁ Sanrio-Style: Catch the Cloud ☁")
screen.bgcolor("#b8d4ff")
screen.tracer(0)

# ============================================================
# GLOBAL COLORS
# ============================================================

PASTEL_BLUE = "#d6f0ff"
PASTEL_PINK = "#ffd9ec"
PASTEL_YELLOW = "#fff3b0"
PASTEL_PURPLE = "#e6dcff"
PASTEL_WHITE = "#fffdfc"
PASTEL_GRAY = "#e8e8ee"
PASTEL_MINT = "#d9fff2"

# ============================================================
# DRAWING HELPERS
# ============================================================

def create_circle_shape(name, color, size=20):
    t = turtle.Turtle()
    t.hideturtle()
    t.penup()
    screen.register_shape(name, (
        (0, size),
        (size, 0),
        (0, -size),
        (-size, 0)
    ))


# ============================================================
# BACKGROUND DECORATION
# ============================================================

bg_drawer = turtle.Turtle()
bg_drawer.hideturtle()
bg_drawer.speed(0)
bg_drawer.penup()

def draw_background():
    bg_drawer.clear()

    # Dreamy twilight gradient layers
    colors = [
        "#8fb8ff",
        "#a8c8ff",
        "#bfd8ff",
        "#d8e6ff"
    ]

    y = -350

    for c in colors:
        bg_drawer.goto(-450, y)
        bg_drawer.color(c)

        bg_drawer.begin_fill()

        for _ in range(2):
            bg_drawer.forward(900)
            bg_drawer.left(90)
            bg_drawer.forward(180)
            bg_drawer.left(90)

        bg_drawer.end_fill()

        y += 180

    # Moon glow
    bg_drawer.goto(300, 220)
    bg_drawer.dot(130, "#fff5cc")

    bg_drawer.goto(315, 235)
    bg_drawer.dot(90, "#d8e6ff")

    # Rainbow
    rainbow_colors = [
        "#ffc8dd",
        "#ffe5a3",
        "#d8ffe0",
        "#cde7ff",
        "#ead7ff"
    ]

    radius = 180

    for c in rainbow_colors:
        bg_drawer.goto(-320, -120)
        bg_drawer.setheading(0)
        bg_drawer.width(14)
        bg_drawer.color(c)

        bg_drawer.pendown()
        bg_drawer.circle(radius, 70)
        bg_drawer.penup()

        radius -= 14

    # Floating decorative stars
    for _ in range(35):
        x = random.randint(-430, 430)
        y = random.randint(-50, 320)

        bg_drawer.goto(x, y)
        bg_drawer.dot(
            random.randint(2, 5),
            random.choice([
                "#fff7cc",
                "#ffffff",
                "#ffd6f0"
            ])
        )

draw_background()

# ============================================================
# FLOATING BACKGROUND STARS
# ============================================================

background_stars = []

for _ in range(40):
    s = turtle.Turtle()
    s.shape("circle")
    s.shapesize(0.2, 0.2)
    s.color(random.choice([
        PASTEL_WHITE,
        PASTEL_YELLOW,
        PASTEL_PINK
    ]))
    s.penup()
    s.goto(random.randint(-440, 440),
           random.randint(-330, 330))
    background_stars.append(s)

# ============================================================
# HUD
# ============================================================

hud = turtle.Turtle()
hud.hideturtle()
hud.penup()
hud.color("#8a8ab0")

title_writer = turtle.Turtle()
title_writer.hideturtle()
title_writer.penup()
title_writer.color("#9b89c9")

message_writer = turtle.Turtle()
message_writer.hideturtle()
message_writer.penup()
message_writer.color("#8b8bb5")

# ============================================================
# PARTICLES
# ============================================================

class Particle:
    def __init__(self, x, y, color):
        self.t = turtle.Turtle()
        self.t.shape("circle")
        self.t.penup()
        self.t.speed(0)
        self.t.color(color)
        self.t.shapesize(random.uniform(0.15, 0.45))
        self.t.goto(x, y)

        self.dx = random.uniform(-3, 3)
        self.dy = random.uniform(-1, 4)
        self.life = random.randint(20, 40)

    def update(self):
        self.life -= 1

        self.t.goto(
            self.t.xcor() + self.dx,
            self.t.ycor() + self.dy
        )

        scale = max(self.life / 40, 0.05)
        self.t.shapesize(scale)

        if self.life <= 0:
            self.t.hideturtle()
            return False
        return True

# ============================================================
# PLAYER
# ============================================================

class Player:
    def __init__(self):

        # Main invisible anchor turtle
        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.penup()
        self.t.speed(0)

        self.x = 0
        self.y = -255

        self.velocity = 0
        self.move_speed = 0.7
        self.max_speed = 8
        self.direction = 0

        # Character pieces
        self.body = turtle.Turtle()
        self.face = turtle.Turtle()
        self.left_ear = turtle.Turtle()
        self.right_ear = turtle.Turtle()
        self.star = turtle.Turtle()

        self.parts = [
            self.star,
            self.left_ear,
            self.right_ear,
            self.body,
            self.face
        ]

        for p in self.parts:
            p.penup()
            p.speed(0)

        self.setup_shapes()

    def setup_shapes(self):

        # Star platform
        self.star.shape("circle")
        self.star.color("#ffe680")
        self.star.shapesize(1.2, 2.2)

        # Body
        self.body.shape("circle")
        self.body.color("#ffffff")
        self.body.shapesize(1.8, 2.2)

        # Face
        self.face.shape("circle")
        self.face.color("#ffd6e8")
        self.face.shapesize(0.35, 0.35)

        # Ears
        for ear in [self.left_ear, self.right_ear]:
            ear.shape("circle")
            ear.color("#ffffff")
            ear.shapesize(0.9, 0.5)

    def move_left(self):
        self.direction = -1

    def move_right(self):
        self.direction = 1

    def stop(self):
        self.direction = 0

    def update(self):

        # Smooth movement
        self.velocity += self.direction * self.move_speed
        self.velocity *= 0.90

        self.velocity = max(
            min(self.velocity, self.max_speed),
            -self.max_speed
        )

        self.x += self.velocity

        # Boundaries
        self.x = max(min(self.x, 390), -390)

        # Floating bounce
        bounce = math.sin(time.time() * 6) * 5

        body_y = self.y + bounce

        # Position body
        self.body.goto(self.x, body_y)

        # Face
        self.face.goto(self.x, body_y - 5)

        # Ears floppy animation
        ear_wobble = math.sin(time.time() * 8) * 4

        self.left_ear.goto(
            self.x - 26,
            body_y + 8 + ear_wobble
        )

        self.right_ear.goto(
            self.x + 26,
            body_y + 8 - ear_wobble
        )

        # Floating glowing star
        self.star.goto(
            self.x,
            body_y - 28
        )

        # Cute blinking effect
        if random.randint(1, 120) == 1:
            self.face.shapesize(0.1, 0.35)
        else:
            self.face.shapesize(0.35, 0.35)

# ============================================================
# FALLING OBJECTS
# ============================================================

class FallingObject:
    def __init__(self):
        self.t = turtle.Turtle()
        self.t.penup()
        self.t.speed(0)

        self.reset()

    def reset(self):
        self.t.goto(
            random.randint(-420, 420),
            random.randint(320, 500)
        )

    def update(self):
        self.t.sety(self.t.ycor() - self.speed)

        if self.t.ycor() < -340:
            self.reset()

class GoldenStar(FallingObject):
    def __init__(self):
        super().__init__()
        self.t.shape("triangle")
        self.t.color("#ffd84d")
        self.t.shapesize(1, 1)
        self.speed = random.uniform(2.5, 4)

class Cloud(FallingObject):
    def __init__(self):
        super().__init__()
        self.t.shape("circle")
        self.t.color("#ffffff")
        self.t.shapesize(1.2, 2)
        self.speed = random.uniform(1.8, 3)

class RainCloud(FallingObject):
    def __init__(self):
        super().__init__()
        self.t.shape("circle")
        self.t.color("#9ea7c7")
        self.t.shapesize(1.5, 2.4)
        self.speed = random.uniform(3, 5)

class Balloon(FallingObject):
    def __init__(self):
        super().__init__()
        self.t.shape("circle")
        self.t.color(random.choice([
            PASTEL_PINK,
            PASTEL_PURPLE,
            PASTEL_MINT
        ]))
        self.t.shapesize(1.2, 1)
        self.speed = random.uniform(2.5, 4)

# ============================================================
# GAME MANAGER
# ============================================================

class GameManager:
    def __init__(self):
        self.player = Player()

        self.stars = [GoldenStar() for _ in range(5)]
        self.clouds = [Cloud() for _ in range(5)]
        self.rainclouds = [RainCloud() for _ in range(3)]
        self.balloons = [Balloon() for _ in range(2)]

        self.particles = []

        self.score = 0
        self.high_score = 0
        self.combo = 1

        self.running = False
        self.paused = False

        self.flash_timer = 0
        self.shake_timer = 0

        self.difficulty_timer = 0
        self.ended = False
        self.end_timer = 0

    # ========================================================
    # START SCREEN
    # ========================================================

    def show_start_screen(self):
        title_writer.clear()
        message_writer.clear()

        title_writer.goto(0, 120)
        title_writer.write(
            "☁ Catch the Cloud ☁",
            align="center",
            font=("Comic Sans MS", 32, "bold")
        )

        message_writer.goto(0, 20)
        message_writer.write(
            "Move with ← and →\nCollect stars and clouds!\nAvoid rainclouds!\n\nPress SPACE to Start",
            align="center",
            font=("Arial", 16, "normal")
        )

    def start_game(self):
        self.running = True
        self.paused = False
        self.score = 0
        self.combo = 1

        title_writer.clear()
        message_writer.clear()

        # Cancel any pending end sequence
        self.ended = False
        self.end_timer = 0

    # ========================================================
    # PARTICLES
    # ========================================================

    def create_particles(self, x, y, color, amount=12):
        for _ in range(amount):
            self.particles.append(
                Particle(x, y, color)
            )

    # ========================================================
    # COLLISION
    # ========================================================

    def collide(self, player_part, obj, radius=38):

      dx = player_part.xcor() - obj.xcor()
      dy = player_part.ycor() - obj.ycor()

      distance = math.sqrt(dx ** 2 + dy ** 2)

      return distance < radius

    # ========================================================
    # UPDATE HUD
    # ========================================================

    def update_hud(self):
        hud.clear()

        hud.goto(0, 300)
        hud.write(
            f"Score: {self.score}      High Score: {self.high_score}      Combo x{self.combo}",
            align="center",
            font=("Arial", 16, "bold")
        )

    # ========================================================
    # FLASH EFFECT
    # ========================================================

    def flash_screen(self):
        if self.flash_timer > 0:
            screen.bgcolor("#f0f0f5")
            self.flash_timer -= 1
        else:
            screen.bgcolor("#dff6ff")

    # ========================================================
    # GAME OVER
    # ========================================================

    def game_over(self):
        self.running = False

        if self.score > self.high_score:
            self.high_score = self.score

        # Start end sequence: show message and begin countdown to exit
        self.ended = True
        self.end_timer = 300  # frames (~5 seconds at 60fps)

        message_writer.clear()
        message_writer.goto(0, 0)

        message_writer.write(
            f"Game Over\n\nFinal Score: {self.score}\n\nPress SPACE to Restart\n\nExiting in {int(self.end_timer/60)}s...",
            align="center",
            font=("Comic Sans MS", 20, "bold")
        )

    # ========================================================
    # MAIN UPDATE
    # ========================================================

    def update(self):

        if not self.running or self.paused:
            screen.update()
            return

        # Difficulty Scaling
        self.difficulty_timer += 1

        if self.difficulty_timer % 600 == 0:
            self.rainclouds.append(RainCloud())

        self.player.update()

        # Floating star twinkle
        for s in background_stars:
            size = random.uniform(0.1, 0.4)
            s.shapesize(size)

        # ----------------------------------------------------
        # STARS
        # ----------------------------------------------------

        for star in self.stars:
            star.update()

            if self.collide(self.player.body, star.t):
                self.score += 10 * self.combo
                self.combo += 1

                self.create_particles(
                    star.t.xcor(),
                    star.t.ycor(),
                    PASTEL_YELLOW,
                    18
                )

                star.reset()

        # ----------------------------------------------------
        # CLOUDS
        # ----------------------------------------------------

        for cloud in self.clouds:
            cloud.update()

            if self.collide(self.player.body, cloud.t):
                self.score += 3
                self.create_particles(
                    cloud.t.xcor(),
                    cloud.t.ycor(),
                    PASTEL_WHITE,
                    8
                )
                cloud.reset()

        # ----------------------------------------------------
        # RAINCLOUDS
        # ----------------------------------------------------

        for rain in self.rainclouds:
            rain.update()

            if self.collide(self.player.body, rain.t):
                self.score -= 15
                self.combo = 1

                self.flash_timer = 10
                self.shake_timer = 10

                self.create_particles(
                    rain.t.xcor(),
                    rain.t.ycor(),
                    PASTEL_GRAY,
                    15
                )

                rain.reset()

        # ----------------------------------------------------
        # BALLOONS
        # ----------------------------------------------------

        for balloon in self.balloons:
            balloon.update()

            if self.collide(self.player.body, balloon.t):
                self.score += 20
                self.combo += 2

                self.create_particles(
                    balloon.t.xcor(),
                    balloon.t.ycor(),
                    balloon.t.color()[0],
                    20
                )

                balloon.reset()

        # ----------------------------------------------------
        # PARTICLES
        # ----------------------------------------------------

        alive_particles = []

        for p in self.particles:
            if p.update():
                alive_particles.append(p)

        self.particles = alive_particles

        # ----------------------------------------------------
        # EFFECTS
        # ----------------------------------------------------

        self.flash_screen()

        # Soft shake
        if self.shake_timer > 0:
            offset = random.randint(-3, 3)
            screen.cv._rootwindow.geometry(
                f"+{200+offset}+{100+offset}"
            )
            self.shake_timer -= 1

        # If game ended, count down and exit automatically unless restarted
        if self.ended:
            # Update countdown display
            secs_left = max(0, int(self.end_timer / 60))
            message_writer.clear()
            message_writer.goto(0, 0)
            message_writer.write(
                f"Game Over\n\nFinal Score: {self.score}\n\nPress SPACE to Restart\n\nExiting in {secs_left}s...",
                align="center",
                font=("Comic Sans MS", 20, "bold")
            )

            self.end_timer -= 1

            if self.end_timer <= 0:
                try:
                    screen.bye()
                except Exception:
                    pass
                return

        # Update HUD
        self.update_hud()

        # Lose condition
        if self.score < -50:
            self.game_over()

        screen.update()

# ============================================================
# GAME SETUP
# ============================================================

game = GameManager()
game.show_start_screen()

# ============================================================
# INPUTS
# ============================================================

screen.listen()

screen.onkeypress(game.player.move_left, "Left")
screen.onkeypress(game.player.move_right, "Right")

screen.onkeyrelease(game.player.stop, "Left")
screen.onkeyrelease(game.player.stop, "Right")

def toggle_pause():
    if game.running:
        game.paused = not game.paused

        if game.paused:
            message_writer.clear()
            message_writer.goto(0, 0)
            message_writer.write(
                "Paused",
                align="center",
                font=("Comic Sans MS", 24, "bold")
            )
        else:
            message_writer.clear()

screen.onkey(toggle_pause, "p")

def start_or_restart():
    game.start_game()

screen.onkey(start_or_restart, "space")

screen.onkey(screen.bye, "Escape")

# ============================================================
# MAIN GAME LOOP
# ============================================================

while True:
    game.update()
    time.sleep(1 / 60)
