class StateMachine:
    def __init__(self, obj):
        self.obj = obj
        self.event_que = []
        self.cur_state = None

    def start(self, state):
        self.cur_state = state
        self.cur_state.enter(self.obj)

    def add_event(self, event):
        self.event_que.append(event)

    def transition(self, new_state_name):
        # 현재 상태를 나가고, 새로운 상태 이름으로 전환
        self.cur_state.exit(self.obj)

        # 새로운 상태로 전환
        if new_state_name == "AutoRun":
            from boy import AutoRun
            self.cur_state = AutoRun
        elif new_state_name == "Run":
            from boy import Run
            self.cur_state = Run
        elif new_state_name == "Idle":
            from boy import Idle
            self.cur_state = Idle

        self.cur_state.enter(self.obj)

    def update(self):
        self.cur_state.do(self.obj)
        while self.event_que:
            event = self.event_que.pop(0)
            if event == "timeout" and self.cur_state.__name__ == "AutoRun":
                self.transition("Idle")

    def draw(self):
        self.cur_state.draw(self.obj)