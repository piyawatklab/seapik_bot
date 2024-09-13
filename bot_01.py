from seleniumbase import Driver

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
import requests

import pandas as pd

df = pd.read_excel('order.xlsx')
data_dict = df[['Word']].to_dict(orient='records')

def send_chat_simple(message):

    try:
        
        # Line Notify
        url = 'https://notify-api.line.me/api/notify'
        token = 'H3ovLE2Wphr9cH0OdrQDhGD9JGQduNnqHDA29oYOlZm'
        headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
        r = requests.post(url, headers=headers, data = {'message':message})
        
    except:
        pass

def run():
    driver = Driver(uc=True)
    for item in data_dict :
        val = {}
        val['word'] = item['Word']

        url = 'https://seapik.com/ai-writer/essay-writer'
        driver.get(url)

        max_time_login = 5
        time_login = 0

        while time_login < max_time_login:
            try:
                login_button = driver.find_elements(By.XPATH, "//button[text()='Log in']")
                if len(login_button) == 0 :
                    
                    textarea = driver.find_elements(By.XPATH, "//textarea")
                    textarea[0].click()
                    textarea[0].clear()
                    textarea[0].send_keys(item['Word'])

                    generate_button = driver.find_elements(By.XPATH, "//span[text()='Generate']")
                    generate_button[0].click()

                    max_retries = 10  # จำนวนครั้งสูงสุดที่อนุญาตให้วนลูป
                    attempts = 0
                    
                    while attempts < max_retries:
                        try:
                            # ใส่โค้ดที่อาจเกิด error ตรงนี้
                            word_button = driver.find_elements(By.XPATH, "//button[text()='Word']")
                            word_button[0].click()
                            
                            output = driver.find_elements(By.XPATH, "//div[contains(@class, '_6ntrmu') and contains(@class, '_183nv7n') and contains(@class, '_hssrob') and contains(@class, '_l4ow3k') and contains(@class, '_1qtlxb5') and contains(@class, 'astro-6nrxhj4w')]")
                            # print(output[0].text)

                            print("บันทึกเรียบร้อย")
                            break  # ถ้ารันสำเร็จจะหลุดลูปทันที
                        except Exception as e:
                            attempts += 1
                            print(f"เกิดข้อผิดพลาด: {e}")
                            print(f"รอสักครู่... (รอบที่ {attempts})")
                            time.sleep(3)
                    else:
                        # ถ้าวนครบ 10 รอบแล้วไม่สำเร็จ ให้แสดง error ใหม่
                        print("เกิดข้อผิดพลาด: ไม่สามารถรันได้สำเร็จหลังจากพยายาม 10 ครั้ง")
                        
                    break
                
                else :
                    time_login += 1
                    # print(f"เกิดข้อผิดพลาด: {e}")
                    print(f"กรุณา Log in เข้าสู้ระบบ... (รอบที่ {time_login})")
                    time.sleep(60)

            except Exception as e:
                time_login += 1
                # print(f"เกิดข้อผิดพลาด: {e}")
                print("เกิดข้อผิดพลาด")
                driver.quit()

        else:
            # ถ้าวนครบ 10 รอบแล้วไม่สำเร็จ ให้แสดง error ใหม่
            print(f"เกิดข้อผิดพลาด: ไม่สามารถรันได้สำเร็จหลังจากพยายาม {max_time_login} ครั้ง")
            driver.quit()

if __name__ == "__main__":
    
    run()