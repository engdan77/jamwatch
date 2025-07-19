from jamwatch.config import Config


class Orchestrator:
    def __init__(self, config: Config):
        self.config = config
        self.running = False

    def start(self):
        self.running = True
