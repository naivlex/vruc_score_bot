import json

__all__ = ['vruc_student_id', 'vruc_password', 'vruc_mailbox', 'vruc_mail_password', 'target_mailbox']

vruc_student_id = '1919810'
vruc_password = '******'

vruc_mailbox = '114514'
vruc_mail_password = '1919810',
target_mailbox = None

try:
    with open('config.json', encoding='utf-8') as fin:
        for k, v in json.load(fin).items():
            globals()[k] = v
except FileNotFoundError as e:
    raise RuntimeError("请拷贝 config-sample.json 为 config.json 并填入学号和密码") from e

if target_mailbox is None:
    target_mailbox = vruc_mailbox
