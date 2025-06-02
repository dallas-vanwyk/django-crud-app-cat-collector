# main_app/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Cat, Toy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import FeedingForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Cat class
# class Cat:
#     def __init__(self, name, breed, description, age):
#         self.name = name
#         self.breed = breed
#         self.description = description
#         self.age = age

# Cat instances
# cats = [
#     Cat('Sachi', 'tortoiseshell', 'Looks like a turtle.', 0),
#     Cat('Lolo', 'tabby', 'Kinda rude.', 3),
#     Cat('Fancy', 'bombay', 'Happy fluff ball.', 4),
#     Cat('Bonk', 'selkirk rex', 'Meows loudly.', 6)
# ]

# home view function
# def home(req):
#     # return HttpResponse('<h1>hi</h1>')
#     return render(req, 'home.html')


class Home(LoginView):
    template_name = 'home.html'


@login_required
def about(req):
    # return HttpResponse('<h1>about</h1>')
    return render(req, 'about.html')

@login_required
def cat_index(req):
    cats = Cat.objects.filter(user=req.user)
    return render(req, 'cats/index.html', {'cats': cats})

@login_required
def cat_detail(req, cat_id):
    cat = Cat.objects.get(id=cat_id)

    # toys = Toy.objects.all()
    toys_cat_doesnt_have = Toy.objects.exclude(id__in = cat.toys.all().values_list('id'))

    feeding_form = FeedingForm()
    return render(req, 'cats/detail.html', {
        'cat': cat,
        'feeding_form': feeding_form,
        'toys': toys_cat_doesnt_have,
    })

# new cat
class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = ['name', 'breed', 'description', 'age']
    # success_url = '/cats/'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# update cat
class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields = ['breed', 'description', 'age']

# delete cat
class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    success_url = '/cats/'

@login_required
def add_feeding(req, cat_id):
    form = FeedingForm(req.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect('cat-detail', cat_id=cat_id)

@login_required
def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect('cat-index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
    # Same as: 
    # return render(
    #     request, 
    #     'signup.html',
    #     {'form': form, 'error_message': error_message}
    # )

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'

class ToyList(LoginRequiredMixin, ListView):
    model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'

def associate_toy(req, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('cat-detail', cat_id=cat_id)

def remove_toy(req, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect('cat-detail', cat_id=cat_id)