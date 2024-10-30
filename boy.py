from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_a

from Lecture10_Character_Controller_1.state_machine import StateMachine, time_out, space_down, left_down, right_down, \
    left_up, right_up, start_event, a_down


# 상태를 Class를 통해서 정의
class Idle:
    @staticmethod
    def enter(boy,e):
        if left_up(e) or right_down(e):
            boy.action = 2
            boy.face_dir = -1
        elif right_up(e) or left_down(e) or start_event(e):
            boy.action = 3
            boy.face_dir = 1

        boy.dir = 0 # 정지 상태
        boy.frame = 0
        # 현재 시간을 저장
        boy.start_time = get_time()

    @staticmethod
    def exit(boy,e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 3:
            boy.state_machine.add_event(('TIME OUT', 0))
        pass
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass

class Sleep:
    @staticmethod
    def enter(boy,e):
        pass
    @staticmethod
    def exit(boy,e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8


    @staticmethod
    def draw(boy):
        if boy.face_dir == 1: #오른쪽 바라보는 상태에서 눕기
            boy.image.clip_composite_draw( boy.frame * 100, 300, 100, 100, 3.141592/2 , '', boy.x - 25, boy.y - 25, 100, 100)
        elif boy.face_dir == -1:
            boy.image.clip_composite_draw( boy.frame * 100, 200, 100, 100, -3.141592/2 , '', boy.x + 25, boy.y - 25, 100, 100)


class Run:
    @staticmethod
    def enter(boy,e):
        if right_down(e) or left_up(e):
            boy.dir = 1  # right direction
            boy.action = 1
        elif left_down(e) or right_up(e):
            boy.dir = -1
            boy.action = 0

        boy.frame = 0

    @staticmethod
    def exit(boy,e):
        pass
    @staticmethod
    def do(boy):
        boy.x += boy.dir * 5
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame*100, boy.action*100 ,100 , 100, boy.x, boy.y)

class AutoRun:
    @staticmethod
    def enter(boy,e):
        boy.auto_speed = 5
        boy.scale = 1
        boy.start_time = get_time()

        if boy.dir == 0:
            boy.dir = 1

    @staticmethod
    def exit(boy,e):
        #boy.scale = 1
        #boy.auto_speed = 5
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.auto_speed += 0.1
        boy.scale += 0.01

        boy.x += boy.dir * boy.auto_speed

        if boy.x >= 800 - (50 * boy.scale):
            boy.dir = -1
        elif boy.x <= 0 + (50 * boy.scale):
            boy.dir = 1

        if get_time() - boy.start_time > 5:
            boy.state_machine.add_event(('TIME OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(
            boy.frame*100, boy.action*100, 100, 100,
            boy.x, boy.y, 100*boy.scale, 100*boy.scale
        )

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)  #Boy's state machine
        self.state_machine.start(Idle) #초기 상태가 Idle
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, time_out: Sleep, a_down: AutoRun},
                Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle, a_down: AutoRun},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, a_down: AutoRun},
                AutoRun: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, time_out: Idle}
            }
        )

    def update(self):
        self.state_machine.update() #State machine 시킴
        #self.frame = (self.frame + 1) % 8

    def handle_event(self, event):
        # event: 입력 이벤트
        # 우리가 state machine에게 전달해줄건 (  ,  )
        if event.type == SDL_KEYDOWN and event.key == SDLK_a:  # 'a' 키 눌림 확인
            self.state_machine.add_event(('a_down', event))  # a_down 이벤트 추가
        else:
            self.state_machine.add_event(('INPUT', event))
    def draw(self):
        self.state_machine.draw()

