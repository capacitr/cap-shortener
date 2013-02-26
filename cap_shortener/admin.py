from django.contrib import admin

from django.contrib.sites.models import Site


from models import ShortenedURL
from django.contrib.redirects.models import Redirect

import random
import string

def view_url(instance):
    site = Site.objects.get_current()
    new_url = "http://%s/%s" % (site.domain, instance.shortened_url.old_path,)
    return "<a href=\"%s\">%s</a>" % (new_url, new_url,) 
view_url.allow_tags = True

class ShortenedURLAdmin(admin.ModelAdmin):

    list_display = ["url", "shortened_url", view_url]

    def save_model(self, request, obj, form, change):
        if not change:
            char_set = string.ascii_uppercase + string.ascii_lowercase
            r = ''.join(random.sample(char_set,6))

            while(Redirect.objects.filter(old_path=r).exists()):
                r = ''.join(random.sample(char_set,6))

            redirect = Redirect()
            redirect.site = Site.objects.get_current() 
            redirect.old_path = r
            redirect.new_path = obj.url
            redirect.save()

            obj.shortened_url = redirect
            obj.save()

        super(ShortenedURLAdmin, self).save_model(request, obj, form, change)

admin.site.register(ShortenedURL, ShortenedURLAdmin)


