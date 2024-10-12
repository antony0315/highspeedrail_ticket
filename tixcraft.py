from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import ddddocr
from datetime import datetime  
import undetected_chromedriver as uc
import time
import re
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed


s = time.time()
driver = uc.Chrome()
driver.get('https://tixcraft.com/activity/detail/25_mogwaitp')

cookie=WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'onetrust-reject-all-handler')))
cookie.click()

element = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/section[2]/div/div[1]/div/ul/li[1]/a"))
)
attribute_value = element.get_attribute("href")

driver.get(attribute_value)




driver.execute_script("document.body.style.transform='scale(0.5)';")

while True:
    try:
        button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='gameList']//button[contains(text(), '立即訂購') and not(./following-sibling::div[contains(text(), '選購一空')])]"))
        )
        button.click()
        if driver.current_url != attribute_value:
            break
    except:
        pass
    
    
seat_area = driver.find_elements(By.CLASS_NAME,'select_form_b')


    
    
seat_info={}

for i in seat_area:
    seat_info[i.find_element(By.TAG_NAME,'a').get_attribute('id')]={}
    try:
        seat_info[i.find_element(By.TAG_NAME,'a').get_attribute('id')]['tag'] = i.find_element(By.TAG_NAME,'a').text
    except:
        seat_info[i.find_element(By.TAG_NAME,'a').get_attribute('id')]['tag'] = ''
    try:
        seat_info[i.find_element(By.TAG_NAME,'a').get_attribute('id')]['price'] = int(re.compile(r'\d{4}\b').findall(i.find_element(By.TAG_NAME,'a').text)[0])
    except:
        seat_info[i.find_element(By.TAG_NAME,'a').get_attribute('id')]['price'] = ''
    

    
seat_info_df = pd.DataFrame.from_dict(seat_info, orient='index') 
seat_info_df.sort_values(by="price",ascending=True,inplace=True) 
seat_id=seat_info_df.head(1).index[0]
 

url_current = driver.current_url
while True:
    try:
        driver.execute_script("document.body.style.transform='scale(0.1)';")
        seat_btn = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID,seat_id))
        )
        if seat_btn:
            seat_btn.click() 
            if driver.current_url != url_current:
                break
    except:
        pass



url_before=driver.current_url

def select_ticket_price(driver, i):
    try:
        ID = str(i // 10) + str(i % 10)
        option = WebDriverWait(driver, 0.1).until(
            EC.presence_of_element_located((By.ID, f'TicketForm_ticketPrice_{ID}'))
        )
        if option:
            select = Select(option)
            select_option = [i.text for i in select.options]
            select.select_by_value(select_option[2])
            return True
    except Exception as e:
        print(e)
        return False


def handle_captcha(driver):
    ocr = ddddocr.DdddOcr()
    screenshot = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, 'TicketForm_verifyCode-image'))
    ).screenshot_as_png
    
    res = ocr.classification(screenshot)
    if len(res) != 4:
        raise ValueError('驗證碼錯誤')
    captcha = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, 'TicketForm_verifyCode'))
    )
    captcha.clear()
    captcha.send_keys(res)

    start = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.ID, 'TicketForm_agree'))
    )
    start.click()
    check = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    check.click()
    return True



while True:
    try:           
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(select_ticket_price, driver, i): i for i in range(20)}
            captcha_future = executor.submit(handle_captcha, driver)
            for future in as_completed(futures):
                if future.result():
                    break  
            captcha_result = captcha_future.result()
            if captcha_result:
                print("驗證碼成功提交！")

        if driver.current_url != url_before:
            break       
    except:
        png = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, 'TicketForm_verifyCode-image'))
        )
        png.click()       

e = time.time()
print(e-s)


googlelogin=WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'loginGoogle')))
googlelogin.click()

email_input=WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'identifierId')))
email_input.send_keys('antony10283')

next_step = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="identifierNext"]/div/button')))
next_step.click()

url_before=driver.current_url

while True:
    try:
        password_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'Passwd')))
        password_input.clear()
        password_input.send_keys("@111185199")
        next_step2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button')))
        next_step2.click()
        if driver.current_url != url_before:
            break    
    except:
        pass
    

other_way = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div[2]/div[2]/div/div/button')))
other_way.click()


url_before=driver.current_url
while True:
    try:
        other_way2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section[2]/div/div/section/div/div/div/ul/li[2]/div/div[2]')))
        other_way2.click()
        if driver.current_url != url_before:
            break    
    except:
        pass
    
url_before=driver.current_url
while True:
    try:
        other_way3 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section[3]/div/div/div[1]/div/div[1]/div/div[1]/input')))
        other_way3.clear()
        other_way3.send_keys("8411490557")

        next_step = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button/span')))
        next_step.click()
        if driver.current_url != url_before:
            break    
    except:
        pass

