import urllib.parse
import smtplib
from email.mime.text import MIMEText
import logging

def mail(tto, subject, body, cc=[]):
    _from = 'bbd.tools@app.nokia-sbell.com'
    _server = '172.24.146.133'

    logging.info(f'tto = {tto}')
    if len(cc) == 0:
       cc = [
          'dongxu.zeng@nokia-sbell.com', 
          #'dandan.yu@nokia-sbell.com'
        ]
    all_recipients = tto + cc
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = _from
    msg['To'] = ','.join(tto)
    msg['Cc'] = ','.join(cc)
    try:
        with smtplib.SMTP(_server) as server:
            server.sendmail(_from, all_recipients, msg.as_string())
            pass
    except Exception as e:
       logging.info(f'Error sending email: {e}')
