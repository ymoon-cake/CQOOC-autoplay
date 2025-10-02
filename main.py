from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from os import system
from datetime import datetime
from function.netCheck import check_network
from function.Login import login
from function.CreateCourseList import get_course_list

print('\033[1;33m注意：本程序只适用于重庆高等教育智慧教育平台\033[0m')
print('\033[31m本程序没有答题、讨论功能\033[0m')
print('github页面：https://github.com/ymoon-cake/CQOOC-autoplay')
print('本程序不可用于商业目的')

print('正在检查网络……')
if check_network():
    print('网络连接成功')
else:
    print('网络连接失败，请联网')

URL = input('请在此处粘贴“课程学习”页面网址：')
USERNAME = input('请输入用户名：')
PASSWORD = input('请输入密码：')
POWEROFF = input('完成后关机？(y/n)：').lower()
LOG_TIME = datetime.now().strftime('%Y%m%d_%H%M%S')

driver = webdriver.Edge()
driver.set_page_load_timeout(30)
try:
    driver.get(URL)
except TimeoutException:
    driver.execute_script('window.stop();')
driver.set_page_load_timeout(300)   # 防止刷新超时

def find_and_click_chapter(chapter):
    try:
        course = WebDriverWait(driver, timeout=180).until(
            lambda d: d.find_element(By.XPATH, f"//p[text()='{chapter}']")
        )

        if is_complete(course):  # 判断是否已经完成
            print(f'{chapter}已学完，跳过')
            return 'jump'

        driver.execute_script("arguments[0].click();", course)
        title = WebDriverWait(driver, timeout=180).until(
            EC.element_to_be_clickable((By.XPATH, '//p[@data-v-5491f82c]'))
        )
        # 消除空格
        title_name, course_name = title.text.replace(" ", ""), chapter.replace(' ', '')
        # 检查是否成功切换
        while course_name != title_name and course_name not in title_name and title_name not in course_name:
            print(f'当前课件 {title_name} 与应看课件 {course_name} 不符，正在切换')
            driver.execute_script("arguments[0].click();", course)  # 使用JavaScript点击，避免隐藏元素点击失败
            sleep(2)
            title = WebDriverWait(driver, timeout=180).until(
                EC.element_to_be_clickable((By.XPATH, '//p[@data-v-5491f82c]'))
            )
            title_name = title.text.replace(' ', '')
        print('成功，判断课件类型')
    except TimeoutException:
        print('加载失败，请检查网络')

def judge_type(chapter):
    print(f'判断{chapter}')
    try:  # 如果是视频
        video = WebDriverWait(driver, timeout=35).until(
            lambda d: d.find_element(By.TAG_NAME, 'video')
        )
        print('是视频，点击播放按钮')
        button = WebDriverWait(driver, timeout=60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.dplayer-icon > svg'))
        )
        button.click()
        print('点击成功，开始播放')
        print('设置二倍速')
        set_double_speed()
        print('设置成功')

        try:
            while True:
                if driver.execute_script('return arguments[0].ended;', video):
                    print('播放完毕')
                    break

                if driver.execute_script('return arguments[0].paused;', video):
                    print('检测到视频暂停')
                    button = WebDriverWait(driver, timeout=60).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '.dplayer-icon > svg'))
                    )
                    button.click()
                    print('已恢复播放')
                    sleep(2)

                sleep(1)

        except StaleElementReferenceException:
            print('页面已更改，正在返回')
            find_and_click_chapter(chapter)
            judge_type(chapter)

    except TimeoutException:
        if check_network():
            flag = driver.find_elements(By.XPATH, "//div[@data-v-5491f82c and contains(text(), '完成倒计时')]")
            if flag:
                count_down_element = driver.find_element(By.XPATH, "//div[@data-v-5491f82c and contains(text(), '完成倒计时')]")
                count_down = count_down_element.text.split('：')
                count_down = int(count_down[1][:-1])
                sleep(count_down)
            print('是PPT，已等待')
        else:
            print('\033[31m网络已断开\033[0m')

