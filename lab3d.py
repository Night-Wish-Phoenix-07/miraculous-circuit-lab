from ursina import *
from circuit import Circuit
import math

# ---------- 1. Solve the circuit ----------
c = Circuit()
c.voltage_source("V1", "in", "0", 9)
c.resistor("R1", "in", "led", 330)
c.resistor("LED", "led", "0", 100)
res = c.solve_dc()
current = abs(res["I_V1"])
brightness = min(current / 0.02, 1)

# ---------- 2. Themes ----------
THEMES = {
    "ladybug": dict(title="Miraculous Ladybug", sky=color.hsv(250, 0.8, 0.15),
                    board=color.red, wire=color.orange, battery=color.yellow,
                    resistor=color.azure, led_hue=0),
    "catnoir": dict(title="Cat Noir", sky=color.hsv(270, 0.6, 0.06),
                    board=color.hsv(0, 0, 0.07), wire=color.hsv(120, 0.9, 0.8),
                    battery=color.hsv(0, 0, 0.2), resistor=color.hsv(120, 0.6, 0.35),
                    led_hue=120),
}
current_theme = "ladybug"

# ---------- 3. 3D world ----------
app = Ursina()
window.title = "Miraculous Circuit Lab"
DirectionalLight().look_at(Vec3(1, -1, -1))

board = Entity(model="cube", scale=(12, 0.5, 8), position=(0, 0, 1))

wires = []
def wire(a, b):
    a, b = Vec3(*a), Vec3(*b)
    wires.append(Entity(model="cube", position=(a + b) / 2,
                        scale=(abs(b.x - a.x) + 0.12, 0.12, abs(b.z - a.z) + 0.12)))

y = 0.4
wire((-4, y, 0), (-0.75, y, 0))
wire((0.75, y, 0), (4, y, 0))
wire((-4, y, 0), (-4, y, 2.5))
wire((-4, y, 2.5), (4, y, 2.5))
wire((4, y, 2.5), (4, y, 0))

battery  = Entity(model="cube", scale=(1.2, 1, 1), position=(-4, 0.75, 0))
resistor = Entity(model="cube", scale=(1.5, 0.5, 0.5), position=(0, 0.5, 0))
led      = Entity(model="sphere", scale=1, position=(4, 0.9, 0))

title_text = Text(text="", position=(-0.80, 0.47), scale=1.8)
Text(text="Battery 9V", position=(-0.80, 0.40), scale=1.2)
Text(text="R1 = 330 ohm", position=(-0.80, 0.36), scale=1.2)
Text(text=f"Current = {current*1000:.2f} mA", position=(-0.80, 0.32), scale=1.2)
Text(text=f"LED brightness = {brightness*100:.0f}%", position=(-0.80, 0.28), scale=1.2)
Text(text="Press L = Ladybug   C = Cat Noir", position=(-0.80, 0.24), scale=1.1)

decor = []

def clear_decor():
    for d in decor:
        destroy(d)
    decor.clear()

def add_spots(spot_color):
    spots = [(-4.5, -1.8), (-2, 3.8), (1.5, -2.2), (4.8, 3.5), (-5, 2.5),
             (2.5, 4.2), (-0.5, -3), (5, -1.5), (-3, 0.8), (0.5, 3.6)]
    for x, z in spots:
        decor.append(Entity(model="sphere", scale=(0.8, 0.05, 0.8),
                            color=spot_color, position=(x, 0.26, z)))

def add_paw(x, z, paw_color):
    decor.append(Entity(model="sphere", scale=(0.9, 0.05, 0.7),
                        color=paw_color, position=(x, 0.26, z)))
    for dx in (-0.45, 0, 0.45):
        decor.append(Entity(model="sphere", scale=(0.3, 0.05, 0.3),
                            color=paw_color, position=(x + dx, 0.26, z + 0.7 + (0.15 if dx == 0 else 0))))

def apply_theme(name):
    global current_theme
    current_theme = name
    t = THEMES[name]
    window.color = t["sky"]
    board.color = t["board"]
    battery.color = t["battery"]
    resistor.color = t["resistor"]
    title_text.text = t["title"]
    for w in wires:
        w.color = t["wire"]
    clear_decor()
    if name == "ladybug":
        add_spots(color.black)
    else:
        for x, z in [(-4.5, -1.8), (-1.5, 3.2), (2, -2.5), (4.8, 3.2), (-5, 2.5)]:
            add_paw(x, z, color.lime)
        decor.append(Entity(model="sphere", scale=0.45, color=color.gold,
                            position=(-4, 1.5, 0)))   # bell (must stay last)

apply_theme("ladybug")

# ---------- 4. Animation + keys ----------
def update():
    hue = THEMES[current_theme]["led_hue"]
    led.color = color.hsv(hue, 1, 0.25 + 0.75 * brightness)
    led.scale = 1 + 0.12 * brightness * math.sin(time.time() * 5)
    if current_theme == "catnoir" and decor:
        decor[-1].y = 1.5 + 0.08 * math.sin(time.time() * 4)

def input(key):
    if key == "l":
        apply_theme("ladybug")
    if key == "c":
        apply_theme("catnoir")

ec = EditorCamera()
ec.rotation_x = 35
camera.z = -18

app.run()
