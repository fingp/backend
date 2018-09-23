import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import platform
import numpy as np
import time
def login(req):
    start_time = time.time()
    file_path = './apiserver/datas/'
    file_name = file_path + 'chromedriver_' + platform.system().lower()
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    chrome_driver = webdriver.Chrome(file_name, chrome_options=options)
    chrome_driver.implicitly_wait(3)

    chrome_driver.get('https://klas.khu.ac.kr/main/viewMainIndex.do')
    chrome_driver.find_element_by_name("USER_ID").send_keys(req['id'])
    chrome_driver.find_element_by_name('PASSWORD').send_keys(req['pw'])
    chrome_driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/form/div[1]/div[2]/a/img').click()
    html = chrome_driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    def login_sucess():
        login_status = []
        login_status.extend(soup.select('#ui-dialog-title-MESSAGE_BOX'))
        login_status.extend(soup.select('#a'))
        if len(login_status) > 0:
            if soup.select('#ui-dialog-title-MESSAGE_BOX')[0].text == '로그인 에러':
                return 0
        else:
            return 1
    chrome_driver.quit()
    res={ "flag": login_sucess()}
    print("--- %s seconds ---" % (time.time() - start_time))
    return res

def get_assignment(req):
    start_time = time.time()
    class_list = ['SWCON22100','CSE33200','AMTH100112','SWCON30200',
                  'CSE43700','CSE40609','CSE20302']#내 수강리스트 테스트용
    temp = np.char.array('https://klas.khu.ac.kr/course/viewCourseClassroom.do?COURSE_ID=2018_20_')
    class_arr = np.array(class_list)
    class_link = temp + class_arr
    LOGIN_INFO = {
        'USER_ID': req['id'],
        'PASSWORD': req['pw']
    }
    with requests.Session() as s:
        login_req = s.post('https://klas.khu.ac.kr/user/loginUser.do', data=LOGIN_INFO)
        # 어떤 결과가 나올까요? (200이면 성공!)
        print(login_req.status_code)
        if login_req.status_code != 200:
            raise Exception('로그인이 되지 않았어요! 아이디와 비밀번호를 다시한번 확인해 주세요.')
        result_list = []
        online_list = []
        start_time = time.time()
        for i in class_link:
            req = s.get(i)
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')
            class_name = soup.find('div', attrs={'class', 'lf'}).text.strip()
            temp_str = class_name + '\n'
            temp_str2 = class_name + '\n'
            for th in soup.find_all('div', attrs={'class': 'mycl_cont_info'}):
                if th.find('div', attrs={'class': 'mycl_cont_top'}).text.strip() == "과제":
                    for temp in th.find_all('div', attrs={'class': ['mycl_cont_mid', 'mycl_cont_bot']}):
                        temp_str += temp.text.strip()
                        if (temp.select('div')[0].has_attr('id')):
                            temp_str += '\n' + temp.select('div')[0]['id']
                            result_list.append(temp_str)
                            temp_str = class_name + '\n'
                elif th.find('div', attrs={'class': 'mycl_cont_top'}).text.strip() == "강의자료":
                    for temp in th.find_all('div', attrs={'class': ['mycl_cont_mid', 'mycl_cont_bot']}):
                        temp_str2 += temp.text.strip()
                        if (temp.select('div')[0].has_attr('id')):
                            temp_str2 += '\n' + temp.select('div')[0]['id']
                            if (temp.select('div')[0].find('a')):
                                temp_str2 += '\n' + 'https://klas.khu.ac.kr' + temp.select('div')[0].find('a').attrs[
                                    'href']
                            else:
                                temp_str2 += '\n' + 'no_files'
                            online_list.append(temp_str2)
                            temp_str2 = class_name + '\n'
    res = []
    for work in result_list:
        temp = [x for x in work.split('\n') if x]
        if temp[3] == "제출 완료":
            temp.append(1)
        else:
            temp.append(0)
        temp_dict = {
            "workType": "0",
            "workCode": temp[4],
            "workCourse": temp[0],
            "workTitle": temp[1],
            "workTime": temp[2],
            "isSubmit": temp[5],
            "workFile": "[*]no_file"
        }
        res.append(temp_dict)
    for online in online_list:
        temp = [x for x in online.split('\n') if x]
        if len(temp) == 7:
            temp_dict = {
                "workType": "2",  # 2강의자료
                "workCode": temp[5],
                "workCourse": temp[0],
                "workTitle": temp[1],
                "workTime": temp[2],
                "isSubmit": "1",  # 강의자료는 다 제출
                "workFile": temp[4].split(')')[1] + "[*]" + temp[6]
            }
            res.append(temp_dict)
        elif len(temp) == 13:
            ing_time = temp[5].split(':')[1].split('/')[0]
            watch_time = 0
            if "분" in ing_time:
                watch_time += int(ing_time.split("분")[0]) * 60
            else:
                watch_time += int(ing_time.split("초")[0])
            course_time = int(temp[3].split(':')[1].split("분")[0]) * 60
            if watch_time > course_time:
                flag = 1
            else:
                flag = 0
            temp_dict = {
                "workType": "1",  # 1인강
                "workCode": temp[11],
                "workCourse": temp[0],
                "workTitle": temp[1],
                "workTime": temp[2],
                "isSubmit": flag,  # 강의자료는 다 제출
                "workFile": temp[10].split(')')[1] + "[*]" + temp[12]
            }
            res.append(temp_dict)
        else:
            print('ERROR')
    print("--- %s seconds ---" % (time.time() - start_time))
    return res