from django.urls import path
from django.views.generic import RedirectView
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login_test, name='home'),
    path('index', views.index, name='index'),
    path('manage', views.manage, name='manage'),
    path('create_location', views.render_create_location, name='create_location'),
    path('save_location', views.create_location, name='save_location'),
    path('create_chore', views.render_create_chore, name='create_chore'),
    path('save_chore', views.create_chore, name='save_chore'),
    path('finish_chore', views.finish_chore, name='finish_chore'),
    path('unfinish_chore', views.unfinish_chore, name='unfinish_chore'),
    path('edit_chore/<int:chore_id>', views.render_edit_chore, name='edit_chore'),
    path('save_edited_chore/<int:chore_id>', views.edit_chore, name='save_edited_chore'),
    path('edit_location/<int:location_id>', views.render_edit_location, name='edit_location'),
    path('save_edited_location/<int:location_id>', views.edit_location, name='save_edited_location'),
    path('delete_chore/<int:chore_id>', views.delete_chore, name='delete_chore'),
    path('delete_location/<int:location_id>', views.delete_location, name='delete_location'),
    path('location_index', views.location_index, name='location_index'),
    path('history', views.history, name='history'),
    path('register', views.register, name='register'),
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('lists', views.render_lists, name='lists'),
    path('create_list', views.render_create_lists, name='create_list'),
    path('save_list', views.create_list, name='save_list'),
    path('select_list/<int:list_id>', views.select_list, name='select_list'),
    path('join_group', views.render_join_group),
    path('group_test', views.group_test),
    path('setup_test', views.setup_test, name='setup_test')
]