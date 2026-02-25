# Enhanced Funny Animation Video Script

import pygame  # For sound and music
import time

# Initialize the mixer
pygame.mixer.init()

# Load sound effects and background music
sound_effect = pygame.mixer.Sound('sounds/effect.wav')
background_music = 'music/background.mp3'

# Function to play background music
def play_background_music():
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.play(-1)  # -1 means loop indefinitely

# Function to play sound effects
def play_sound_effect():
    sound_effect.play()

# Function to stop all sounds
def stop_all_sounds():
    pygame.mixer.music.stop()
    pygame.mixer.stop()

# Main function to run the animation
def run_animation():
    play_background_music()
    print('Animation is running...')
    time.sleep(2)  # Simulating animation duration
    play_sound_effect()
    print('Sound effect played!')
    time.sleep(2)
    stop_all_sounds()

if __name__ == '__main__':
    run_animation()