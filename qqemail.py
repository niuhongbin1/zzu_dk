# coding=utf-8
"""
作者：川川
@时间  : 2021/11/10 11:50
群：970353786
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_email(msg_from, passwd, msg_to, text_content):
    msg = MIMEMultipart()
    subject = "zzujk"  # 主题
    text = MIMEText(text_content)
    msg.attach(text)

    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print("发送成功")
    except smtplib.SMTPException as e:
        print("发送失败")
    finally:
        s.quit()


def out(t):
    msg_from = '3225272214@qq.com'  # 发送方邮箱
    passwd = '**********'  # 填入发送方邮箱的授权码（就是刚刚你拿到的那个授权码）
    msg_to = '3225272214@qq.com'  # 收件人邮箱
    send_email(msg_from,passwd,msg_to,t) 

if __name__ == '__main__':

    msg_from = '28****579@qq.com'  # 发送方邮箱
    passwd = 'dw****rodhda'  # 填入发送方邮箱的授权码（就是刚刚你拿到的那个授权码）
    msg_to = '2****9579@qq.com'  # 收件人邮箱

    with open("log_t.txt", "r",encoding="utf-8") as f:  # 打开文件
        data = f.read()  # 读取文件
        text_content = data # 发送的邮件内容
        send_email(msg_from,passwd,msg_to,text_content)  
