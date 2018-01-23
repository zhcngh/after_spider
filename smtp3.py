import smtplib
import email.mime.multipart
import email.mime.text
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_email(subject='', content=''):
    mail_host ='smtp.163.com'
    mail_port=25
    mail_user='xx@163.com'
    mail_pass='xx'

    sender='xx@163.com' 
    receivers = ['xx@qq.com']

    msg = email.mime.multipart.MIMEMultipart()
    msg['from'] = sender
    msg['to'] = ','.join(receivers)
    msg['subject'] = subject
    content = content
    txt = email.mime.text.MIMEText(content, 'html', 'utf-8')
    msg.attach(txt)


    # 添加附件，传送D:/软件/yasuo.rar文件
    # part = MIMEApplication(open('D:/软件/yasuo.rar','rb').read())
    # part.add_header('Content-Disposition', 'attachment', filename="yasuo.rar")
    # msg.attach(part)

    smtp = smtplib.SMTP()
    smtp.connect(mail_host, mail_port)
    smtp.login(sender, mail_pass)
    smtp.sendmail(sender, receivers, str(msg))
    print("发送成功！")
    smtp.quit()

# try:
#     subject = 'Python 测试邮件'
#     #content = '<a href="http://www.baidu.com">这是一封来自 Python 编写的测试邮件。</a>'
#     send_email(subject, str(content))
# except Exception as err:
#     print(err)