from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import ddddocr
from datetime import datetime  
import undetected_chromedriver as uc


def order_info_flow(driver,ticket_count:str,startStation:str,destination:str,order_date:str,toTime:str):
    searchTime=str(int(toTime[:2])-2).zfill(2)+':'+'00'
    try:
        cookie_btn = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div[3]/div/div/button')))
        cookie_btn.click()
    except:
        pass
    #訂票數量
    select_element=WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/main/section/div/div/form/div[5]/div/div[1]/div/select')))
    select_element=Select(select_element)
    select_element.select_by_visible_text(ticket_count)
    #出發站
    select_element=WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/main/section/div/div/form/div[4]/div[1]/div/div[1]/div/select')))
    select_element=Select(select_element)
    select_element.select_by_visible_text(startStation)
    #抵達站
    select_element=WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/main/section/div/div/form/div[4]/div[1]/div/div[3]/div/select')))
    select_element=Select(select_element)
    select_element.select_by_visible_text(destination)
    #日期
    js='document.getElementsByClassName("uk-input")[0].removeAttribute("readonly");'
    driver.execute_script(js)
    driver.execute_script("document.getElementById('toTimeInputField').value = arguments[0];", order_date)
    #時間
    select_element=WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/main/section/div/div/form/div[4]/div[2]/div/div[2]/div[1]/select')))
    select_element=Select(select_element)
    select_element.select_by_visible_text(searchTime)
 
    while True:
        with open('captcha.png', 'wb') as f:
            f.write(WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/main/section/div/div/form/div[6]/div[2]/div/img'))).screenshot_as_png)
        ocr=ddddocr.DdddOcr()
        with open('captcha.png', 'rb') as f:
            img=f.read()
        res=ocr.classification(img)
        captcha=WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/main/section/div/div/form/div[6]/div[2]/div/input')))
        captcha.send_keys(res)
        start=WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/main/section/div/div/form/input')))
        start.click()
        if driver.current_url == "https://irs.thsrc.com.tw/IMINT/?wicket:interface=:1::":
            break       
    return None


 
def complete_order(driver,orderID:str,phone:str,email:str,toTime:str,ticket_count:str,*args):   
    elements = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.ID, 'QueryArrival'))
    )
    time_list=[datetime.strptime(i.text,'%H:%M') for i in elements]
    time_diff=max([time for time in time_list if time < datetime.strptime(toTime,'%H:%M')])
    time_choose=str(time_diff.hour).zfill(2)+':'+str(time_diff.minute).zfill(2)
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f"[queryarrival='{time_choose}']"))
    )
    element.click()
    confirm_button=WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "SubmitButton"))
    )
    confirm_button.click()
    order_id_input=WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "dummyId"))
    )
    order_id_input.send_keys(orderID)
    order_phone_input=WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "dummyPhone"))
    )
    order_phone_input.send_keys(phone)
    order_email_input=WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, 'email'))
    )
    order_email_input.send_keys(email)
    
    try:
        for num,psg_id in enumerate(args[:int(ticket_count)]):
            passsenger_id_input_name = f"TicketPassengerInfoInputPanel:passengerDataView:{num}:passengerDataView2:passengerDataIdNumber"
            passsenger_id_input=WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.NAME, passsenger_id_input_name))
            )
            passsenger_id_input.send_keys(psg_id)
    except:
        pass
    
    
    try:
        member_check = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "memberSystemRadio1")))
        member_check.click()
    except:
        pass

    try:
        member_check2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "memberShipCheckBox")))
        member_check2.click()
    except:
        pass

    try:
        check_box=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "agree")))
        check_box.click()
    except:
        pass
    
    submit=WebDriverWait(driver, 20).until(
          EC.presence_of_element_located((By.ID, "isSubmit"))
      )
    submit.click()
    
    submit2=WebDriverWait(driver, 20).until(
          EC.presence_of_element_located((By.NAME, "SubmitButton"))
    )
    submit2.click()
    try:
        submit=WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/div/div[2]/input[2]"))
        )
        submit.click()
    except:
        pass
    try:
        second_check=WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/div/div[2]/input"))
        )
        second_check.click()
    except:
        pass



if __name__=='__main__':
    ticket_count='1'
    startStation="台中"
    destination="台北"
    order_date="2024/08/20"
    toTime="08:40"
    orderID="L123456789"
    psgID="L123456789","L123456788"
    phone="0981064195"
    email="antony10283@gmail.com"
    driver=uc.Chrome()
    driver.get('https://irs.thsrc.com.tw/IMINT/?locale=tw')
    order_info_flow(driver,ticket_count,startStation,destination,order_date,toTime)
    complete_order(driver,orderID,phone,email,toTime,ticket_count,*psgID)
    
    
    
    
    
    
    
   






    
