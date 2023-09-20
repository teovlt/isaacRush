import pygame

class Timer:
    def __init__(self):
        self.startTime = 0
        self.bestTime = 0

    def start(self):
        self.startTime = pygame.time.get_ticks()

    def update_best_time(self, current_time):
        if current_time < self.bestTime or self.bestTime == 0:
            self.bestTime = current_time

    def get_current_time(self):
        return pygame.time.get_ticks() - self.startTime

    def drawCurrent(self):
        font = pygame.font.Font(None, 36)
        current_time = pygame.time.get_ticks() - self.startTime
        current_time_str = f"Time: {current_time / 1000:.1f} s"
        current_time_text = font.render(current_time_str, True, "white")
        return current_time_text

    def drawBest(self):
        font = pygame.font.Font(None, 36)
        best_time_str = f"Best Time: {self.bestTime / 1000} s"
        best_time_text = font.render(best_time_str, True, "white")
        return best_time_text

    def stop(self, currenTime):
        saveTime = currenTime
        return saveTime

