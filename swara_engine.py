import speech_recognition as sr
from deep_translator import MyMemoryTranslator
from gtts import gTTS
import os

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

        # Map short codes to full language names for MyMemory Translator to prevent code errors
        lang_name_map = {
            'te': 'telugu', 'hi': 'hindi', 'en': 'english', 'ta': 'tamil',
            'kn': 'kannada', 'ml': 'malayalam', 'bn': 'bengali', 'gu': 'gujarati',
            'mr': 'marathi', 'pa': 'punjabi', 'ur': 'urdu', 'es': 'spanish',
            'fr': 'french', 'de': 'german', 'ar': 'arabic', 'zh-CN': 'chinese simplified'
        }
        
        src_name = lang_name_map.get(src_lang, 'english')
        tgt_name = lang_name_map.get(tgt_lang, 'english')

        # 2. Translate using MyMemory (Completely avoids Google IP blocks)
        translator = MyMemoryTranslator(source=src_name, target=tgt_name)
        translated_text = translator.translate(original_text)

        if not translated_text:
            translated_text = original_text

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
