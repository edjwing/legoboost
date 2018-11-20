class Controller:

    myhub = None

    acceleration = 0
    steering = 0
    adjust_step = 20

    motor_a = 0.0
    motor_b = 0.0

    def __init__(self, movehub=None):
        self.myhub = movehub

    def accel(self):
        if self.acceleration <= 80:
            self.acceleration += self.adjust_step
        if 0 <= self.acceleration <= self.adjust_step:
            self.steering = 0
        self.output_wheel()

    def deaccel(self):
        if self.acceleration >= -80:
            self.acceleration -= self.adjust_step
        if -self.adjust_step <= self.acceleration <= 0:
            self.steering = 0
        self.output_wheel()

    def steer_left(self):
        if self.steering >= -40:
            self.steering -= self.adjust_step
        self.output_wheel()

    def steer_right(self):
        if self.steering <= 40:
            self.steering += self.adjust_step
        self.output_wheel()

    def output_wheel(self):
        if self.acceleration == 0:
            self.motor_a = self.steering / 100.0
            self.motor_b = -self.steering / 100.0
        else:
            self.motor_a = self.acceleration / 100.0
            self.motor_b = self.acceleration / 100.0
            if self.steering > 0:
                self.motor_b = (self.acceleration * (100 - self.steering)) / 10000.0
            elif self.steering < 0.0:
                self.motor_a = (self.acceleration * (100 + self.steering)) / 10000.0

        if self.myhub is not None:
            if -0.2 < self.motor_a < 0.2:
                self.myhub.motor_A.stop()
            else:
                self.myhub.motor_A.constant(self.motor_a)
            if -0.2 < self.motor_b < 0.2:
                self.myhub.motor_B.stop()
            else:
                self.myhub.motor_B.constant(self.motor_b)

    def __str__(self):
        return '[Controller] D/R:' + str(self.acceleration) + ' || L/R:' + str(self.steering)\
            + ' || A/B:' + str(self.motor_a) + '/' + str(self.motor_b)