# main_app/views.py

from django.shortcuts import render
from django.http import HttpResponse

# Cat class
class Cat:
    def __init__(self, name, breed, description, age):
        self.name = name
        self.breed = breed
        self.description = description
        self.age = age

# Cat instances
cats = [
    Cat('Sachi', 'tortoiseshell', 'Looks like a turtle.', 0),
    Cat('Lolo', 'tabby', 'Kinda rude.', 3),
    Cat('Fancy', 'bombay', 'Happy fluff ball.', 4),
    Cat('Bonk', 'selkirk rex', 'Meows loudly.', 6)
]

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
    return render(req, 'cats/index.html', {'cats': cats})

