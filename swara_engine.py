import speech_recognition as sr
from gtts import gTTS
import os
import requests

def raw_google_api_translate(text, source_lang, target_lang):
    """Bypasses API limits for all global languages."""
    url = "https://translate.googleapis.com/translate_a/single"
    params = {"client": "gtx", "sl": source_lang, "tl": target_lang, "dt": "t", "q": text}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return "".join([sentence[0] for sentence in response.json()[0]])

def process_audio(audio_file_path, source_lang_code, target_lang_code):
    recognizer = sr.Recognizer()
    
    # 1. Speech to Text (Now dynamic for any language)
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
            # Passes the exact language code (e.g., 'es' for Spanish, 'te' for Telugu)
            recognized_text = recognizer.recognize_google(audio_data, language=source_lang_code)
    except sr.UnknownValueError:
        return None, None, "Could not understand the audio. Please speak clearly."
    except Exception as e:
        return None, None, f"Error processing audio: {e}"

    # 2. Translation
    try:
        translated_text = raw_google_api_translate(recognized_text, source_lang_code, target_lang_code)
    except Exception as e:
        return recognized_text, None, f"Translation error: {e}"

    # 3. Text to Speech
    try:
        output_audio_path = "translated_output.mp3"
        if os.path.exists(output_audio_path):
            os.remove(output_audio_path)
            
        tts = gTTS(text=translated_text, lang=target_lang_code)
        tts.save(output_audio_path)
    except Exception as e:
        return recognized_text, translated_text, f"Audio generation error: {e}"

    return recognized_text, translated_text, output_audio_path