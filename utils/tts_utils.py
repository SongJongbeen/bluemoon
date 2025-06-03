import os
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
import uuid

load_dotenv()

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    return OpenAI(api_key=api_key)

def text_to_speech_file(text, filename=None, model="tts-1", voice="alloy"):
    """
    OpenAI TTS API로 텍스트를 mp3로 변환하고 파일 경로 반환
    """
    client = get_openai_client()
    if filename is None:
        filename = f"tts_{uuid.uuid4().hex}.mp3"
    speech_file_path = Path(filename)
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text
    )
    with open(speech_file_path, 'wb') as file:
        for chunk in response.iter_bytes():
            file.write(chunk)
    return str(speech_file_path)

def remove_file(filepath):
    try:
        os.remove(filepath)
    except Exception:
        pass
