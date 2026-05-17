import time

class GameManager:

    def __init__(self):
        self.active = False
        self.last_word = None
        self.used_words = []
        self.last_player = None
        self.last_time = time.time()

game = GameManager()
