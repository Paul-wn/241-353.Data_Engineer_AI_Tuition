from playwright.sync_api import sync_playwright
import bs4 as bs
import pandas as pd
import time 
import requests
import re

df = pd.read_csv('..\data\major_link.csv')
data = pd.DataFrame(columns=['มหาวิทยาลัย', 'หลักสูตร' , 'หลักสูตรEng', 'ประเภทหลักสูตร', 'วิทยาเขต', 'ค่าใช้จ่าย'])
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
        majors = span.find('small')
        major , specific = majors.find_all('a')
        dl = soup.find('dl')
        data = {
            'มหาวิทยาลัย': name.strip(),
            'คณะ': major.text.strip(),
            'สาขา': specific.text.strip(),
            'หลักสูตร': '',
            'หลักสูตรEng': '',
            'ประเภทหลักสูตร': '',
            'วิทยาเขต': '',
            'ค่าใช้จ่าย': ''
        }

        # วนลูปดู dt และ dd คู่กัน
        dts = dl.find_all('dt')
        dds = dl.find_all('dd')

        for dt, dd in zip(dts, dds):
            title = dt.get_text(strip=True)
            value = dd.get_text(strip=True)

            if title == 'ชื่อหลักสูตร':
                data['หลักสูตร'] = value
            elif title == 'ชื่อหลักสูตรภาษาอังกฤษ':
                data['หลักสูตรEng'] = value
            elif title == 'ประเภทหลักสูตร':
                data['ประเภทหลักสูตร'] = value
            elif title == 'วิทยาเขต':
                data['วิทยาเขต'] = value
            elif title == 'ค่าใช้จ่าย':
               data['ค่าใช้จ่าย'] = value

                    

        new_data = pd.DataFrame([data])
            
            # รวม DataFrame
        data = pd.concat([df, new_data], ignore_index=True)
        browser.close()

        return data
    
for i in df['link']:
    data = parser(i, data)
    print('success')

data.to_csv('raw.csv', index=False)