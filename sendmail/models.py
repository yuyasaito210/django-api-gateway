from django.db import models

class MailSetting(models.Model):
    api_key = models.CharField(max_length=100)
    secret_key = models.CharField(max_length=100)
    from_email = models.CharField(max_length=200)
    from_name = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    text_content = models.TextField()
    html_content = models.TextField()
