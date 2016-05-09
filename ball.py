import numpy as np


class Ball:
    """position, vitesse, id, canvas, radius, alpha, cw, cb, color"""
    def __init__ (self, position, vitesse, id, canvas, radius, alpha, cw, cb, color, dt, create_ball=True):
        self.position_x = position[0]
        self.position_y = position[1]
        self.vitesse_x = vitesse[0]
        self.vitesse_y = vitesse[1]
        self.id = id
        self.radius = radius
        self.alpha = alpha
        self.cw = cw
        self.cb = cb
        self.color = color
        self.canvas = canvas
        self.xmax = self.canvas.winfo_width() - self.radius
        self.ymax = self.canvas.winfo_height() - self.radius
        self.xmin = self.radius
        self.ymin = self.radius

        self.dt = dt
        self.computed_alpha = (1 - dt * self.alpha)
        if create_ball:
            self.canvasBall = canvas.create_oval(-radius,-radius,radius,radius,outline='black',fill=color)

    def copy(self):
        return Ball([self.position_x, self.position_y], [self.vitesse_x, self.vitesse_y], self.id,\
                     self.canvas, self.radius, self.alpha, self.cw, self.cb, self.color, self.dt, create_ball=False)

    def get_position(self):
        return np.array([self.position_x, self.position_y])

    def get_vitesse(self):
        return np.array([self.vitesse_x, self.vitesse_y])

    def add_impulse (self, impulse):
        self.vitesse_x += impulse[0]
        self.vitesse_y += impulse[1]

    def update (self, dt, simulate=False, collision_points=None):
        nextVitesse_x = self.computed_alpha * self.vitesse_x
        nextVitesse_y = self.computed_alpha * self.vitesse_y
        nextPosition_x = self.position_x + nextVitesse_x * dt
        nextPosition_y = self.position_y + nextVitesse_y * dt

        if nextPosition_x < self.xmin or nextPosition_x > self.xmax:
            nextVitesse_x *= -self.cw
            nextPosition_x = self.position_x + nextVitesse_x * dt
            if simulate:
                collision_points.append([self.position_x, self.position_y])

        if nextPosition_y < self.ymin or nextPosition_y > self.ymax:
            nextVitesse_y *= -self.cw
            nextPosition_y = self.position_y + nextVitesse_y * dt
            if simulate:
                collision_points.append([self.position_x, self.position_y])

        self.position_x = nextPosition_x
        self.position_y = nextPosition_y
        self.vitesse_x = nextVitesse_x
        self.vitesse_y = nextVitesse_y

    def update_graphics (self):
        self.xmax = self.canvas.winfo_width() - self.radius
        self.ymax = self.canvas.winfo_height() - self.radius
        self.xmin = self.radius
        self.ymin = self.radius
       	#self.canvasBall = self.canvas.create_oval(-self.radius, -self.radius, self.radius, self.radius,\
        #                                           outline='black',fill=self.color)
        self.canvas.coords(self.canvasBall, self.position_x - self.radius,\
                                            self.position_y - self.radius,\
                                            self.position_x + self.radius,\
                                            self.position_y + self.radius)
