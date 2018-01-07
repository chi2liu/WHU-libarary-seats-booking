import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_email(email_address, subject, time, seat):
    # 第三方 SMTP 服务
    mail_host = "smtp-mail.outlook.com"  # 设置服务器
    mail_user = "seatkiller@outlook.com"  # 用户名
    mail_pass = "simplebutunique2018"  # 口令

    sender = 'seatkiller@outlook.com'
    receivers = email_address  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(time + ':' + seat, 'plain', 'utf-8')
    message['From'] = sender
    message['To'] = receivers

    message['Subject'] = Header(subject, 'utf-8')

    s = smtplib.SMTP()
    s.connect(mail_host, 25)  # 25 为 SMTP 端口号
    s.starttls()
    s.login(mail_user, mail_pass)
    s.sendmail(sender, receivers, message.as_string())
    print('通知邮件发送成功，请及时查看！')
