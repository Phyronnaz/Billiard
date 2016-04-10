import numpy as np


class Player:
    score = 0
    hit_list = []
    power = 1000
    angle = 0.26
    use_mouse = True

    """ball, canvas"""
    def __init__(self, ball, canvas=None, target_position=None):
        self.ball = ball
        if target_position is None:
            self.target_position = self.ball.get_position()
        else:
            self.target_position = target_position

        if not(canvas is None):
            self.line = canvas.create_line(0,0,1,1, arrow='last', width=5, smooth=1, dash=10)
            self.canvas = canvas
            #Events
            canvas.bind("<Motion>", self.motion)
            canvas.bind("<Button-1>",  self.on_mouse_down)
            canvas.bind("<Down>", self.arrow_down)
            canvas.bind("<Up>", self.arrow_up)
            canvas.bind("<Left>", self.arrow_left)
            canvas.bind("<Right>", self.arrow_right)

    def update(self):
        if self.is_moving():
            self.target_position = self.ball.get_position()
        else:
            if len(self.hit_list) >= 2:
                self.score += 1
                print(self.score)
            self.hit_list = []

        if not(self.use_mouse or self.is_moving()):
            self.target_position = self.ball.get_position() + np.array([np.cos(self.angle)*self.power,\
                                                                  np.sin(self.angle)*self.power])

        self.canvas.coords(self.line, self.ball.position_x,\
                                      self.ball.position_y,\
                                      self.target_position[0],\
                                       self.target_position[1])

    def add_hit(self, b):
        if not(b in self.hit_list):
            self.hit_list.append(b)

    def on_mouse_down(self, event):
        self.fire()

    def fire(self):
        if self.is_moving():
            return
        vitesse = self.target_position - self.ball.get_position()
        vitesse *= 5
        self.ball.add_impulse(vitesse)

    def motion(self, event):
        if self.use_mouse:
            self.target_position = np.array([event.x, event.y])

    def arrow_down(self, event):
        self.power -= self.power / 100 + 1

    def arrow_up(self, event):
        self.power += self.power / 100 + 1

    def arrow_left(self, event):
        self.angle -= 1/self.power * 10

    def arrow_right(self, event):
        self.angle += 1/self.power * 10

    def is_moving(self):
        return self.ball.vitesse_x ** 2 + self.ball.vitesse_y ** 2 >= 1
