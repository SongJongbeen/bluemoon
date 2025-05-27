import os
import requests
import yaml
from dotenv import load_dotenv

load_dotenv()

def load_prompts():
    with open('data/prompts.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def ask_perplexity(question):
    prompts = load_prompts()
    system_prompt = prompts['system']['content']

    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('PERPLEXITY_API_KEY')}"
    }
    payload = {
        "model": "sonar-pro",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        "temperature": 0.2,
        "return_images": False
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return "Perplexity API 호출 중 오류가 발생했습니다."
