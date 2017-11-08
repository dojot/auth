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
    s.login(conf.emailUsername, conf.emailPasswd)

    x = s.sendmail(conf.emailUsername, [to], msg.as_string())
    s.quit()
