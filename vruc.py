#! /usr/bin/env python3

import requests

def checkvrucLogin(cookie: str, session: requests.Session):
    print(cookie)
    for item in cookie.split(';'):
        item = item.strip()
        key, val = item.split('=')
        session.cookies.set(key, val, domain='v.ruc.edu.cn')

    with session.get('https://v.ruc.edu.cn') as req:
        assert req.url == 'https://v.ruc.edu.cn/v1me/', "VRUC login failed"
