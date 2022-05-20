import profile
from urllib import request
from django.shortcuts import render, redirect, HttpResponse
from .models import Chore, Location, History, List
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from datetime import date, timedelta, datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import secrets

#Indexs & Finishing Chores
def index(request):
    check_for_renew()
    context = {
        'chores' : Chore.objects.filter(list = List.objects.get(id = request.session['list_id'])),
        'list' : List.objects.get(id = request.session['list_id'])
    }
    return render(request, 'index.html', context)

def location_index(request):
    check_for_renew()
    context = {
        'location' : Location.objects.filter(list = List.objects.get(id = request.session['list_id'])).order_by('name')
    }
    return render(request, 'location_index.html', context)

def check_for_renew():
    today = date.today()
    for chore in Chore.objects.all():
        if chore.renew_date and chore.renew_date <= today:
            if not chore.renew_freq == 0:
                chore.done_date = None
                chore.renew_date = None
                chore.save()
    return

def finish_chore(request):
    if request.method == 'POST':
        today = date.today()
        time_now = datetime.now()
        for chores in request.POST.getlist('chores'):
            update_chore = Chore.objects.get(id = chores)
            update_chore.done_date = today
            update_chore.renew_date = today + timedelta(update_chore.renew_freq)
            update_chore.save()
            History.objects.create(
                chore = Chore.objects.get(id = chores),
                finished_at = time_now,
                list = List.objects.get(id = request.session['list_id']),
                user = request.user.profile
            )
    return redirect('/index')

def unfinish_chore(request):
    if request.method =='POST':
        for chore in request.POST.getlist('chores'):
            update_chore = Chore.objects.get(id = chore)
            update_chore.done_date = None
            update_chore.renew_date = None
            update_chore.save()
    return redirect('/index')

#Lists
def render_lists(request):
    context = {
        'owned_lists' : List.objects.filter(owner = request.user.profile),
        'joined_lists' : List.objects.filter(member = request.user.profile)
    }
    return render(request, 'lists.html', context)

def render_create_lists(request):
    return render(request, 'create_list.html')

def render_join_group(request):
    return render(request, 'join_group.html')

def group_test(request):
    if request.method == 'POST':
        errors = group_code_validation(request.POST,user=request.user.profile)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='alert alert-danger')
            return redirect('/join_group')
        list = List.objects.get(group_code = request.POST['code'])
        list.member.add(request.user.profile)
        return redirect('/lists')


def create_list(request):
    if request.method == 'POST':
        if len(request.POST['name']) < 1:
            messages.error(request, 'Please Input a name', extra_tags='alert alert-danger')
            return redirect('/create_list')
        code = secrets.token_hex(3)
        List.objects.create(
            name = request.POST['name'],
            owner = request.user.profile,
            group_code = code
        )
        Location.objects.create(
            name = 'None',
            list = List.objects.last()
        )
        request.session['list_id'] = List.objects.last().id
        return redirect('/index')
    else:
        return redirect('/manage')

def select_list(request, list_id):
    request.session['list_id'] = list_id
    return redirect('/index')


#Creating/Editing/Deleting Chores and Locations
def manage(request):
    context = {
        'location': Location.objects.filter(list = List.objects.get(id = request.session['list_id'])).order_by('name'),
        'list' : List.objects.get(id = request.session['list_id'])
    }
    return render(request, 'manage.html', context)

def render_create_chore(request):
    context = {
        'location' : Location.objects.filter(list = List.objects.get(id = request.session['list_id'])).order_by('name')
    }
    return render(request, 'create_chore.html', context)

def render_create_location(request):
    return render(request, 'create_location.html')

def render_edit_chore(request, chore_id):
    context = {
        'chore' : Chore.objects.get(id = chore_id),
        'history' : History.objects.filter(chore = Chore.objects.get(id=chore_id))
    }
    return render(request, 'edit_chore.html', context)

def render_edit_location(request, location_id):
    context = {
        'location' : Location.objects.get(id = location_id)
    }
    return render(request, 'edit_location.html', context)

def create_chore(request):
    if request.method == 'POST':
        locations = request.POST.getlist('location')
        if not request.POST['number']:
            renew_num = 0
        else:
            renew_num = request.POST['number']
        errors = create_task_validation(request.POST, loc=locations, num=renew_num)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='alert alert-danger')
            return redirect('/create_chore')
        for loc in request.POST.getlist('location'):
            locat = Location.objects.filter(name=loc).filter(list = List.objects.get(id = request.session['list_id']))
            chore = Chore.objects.create(
                name = request.POST['name'],
                renew_freq = renew_num,
                location = locat[0],
                list = List.objects.get(id = request.session['list_id'])
            )
    return redirect('/index')

def create_location(request):
    if request.method == 'POST':
        errors = location_validation(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='alert alert-danger')
            return redirect('/create_location')
        loc = Location.objects.create(
            name = request.POST['name'],
            list = List.objects.get(id = request.session['list_id'])
        )
    return redirect('/manage')

