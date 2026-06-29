from django.core.management.base import BaseCommand
from mailer.utils import send_all_mails

class Command(BaseCommand):
    help = "Send job application emails to companies"

    def handle(self, *args, **kwargs):
        send_all_mails()
        self.stdout.write(
            self.style.SUCCESS("✅ All emails sent successfully")
        )
