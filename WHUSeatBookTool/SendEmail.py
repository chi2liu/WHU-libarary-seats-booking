import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_email(email_address, subject, content):

    # 第三方 SMTP 服务
    mail_host = "smtp.163.com"  # 设置服务器
    mail_user = "eclipseforweb@163.com"  # 用户名
    mail_pass = "python3"  # 口令

    sender = 'eclipseforweb@163.com'
    receivers = email_address  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = sender
    message['To'] = receivers

    message['Subject'] = Header(subject, 'utf-8')

    try:
        server = smtplib.SMTP(mail_host, 25)
        # server.set_debuglevel(1)
        server.starttls()
        server.login(mail_user, mail_pass)
        server.sendmail(sender, receivers, message.as_string())
        server.quit()
    except Exception:
        print('邮件发送失败！')
        return 'email wrong!'
    else:
        print('邮件发送成功！')
