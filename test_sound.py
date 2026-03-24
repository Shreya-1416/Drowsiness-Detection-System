import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load your alarm file
pygame.mixer.music.load("alarm.wav")

# Play the alarm
pygame.mixer.music.play()

print("Alarm playing... Press Enter to stop")
input()  # Waits until you press Enter

# Stop the music
pygame.mixer.music.stop()
print("Stopped")
