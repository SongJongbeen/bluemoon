import random

def promote_item():
    steps = [
        (0.90, "★", "고급"),
        (0.85, "★★", "레어"),
        (0.80, "★★★", "레어"),
        (0.50, "★★★★", "엘리트"),
        (0.40, "★★★★★", "에픽"),
        (0.10, "★★★★★★", "전설"),
    ]

    current_grade = "☆"
    current_name = "일반"

    for chance, grade, name in steps:
        if random.random() < chance:
            current_grade = grade
            current_name = name
        else:
            break  # 실패 시 즉시 종료

    return f"{current_grade} ({current_name})"
