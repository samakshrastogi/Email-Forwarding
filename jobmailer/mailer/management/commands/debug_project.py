import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
from django.template.loader import get_template
from django.core.mail import get_connection as get_mail_connection

from mailer.models import Company, Domain


class Command(BaseCommand):
    help = "Debug entire jobmailer project setup"

    def success(self, msg):
        self.stdout.write(self.style.SUCCESS(f"✔ {msg}"))

    def error(self, msg):
        self.stdout.write(self.style.ERROR(f"✖ {msg}"))

    def handle(self, *args, **kwargs):
        self.stdout.write("\n🔍 STARTING PROJECT DEBUG\n")

        # ------------------------------
        # Settings check
        # ------------------------------
        try:
            assert settings.SECRET_KEY
            self.success("Settings loaded")
        except Exception:
            self.error("Settings not loaded")

        # ------------------------------
        # Database check
        # ------------------------------
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            self.success("Database connection OK")
        except Exception as e:
            self.error(f"Database error: {e}")

        # ------------------------------
        # Models check
        # ------------------------------
        try:
            company_count = Company.objects.count()
            domain_count = Domain.objects.count()
            self.success(
                f"Models OK (Companies: {company_count}, Domains: {domain_count})"
            )
        except Exception as e:
            self.error(f"Model error: {e}")

        # ------------------------------
        # Active companies
        # ------------------------------
        active_count = Company.objects.filter(is_active=True).count()
        self.success(f"Active companies: {active_count}")

        # ------------------------------
        # PDF files check
        # ------------------------------
        missing_pdfs = []
        for domain in Domain.objects.all():
            if not domain.pdf or not os.path.exists(domain.pdf.path):
                missing_pdfs.append(domain.name)

        if missing_pdfs:
            self.error(f"Missing PDFs for domains: {', '.join(missing_pdfs)}")
        else:
            self.success("All domain PDFs found")

        # ------------------------------
        # Email template
        # ------------------------------
        try:
            get_template("email.txt")
            self.success("Email template loaded")
        except Exception as e:
            self.error(f"Email template missing: {e}")

        # ------------------------------
        # Email SMTP config
        # ------------------------------
        try:
            conn = get_mail_connection()
            conn.open()
            conn.close()
            self.success("SMTP connection OK")
        except Exception as e:
            self.error(f"SMTP error: {e}")

        # ------------------------------
        # Auth URLs
        # ------------------------------
        try:
            assert settings.LOGIN_URL
            self.success("Login URL configured")
        except Exception:
            self.error("LOGIN_URL not set")

        self.stdout.write("\n✅ DEBUG COMPLETE\n")
