from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import DefinitionsContent, DefinitionsPostViewTracking
from django.utils.safestring import mark_safe
from django.contrib.auth.models import Group
import markdown
import json
from django.views.decorators.csrf import csrf_exempt

def render_definitions_post(request, slug):
    post = get_object_or_404(DefinitionsContent, slug=slug)
    if request.user.is_authenticated:
        DefinitionsPostViewTracking.objects.create(post=post, user=request.user)
    can_view_extra_info = request.user.groups.filter(name__in=['engineer', 'analyst']).exists()
    html_content = markdown.markdown(post.content)
    return render(request, 'definitions/definitions_post_view.html', {
        'post': post,
        'content': mark_safe(html_content),
        'last_modified_by': post.last_modified_by if can_view_extra_info else None,
        'last_modified_at': post.last_modified_at if can_view_extra_info else None,
        'can_view_extra_info': can_view_extra_info
    })

def sql_definitions_view(request):
    all_posts = DefinitionsContent.objects.all()
    return render(request, 'definitions/sql_definitions.html', {'all_posts': all_posts})

@csrf_exempt
def create_definitions_post(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except Exception as e:
            return JsonResponse({"error": "Invalid JSON data", "details": str(e)}, status=400)
        
        title = data.get("title")
        summary = data.get("summary")
        description = data.get("description")
        content_field = data.get("content")
        
        if not title or not content_field:
            return JsonResponse({"error": "Missing required fields: title and content"}, status=400)
        
        new_post = DefinitionsContent.objects.create(
            title=title,
            summary=summary,
            description=description,
            content=content_field,
            creator=request.user if request.user.is_authenticated else None
        )
        return JsonResponse({"status": "success", "id": new_post.id})
    else:
        return JsonResponse({"error": "POST request required."}, status=405)
