import time
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.template import TemplateDoesNotExist


from .models import Company


SPAM_DELAY_SECONDS = 3


def _normalize_domain_to_filename(domain_name: str) -> str:
    return domain_name.upper().replace("/", "").replace(" ", "_")


def _render_subject_and_body(template_name: str, context: dict):
    rendered = render_to_string(template_name, context).strip()

    lines = rendered.splitlines()

    if not lines or not lines[0].startswith("Subject:"):
        raise ValueError("Email template must start with 'Subject:'")

    subject = lines[0].replace("Subject:", "").strip()
    body = "\n".join(lines[1:]).lstrip()

    return subject, body


def _build_email(company: Company) -> EmailMessage:
    domain_file = _normalize_domain_to_filename(company.domain.name)
    template_name = f"mailer/domains/{domain_file}.txt"

    context = {
        "contact": company.contact_name,
        "company": company.company_name,
        "domain": company.domain.name,
    }

    try:
        subject, body = _render_subject_and_body(template_name, context)
    except (TemplateDoesNotExist, ValueError):
        subject, body = _render_subject_and_body("mailer/domains/SOFTWARE_DEVELOPER.txt", context)

    email = EmailMessage(
        subject=subject,
        body=body,
        to=[company.email],
    )

    email.attach_file(company.domain.pdf.path)
    return email


def send_mail_to_company(company: Company) -> bool:
    if not company.is_active:
        return False

    email = _build_email(company)
    email.send()

    company.last_sent = now()
    company.save(update_fields=["last_sent"])

    time.sleep(SPAM_DELAY_SECONDS)
    return True


def send_all_mails():
    companies = Company.objects.filter(is_active=True)

    for company in companies:
        send_mail_to_company(company)