def edit_chore(request, chore_id):
    if request.method == 'POST':
        if not request.POST['number']:
            renew_num = 0
        else:
            renew_num = request.POST['number']
        errors = edit_task_validation(request.POST, num=renew_num)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='alert alert-danger')
            return redirect(f'/edit_chore/{chore_id}')
        update_chore = Chore.objects.get(id = chore_id)
        update_chore.name = request.POST['name']
        update_chore.renew_freq = renew_num
        if update_chore.done_date:
            update_chore.renew_date = update_chore.done_date + timedelta(int(update_chore.renew_freq))
        update_chore.save()
    return redirect('/manage')

def edit_location(request, location_id):
    if request.method == 'POST':
        errors = location_validation(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='alert alert-danger')
            return redirect(f'/edit_location/{location_id}')
        update_location = Location.objects.get(id = location_id)
        update_location.name = request.POST['name']
        update_location.save()
    return redirect('/manage')

def delete_chore(request, chore_id):
    if request.method == 'POST':
        delete_chore = Chore.objects.get(id = chore_id)
        delete_chore.delete()
    return redirect('/manage')

def delete_location(request, location_id):
    if request.method == 'POST':
        delete_location = Location.objects.get(id = location_id)
        delete_location.delete()
    return redirect('/manage')

#User Views
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to Login')
            return redirect('/login')
    else:
        form = UserRegisterForm()
    context = {
        'form' : form
    }
    return render(request, 'register.html', context )

def login_test(request):
    if request.user.is_authenticated and request.user.username == 'TestUser':
        if 'list_id' in request.session:
            return redirect('/index')
        else:
            return redirect('/setup_test')
    if request.user.is_authenticated:
        if 'list_id' in request.session:
            return redirect('/index')
        return redirect('/lists')
    else:
        return redirect('/login')

#Testing Views
@login_required
def history(request):
    context = {
        'history' : History.objects.filter(list = List.objects.get(id = request.session['list_id'])) 
    }
    return render(request, 'history.html',context)

# Validations
def group_code_validation(form,user):
    errors = {}
    list = List.objects.filter(group_code = form['code'])
    if len(list) == 0:
        errors['wrong code'] = 'This code is invalid'
        return errors
    list = list[0]
    if list.owner == user:
        errors['owner'] = 'You own this list'
    if user in list.member.all():
        errors['member'] = 'You are already a member'
    return errors

def location_validation(form):
    errors = {}
    if len(form['name']) < 1:
        errors['name'] = 'Please Input a Name'
    return errors

def create_task_validation(form, loc, num):
    errors = {}
    if len(form['name']) < 1:
        errors['name'] = 'Please Input a Name'
    if int(num) < 0:
        errors['number'] = 'Renew must be 0 or higher'
    if not loc:
        errors['location'] = 'Please select one or more location'
    return errors

def edit_task_validation(form, num):
    errors = {}
    if len(form['name']) < 1:
        errors['name'] = 'Please Input a Name'
    if int(num) < 0:
        errors['number'] = 'Renew must be 0 or higher'
    return errors

#TestUser
def setup_test(request):
    lists = List.objects.filter(owner = request.user.profile)
    for list in lists:
        list.delete()
    code = secrets.token_hex(3)
    List.objects.create(
            name = "Chore List",
            owner = request.user.profile,
            group_code = code
        )
    Location.objects.create(
        name = 'None',
        list = List.objects.last()
    )
    Location.objects.create(
        name = 'Bathroom',
        list = List.objects.last()
    )
    Chore.objects.create(
        name = 'Wipe Mirror',
        renew_freq = 7,
        location = Location.objects.last(),
        list = List.objects.last()
        )
    Chore.objects.create(
            name = 'Scrub Toilet',
            renew_freq = 7,
            location = Location.objects.last(),
            list = List.objects.last()
        )
    Location.objects.create(
        name = 'Bedroom',
        list = List.objects.last()
    )
    Chore.objects.create(
        name = 'Make Bed',
        renew_freq = 1,
        location = Location.objects.last(),
        list = List.objects.last()
    )
    code = secrets.token_hex(3)
    List.objects.create(
        name = "Grocery List",
        owner = request.user.profile,
        group_code = code
    )
    Location.objects.create(
        name = 'None',
        list = List.objects.last()
    )
    Location.objects.create(
        name = 'Costco',
        list = List.objects.last()
    )
    Chore.objects.create(
        name = 'Vegetables',
        renew_freq = 1,
        location = Location.objects.last(),
        list = List.objects.last()
    )
    Chore.objects.create(
        name = 'Chicken',
        renew_freq = 1,
        location = Location.objects.last(),
        list = List.objects.last()
    )
    Location.objects.create(
        name = 'Trader Joe\'s',
        list = List.objects.last()
    )
    Chore.objects.create(
        name = 'Ginger Snaps',
        renew_freq = 1,
        location = Location.objects.last(),
        list = List.objects.last()
    )
    request.session['list_id'] = List.objects.last().id
    return redirect('/lists')
