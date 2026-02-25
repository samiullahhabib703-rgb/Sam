import os
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from scipy.interpolate import interp1d
import math

def create_character(width=150, height=200, char_type="blob", color=(255, 200, 100)):
    """Create animated character with different styles"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    if char_type == "blob":
        # Draw a blob character with arms and legs
        draw.ellipse([20, 10, 130, 130], fill=color, outline='black', width=3)  # Head
        draw.rectangle([40, 130, 110, 180], fill=color, outline='black', width=2)  # Body
        draw.ellipse([30, 140, 60, 180], fill=color, outline='black', width=2)  # Left leg
        draw.ellipse([90, 140, 120, 180], fill=color, outline='black', width=2)  # Right leg
        
        # Eyes
        draw.ellipse([50, 40, 70, 60], fill='white', outline='black', width=2)
        draw.ellipse([80, 40, 100, 60], fill='white', outline='black', width=2)
        draw.ellipse([55, 45, 65, 55], fill='black')  # Left pupil
        draw.ellipse([85, 45, 95, 55], fill='black')  # Right pupil
        
        # Smile
        draw.arc([50, 60, 100, 90], 0, 180, fill='black', width=3)
        
    elif char_type == "square":
        # Square robot character
        draw.rectangle([10, 10, 140, 140], fill=color, outline='black', width=3)
        draw.rectangle([30, 140, 70, 190], fill=color, outline='black', width=2)  # Left leg
        draw.rectangle([80, 140, 120, 190], fill=color, outline='black', width=2)  # Right leg
        
        # Eyes
        draw.rectangle([40, 40, 60, 60], fill='cyan', outline='black', width=2)
        draw.rectangle([80, 40, 100, 60], fill='cyan', outline='black', width=2)
        
        # Mouth
        draw.rectangle([45, 80, 95, 90], fill='red')
        
    elif char_type == "circle":
        # Round character
        draw.ellipse([10, 10, 140, 140], fill=color, outline='black', width=3)
        draw.ellipse([35, 145, 65, 190], fill=color, outline='black', width=2)  # Left leg
        draw.ellipse([85, 145, 115, 190], fill=color, outline='black', width=2)  # Right leg
        
        # Eyes
        draw.ellipse([40, 50, 60, 70], fill='black')
        draw.ellipse([80, 50, 100, 70], fill='black')
        
        # Happy mouth
        draw.arc([40, 70, 100, 100], 0, 180, fill='black', width=3)
    
    return img

def create_walking_animation(char_img, num_frames=10, direction='right'):
    """Create walking animation frames"""
    frames = []
    base_width, base_height = char_img.size
    
    for i in range(num_frames):
        # Create a copy for each frame
        frame_img = char_img.copy()
        
        # Add a slight bounce effect
        bounce = int(math.sin(i * math.pi / num_frames) * 10)
        
        # Create canvas with offset
        canvas = Image.new('RGBA', (base_width + 40, base_height), (0, 0, 0, 0))
        
        if direction == 'right':
            x_pos = i * 4
        else:
            frame_img = frame_img.transpose(Image.FLIP_LEFT_RIGHT)
            x_pos = (num_frames - i) * 4;
            
        canvas.paste(frame_img, (x_pos, bounce), frame_img)
        frames.append(np.array(canvas))
    
    return frames

def create_jumping_animation(char_img, num_frames=15):
    """Create jumping animation"""
    frames = []
    base_width, base_height = char_img.size
    canvas_height = base_height + 100;
    
    for i in range(num_frames):
        # Parabolic jump motion
        progress = i / num_frames
        jump_height = int(math.sin(progress * math.pi) * 80)
        
        canvas = Image.new('RGBA', (base_width, canvas_height), (0, 0, 0, 0))
        canvas.paste(char_img, (0, canvas_height - base_height - jump_height), char_img)
        frames.append(np.array(canvas))
    return frames

def create_dancing_animation(char_img, num_frames=16):
    """Create dancing animation with rotation"""
    frames = []
    
    for i in range(num_frames):
        angle = (i / num_frames) * 360
        # Slight tilt for dancing effect
        tilt = int(math.sin(i * math.pi / num_frames) * 15)
        
        rotated = char_img.rotate(tilt, expand=False, resample=Image.BICUBIC)
        frames.append(np.array(rotated))
    
    return frames

def make_frame(t, width=1280, height=720):
    """Generate frames for the video"""
    # Create background with gradient
    background = np.zeros((height, width, 3), dtype=np.uint8)
    background[:, :] = [100, 180, 255]  # Light blue
    
    return background

def create_funny_video_enhanced(output_path='funny_animation_video_enhanced.mp4'):
    """Create an enhanced funny video with animations and effects"""
    
    width, height = 1280, 720
    fps = 24
    clips = []
    
    print("🎬 Creating enhanced funny animation video...")
    print("=" * 50)
    
    # Scene 1: Introduction with dancing character
    print("📍 Scene 1: Dancing Introduction...")
    char1 = create_character(150, 200, "blob", (255, 200, 100))
    dance_frames = create_dancing_animation(char1, num_frames=16)
    
    bg1 = ColorClip(size=(width, height), color=(100, 180, 255)).set_duration(3)
    
    dance_clip = ImageSequenceClip(dance_frames, durations=[0.1]*len(dance_frames)).set_duration(3)
    dance_clip = dance_clip.set_position(('center', 'center'))
    
    text1 = TextClip("🎉 Hello! I'm your funny AI friend!", 
                     fontsize=50, color='white', font='Arial-Bold',
                     method='caption', size=(width-100, None))
    text1 = text1.set_duration(3).set_position(('center', 0.1), relative=True)
    
    scene1 = CompositeVideoClip([bg1, dance_clip, text1])
    clips.append(scene1)
    
    # Scene 2: Walking animation
    print("📍 Scene 2: Walking Character...")
    char2 = create_character(150, 200, "square", (200, 100, 255))
    walk_frames = create_walking_animation(char2, num_frames=20, direction='right')
    
    bg2 = ColorClip(size=(width, height), color=(255, 200, 100)).set_duration(3)
    
    walk_clip = ImageSequenceClip(walk_frames, durations=[0.08]*len(walk_frames)).set_duration(3)
    walk_clip = walk_clip.set_position(('center', 'center'))
    
    text2 = TextClip("Watch me strut my stuff! 💃", 
                     fontsize=50, color='white', font='Arial-Bold',
                     method='caption', size=(width-100, None))
    text2 = text2.set_duration(3).set_position(('center', 0.1), relative=True)
    
    scene2 = CompositeVideoClip([bg2, walk_clip, text2])
    clips.append(scene2)
    
    # Scene 3: Jumping animation
    print("📍 Scene 3: Jumping Character...")
    char3 = create_character(150, 200, "circle", (100, 255, 150))
    jump_frames = create_jumping_animation(char3, num_frames=15)
    
    bg3 = ColorClip(size=(width, height), color=(255, 150, 150)).set_duration(3)
    
    jump_clip = ImageSequenceClip(jump_frames, durations=[0.1]*len(jump_frames)).set_duration(3)
    jump_clip = jump_clip.set_position(('center', 'center'))
    
    text3 = TextClip("Wheeeee! I can jump! 🤸", 
                     fontsize=50, color='white', font='Arial-Bold',
                     method='caption', size=(width-100, None))
    text3 = text3.set_duration(3).set_position(('center', 0.1), relative=True)
    
    scene3 = CompositeVideoClip([bg3, jump_clip, text3])
    clips.append(scene3)
    
    # Scene 4: Multiple characters dancing
    print("📍 Scene 4: Party Time with Multiple Characters...")
    char_blob = create_character(100, 150, "blob", (255, 200, 100))
    char_square = create_character(100, 150, "square", (200, 100, 255))
    char_circle = create_character(100, 150, "circle", (100, 255, 150))
    
    dance_frames_blob = create_dancing_animation(char_blob, num_frames=16)
    dance_frames_square = create_dancing_animation(char_square, num_frames=16)
    dance_frames_circle = create_dancing_animation(char_circle, num_frames=16)
    
    bg4 = ColorClip(size=(width, height), color=(200, 100, 255)).set_duration(3)
    
    dance_clip_blob = ImageSequenceClip(dance_frames_blob, durations=[0.1]*len(dance_frames_blob)).set_duration(3)
    dance_clip_blob = dance_clip_blob.set_position(('center', 'center')).set_size((200, 300))
    
    dance_clip_square = ImageSequenceClip(dance_frames_square, durations=[0.1]*len(dance_frames_square)).set_duration(3)
    dance_clip_square = dance_clip_square.set_position(('left', 'center')).set_size((200, 300))
    
    dance_clip_circle = ImageSequenceClip(dance_frames_circle, durations=[0.1]*len(dance_frames_circle)).set_duration(3)
    dance_clip_circle = dance_clip_circle.set_position(('right', 'center')).set_size((200, 300))
    
    text4 = TextClip("LET'S PARTY! 🎊🎉🎈", 
                     fontsize=60, color='white', font='Arial-Bold',
                     method='caption', size=(width-100, None))
    text4 = text4.set_duration(3).set_position(('center', 0.1), relative=True)
    
    scene4 = CompositeVideoClip([bg4, dance_clip_blob, dance_clip_square, dance_clip_circle, text4])
    clips.append(scene4)
    
    # Scene 5: Finale
    print("📍 Scene 5: Funny Finale...")
    char_finale = create_character(200, 250, "blob", (255, 255, 100))
    jump_frames_finale = create_jumping_animation(char_finale, num_frames=15)
    
    bg5 = ColorClip(size=(width, height), color=(150, 255, 150)).set_duration(3)
    
    jump_clip_finale = ImageSequenceClip(jump_frames_finale, durations=[0.1]*len(jump_frames_finale)).set_duration(3)
    jump_clip_finale = jump_clip_finale.set_position(('center', 'center'))
    
    text5 = TextClip("Thanks for watching! Don't forget to LAUGH! 😂", 
                     fontsize=50, color='white', font='Arial-Bold',
                     method='caption', size=(width-100, None))
    text5 = text5.set_duration(3).set_position(('center', 0.1), relative=True)
    
    emoji_text = TextClip("🎬✨🎪🎭🎨🎵", 
                          fontsize=80, color='white', font='Arial-Bold')
    emoji_text = emoji_text.set_duration(3).set_position(('center', 0.5), relative=True)
    
    scene5 = CompositeVideoClip([bg5, jump_clip_finale, text5, emoji_text])
    clips.append(scene5)
    
    # Combine all scenes
    print("🎬 Combining all scenes...")
    final_video = concatenate_videoclips(clips)
    
    # Write video file
    print("💾 Writing video file...")
    final_video.write_videofile(output_path, fps=fps, verbose=False, logger=None, codec='libx264', audio_codec='aac')
    
    print("=" * 50)
    print(f"✅ Enhanced video created successfully!")
    print(f"📹 File: {output_path}")
    print(f"⏱️ Duration: {len(clips) * 3} seconds")
    print("🎉 Enjoy your funny AI animation!")

if __name__ == "__main__":
    create_funny_video_enhanced()