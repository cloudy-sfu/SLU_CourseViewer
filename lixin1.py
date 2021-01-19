from math import ceil

import pandas as pd
import requests

chrome87 = {
    "Host": "mcenter.lixin.edu.cn",
    "Connection": "keep-alive",
    "Content-Length": "65",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "DNT": "1",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/87.0.4280.141 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://mcenter.lixin.edu.cn",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://mcenter.lixin.edu.cn/index_sso.jsp",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
}
server_url = "https://mcenter.lixin.edu.cn/r/jd"


class Inquiry:
    def __init__(self, username: str):
        self.username = username

        self.sess = requests.Session()
        self.sess.trust_env = False  # dis-trust system proxies
        self.sess.verify = False
        self.user_info = {
            "userid": username,
            "cmd": "CLIENT_USER_LOGIN",
            "deviceType": "pc",
            "sid": "",
            "lang": "cn",
        }

    def run(self):
        json_response = self.sess.post(server_url, data=self.user_info, headers=chrome87)
        sid = json_response.json()['data']['sid']
        current_page = 1
        inquiry_data = {
            "cmd": "CLIENT_DW_DATA_GRIDJSON",
            "sid": sid,
            "appId": "com.awspaas.user.apps.lixin.studentsystem",
            "pageNow": str(current_page),
            "processGroupId": "obj_1fc62306df7c4024911ff1b3532ac271",
            "dwViewId": "obj_0bbeb4222c314adcb878860d2ae93b3e",
            "limit": "25",
        }
        chrome87_plus = {
            **chrome87,
            "Referer": f"https://mcenter.lixin.edu.cn/r/w?cmd=CLIENT_USER_HOME&sid={sid}"
        }
        response = self.sess.post(server_url, data=inquiry_data, headers=chrome87_plus).json()
        courses = response['data']['maindata']['items']
        total = float(response['data']['maindata']['pageInfo']['total']) / 25
        for current_page in range(2, ceil(total) + 1):
            inquiry_data['pageNow'] = str(current_page)
            response = self.sess.post(server_url, data=inquiry_data, headers=chrome87_plus).json()
            courses += response['data']['maindata']['items']

        df = pd.DataFrame(columns=['semester', 'season', 'course_id', 'name', 'course_type', 'credits',
                                   'score', 'exam_type', 'score_label', 'grade_points', 'create_time'])
        for course in courses:
            df = df.append({
                'semester': course['XN'], 'season': int(course['XQ']), 'course_id': course['KCH'],
                'name': course['KCM'], 'course_type': course['KCLB'], 'credits': float(course['XF']),
                'score': float(course['KSCJ']), 'exam_type': course['KSFS'], 'score_label': course['CJLB'],
                'grade_points': float(course['JD']), 'create_time': pd.to_datetime(course['_CREATEDATE']),
            }, ignore_index=True)
        return df
