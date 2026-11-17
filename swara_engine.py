import speech_recognition as sr
from deep_translator import LibreTranslator
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

        # 2. Translate using LibreTranslate (Bypasses Google entirely)
        # Note: LibreTranslate uses standard 2-letter codes like 'te', 'hi', 'en'
        translator = LibreTranslator(source=src_lang, target=tgt_lang)
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
