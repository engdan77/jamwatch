from jamwatch.param import Param


class Orchestrator:
    def __init__(self, param: Param):
        self.param = param
        self.running = False

    def start(self):
        self.running = True
