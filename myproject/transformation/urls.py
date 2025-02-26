from django.urls import path
from . import views

urlpatterns = [
    # When you post to /markdown_app/ (the root of the app), use the create view.
    path('', views.create_transformation_post, name='create_transformation_post'),
    
    # Other endpoints (for example, rendering posts by slug).
    path('post/<slug:slug>/', views.render_transformation_post, name='render_transformation_post'),
    path('sql_definitions/', views.sql_definitions_view, name='sql_definitions'),
]
