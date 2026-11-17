import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import time

def process_audio(audio_file_path, src_lang, tgt_lang):
    recognizer = sr.Recognizer()

    try:
        # 1. Recognize spoken audio
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
        
        # Speech recognition mapping
        speech_lang = src_lang
        if src_lang == 'zh-CN':
            speech_lang = 'zh'
            
        original_text = recognizer.recognize_google(audio_data, language=speech_lang)

        # 2. Stable Translation using GoogleTranslator with error handling
        # If the direct route fails due to server limits, we use a simple try-except fallback
        try:
            if src_lang != 'en' and tgt_lang != 'en':
                # Step A: Translate regional language to English
                english_bridge = GoogleTranslator(source=src_lang, target='en').translate(original_text)
                time.sleep(0.5)
                # Step B: Translate English to target language
                translated_text = GoogleTranslator(source='en', target=tgt_lang).translate(english_bridge)
            else:
                translated_text = GoogleTranslator(source=src_lang, target=tgt_lang).translate(original_text)
        except Exception:
            # Fallback if bridge translation hits a rate limit: try direct translation
            translated_text = GoogleTranslator(source=src_lang, target=tgt_lang).translate(original_text)

        # 3. Generate Audio Output
        tts_lang = tgt_lang
        if tgt_lang == 'zh-CN':
            tts_lang = 'zh-CN'
            
        tts = gTTS(text=translated_text, lang=tts_lang)
        output_file = "output.mp3"
        tts.save(output_file)

        return original_text, translated_text, output_file

    except Exception as e:
        return None, None, str(e)
