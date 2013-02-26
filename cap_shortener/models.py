from django.db import models
from django.contrib.sites.models import Site

class ShortenedURL(models.Model):
    url = models.TextField("URL to shorten")
    shortened_url = models.ForeignKey('redirects.Redirect', blank=True, null=True, editable=False)

