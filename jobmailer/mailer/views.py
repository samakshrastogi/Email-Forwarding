import csv
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.timezone import localtime

from .models import Company
from .utils import send_mail_to_company, send_all_mails


@login_required
def mail_status_table(request):
    companies = Company.objects.select_related("domain").all()

    search_query = request.GET.get("q", "").strip()
    if search_query:
        companies = (
            companies.filter(company_name__icontains=search_query)
            | companies.filter(email__icontains=search_query)
            | companies.filter(domain__name__icontains=search_query)
        )

    status = request.GET.get("status")
    if status == "sent":
        companies = companies.filter(last_sent__isnull=False)
    elif status == "not_sent":
        companies = companies.filter(last_sent__isnull=True)

    companies = companies.order_by("company_name")

    context = {
        "companies": companies,
        "search_query": search_query,
        "status": status,
    }

    return render(request, "mailer/mail_status.html", context)


@login_required
def send_again(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if company.is_active:
        send_mail_to_company(company)

    return HttpResponseRedirect(reverse("mail_status"))


@login_required
def send_all(request):
    if request.method == "POST":
        send_all_mails()

    return HttpResponseRedirect(reverse("mail_status"))


@login_required
def export_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="mail_status.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "S.No",
        "Company Name",
        "Contact Name",
        "Email",
        "Domain",
        "Mail Status",
        "Last Sent",
    ])

    companies = Company.objects.select_related("domain").order_by("company_name")

    for idx, company in enumerate(companies, start=1):
        writer.writerow([
            idx,
            company.company_name,
            company.contact_name,
            company.email,
            company.domain.name,
            company.mail_status,
            localtime(company.last_sent).strftime("%Y-%m-%d %H:%M:%S")
            if company.last_sent else "",
        ])

    return response
