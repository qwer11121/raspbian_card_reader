import smtplib
from email.mime.text import MIMEText


def mail(recipient_list, subject, body):
    server = smtplib.SMTP("smtp.office365.com", 587)
    user = ""
    password = ""
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(user, password)
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = ", ".join(recipient_list)
    server.sendmail(user, recipient_list, msg.as_string())
    print("done")
    server.close()
    

if __name__ == "__main__":
    pass

    
