import os
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from scipy.interpolate import interp1d
import math
from pydub import AudioSegment
from pydub.generators import Sine, WhiteNoise
from pydub.scipy_effects import normalize
import io

def create_character(width=150, height=200, char_type="blob", color=(255, 200, 100)):
    """Create animated character with different styles"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    if char_type == "blob":
        draw.ellipse([20, 10, 130, 130], fill=color, outline='black', width=3)
        draw.rectangle([40, 130, 110, 180], fill=color, outline='black', width=2)
        draw.ellipse([30, 140, 60, 180], fill=color, outline='black', width=2)
        draw.ellipse([90, 140, 120, 180], fill=color, outline='black', width=2)
        draw.ellipse([50, 40, 70, 60], fill='white', outline='black', width=2)
        draw.ellipse([80, 40, 100, 60], fill='white', outline='black', width=2)
        draw.ellipse([55, 45, 65, 55], fill='black')
        draw.ellipse([85, 45, 95, 55], fill='black')
        draw.arc([50, 60, 100, 90], 0, 180, fill='black', width=3)
        
elif char_type == "square":
        draw.rectangle([10, 10, 140, 140], fill=color, outline='black', width=3)
        draw.rectangle([30, 140, 70, 190], fill=color, outline='black', width=2)
        draw.rectangle([80, 140, 120, 190], fill=color, outline='black', width=2)
        draw.rectangle([40, 40, 60, 60], fill='cyan', outline='black', width=2)
        draw.rectangle([80, 40, 100, 60], fill='cyan', outline='black', width=2)
        draw.rectangle([45, 80, 95, 90], fill='red')
        
elif char_type == "circle":
        draw.ellipse([10, 10, 140, 140], fill=color, outline='black', width=3)
        draw.ellipse([35, 145, 65, 190], fill=color, outline='black', width=2)
        draw.ellipse([85, 145, 115, 190], fill=color, outline='black', width=2)
        draw.ellipse([40, 50, 60, 70], fill='black')
        draw.ellipse([80, 50, 100, 70], fill='black')
        draw.arc([40, 70, 100, 100], 0, 180, fill='black', width=3)
    
    return img

def create_walking_animation(char_img, num_frames=10, direction='right'):
    """Create walking animation frames"""
    frames = []
    base_width, base_height = char_img.size
    
    for i in range(num_frames):
        frame_img = char_img.copy()
        bounce = int(math.sin(i * math.pi / num_frames) * 10)
        canvas = Image.new('RGBA', (base_width + 40, base_height), (0, 0, 0, 0))
        
        if direction == 'right':
            x_pos = i * 4
        else:
            frame_img = frame_img.transpose(Image.FLIP_LEFT_RIGHT)
            x_pos = (num_frames - i) * 4
            
        canvas.paste(frame_img, (x_pos, bounce), frame_img)
        frames.append(np.array(canvas))
    
    return frames

def create_jumping_animation(char_img, num_frames=15):
    """Create jumping animation"""
    frames = []
    base_width, base_height = char_img.size
    canvas_height = base_height + 100;
    
    for i in range(num_frames):
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
        tilt = int(math.sin(i * math.pi / num_frames) * 15)
        rotated = char_img.rotate(tilt, expand=False, resample=Image.BICUBIC)
        frames.append(np.array(rotated))
    
    return frames

def create_sound_effect(effect_type='beep', duration=0.5, freq=440):
    """Create sound effects using pydub"""
    sample_rate = 44100;
    
    if effect_type == 'beep':
        sine = Sine(freq).to_audio_segment(duration=int(duration*1000))
        return sine;
    
    elif effect_type == 'pop':
        sine = Sine(400).to_audio_segment(duration=100)
        return sine;
    
    elif effect_type == 'whoosh':
        sine = Sine(100).to_audio_segment(duration=int(duration*1000))
        return sine;
    
    elif effect_type == 'jump':
        sine = Sine(600).to_audio_segment(duration=100) + Sine(800).to_audio_segment(duration=100)
        return sine;
    
    elif effect_type == 'laugh':
        laugh = Sine(200).to_audio_segment(duration=300) + AudioSegment.silent(duration=100)
        return laugh;
    
    elif effect_type == 'tada':
        notes = [523, 659, 784, 1047]
        tada = AudioSegment.empty()
        for note in notes:
            tada += Sine(note).to_audio_segment(duration=150)
        return tada;
    
    else:
        return Sine(freq).to_audio_segment(duration=int(duration*1000))

def create_background_music(duration_ms=15000):
    """Create upbeat background music"""
    bpm = 120;
    beat_duration = int((60 / bpm) * 1000);
    melody = AudioSegment.empty();
    pattern = [262, 330, 392, 494, 392, 330, 262, 294];
    
    num_repeats = duration_ms // (beat_duration * len(pattern));
    
    for _ in range(num_repeats + 1):
        for note in pattern:
            melody += Sine(note).to_audio_segment(duration=beat_duration);
            if len(melody) >= duration_ms:
                return melody[:duration_ms];
    
    return melody[:duration_ms];

def create_voiceover_text_to_audio(text, duration=2):
    """Create voiceover narration (simulated with tones)"""
    sample_rate = 44100;
    num_samples = int(duration * sample_rate);
    
    t = np.linspace(0, duration, num_samples);
    frequency = 400 + 200 * np.sin(2 * np.pi * t);
    audio_data = np.sin(2 * np.pi * frequency * t) * 0.3;
    
    audio_int16 = np.int16(audio_data * 32767);
    audio_segment = AudioSegment(
        audio_int16.tobytes(),
        frame_rate=sample_rate,
        sample_width=2,
        channels=1
    );
    
    return audio_segment;

def create_funny_video_ultimate(output_path='funny_animation_ultimate.mp4'):
    """Create the ULTIMATE funny video with all features"""
    
    width, height = 1280, 720;
    fps = 24;
    clips = [];
    
    print("=" * 70);
    print("🎬 CREATING ULTIMATE FUNNY ANIMATION VIDEO WITH FULL AUDIO! 🎬");
    print("=" * 70);
    
    print("\n🎵 Step 1: Generating Background Music...");
    bg_music = create_background_music(duration_ms=15000);
    
    print("📍 Step 2: Scene 1 - Dancing Introduction...");
    char1 = create_character(150, 200, "blob", (255, 200, 100));
    dance_frames = create_dancing_animation(char1, num_frames=16);
    bg1 = ColorClip(size=(width, height), color=(100, 180, 255)).set_duration(3);
    dance_clip = ImageSequenceClip(dance_frames, durations=[0.1]*len(dance_frames)).set_duration(3);
    dance_clip = dance_clip.set_position(('center', 'center'));
    text1 = TextClip("🎉 Hello! I'm your funny AI friend!", fontsize=50, color='white', font='Arial-Bold', method='caption', size=(width-100, None));
    text1 = text1.set_duration(3).set_position(('center', 0.1), relative=True);
    
    voice1 = create_voiceover_text_to_audio("Hello I am your funny AI friend", duration=2);
    laugh_effect = create_sound_effect('laugh', duration=0.5) * 2;
    scene1_audio = voice1 + AudioSegment.silent(duration=1000);
    
    scene1 = CompositeVideoClip([bg1, dance_clip, text1]);
    scene1_audio_clip = AudioFileClip("temp_scene1.wav", fps=44100);
    try:
        with open("temp_scene1.wav", "wb") as f:
            f.write(scene1_audio.export(format="wav").read());
        scene1_audio_clip = AudioFileClip("temp_scene1.wav");
        scene1 = scene1.set_audio(scene1_audio_clip);
    except:
        print("⚠️  Audio processing skipped for scene 1");
    clips.append(scene1);
    
    print("📍 Step 3: Scene 2 - Walking Character...");
    char2 = create_character(150, 200, "square", (200, 100, 255));
    walk_frames = create_walking_animation(char2, num_frames=20, direction='right');
    bg2 = ColorClip(size=(width, height), color=(255, 200, 100)).set_duration(3);
    walk_clip = ImageSequenceClip(walk_frames, durations=[0.08]*len(walk_frames)).set_duration(3);
    walk_clip = walk_clip.set_position(('center', 'center'));
    text2 = TextClip("Watch me strut my stuff! 💃", fontsize=50, color='white', font='Arial-Bold', method='caption', size=(width-100, None));
    text2 = text2.set_duration(3).set_position(('center', 0.1), relative=True);
    
    voice2 = create_voiceover_text_to_audio("Watch me strut my stuff", duration=2);
    whoosh = create_sound_effect('whoosh', duration=2);
    scene2_audio = voice2.overlay(whoosh);
    
    scene2 = CompositeVideoClip([bg2, walk_clip, text2]);
    try:
        with open("temp_scene2.wav", "wb") as f:
            f.write(scene2_audio.export(format="wav").read());
        scene2_audio_clip = AudioFileClip("temp_scene2.wav");
        scene2 = scene2.set_audio(scene2_audio_clip);
    except:
        print("⚠️  Audio processing skipped for scene 2");
    clips.append(scene2);
    
    print("📍 Step 4: Scene 3 - Jumping Character...");
    char3 = create_character(150, 200, "circle", (100, 255, 150));
    jump_frames = create_jumping_animation(char3, num_frames=15);
    bg3 = ColorClip(size=(width, height), color=(255, 150, 150)).set_duration(3);
    jump_clip = ImageSequenceClip(jump_frames, durations=[0.1]*len(jump_frames)).set_duration(3);
    jump_clip = jump_clip.set_position(('center', 'center'));
    text3 = TextClip("Wheeeee! I can jump! 🤸", fontsize=50, color='white', font='Arial-Bold', method='caption', size=(width-100, None));
    text3 = text3.set_duration(3).set_position(('center', 0.1), relative=True);
    
    voice3 = create_voiceover_text_to_audio("Wheeee I can jump", duration=2);
    jump_sound = create_sound_effect('jump', duration=0.2) * 3;
    scene3_audio = voice3.overlay(jump_sound);
    
    scene3 = CompositeVideoClip([bg3, jump_clip, text3]);
    try:
        with open("temp_scene3.wav", "wb") as f:
            f.write(scene3_audio.export(format="wav").read());
        scene3_audio_clip = AudioFileClip("temp_scene3.wav");
        scene3 = scene3.set_audio(scene3_audio_clip);
    except:
        print("⚠️  Audio processing skipped for scene 3");
    clips.append(scene3);
    
    print("📍 Step 5: Scene 4 - Party Time!");
    char_blob = create_character(100, 150, "blob", (255, 200, 100));
    char_square = create_character(100, 150, "square", (200, 100, 255));
    char_circle = create_character(100, 150, "circle", (100, 255, 150));
    
    dance_frames_blob = create_dancing_animation(char_blob, num_frames=16);
    dance_frames_square = create_dancing_animation(char_square, num_frames=16);
    dance_frames_circle = create_dancing_animation(char_circle, num_frames=16);
    
    bg4 = ColorClip(size=(width, height), color=(200, 100, 255)).set_duration(3);
    dance_clip_blob = ImageSequenceClip(dance_frames_blob, durations=[0.1]*len(dance_frames_blob)).set_duration(3).set_position(('center', 'center')).set_size((200, 300));
    dance_clip_square = ImageSequenceClip(dance_frames_square, durations=[0.1]*len(dance_frames_square)).set_duration(3).set_position(('left', 'center')).set_size((200, 300));
    dance_clip_circle = ImageSequenceClip(dance_frames_circle, durations=[0.1]*len(dance_frames_circle)).set_duration(3).set_position(('right', 'center')).set_size((200, 300));
    
    text4 = TextClip("LET'S PARTY! 🎊🎉🎈", fontsize=60, color='white', font='Arial-Bold', method='caption', size=(width-100, None));
    text4 = text4.set_duration(3).set_position(('center', 0.1), relative=True);
    
    voice4 = create_voiceover_text_to_audio("Let's party", duration=2);
    tada_sound = create_sound_effect('tada', duration=1) + create_sound_effect('tada', duration=1);
    scene4_audio = voice4.overlay(tada_sound);
    
    scene4 = CompositeVideoClip([bg4, dance_clip_blob, dance_clip_square, dance_clip_circle, text4]);
    try:
        with open("temp_scene4.wav", "wb") as f:
            f.write(scene4_audio.export(format="wav").read());
        scene4_audio_clip = AudioFileClip("temp_scene4.wav");
        scene4 = scene4.set_audio(scene4_audio_clip);
    except:
        print("⚠️  Audio processing skipped for scene 4");
    clips.append(scene4);
    
    print("📍 Step 6: Scene 5 - Finale!");
    char_finale = create_character(200, 250, "blob", (255, 255, 100));
    jump_frames_finale = create_jumping_animation(char_finale, num_frames=15);
    bg5 = ColorClip(size=(width, height), color=(150, 255, 150)).set_duration(3);
    jump_clip_finale = ImageSequenceClip(jump_frames_finale, durations=[0.1]*len(jump_frames_finale)).set_duration(3);
    jump_clip_finale = jump_clip_finale.set_position(('center', 'center'));
    text5 = TextClip("Thanks for watching! Don't forget to LAUGH! 😂", fontsize=50, color='white', font='Arial-Bold', method='caption', size=(width-100, None));
    text5 = text5.set_duration(3).set_position(('center', 0.1), relative=True);
    emoji_text = TextClip("🎬✨🎪🎭🎨🎵", fontsize=80, color='white', font='Arial-Bold');
    emoji_text = emoji_text.set_duration(3).set_position(('center', 0.5), relative=True);
    
    voice5 = create_voiceover_text_to_audio("Thanks for watching don't forget to laugh", duration=2);
    laugh_finale = create_sound_effect('laugh', duration=1) * 2;
    scene5_audio = voice5.overlay(laugh_finale);
    
    scene5 = CompositeVideoClip([bg5, jump_clip_finale, text5, emoji_text]);
    try:
        with open("temp_scene5.wav", "wb") as f:
            f.write(scene5_audio.export(format="wav").read());
        scene5_audio_clip = AudioFileClip("temp_scene5.wav");
        scene5 = scene5.set_audio(scene5_audio_clip);
    except:
        print("⚠️  Audio processing skipped for scene 5");
    clips.append(scene5);
    
    print("\n🎬 Step 7: Combining All Scenes...");
    final_video = concatenate_videoclips(clips);
    
    print("🔊 Step 8: Mixing Audio Tracks...");
    try:
        with open("temp_bg_music.wav", "wb") as f:
            f.write(bg_music.export(format="wav").read());
        bg_music_clip = AudioFileClip("temp_bg_music.wav");
        bg_music_clip = bg_music_clip.volumex(0.3);
        final_audio = CompositeAudioClip([bg_music_clip, final_video.audio.volumex(1.0)]);
        final_video = final_video.set_audio(final_audio);
    except:
        print("⚠️  Background music mixing skipped");
    
    print("💾 Step 9: Writing Video File...");
    final_video.write_videofile(output_path, fps=fps, verbose=False, logger=None, codec='libx264', audio_codec='aac');
    
    print("\n" + "=" * 70);
    print("✅ ULTIMATE VIDEO CREATED SUCCESSFULLY!");
    print("=" * 70);
    print(f"📹 File: {output_path}");
    print(f"⏱️ Duration: 15 seconds");
    print(f"📊 Resolution: 1280x720 (HD)");
    print(f"🎬 Features:");
    print(f"   ✨ Advanced character animations");
    print(f"   💃 Dancing, walking, and jumping");
    print(f"   🎵 Background music + sound effects + voiceover");
    print(f"   🌈 Dynamic colorful backgrounds");
    print(f"   🎭 Multiple unique characters");
    print(f"   📢 Professional audio mixing");
    print("=" * 70);
    print("🎉 Enjoy your funny AI animation masterpiece!");
    print("=" * 70);
    
    # Clean up temporary files
    for temp_file in ["temp_scene1.wav", "temp_scene2.wav", "temp_scene3.wav", "temp_scene4.wav", "temp_scene5.wav", "temp_bg_music.wav"]:
        if os.path.exists(temp_file):
            os.remove(temp_file);

if __name__ == "__main__":
    create_funny_video_ultimate()