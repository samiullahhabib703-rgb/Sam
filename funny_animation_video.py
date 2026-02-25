from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont

# Prepare your assets
characters = ['Character 1', 'Character 2']
texts = ['Hello!', 'Hi there!']

# Create a blank image
width, height = 640, 480
background_color = (255, 255, 255)  # White
image = Image.new('RGB', (width, height), background_color)

# Drawing text on the image
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

for i, character in enumerate(characters):
    draw.text((50, 50 + i * 100), f'{character}: {texts[i]}', fill=(0, 0, 0), font=font)

# Save the image as a frame
image_path = 'frame.png'
image.save(image_path)

# Create a video clip from image
clip = ImageClip(image_path).set_duration(2)

# Add more clips or animate transitions as needed
final_clip = concatenate_videoclips([clip])

# Export the final video
final_clip.write_videofile('funny_animation_video.mp4', fps=24)