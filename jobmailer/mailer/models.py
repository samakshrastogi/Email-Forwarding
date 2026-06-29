from django.db import models
from django.utils.timezone import now


class Domain(models.Model):
    name = models.CharField(max_length=100, unique=True)
    pdf = models.FileField(upload_to="pdfs/")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Company(models.Model):
    company_name = models.CharField(max_length=200)
    email = models.EmailField()
    contact_name = models.CharField(max_length=100)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    last_sent = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["company_name"]
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.company_name

    @property
    def mail_status(self):
        return "Sent" if self.last_sent else "Not Sent"

    def mark_sent(self):
        self.last_sent = now()
        self.save(update_fields=["last_sent"])
