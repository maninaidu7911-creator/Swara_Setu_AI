import speech_recognition as sr
from translate import Translator
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

        # 2. Direct translation using the 'translate' library (No API keys or rate limits)
        # Handle Chinese language code format for the translator
        from_lang = src_lang.split('-')[0] if src_lang else 'en'
        to_lang = tgt_lang.split('-')[0] if tgt_lang else 'en'

        translator = Translator(from_lang=from_lang, to_lang=to_lang)
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
