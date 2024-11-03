from pico2d import *
from boy import Boy
from grass import Grass

def handle_events(boy):
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_a:  # 'a' 키로 AutoRun 상태 진입
                boy.enter_auto_run()
            elif event.key == SDLK_RIGHT:
                boy.start_running(1)  # 오른쪽 이동
            elif event.key == SDLK_LEFT:
                boy.start_running(-1)  # 왼쪽 이동
        elif event.type == SDL_KEYUP:
            if event.key in (SDLK_RIGHT, SDLK_LEFT):
                boy.stop_running()  # 방향키에서 손을 뗐을 때 Idle 상태로 돌아감

def reset_world():
    global running
    global grass
    global boy

    running = True
    grass = Grass()
    boy = Boy()

def update_world():
    boy.update()
    grass.update()

def render_world():
    clear_canvas()
    grass.draw()
    boy.draw()
    update_canvas()

# Main loop
open_canvas()
reset_world()
while running:
    handle_events(boy)
    update_world()
    render_world()
    delay(0.01)
close_canvas()