def set_double_speed():
    button = driver.find_element(By.XPATH, "//div[@data-speed='2']")
    driver.execute_script('arguments[0].click()', button)

def is_complete(course):
    try:
        icon_element = course.find_element(By.XPATH, "./following-sibling::div[@class='complate-icon']//img")
        if icon_element.get_attribute('src') == "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAfhJREFUSEu9lj1oE2EYx//PqaDYDJHaQlCoH7k4dVYuUMFFERSHQIeCUcxiih/QpXS4u9Gp9MNJwSWC4CAKKgiClgSLg4hkMIkBISFrhwhKPu4p7zWXz7vLXWjMmPd5/r/3+XyP4PKbVS+e+Cc1rsPgqyCcARBqmVfAKEKit4eNg69/6J/KTjJkdxBRlRATdGbcAviA2yUAahLhGTHUnJ6p9NsOACKqco2BFIMD7sK9pwSqErCQ0zNvuk96AGEteg8wVsGQ/Ii3bQkGID0saOl16782QNzcIH41snhH0ZCYbliRmAAz58BPv2lxLqyZrnOiJiZA1pQnzHxnpLQ4OBHR07yWSZBoxb+o/x7eLX7x1DyCQzMk69EkG8amX3cv9iRJiySryjsGX/Hi0G8zHZhEeOo00sWvtu4Eek+ypuSYWfYLOHv8FFLxDRw7GsSltRhKOwMzBiLKC0CVmSf8ALrFPxe+IPF8yT4Coj+ugNsX5vGtlMX3crYt0C9+98Uy6s26K8A2RSeDIXy8/xK1Rg1CZOvXNvyIC+JeilyKvHL5AW6ej5mQRx8eIzkXN3Mu0uJ2885QiyIPaVMLYjl5FTcjEG3qZdAsiB9xscbNQfO6KkRN7FrRcR9Zq+K/LLsWZHzr2gpzrA+OBRnrk9kFGd+j390V+/HZsgvSIhcecicecAAAAABJRU5ErkJggg==":
            return True
        else:
            return False
    except NoSuchElementException:
        # 有些课件没有图标
        return False

def write_error(e, chapter):
    file_name = f'error_{LOG_TIME}.log'
    information = f'{chapter} 学习失败，错误原因：\n{e}\n\n'
    with open(file_name, 'a', encoding='utf-8') as f:
        f.write(information)

    return file_name

def main():

    print('开始登录')
    login(driver, USERNAME, PASSWORD)
    print('登录成功')

    chapters = get_course_list(driver, URL, USERNAME, PASSWORD)

    error = []
    for chapter in chapters:
        try:
            # 点击视频/课件
            print(f'查找并点击{chapter}')
            if find_and_click_chapter(chapter) == 'jump':
                continue
            # 判断类型
            judge_type(chapter)
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
            print(f'\033[31m发生错误{e}，\n{chapter}将在之后重试\033[0m')
            log_name = write_error(e, chapter)
            print(f'事件已写入到日志 {log_name}')
            error.append(chapter)


    timeout = 3 # 防止无限循环
    while error and timeout > 0:
        for chapter in error:
            try:
                print(f'重试{chapter}')
                print(f'查找并点击{chapter}')
                if find_and_click_chapter(chapter) == 'jump':
                    continue
                # 判断类型
                judge_type(chapter)
                error.remove(chapter)
            except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
                print(f'\033[31m发生错误{e}，\n{chapter}将在之后重试\033[0m')
                log_name = write_error(e, chapter)
                print(f'事件已写入到日志 {log_name}')
        timeout -= 1

    print(f'总共学习了{len(chapters)}个课件，其中{len(error)}个课件学习失败：')
    for i in error:
        print(i)

    driver.quit()



if __name__ == '__main__':
    main()
    print('程序运行完毕')
    if POWEROFF == 'y':
        for i in range(11, 0, -1):
            print(f'\033[31m{i}秒后自动关机，你可以按Ctrl+C取消\033[0m')
            sleep(i)
        system('shutdown /s /t 0')
