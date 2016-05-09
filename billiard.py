import numpy as np
from player import Player
import math


class Billiard:
    """balls, player, dt"""
    def __init__(self, balls, player, dt):
        self.balls = balls
        self.player = player
        self.dt = dt
        self.is_simulating = False
        self.sqr_radius = balls[0].radius ** 2 * 4

    def update(self):
        self.check_collisions()
        for k in self.balls:
            if self.is_simulating and k.id == 0:
                k.update(self.dt, simulate=True, collision_points=self.collision_points)
            else:
                k.update(self.dt)

    def update_graphics(self):
        self.player.update()
        for k in self.balls:
            k.update_graphics()

    def simulate(self):
        self.dt
        if self.player.is_moving():
            return []
        self.is_simulating = True
        self.collision_points = [self.player.ball.get_position()]
        self.player.fire()
        while self.player.is_moving():
            self.update()
        self.collision_points.append(self.player.ball.get_position())
        return self.collision_points

    def copy(self):
        new_balls = [b.copy() for b in self.balls]
        return Billiard(new_balls, Player(new_balls[0], target_position=self.player.target_position), self.dt)

    def check_collisions (self):
        for a in range(len(self.balls)):
            for b in range(a):
                if (self.balls[a].position_x-self.balls[b].position_x)** 2 +\
                   (self.balls[a].position_y-self.balls[b].position_y) ** 2 < self.sqr_radius:
                    d = math.sqrt((self.balls[a].position_x-self.balls[b].position_x)** 2 +\
                        (self.balls[a].position_y-self.balls[b].position_y) ** 2)
                    k = self.balls[a]
                    l = self.balls[b]

                    #Normal collision
                    Vr = k.get_vitesse() - l.get_vitesse()
                    N = (k.get_position() - l.get_position()) / d

                    I = N * abs(Vr.dot(N)) * (1 + k.cb) / 2

                    k.add_impulse(I)
                    l.add_impulse(-I)

                    #Score && simulation
                    if b == 0:
                        self.player.add_hit(k)
                        if self.is_simulating:
                            self.collision_points.append(l.get_position())
