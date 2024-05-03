import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

email_user = "erockrpidevicealert@gmail.com"
email_password = "zfarpmyhbgwomytx"
email_send = "kglasgowerock@gmail.com"
minutes_count = 0

while True:
    time.sleep(60)
    subject = "DATA COLLECTION RUNNING FOR " + str(minutes_count) + " MINUTE(S)"
    msg = MIMEMultipart()
    msg["From"] = email_user
    msg["To"] = email_send
    msg["Subject"] = subject 

    body = "DATA COLLECTION PROGRAM IS STILL IN PROCESS. SEND AN EMAIL TO 'erockrpidevicealert@gmail.com' WITH 'STOP' AS THE SUBJECT TO TERMINATE DATA COLLECTION."
    msg.attach(MIMEText(body,"plain"))
    text = msg.as_string()
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(email_user,email_password)

    server.sendmail(email_user,email_send,text)
    server.quit()
    minutes_count += 1
    