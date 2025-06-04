import csv
import json
from collections import defaultdict

# CSV 파일 읽기
input_csv = 'data/명단 - 어비스.csv'
output_json = 'data/members.json'

members = defaultdict(list)

with open(input_csv, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)

    for row in reader:
        if len(row) < 2 or not row[1].strip():
            continue
        main = row[1].strip()
        for i in range(3, len(row), 2):  # 3, 5, ... (부캐 위치)
            sub = row[i].strip()
            if sub and sub != main and sub not in members[main]:
                members[main].append(sub)
        if main not in members[main]:
            members[main].insert(0, main)  # 대표도 부캐 리스트에 포함


# members.json과 같은 구조로 변환
# (대표 캐릭터가 부캐 리스트를 가지는 구조)
result = {}
for main, chars in members.items():
    unique_chars = list(set(chars))  # 중복 제거
    result[main] = unique_chars

# JSON으로 저장
with open(output_json, 'w', encoding='utf-8') as f:
    json.dump({"members": result}, f, ensure_ascii=False, indent=2)

print(f"{output_json} 파일이 생성되었습니다.")
