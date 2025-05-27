import json

def load_members():
    with open('data/members.json', 'r', encoding='utf-8') as f:
        return json.load(f)['members']

def search_member(query):
    members = load_members()

    # 직접 메인 캐릭터(key)와 일치하는 경우
    if query in members:
        return query, members[query]

    # 부캐릭터(value 리스트 내)와 일치하는 경우
    for main_char, alts in members.items():
        if query in alts and query != main_char:
            return main_char, alts

    return None, None
