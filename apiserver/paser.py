import requests
from bs4 import BeautifulSoup
import numpy as np
from . import models

def login(req):
    LOGIN_INFO = {
        'USER_ID': req['id'],
        'PASSWORD': req['pw']
    }
    with requests.Session() as s:
        login_req = s.post('https://klas.khu.ac.kr/user/loginUser.do', data=LOGIN_INFO)
        # 어떤 결과가 나올까요? (200이면 성공!)
        print(login_req.status_code)
        if login_req.status_code != 200:
            #raise Exception('페이지 로딩 실패' + str(login_req.status_code))
            flag = 0;
        else : # 로그인 성공문
            if len(s.cookies) == 1:
                #raise Exception('로그인 실패')
                flag = 0;
            else:
                user_set = models.UserTb.objects.filter(klas_id=req['id'])
                if not user_set.exists(): #존재하지 않을시
                    req = s.get('https://klas.khu.ac.kr/classroom/viewClassroomCourseMoreList.do?courseType=ing')
                    html = req.text
                    soup = BeautifulSoup(html, 'html.parser')
                    class_list = ''
                    table_body = soup.find('tbody')
                    rows = table_body.find_all('tr')
                    if rows[0].text.strip() != "데이터가 존재하지 않습니다.":
                        for row in rows:
                            class_list += row.find_all('td')[1].text.strip().split('[')[1].split(']')[0] + ','
                    user = models.UserTb( klas_id=LOGIN_INFO['USER_ID'], class_2018_2=class_list)
                    user.save()
                flag=1;
    res = {"flag": flag}
    return res
'''
def get_classlist(req):
    LOGIN_INFO = {
        'USER_ID': req['id'],
        'PASSWORD': req['pw']
    }
    with requests.Session() as s:
        login_req = s.post('https://klas.khu.ac.kr/user/loginUser.do', data=LOGIN_INFO)
        # 어떤 결과가 나올까요? (200이면 성공!)
        print(login_req.status_code)
        if login_req.status_code != 200:
            raise Exception('홈페이지 오류')
        req = s.get('https://klas.khu.ac.kr/classroom/viewClassroomCourseMoreList.do?courseType=ing')
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        class_list = []
        table_body = soup.find('tbody')
        rows = table_body.find_all('tr')
        if rows[0].text.strip() != "데이터가 존재하지 않습니다.":
            for row in rows:
                class_list.append(row.find_all('td')[1].text.strip().split('[')[1].split(']')[0])
'''
def get_assignment(req):
    user_set = models.UserTb.objects.get(klas_id=req['id'])
    class_list=str(user_set.class_2018_2).split(',')
    class_list.pop()
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
            raise Exception('홈페이지 오류')
        result_list = []
        online_list = []
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
                                temp_str2 += '\n' + 'https://klas.khu.ac.kr' + temp.select('div')[0].find('a').attrs['href'].split("..")[1]
                            else:
                                temp_str2 += '\n' + 'no_files'
                            online_list.append(temp_str2)
                            temp_str2 = class_name + '\n'

    def check_time(str_):
        if str_ == "기간없음":
            return [0, 0]
        else:
            return str_.split(' - ')
    res = []
    for work in result_list:
        temp = [x for x in work.split('\n') if x]
        if temp[3] == "제출 완료":
            temp.append(1)
        else:
            temp.append(0)
        create_time, finish_time = check_time(temp[2].split("기간:")[1])
        temp_dict = {
            "workType": "0",
            "workCode": temp[4],
            "workCourse": temp[0],
            "workTitle": temp[1],
            "workCreateTime": create_time,
            "workFinishTime": finish_time,
            "isSubmit": temp[5],
            "workFile": "[*]no_file"
        }
        res.append(temp_dict)
    for online in online_list:
        temp = [x for x in online.split('\n') if x]
        if len(temp) == 7:
            create_time, finish_time = check_time(temp[2].split("기간:")[1])
            temp_dict = {
                "workType": "2",  # 2강의자료
                "workCode": temp[5],
                "workCourse": temp[0],
                "workTitle": temp[1],
                "workCreateTime": create_time,
                "workFinishTime": finish_time,
                "isSubmit": "1",  # 강의자료는 다 제출
                "workFile": temp[4].split(')')[1] + "[*]" + temp[6]
            }
            res.append(temp_dict)
        elif len(temp) == 13:
            create_time, finish_time = check_time(temp[2].split("기간:")[1])
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
                "workCreateTime": create_time,
                "workFinishTime": finish_time,
                "isSubmit": flag,  # 강의자료는 다 제출
                "workFile": temp[10].split(')')[1] + "[*]" + temp[12]
            }
            res.append(temp_dict)
        else:
            print('ERROR')
    return res