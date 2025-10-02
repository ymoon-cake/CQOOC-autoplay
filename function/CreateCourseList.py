from selenium.webdriver.common.by import By
from time import sleep
from os import getcwd

def get_course_list(driver, url, username, password):
    course_id = url[url.index('=') + 1:]
    print(f'课程id={course_id} 正在查找本地目录', getcwd()+fr'\course\{course_id}.txt')
    try:
        with open(f'course/{course_id}.txt', 'r', encoding='utf-8') as f:
            course_list = [c.rstrip('\n') for c in f.readlines()]
        if course_list[0]:
            print('文件有效')
    except FileNotFoundError or IndexError:
        print('文件无效')
        print('正在联网获取课程目录……')
        sleep(3)
        print('开始收集课程目录')
        course_list = driver.find_elements(By.CSS_SELECTOR, 'p.title[data-v-4b743227]')
        course_list = [text for c in course_list if (text := c.get_attribute('textContent')) and text.strip() and not any(kw in text for kw in ['测验', '考试', '讨论'])]

        print('写入磁盘……')
        with open(f'course/{course_id}.txt', 'w+', encoding='utf-8') as f:
            for c in course_list:
                f.write(c + '\n')
        print('写入成功')

    print('课程目录收集完毕')
    return course_list