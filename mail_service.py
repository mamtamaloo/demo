from flask_mail import Message

def send_email(subject, sender, recipients, text_body, html_body):
    print(subject,sender)
    msg = Message(subject, sender=sender, recipients=[recipients])
    msg.html = "".join(html_body)
    from run import mail
    mail.send(msg)
    return "Sent"
