from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://mobigg.kr/")

# "데이안" 버튼 찾기
deian_btn = driver.find_element(By.XPATH, "//*[@id=\"app\"]/div/main/div/section/div[2]/section[3]/div[1]/button[5]")

# JavaScript로 강제 클릭
driver.execute_script("arguments[0].click();", deian_btn)

# 이후 데이터가 로드될 때까지 대기
time.sleep(2)

# 렌더링된 HTML을 BeautifulSoup으로 파싱
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# save the soup to a file
with open("soup.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

# 데이안 서버의 report-list 섹션 찾기
card_report_list = soup.find('section', class_='card report-list')
if card_report_list:
    # display: none;인 안내 div 찾기
    display_none_div = card_report_list.find('div', style=lambda x: x and 'display: none' in x)
    # report-card auto-generated div 찾기
    report_cards = card_report_list.find_all('div', class_='report-card auto-generated')

    if display_none_div and not report_cards:
        print("심층 검은 구멍 정보 없음")
    elif report_cards:
        print("심층 검은 구멍 정보 있음")
        for card in report_cards:
            card_text = card.get_text(strip=True)
            # 정규 표현식을 사용하여 검은 구멍 정보 (남은 시간) 추출
            match = re.search(r'(.+)남은 시간:(.+)(좋아요)', card_text)
            if match:
                remaining_time = match.group(2)
                print(f"남은 시간: {remaining_time}")
            else:
                print("남은 시간 정보를 찾을 수 없음")
    else:
        print("데이터 구조를 다시 확인 필요")
else:
    print("card report-list 섹션을 찾을 수 없음")

driver.quit()
