from tkinter import *
import numpy as np

rouge_touchee = False
jaune_touchee = False
fenetre = Tk()
canvas = Canvas(fenetre, width=1000, height=600)
canvas.configure(background='forest green')
text = canvas.create_text(100, 50, text=("score du joueur : ", 0))
canvas.pack()
canvas.focus_set()
canvas.update()
masse = 100
alpha = 0.5
dt = 0.001
rayon = 10
xmax, ymax = 1000 - rayon, 600 - rayon
xmin, ymin = rayon, rayon
coeff_bande = 0.6
coeff_bille = 0.9
distflechex = 0
distflechey = 0
nbcoups = 0

ligne = canvas.create_line(0, 0, 0, 0, arrow='first', width=3)


class Bille:
    xmax, ymax = 1000 - rayon, 600 - rayon
    xmin, ymin = rayon, rayon

    def __init__(self, position, vitesse, alpha, canvas_bille):
        self.position = position
        self.vitesse = vitesse
        self.alpha = alpha
        self.canvas_bille = canvas_bille
        self.touchee = False

    def copy(self):
        return Bille(self.position, self.vitesse, self.alpha, self.canvas_bille)

    def update(self, dt):
        acceleration = - alpha * self.vitesse
        newVitesse = self.vitesse + acceleration * dt
        newPosition = self.position + newVitesse * dt

        if not (self.xmin <= newPosition[0] <= self.xmax):
            newVitesse[0] *= -coeff_bande
            newPosition = self.position + newVitesse * dt
        if not (self.ymin <= newPosition[1] <= self.ymax):
            newVitesse[1] *= -coeff_bande
            newPosition = self.position + newVitesse * dt

        self.position = newPosition
        self.vitesse = newVitesse


billes = []
positions = [(100, 150), (150, 150), (150, 180)]
couleurs = ['white', 'yellow', 'red']
for k in range(len(positions)):
    bille = canvas.create_oval(-10, -10, 10, 10, outline='black', fill=couleurs[k])
    billes.append(Bille(np.array(positions[k]), np.array([0, 0]), 0.5, bille))


def collision(m_billes):
    global rayon, coeff_bille

    for b in range(len(m_billes)):
        for a in range(b):
            b1 = m_billes[b]
            b2 = m_billes[a]
            d = np.linalg.norm(b1.position - b2.position)
            if d < 2 * rayon:
                Vr = b1.vitesse - b2.vitesse
                N = (b1.position - b2.position) / d
                P = abs(Vr.dot(N))
                I = (1 + coeff_bille) * P * N / 2
                b1.vitesse += I
                b2.vitesse += -I

                if b == 0 or a == 0:
                    m_billes[a].touchee = True
                    m_billes[b].touchee = True


def click(event, billes, ligne, canvas):
    for bille in billes:
        bille.touchee = False

    canvas.coords(ligne, event.x, event.y, billes[0].position[0], billes[0].position[1])
    billes[0].vitesse = 10 * np.array([event.x - billes[0].position[0], event.y - billes[0].position[1]])


def space(event, billes, ligne, canvas):
    for bille in billes:
        bille.touchee = False

    canvas.coords(ligne, 0, 0, 0, 0)
    billes[1].vitesse = np.array([0, 0])
    billes[2].vitesse = np.array([0, 0])
    billes[0].vitesse = intelligence_artificielle(billes)


def intelligence_artificielle(billes):
    dt = 0.001
    new_billes = [bille.copy() for bille in billes]
    v = 5000
    for theta in np.linspace(0, 2 * np.pi, 100):
        new_billes[0].vitesse = v * np.array([np.cos(theta), np.sin(theta)])
        for k in range(int(5 / dt)):
            main_update(dt, new_billes)
        if new_billes[1].touchee and new_billes[2].touchee:
            return v * np.array([np.cos(theta), np.sin(theta)])
        new_billes = [bille.copy() for bille in billes]
    print("Laouen est un fils de gnoll")
    return (np.array([0, 0]))


canvas.bind('<Button-1>', lambda event: click(event, billes, ligne, canvas))
canvas.bind('<space>', lambda event: space(event, billes, ligne, canvas))


def main_update(dt, m_billes):
    collision(m_billes)

    for bille in m_billes:
        bille.update(dt)


def main(dt, billes, nbcoups):
    main_update(dt, billes)
    for bille in billes:
        canvas.coords(bille.canvas_bille, bille.position[0] - 10, bille.position[1] - 10,
                      bille.position[0] + 10, bille.position[1] + 10)
    if billes[1].touchee and billes[2].touchee:
        nbcoups += 1
        canvas.itemconfigure(text, text=nbcoups)
        for bille in billes:
            bille.touchee = False
    fenetre.after(1, lambda: main(dt, billes, nbcoups))


main(dt, billes, nbcoups)
fenetre.mainloop()
