from django.urls import path
from . import views

urlpatterns = [
    # When you post to /markdown_app/ (the root of the app), use the create view.
    path('', views.create_ticket_post, name='create_ticket_post'),
    
    # Other endpoints (for example, rendering posts by slug).
    path('post/<slug:slug>/', views.render_ticket_post, name='render_ticket_post'),
    path('sql_definitions/', views.sql_definitions_view, name='sql_definitions'),
]
