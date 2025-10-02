from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def login(driver, username, password):
    print('正在输入用户名')
    username_input = WebDriverWait(driver, timeout=10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.username-box > .ant-input'))
    )
    username_input.send_keys(username)
    print('用户名输入成功')
    print('正在输入密码')
    password_input = WebDriverWait(driver, timeout=10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.password-box > .ant-input'))
    )
    password_input.send_keys(password)
    print('点击登录按钮')
    button = WebDriverWait(driver, timeout=10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.submit-btn'))
    )
    driver.execute_script('arguments[0].click()', button)
    print('点击成功')

    try:
        WebDriverWait(driver, timeout=5).until(
            lambda d:d.find_element(By.XPATH, "//span[text()='登录成功']")
        )
        sleep(5)
        print('刷新页面')
        driver.refresh()
        print('刷新成功')
    except TimeoutException:
        print('\033[31mERROR: 用户名或密码错误\033[0m')
        quit()