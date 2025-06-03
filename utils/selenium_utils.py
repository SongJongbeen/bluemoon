# utils/selenium_utils.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time

SERVER_IDX = {
    "알리사": 1,
    "메이븐": 2,
    "라사": 3,
    "칼릭스": 4,
    "데이안": 5,
    "아이라": 6,
    "던컨": 7
}

def get_server_soup(
    url: str,
    server_name: str,
    wait_sec: int = 2,
    headless: bool = True
) -> BeautifulSoup:
    """
    mobigg.kr에서 원하는 서버(예: '데이안')의 데이터를 렌더링한 후 BeautifulSoup 객체로 반환

    :param url: 크롤링할 페이지 주소
    :param server_name: 클릭할 서버명 (예: '데이안')
    :param wait_sec: 각 단계별 대기 시간(초)
    :param headless: 크롬 창을 띄울지 여부
    :return: BeautifulSoup 객체
    """
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    # overlay가 있으면 사라질 때까지 대기
    try:
        overlays = driver.find_elements(By.CLASS_NAME, "overlay")
        if overlays:
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "overlay"))
            )
    except TimeoutException:
        # overlay가 안 사라지면 강제로 지움
        driver.execute_script("""
            let overlays = document.getElementsByClassName('overlay');
            for(let i=0; i<overlays.length; i++) {
                overlays[i].style.display = 'none';
            }
        """)

    # 서버 버튼 클릭
    try:
        server_button = driver.find_element(By.XPATH, f"//*[@id=\"app\"]/div/main/div/section/div[2]/section[3]/div[1]/button[{SERVER_IDX[server_name]}]")
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", server_button)
    except Exception as e:
        driver.quit()
        raise RuntimeError(f"서버 버튼 클릭 실패: {e}")

    time.sleep(wait_sec)  # 데이터 렌더링 대기

    html = driver.page_source
    driver.quit()
    return BeautifulSoup(html, "html.parser")
