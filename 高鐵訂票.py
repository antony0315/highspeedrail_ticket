from selenium import webdriver
from selenium.webdriver.support.ui import Select
import ddddocr
from datetime import datetime  
import time



def order_info_flow(ticket_count:str,startStation:str,destination:str,order_date:str,toTime:str):
    searchTime=str(int(toTime[:2])-2).zfill(2)+':'+'00'
    driver.get('https://irs.thsrc.com.tw/IMINT/?locale=tw')
    try:
        driver.find_element_by_id('cookieAccpetBtn').click()
    except:
        pass
    select_element=driver.find_element_by_name('ticketPanel:rows:0:ticketAmount')
    select_element=Select(select_element)
    select_element.select_by_visible_text(ticket_count)
    select_element=driver.find_element_by_name('selectStartStation')
    select_element=Select(select_element)
    select_element.select_by_visible_text(startStation)
    select_element=driver.find_element_by_name('selectDestinationStation')
    select_element=Select(select_element)
    select_element.select_by_visible_text(destination)
    js='document.getElementsByClassName("uk-input")[0].removeAttribute("readonly");'
    driver.execute_script(js)
    driver.execute_script("document.getElementById('toTimeInputField').value = arguments[0];", order_date)
    select_element=driver.find_element_by_name('toTimeTable')
    select_element=Select(select_element)
    select_element.select_by_visible_text(searchTime)
    with open('captcha.png', 'wb') as f:
        f.write(driver.find_element_by_id('BookingS1Form_homeCaptcha_passCode').screenshot_as_png)
    ocr=ddddocr.DdddOcr()
    with open('captcha.png', 'rb') as f:
        img=f.read()
    res=ocr.classification(img)
    captcha=driver.find_element_by_name('homeCaptcha:securityCode')
    captcha.send_keys(res)
    start=driver.find_element_by_id("SubmitButton")
    start.click()
    if driver.current_url == "https://irs.thsrc.com.tw/IMINT/?locale=tw":
        raise ValueError('失敗')
    return None



def retry_function(func, max_attempts=10, delay=1):
    try:
        return func
    except Exception as e:
        if max_attempts > 1:
            print(f"Attempt failed: {e}. Retrying...")
            time.sleep(delay)
            return retry_function(func, max_attempts - 1, delay)
        else:
            print("Max attempts reached. Failed to execute function.")
            raise
            



 
def complete_order(orderID:str,phone:str,email:str,toTime:str,*args):   
    time_list=[datetime.strptime(i.text,'%H:%M') for i in driver.find_elements_by_id('QueryArrival')]
    time_diff=max([time for time in time_list if time < datetime.strptime(toTime,'%H:%M')])
    time_choose=str(time_diff.hour).zfill(2)+':'+str(time_diff.minute).zfill(2)
    element = driver.find_element_by_css_selector(f"[queryarrival='{time_choose}']")
    element.click()
    confirm_button=driver.find_element_by_name("SubmitButton")
    confirm_button.click()
    order_id_input=driver.find_element_by_name("dummyId")
    order_id_input.send_keys(orderID)
    order_phone_input=driver.find_element_by_name("dummyPhone")
    order_phone_input.send_keys(phone)
    order_email_input=driver.find_element_by_name('email')
    order_email_input.send_keys(email)
    try:
        for num,psg_id in enumerate(args):
            passsenger_id_input=driver.find_element_by_name(f"TicketPassengerInfoInputPanel:passengerDataView:{num}:passengerDataView2:passengerDataIdNumber")
            passsenger_id_input.send_keys(psg_id)
    except:
        pass
    check_box=driver.find_element_by_name("agree")
    check_box.click()
    submit=driver.find_element_by_id("isSubmit")
    submit.click()
    try:
        submit=driver.find_element_by_xpath("/html/body/div[7]/div/div[2]/input[2]")
        submit.click()
    except:
        pass
    try:
        second_check=driver.find_element_by_xpath("/html/body/div[7]/div/div[2]/input")
        second_check.click()
    except:
        pass




if __name__=='__main__':
    path=r"C:\Users\anton\OneDrive\桌面\chromedriver.exe"
    option=webdriver.ChromeOptions()
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option("useAutomationExtension",False)
    option.add_argument('--disable-blink-features=AutomationControlled')
    ticket_count='2'
    startStation="台中"
    destination="桃園"
    order_date="2024/05/01"
    toTime="08:40"
    orderID="L125454219"
    psgID="L125454219","L123456789"
    phone="0981064195"
    email="antony10283@gmail.com"
    driver=webdriver.Chrome(path,options=option)
    retry_function(order_info_flow(ticket_count,startStation,destination,order_date,toTime),10,1)
    complete_order(orderID,phone,email,toTime,psgID)
    
    
    




