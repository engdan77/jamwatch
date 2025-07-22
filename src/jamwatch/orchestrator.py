from jamwatch.config import OrchestratorParams


class Orchestrator:
    def __init__(self, config: OrchestratorParams):
        self.config = config
        self.running = False

    def start(self):
        self.running = True
