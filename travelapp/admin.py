from django.contrib import admin
from .models import *
from django.urls import path
from django.utils.html import mark_safe
from django.template.response import TemplateResponse
from django.db.models import Count
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .util import *


class TourForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Tour
        fields = '__all__'


class TravelappAdmin(admin.ModelAdmin):
    list_display = ("id", "name_tour", "active")
    search_fields = ['subject', 'category']
    readonly_fields = ['image_view']

    def image_view(self, course):
        if course:
            return mark_safe(
                '<img src="/static/{url}" width="120" />' \
                    .format(url=course.image.name)
            )

    def get_urls(self):
        return [
                   path('tourstat/', self.stats_view)
               ] + super().get_urls()

    def stats_view(self, request):
        return TemplateResponse(request,
                                'admin/tourstat.html', {
                                'count_tour': stat_tour_category(),
                                'tour_all': stat_tour_all(),
                                })


class TourGuideAdmin(admin.ModelAdmin):
    readonly_fields = ['imageTourGuide']


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['name', 'created_date']
    list_display = ['id', 'name', 'created_date']


# sửa amdin
class TravelAppAdminSite(admin.AdminSite):
    site_header = 'Hệ thống quản lý tour'


admin.site = TravelAppAdminSite(name='myadmin')

# web
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Tour, TravelappAdmin)
admin.site.register(TourGuide)
admin.site.register(Customer)
admin.site.register(Artical)
