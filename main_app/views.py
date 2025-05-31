# main_app/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Cat
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import FeedingForm

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
def home(req):
    # return HttpResponse('<h1>hi</h1>')
    return render(req, 'home.html')

# about view
def about(req):
    # return HttpResponse('<h1>about</h1>')
    return render(req, 'about.html')

# all cats view
def cat_index(req):
    cats = Cat.objects.all()
    return render(req, 'cats/index.html', {'cats': cats})

# cat detail view
def cat_detail(req, cat_id):
    cat = Cat.objects.get(id=cat_id)
    feeding_form = FeedingForm()
    return render(req, 'cats/detail.html', {
        'cat': cat, 'feeding_form': feeding_form
    })

# new cat
class CatCreate(CreateView):
    model = Cat
    fields = '__all__'
    # success_url = '/cats/'

# update cat
class CatUpdate(UpdateView):
    model = Cat
    fields = ['breed', 'description', 'age']

# delete cat
class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats/'

# add feeding view function
def add_feeding(req, cat_id):
    form = FeedingForm(req.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect('cat-detail', cat_id=cat_id)