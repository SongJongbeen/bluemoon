import json

def is_privacy_allowed(username, path="privacy.json"):
    """
    닉네임이 privacy.json에서 True면 허용, False면 거부
    """
    with open(path, encoding="utf-8") as f:
        privacy = json.load(f)
    return privacy.get(username, True)  # 기본값 True
