#! /usr/bin/env python3

import json
import base64
import requests

from io import BytesIO
from PIL import Image

import config

iframe_pattern = '<iframe id="login-iframe" src="'
csrf_pattern = 'name="csrftoken" value="'

def checkvrucLogin(session: requests.Session) -> bool:
    with session.get('https://v.ruc.edu.cn') as req:
        return 'v.ruc.edu.cn/v1me' in req.url

def vrucLogin(username: str, password: str, session: requests.Session, captcha_retry_limit: int = 3):
    with session.get('https://v.ruc.edu.cn', allow_redirects=True) as req:
        text = req.text
        iframeURLBegin = text.find(iframe_pattern) + len(iframe_pattern)
        iframeURLEnd = text.find('"', iframeURLBegin)
        iframeURL = text[iframeURLBegin:iframeURLEnd]

    with session.get(f'https://v.ruc.edu.cn{iframeURL}', allow_redirects=True) as req:
        text = req.text
        csrfPos = text.find(csrf_pattern) + len(csrf_pattern)
        csrfEndPos = text.find('"', csrfPos)
        token = text[csrfPos:csrfEndPos]
    
    for ind in range(captcha_retry_limit):
        with session.get('https://v.ruc.edu.cn/auth/captcha') as req:
            capt = req.json()
            capt_id: str = capt['id']
            capt_data: str = capt['b64s']

        with session.post(
            'https://v.ruc.edu.cn/auth/login',
            data=json.dumps({
                'username': f'ruc:{username}',
                'password': password,
                'code': solve_captcha_manually(capt_data.replace('data:image/png;base64,', '')),
                'remember_me': 'true',
                'redirect_uri': '/',
                'twofactor_password': '',
                'twofactor_recovery': '',
                'token': token,
                'captcha_id': capt_id
            }),
            headers={
                "Accept": "application/json",
                "Content-type": "application/x-www-form-urlencoded"
            },
            allow_redirects=True
        ) as req:
            resp_text = req.text
            if req.status_code == 400:
                resp_data = req.json()

                if 'captcha' in resp_data['error_description'].lower():
                    print("Wrong captcha, try again ({}/{})".format(ind+1, captcha_retry_limit))
                    continue
                else:
                    raise RuntimeError('wrong password') from ValueError(resp_text)
        
        with session.get('https://v.ruc.edu.cn') as req:
            assert 'login' not in req.url, f"VRUC login failed, data: \n{resp_text}"
            break
    else:
        raise RuntimeError('captcha limit exceeded')


def solve_captcha_manually(b64s: str) -> str:
    grayscale = " .:-=+*#%@"

    with Image.open(BytesIO(base64.b64decode(b64s))) as img:
        _, _, _, alpha = img.split()

        if config.captcha_on_ascii:
            for r in range(0, alpha.size[1], 2):
                for c in range(0, alpha.size[0]):
                    a0 = alpha.getpixel((c, r))

                    if r + 1 < alpha.size[1]:
                        a1 = alpha.getpixel((c, r + 1))
                    else:
                        a1 = 0.0

                    print(grayscale[int((a0 + a1) / 512 * 10)], end='')
                print()
            print()
        else:
            alpha.show()
        ret = input('Captcha: ').strip()
        
    return ret

def solve_captcha_knn(b64s: str) -> str:
    """
    have a try with knn
    k = 1 works perfectly
    split alpha channel into 4 boxes 
    each of them just fit one letter
    normalize their size, calc the difference with labeled image
    the one with the least sum of the squares of the difference is the answer
    """
