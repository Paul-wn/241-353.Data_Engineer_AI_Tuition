from playwright.sync_api import sync_playwright
import bs4 as bs
import pandas as pd
import time 
import requests

df = pd.read_csv('major_link.csv')
data = pd.DataFrame(columns=['มหาวิทยาลัย', 'คณะ', 'สาขา', 'หลักสูตร' , 'หลักสูตรEng', 'ประเภทหลักสูตร', 'วิทยาเขต', 'ค่าใช้จ่าย'])
def parser(link ,df):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(link)
        page.wait_for_load_state('networkidle')  # รอให้โหลดเสร็จ
        html = page.content()
        soup = bs.BeautifulSoup(html, 'html.parser')
        span = soup.find('span', class_='name')
        name = span.find('a').text

        small = span.find('small')
        major_tag = small.find_all('a')
        major , specific = major_tag

        details = soup.find('dl')
        # head = details.find_all('dt')
        description = details.find_all('dd')

        new_data = pd.DataFrame({
                'มหาวิทยาลัย': [name.strip() if name else ''],
                'คณะ': [major.text.strip() if major else ''],
                'สาขา': [specific.text.strip() if specific else ''],
                'หลักสูตร': [description[0].text.strip() if len(description) > 0 else ''],
                'หลักสูตรEng': [description[1].text.strip() if len(description) > 1 else ''],
                'ประเภทหลักสูตร': [description[2].text.strip() if len(description) > 2 else ''],
                'วิทยาเขต': [description[3].text.strip() if len(description) > 3 else ''],
                'ค่าใช้จ่าย': [description[4].text.strip() if len(description) > 4 else '']
            })
            
            # รวม DataFrame
        data = pd.concat([df, new_data], ignore_index=True)
        browser.close()

        return data
    
for i in df['link']:
    data = parser(i, data)
    print('success')

data.to_csv('Tuition.csv', index=False)