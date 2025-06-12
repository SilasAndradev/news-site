from django.contrib import admin

# Register your models here.
from users.models import ReaderProfile
from news.models import (
    News,
    NewsArchives,
    NewsComments,
)


admin.site.register(ReaderProfile)
admin.site.register(News)
admin.site.register(NewsArchives)
admin.site.register(NewsComments)
