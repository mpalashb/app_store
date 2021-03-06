import threading

from django.core.mail import EmailMessage
from django.conf import settings


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        try:

            print("==================================")
            print("Email send-> Started!")
            print("==================================")
            msg = EmailMessage(self.subject, self.html_content,
                               settings.DEFAULT_FROM_EMAIL, self.recipient_list)
            msg.content_subtype = "html"
            msg.send()
            print("==================================")
            print("Email send-> Completed!")
            print("==================================")
            return {"detail": "Email has been send!"}
        except Exception as p:
            print("==================================")
            print(f"Email send-> Error! | Reason -> {p}")
            print("==================================")


def send_html_mail(subject, html_content, recipient_list):
    EmailThread(subject, html_content, recipient_list).start()
