import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send(email, password, target, subject, body):
    print("send email")

    from_address = email
    to_address = target

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)

    server.sendmail(email, target, text)
    server.quit()