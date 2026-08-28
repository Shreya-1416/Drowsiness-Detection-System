import pygame

pygame.mixer.init()
pygame.mixer.music.load("alarm_fixed.wav")
pygame.mixer.music.play()

print("Alarm playing... Press Enter to stop")
input()

pygame.mixer.music.stop()
pygame.mixer.quit()