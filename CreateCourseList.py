from selenium.webdriver.common.by import By
from time import sleep

def get_course_list(driver):
    print('正在获取课程目录……')
    sleep(3)

    print('开始收集课程目录')
    course_list = driver.find_elements(By.CSS_SELECTOR, 'p.title[data-v-4b743227]')
    course_list = [course for course in course_list if (text := course.get_attribute('textContent')) and not any(kw in text for kw in ['测验', '考试', '讨论'])]
    print('课程目录收集完毕')

    return course_list