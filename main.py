#! /usr/bin/env python3

import time
import json
import base64
import requests
import traceback

from mail import send_mail
import vruc

# import logging
# import http.client as http_client
# http_client.HTTPConnection.debuglevel = 1

# # You must initialize logging, otherwise you'll not see debug output.
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

prolog = """
<html lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
</head>
<body>
<style>
table, th, td {
  border:1px solid black;
}
</style>
<table>
<tr>
<th>课程</th>
<th>学分</th>
<th>绩点</th>
<th>平时成绩</th>
<th>期末成绩</th>
<th>总成绩</th>
</tr>
"""
epilog = "</table>\r\n</body>\r\n</html>\r\n"


def main():
    course_data = {}
    vruc_cookie = input('JS cookie: ')
    # php_session = input('session: ')
    # if php_session:
    #     vruc_cookie = vruc_cookie + '; session=' + php_session

    try:
        while True:
            with requests.session() as session:
                vruc.checkvrucLogin(vruc_cookie, session)

                with session.get(
                    'https://v.ruc.edu.cn/oauth2/authorize?response_type=code&scope=all&state=yourstate&client_id=5d25ae5b90f4d14aa601ede8.ruc&redirect_uri=http://jw.ruc.edu.cn/secService/oauthlogin',
                    allow_redirects=True
                ) as req:
                    print(req.url)
                    assert 'jw.ruc.edu.cn/Njw2017/index.html' in req.url, "API changed"

                token: str = session.cookies.get('token')

                exp_time = json.loads(
                    base64.b64decode(token.split('.')[1]))['exp']

                session.cookies.set('token', '', domain='jw.ruc.edu.cn')
                print(session.cookies.get_dict('jw.ruc.edu.cn'))

                # while time.time() < exp_time:
                with session.post(
                    "https://jw.ruc.edu.cn/resService/jwxtpt/v1/xsd/cjgl_xsxdsq/findKccjList?resourceCode=XSMH0507&apiCode=jw.xsd.xsdInfo.controller.CjglKccjckController.findKccjList",
                    json={
                        "pyfa007id": "1",
                        "jczy013id": [],
                        "fxjczy005id": "",
                        "cjckflag": "xsdcjck",
                        "page": {
                            "pageIndex": 1,
                            "pageSize": 500,
                            "orderBy": "[{\"field\":\"jczy013id\",\"sortType\":\"asc\"}]",
                            "conditions": "QZDATASOFTJddJJVIJY29uZGl0aW9uR3JvdXAlMjIlM0ElNUIlN0IlMjJsaW5rJTIyJTNBJTIyYW5kJTIyJTJDJTIyY29uZGl0aW9uJTIyJTNBJTVCJTVEJTdEyTTECTTE"
                        }
                    },
                    headers={'token': token,
                             "accept": "application/json, text/plain, */*",
                             "userrolecode": "student"}
                ) as req:
                    if req.status_code == 200:
                        data = req.json()
                    else:
                        time.sleep(30)
                        continue

                updated = []

                if data['errorCode'] != 'success':
                    send_mail('ERROR', str(data))
                else:
                    for course in data['data']:
                        xnxq: str = course['xnxq']
                        kcname: str = course['kcname']
                        xf: int = course['xf']
                        jd: float = course['jd']
                        score: int = course['zcj']
                        score1: str = course['cjxm1']
                        score2: str = course['cjxm3']

                        if kcname:
                            course_id = xnxq + '-' + kcname
                            course_value = "<td>{}</td>\r\n<td>{}</td>\r\n<td>{}</td>\r\n<td>{}</td>\r\n<td>{}</td>\r\n".format(
                                xf,
                                jd or xf,
                                score1 or 'null',
                                score2 or 'null',
                                score or 'null')

                            if course_data.get(course_id, None) != course_value:
                                course_data[course_id] = course_value
                                updated.append('<tr>\r\n<td>{}</td>\r\n{}</tr>\r\n'.format(
                                    course_id, course_value))

                if updated:
                    send_mail('成绩更新', prolog +
                              '\r\n'.join(updated)+epilog, 'html')

                time.sleep(300)
    except Exception as e:
        send_mail('发生错误', '\n'.join(traceback.format_exception(e)))
        raise


if __name__ == '__main__':
    main()
