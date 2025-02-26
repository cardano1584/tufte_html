from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect, get_object_or_404
from django.utils.html import format_html
from django.urls import reverse
from .models import ChallangeContent, ChallangePostVersion

class PostVersionInline(admin.TabularInline):
    model = ChallangePostVersion
    readonly_fields = ['title', 'summary', 'description', 'content', 'changed_by', 'version_created_at', 'get_restore_link', 'get_active_status']
    extra = 0
    can_delete = False

    class Media:
        js = (
            '/static/challange/codemirror/lib/codemirror.js', 
            '/static/challange/codemirror/mode/markdown/markdown.js', 
            '/static/challange/js/init_codemirror.js', 
        )
        css = {
            'all': (
                '/static/challange/codemirror/lib/codemirror.css',
            )
        }

    def get_restore_link(self, obj):
        if obj.pk:
            return format_html('<a class="button">Restore</a>',
                               reverse('admin:restore_version', args=[obj.pk]))
        return None
    get_restore_link.short_description = "Restore Version"

    def get_active_status(self, obj):
        if obj.post.title == obj.title and obj.post.content == obj.content:
            return format_html('<span style="color:green;">✔</span>')
        return ''
    get_active_status.short_description = "Active Version"

class ChallangeContentAdmin(admin.ModelAdmin):
    inlines = [PostVersionInline]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ('creator', 'created_at', 'last_modified_by', 'last_modified_at')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creator = request.user
        obj.last_modified_by = request.user
        super().save_model(request, obj, form, change)
        if 'content' in form.changed_data:
            ChallangePostVersion.objects.create(
                post=obj, 
                title=obj.title, 
                summary=obj.summary, 
                description=obj.description, 
                content=obj.content, 
                changed_by=request.user
            )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:version_id>/restore/', self.admin_site.admin_view(self.restore_version), name='restore_version'),
        ]
        return custom_urls + urls

    def restore_version(self, request, version_id):
        version = get_object_or_404(ChallangePostVersion, pk=version_id)
        content = version.post
        content.title = version.title
        content.description = version.description
        content.summary = version.summary
        content.content = version.content
        content.last_modified_by = request.user
        content.save()
        self.message_user(request, f"The content '{{ content.title }}' was successfully restored to a previous version.")
        return redirect('admin:app_list', app_label=self.model._meta.app_label)

admin.site.register(ChallangeContent, ChallangeContentAdmin)
