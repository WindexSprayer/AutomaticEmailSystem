import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

email_user = "erockrpidevicealert@gmail.com"
email_password = "zfarpmyhbgwomytx"
email_send = "kglasgowerock@gmail.com"

subject = "STARTING DATA COLLECTION SCRIPTS"

msg = MIMEMultipart()
msg["From"] = email_user
msg["To"] = email_send
msg["Subject"] = subject

body = "WE HAVE DETECTED AN EMAIL TO BEGIN PROCESSING DATA. PLEASE CHECK ON DEVICE IF THIS WAS NOT EXPECTED"
msg.attach(MIMEText(body,"plain"))
text = msg.as_string()
server = smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
server.login(email_user,email_password)

server.sendmail(email_user,email_send,text)
server.quit()