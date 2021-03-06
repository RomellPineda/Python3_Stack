from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.db.models import Q
from datetime import datetime
from .models import *
# import bcrypt
# import re
# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your views here.
def index(request):
    return render(request, 'gigs_app/index.html')

def register(request):
    if request.method != 'POST':
        return redirect('/')

    result = User.objects.validate_register(request.POST)

    # error = False
    # if len(request.POST['first_name']) < 2:
    #     messages.error(request,'Name must be 2 or more characters')
    #     error = True
    # if not request.POST['first_name'].isalpha() or not request.POST['last_name'].isalpha():
    #     messages.error(request,'First and last name must not contain numbers or spaces')
    #     error = True
    # if not EMAIL_REGEX.match(request.POST['email']):
    #     messages.error(request,'Invalid email')
    #     error = True
    # if len(User.objects.filter(email = request.POST['email'])) > 0:
    #     messages.error(request,'User already exsist')
    #     error = True
    # if len(request.POST['password']) < 8:
    #     messages.error(request,'Password must be 8 or more characters in length')
    #     error = True
    # if request.POST['password'] != request.POST['confirm_pw']:
    #     messages.error(request,'Password and confirm password must match')
    #     error = True
    # 
    # if len(errors):
    #     for error in errors:
    #         messages.error(request, error)
    #     return redirect('/')
    # else:
        # hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        # user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hashed)
        # request.session['user_id'] = user.id
        # request.session['user_name'] = user.first_name
    #     print(user.id)
    #     print(user.first_name)
    # return redirect('/home')

    if 'success' in result:
        request.session[user_id] = result['success'].id
        return redirect('/home')
    else:
        for key, values in result.items():
            messages.error(request, value)
        return redirect('/')


def login(request):
    if request.method != 'POST':
        return redirect('/')
    # user = User.objects.filter(email = request.POST['email'])
    # if len(user) > 0:
    #     shmuser = user[0]
    #     if bcrypt.checkpw(request.POST['password'].encode(), shmuser.password.encode()):
    #         request.session['user_id'] = shmuser.id
    #         request.session['user_name'] = shmuser.first_name
    #         return redirect('/home')
    #     else:
    #         messages.error(request, 'Email or password invalid' )
    #         return redirect('/')
    # else:
    #     messages.error(request, 'Email or password invalid')
    #     return redirect('/')

    result = User.objects.login(request.POST)
    if 'success' in result:
        request.session['user_id'] = result['success'].id
        return redirect('/home')
    else:
        messages.error(request, 'Email or password invalid')
        return redirect('/')

def home(request):
    if not 'user_id' in request.session:
        return redirect('/')
    context = {
        'user' : User.objects.get(id = request.session['user_id']),
        'myjobs' : Job.objects.filter(Q(posted_by_id=request.session['user_id'])|Q(worker=request.session['user_id'])).order_by('created_at'),
        'otherjobs' : Job.objects.exclude(posted_by_id=request.session['user_id']).exclude(worker__id=request.session['user_id']).order_by('created_at'),
    }
    return render(request, 'gigs_app/home.html', context)

def info(request, number):
    date = Job.objects.get(id=number)
    print(date)
    context = {
        'info' : Job.objects.get(id=number),
        'user' : Job.objects.get(id=number).posted_by,
        'date' : datetime.strftime(date.created_at, '%B-%e-%Y')
    }
    return render(request, 'gigs_app/info.html', context)

def addjob(request):
    return render(request, 'gigs_app/add.html')

def process(request):
    if not 'user_id' in request.session:
        return redirect('/')
    if request.method != 'POST':
        return redirect('/')
    print(request.POST)
    error = False
    if len(request.POST['title']) < 3:
        messages.error(request,'Title must be 3 or more characters')
        error = True
    if len(request.POST['desc']) < 10:
        messages.error(request,'Description must be 10 or more characters')
        error = True
    if len(request.POST['location']) < 1:
        messages.error(request,'Location must not be blank')
        error = True
    if error:
        return redirect('/addjob')
    nj = Job.objects.create(title = request.POST['title'], location = request.POST['location'], posted_by = User.objects.get(id = request.session['user_id']), desc = request.POST['desc'])
    request.session['nj_id'] = nj.id
    return redirect('/home')

def edit(request, number):
    cont = {'jo' : Job.objects.get(id = number)}
    return render(request, 'gigs_app/edit.html', cont)

def join(request, number):
    u1 = User.objects.get(id = request.session['user_id'])
    j1 = Job.objects.get(id = number)
    u1.working.add(j1)
    return redirect('/home')

def delete(request, number):
    jd = Job.objects.get(id = number)
    jd.delete()
    return redirect('/home')

def logout(request):
    request.session.clear()
    return redirect('/')

def update(request, number):
    if not 'user_id' in request.session:
        return redirect('/')
    if request.method != 'POST':
        return redirect('/')
    print(request.POST)
    error = False
    if len(request.POST['title']) < 3:
        messages.error(request,'Title must be 3 or more characters')
        error = True
    if len(request.POST['desc']) < 10:
        messages.error(request,'Description must be 10 or more characters')
        error = True
    if len(request.POST['location']) < 1:
        messages.error(request,'Location must not be blank')
        error = True
    if error:
        return redirect('/addjob')
    else:
        nj = Job.objects.get(id=number)
        nj.title = request.POST['title']
        nj.location = request.POST['location']
        nj.desc = request.POST['desc']
        nj.save()
        return redirect('/home')
