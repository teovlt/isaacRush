import time
import pygame

class Timer:
    def __init__(self):
        self.startTime = 0
        self.bestTime = 0

    def start(self):
        self.startTime = time.monotonic()

    def update_best_time(self, elapsed_time):
        if elapsed_time < self.bestTime or self.bestTime == 0:
            self.bestTime = elapsed_time

    def drawCurrent(self, elapsed_time):
        font = pygame.font.Font(None, 36)
        current_time_str = f"Time: {elapsed_time:.1f} s"
        current_time_text = font.render(current_time_str, True, "white")
        return current_time_text
    def drawBest(self):
        font = pygame.font.Font(None, 36)
        best_time_str = f"Best Time: {self.bestTime:.3f} s"
        best_time_text = font.render(best_time_str, True, "white")
        return best_time_text


