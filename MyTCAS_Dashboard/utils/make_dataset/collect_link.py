import asyncio
from playwright.sync_api import sync_playwright
import bs4
import time 
import pandas as pd
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # headless=True จะไม่แสดง browser
    page = browser.new_page()
    page.goto("https://course.mytcas.com/")
    page.wait_for_selector("#search")
    page.type("#search", "วิศวกรรมปัญญาประดิษฐ์", delay=100)
    page.click("#search")
    # รอให้ผลลัพธ์โหลด (อาจต้องปรับเวลา)
    page.wait_for_timeout(5000)
    html = page.content()
    browser.close()

# # ใช้ bs4 วิเคราะห์ข้อมูล
print("before")
time.sleep(2)
print("after")
soup = bs4.BeautifulSoup(html, "html.parser")
results = soup.find("ul", class_ = 't-programs')  # ตัวอย่างค้นหา li ทั้งหมด

df = pd.DataFrame(columns=['Link'])
with open('major_link.csv' , 'a' , encoding="utf-8") as f:
    for r in results.find_all('li'):
        link = r.find('a')['href']
        print(link)
        f.write('https://course.mytcas.com'+link + "\n")
        # df = df.append({'Link': 'https://course.mytcas.com'+link}, ignore_index=True)
        # df.to_csv('major_link.csv', index=False)

