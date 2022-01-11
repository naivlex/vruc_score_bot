import base64
import urllib.parse

def encode(s: bytes) -> bytes:
    r = bytearray(s[:])
    r[1] = s[len(s) - 2]
    r[3] = s[len(s) - 4]
    r[5] = s[len(s) - 6]
    r[7] = s[len(s) - 8]
    r[len(s) - 2] = s[1]
    r[len(s) - 4] = s[3]
    r[len(s) - 6] = s[5]
    r[len(s) - 8] = s[7]

    return bytes(b"QZDATASOFT" + r)

def decode(s: bytes) -> bytes:
    assert s.startswith(b"QZDATASOFT")
    s = s[10:]
    r = bytearray(s[:])
    r[1] = s[len(s) - 2]
    r[3] = s[len(s) - 4]
    r[5] = s[len(s) - 6]
    r[7] = s[len(s) - 8]
    r[len(s) - 2] = s[1]
    r[len(s) - 4] = s[3]
    r[len(s) - 6] = s[5]
    r[len(s) - 8] = s[7]

    return r

# print(urllib.parse.unquote_plus(base64.b64decode(decode(b"QZDATASOFTJddJJVIJY29uZGl0aW9uR3JvdXAlMjIlM0ElNUIlN0IlMjJsaW5rJTIyJTNBJTIyYW5kJTIyJTJDJTIyY29uZGl0aW9uJTIyJTNBJTVCJTVEJTdEyTTECTTE")).decode()))
