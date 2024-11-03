from pico2d import *
from state_machine import StateMachine

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 1
        self.size = 1.0
        self.speed = 5
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)

    def enter_auto_run(self):
        self.state_machine.transition("AutoRun")

    def start_running(self, direction):
        self.dir = direction
        self.state_machine.transition("Run")

    def stop_running(self):
        self.state_machine.transition("Idle")

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

class AutoRun:
    @staticmethod
    def enter(boy):
        print('Enter AutoRun')
        boy.size = 1.5
        boy.speed = 10
        boy.start_time = get_time()

    @staticmethod
    def exit(boy):
        print('Exit AutoRun')
        boy.size = 1.0
        boy.speed = 5

    @staticmethod
    def do(boy):
        elapsed_time = get_time() - boy.start_time
        if elapsed_time > 5:
            boy.state_machine.add_event("timeout")
        else:
            boy.x += boy.dir * boy.speed
            boy.frame = (boy.frame + 2) % 8
            if boy.x <= 0 or boy.x >= 800:
                boy.dir *= -1

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_composite_draw(int(boy.frame * 100.25), int(1 * 100.5), int(100.25), int(100.5),
                                          0, '', boy.x, boy.y, int(100.25 * boy.size), int(100.5 * boy.size))
        else:
            boy.image.clip_composite_draw(int(boy.frame * 100.25), int(0 * 100.5), int(100.25), int(100.5),
                                          0, '', boy.x, boy.y, int(100.25 * boy.size), int(100.5 * boy.size))

class Idle:
    @staticmethod
    def enter(boy):
        print('Enter Idle')
        boy.size = 1.0

    @staticmethod
    def exit(boy):
        print('Exit Idle')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(int(boy.frame * 100.25), int(3 * 100.5), int(100.25), int(100.5), boy.x, boy.y)
        else:
            boy.image.clip_draw(int(boy.frame * 100.25), int(2 * 100.5), int(100.25), int(100.5), boy.x, boy.y)

class Run:
    @staticmethod
    def enter(boy):
        print('Enter Run')
        boy.size = 1.0
        boy.speed = 3

    @staticmethod
    def exit(boy):
        print('Exit Run')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

        if (boy.dir == 1 and boy.x < 800) or (boy.dir == -1 and boy.x > 0):
            boy.x += boy.dir * boy.speed

    @staticmethod
    def draw(boy):
        if boy.dir == 1:
            boy.image.clip_draw(int(boy.frame * 100.25), int(1 * 100.5), int(100.25), int(100.5), boy.x, boy.y)
        else:
            boy.image.clip_draw(int(boy.frame * 100.25), int(0 * 100.5), int(100.25), int(100.5), boy.x, boy.y)