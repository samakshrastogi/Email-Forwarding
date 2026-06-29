from django.urls import path
from . import views

urlpatterns = [
    path("", views.mail_status_table, name="mail_status"),
    path("send-again/<int:company_id>/", views.send_again, name="send_again"),
    path("send-all/", views.send_all, name="send_all"),
    path("export-csv/", views.export_csv, name="export_csv"),
]
