import smtplib
from email.mime.text import MIMEText
import getpass


import conf


def sendMail(to, subject, htmlMsg):
    msg = MIMEText(htmlMsg, 'html')

    msg['Subject'] = subject
    msg['From'] = conf.emailUsername
    msg['To'] = to

    s = smtplib.SMTP(conf.emailHost, conf.emailPort)
    s.starttls()
    passwd = getpass.getpass()
    s.login(conf.emailUsername, passwd)

    x = s.sendmail(conf.emailUsername, [to], msg.as_string())
    s.quit()


html = '<h1>A nice e-mail tittle</h1><p>A fine email body</p>'
sendMail('lordale@yopmail.com', 'another example', html)
