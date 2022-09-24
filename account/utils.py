from django.core.mail import EmailMessage, EmailMultiAlternatives
from email.mime.image import MIMEImage

import threading



class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
   
    @staticmethod
    def send_email(data):
        body_html = f'''<html>
    <body>
        <h1>Hi,{data['name']}</h1>
        {data['email_body']}
        <footer>  <img src="https://i.ibb.co/5j3rTYp/logo.png" /></footer>
    </body>
</html>
'''
        # email = EmailMessage(
        #     subject=data['email_subject'], body=body_html, to=[data['to_email']])
        # email.send()

        msg = EmailMultiAlternatives(
        data['email_subject'],
        body_html,
        to=[data['to_email']]
    )

        msg.mixed_subtype = 'related'
        msg.attach_alternative(body_html, "text/html")
        msg.send()
       
        