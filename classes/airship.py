import time

class Airship:
    def __init__(self, id, spawn_local):
        self.id = id
        self.spawn_time = time.perf_counter()
        self.spawn_local = spawn_local