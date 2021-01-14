import smtplib

def send_email(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login("senderemail@gmail.com", "senderpswd")
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail("senderemail@gmail.com", "recepientemail@gmail.com", message)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send.")