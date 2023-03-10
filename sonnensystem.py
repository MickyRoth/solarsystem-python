# Mit den physikalischen SI-Einheiten rechnen (meter, AU, kg, Sekunden...)
# Bei dem Zeichnen dem Bildschirm verwenden einen Maßstab
# Beim gezeichneten Radius verwenden wir eigene Werte
# Wir berechnen keine Kollisionen 
# Wir nehmen nur die inneren 4 Planeten (Merkur, Venus, Erde, Mars) und die Sonne
# Wir berechnen nur 2D
# Wir berücksichtigen die physikalisch korrekten Beeinflussungen der Planeten untereinander
# Wir berechnen zunächst die Kraft, mit der Masse zusammen ergibt sich die Beschleunigung
# Genauigkeit 1 Tag, lässt sich aber anpassen
import pygame  # Für die Grafik      pip3.11 install pygame
import math
# 1. Konstanten für Grafik setzen
# 2. Klasse Planet implementieren
# 3. Hauptprogramm läuft in einer Scheife
pygame.init()   # Initialisierung
WIDTH = 800     # Breite
HEIGHT = 800    # Höhe
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))   # Definition Fenster
pygame.display.set_caption("Solar Simulator 1.0")
WHITE = (255,255,255)  # Farben
YELLOW = (255,255,0)
BLUE = (100,150,240)
RED = (190,40,40)
GREEN = (0,170,0)
DARK_GREY = (80,80,80)
BLACK = (0,0,0)
BACKGROUND = (10,10,10)
MAGENTA = (255,0,255)

class Planet:
    AU = 150e6 * 1000 # Astronomische Einheit in metern
    G = 6.67428e-11   # Gravitionskonstante
    SCALE = 150 / AU  # Umrechnung in Pixel 150px = 1 AU
    TIMESTEP = 3600*24 # Zeitfaktor zum Berechnen: 1 Tag

    def __init__(self, x, y, xvel, yvel, pxradius, color, mass):
        self.x = x * Planet.AU 
        self.y = y * Planet.AU 
        self.xvel = xvel
        self.yvel = yvel
        self.radius = pxradius
        self.color = color
        self.mass = mass

        self.orbit = []
    
    def attraction(self, other):
        distance_x = other.x - self.x  # x-Entfernung
        distance_y = other.y - self.y
        distance = math.sqrt(distance_x **2 + distance_y **2)  # Gesamtentfernung mit Pythagoras
        force = self.G * self.mass * other.mass / (distance**2) # Gesamtkraft mit G
        alpha = math.atan2(distance_y, distance_x)      # Winkel berechnen zwischen x und y-Entfernung, Tangenssatz im Dreieck
        fx = math.cos(alpha) * force  # Kraft in x-Richtung
        fy = math.sin(alpha) * force  
        return fx, fy

    def update_position(self, planets):
        total_fx = 0  # Summe der Kräfte auf 0
        total_fy = 0
        for planet in planets:  # Durch alle Planeten
            if self == planet: continue  # Außer mich selbst
            fx, fy = self.attraction(planet)  # Kräfte berechnen
            total_fx = total_fx + fx    # Aufsummieren der Kräfte
            total_fy = total_fy + fy
        self.xvel = self.xvel + total_fx / self.mass * self.TIMESTEP # Neue Geschwindigkeit berechnen und addieren
        self.yvel = self.yvel + total_fy / self.mass * self.TIMESTEP
        self.x = self.x + self.xvel * Planet.TIMESTEP  # Neue X-Position nach Zeitintervall
        self.y = self.y + self.yvel * Planet.TIMESTEP
        #print(self.x, self.y)
        self.orbit.append((self.x * self.SCALE + WIDTH/2, self.y * self.SCALE + HEIGHT/2))  # x und y-Pixel-Position in die Liste einfügen

    
    def draw(self, WINDOW):
        
        if len(self.orbit) > 2:
            pygame.draw.lines(WINDOW, self.color, False, self.orbit, 2)
        
        
        px = self.x * self.SCALE + WIDTH / 2    # Berechnung der Pixelkoordinate
        py = self.y * self.SCALE + HEIGHT / 2
        pygame.draw.circle(WINDOW, self.color, (px, py), self.radius)		   # Planet zeichnen
        
# Hauptprogramm
run = True
#           x, y, xvel, yvel, radius, farbe, masse       x,y in AU | xvel, yvel in m/s | radius in px | masse in kg
sun =   Planet(0, 0, 0, 0, 18, YELLOW, 1.98892e30)  # Masse: 1.98892 * 10^30
earth=  Planet(-1, 0, 0, 29783, 12, BLUE, 5.972e24)   # x und y mit Planet.AU MULTIPLIZIEREN!!
mars =  Planet(-1.524, 0, 0, 24077, 8, RED, 6.39e23)
mercury=Planet(+0.387, 0, 0, -47400, 6, DARK_GREY, 3.3e23)
venus = Planet(+0.723, 0, 0, -35020, 12, WHITE, 4.8685e24)
comet1 =Planet(-2, -2, 12000, 4000, 3, GREEN, 1e6)
comet2 =Planet(2, -2, -13000, 3000, 3, MAGENTA, 1e6)
comet3 =Planet(2, 2, -10000, -3000, 3, BLUE, 1e6)

planets = [sun, earth, mars, mercury, venus, comet1, comet2, comet3]  # Liste der Planeten
clock = pygame.time.Clock()  # Clock-Objekt für Framekontrolle

while run:
    clock.tick(60)  # max 60 Frames/s
    for event in pygame.event.get():  # Schleife durch alle Events
        if event.type == pygame.QUIT:  # Wenn QUIT
            run = False               # Schleifenbedingung auf False
    WINDOW.fill(BACKGROUND)    # Neuen Bildschirm löschen
    for planet in planets:     # Durch alle Planeten
        planet.update_position(planets) # Neue Positionen
        planet.draw(WINDOW)   # Auf neuem Bildschirm malen (Planeten und Orbitspuren)
    pygame.display.update()   # Auf neuen Bildschirm umschalten

pygame.quit()  # Pygame Objekte löschen und Bildschirm schließen