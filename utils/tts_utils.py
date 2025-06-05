import os
from pathlib import Path
import uuid
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

VOICES = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']
DEFAULT_VOICE = 'shimmer'

class TTSManager:
    def __init__(self):
        self.voice = DEFAULT_VOICE

    def set_voice(self, voice):
        if voice in VOICES:
            self.voice = voice
            return True
        return False

    def get_voice(self):
        return self.voice

    def get_openai_client(self):
        api_key = os.getenv("OPENAI_API_KEY")
        return OpenAI(api_key=api_key)

    def text_to_speech_file(self, text, filename=None, model="tts-1"):
        client = self.get_openai_client()
        if filename is None:
            filename = f"tts_{uuid.uuid4().hex}.mp3"
        speech_file_path = Path(filename)
        response = client.audio.speech.create(
            model=model,
            voice=self.voice,
            input=text
        )
        with open(speech_file_path, 'wb') as file:
            for chunk in response.iter_bytes():
                file.write(chunk)
        return str(speech_file_path)

tts_manager = TTSManager()

def text_to_speech_file(text, filename=None, model="tts-1"):
    return tts_manager.text_to_speech_file(text, filename, model)

def remove_file(filepath):
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        else:
            print(f"파일이 존재하지 않음: {filepath}")
            return False
    except PermissionError:
        print(f"파일 삭제 권한 없음: {filepath}")
        return False
    except OSError as e:
        print(f"파일 삭제 중 오류 발생: {filepath} - {str(e)}")
        return False

def set_voice(voice):
    return tts_manager.set_voice(voice)

def get_voice():
    return tts_manager.get_voice()
