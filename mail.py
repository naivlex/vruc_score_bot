import smtplib
import traceback
from email.mime.text import MIMEText
from email.header import Header

import config

# 第三方 SMTP 服务
mail_host = "smtp.ruc.edu.cn"  # 设置服务器
mail_user = config.vruc_mailbox   # 用户名
mail_pass = config.vruc_mail_password  # 口令


sender = mail_user
receivers = [config.target_mailbox]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱


def send_mail(title: str, content: str, mimetype: str = 'plain'):
    message = MIMEText(content, mimetype, 'utf-8')
    message['From'] = Header("成绩监视 BOT", 'utf-8')
    message['To'] = Header(mail_user, 'utf-8')

    subject = title
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件")
        traceback.print_exception(e)
