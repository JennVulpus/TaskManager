from django.shortcuts import render, redirect, HttpResponse
from .models import Chore, Location, History, List
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from datetime import date, timedelta, datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

#Indexs & Finishing Chores
def index(request):
    check_for_renew()
    context = {
        'chores' : Chore.objects.filter(list_chore = List.objects.get(id = request.session['list_id']))
    }
    return render(request, 'index.html', context)

def location_index(request):
    check_for_renew()
    context = {
        'location' : Location.objects.filter(list_location = List.objects.get(id = request.session['list_id'])).order_by('name')
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
                finished_at = time_now
            )
    return redirect('/')

def unfinish_chore(request):
    if request.method =='POST':
        for chore in request.POST.getlist('chores'):
            update_chore = Chore.objects.get(id = chore)
            update_chore.done_date = None
            update_chore.renew_date = None
            update_chore.save()
    return redirect('/')

#Lists
def render_lists(request):
    context = {
        'lists' : List.objects.all()
    }
    return render(request, 'lists.html', context)

def render_create_lists(request):
    return render(request, 'create_list.html')

def create_list(request):
    if request.method == 'POST':
        List.objects.create(
            name = request.POST['name']
        )
        request.session['list_id'] = List.objects.last().id
        return redirect('/')
    else:
        return redirect('/manage')

def select_list(request, list_id):
    request.session['list_id'] = list_id
    return redirect('/')


#Creating/Editing/Deleting Chores and Locations
def manage(request):
    context = {
        'location': Location.objects.filter(list_location = List.objects.get(id = request.session['list_id'])).order_by('name')
    }
    return render(request, 'manage.html', context)

def render_create_chore(request):
    context = {
        'location' : Location.objects.all()
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
        l = List.objects.get(id = request.session['list_id'])
        for loc in request.POST.getlist('location'):
            chore = Chore.objects.create(
                name = request.POST['name'],
                renew_freq = request.POST['number'],
                location = Location.objects.get(name=loc),
            )
            chore.list_chore.add(l)
    return redirect('/')

def create_location(request):
    if request.method == 'POST':
        l = List.objects.get(id = request.session['list_id'])
        loc = Location.objects.create(
            name = request.POST['name']
        )
        loc.list_location.add(l)
    return redirect('/manage')

def edit_chore(request, chore_id):
    if request.method == 'POST':
        update_chore = Chore.objects.get(id = chore_id)
        update_chore.name = request.POST['name']
        update_chore.renew_freq = request.POST['number']
        update_chore.location = Location.objects.get(name=request.POST['location'])
        if update_chore.done_date:
            update_chore.renew_date = update_chore.done_date + timedelta(int(update_chore.renew_freq))
        update_chore.save()
    return redirect('/manage')

def edit_location(request, location_id):
    if request.method == 'POST':
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

#Testing Views
@login_required
def history(request):
    context = {
        'history' : History.objects.all() 
    }
    return render(request, 'history.html',context)

def test(request):
    context = {
        'chores' : Chore.objects.all().order_by('name')
    }
    return render(request, 'test.html', context)
