from django.shortcuts import render
from django.core.files.images import ImageFile
from tempfile import TemporaryFile
from PIL import Image, ImageDraw
from .forms import UserInformation
from .models import Page
import string
import random


def create_image(text_string, file):
    tmp = Image.new('RGB', (1, 1))
    tmp_d = ImageDraw.Draw(tmp)
    text_width, text_height = tmp_d.textsize(text_string)
    width = text_width + 10
    height = text_height + 10
    img = Image.new('RGB', (width, height), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((5, 5), text_string, fill=(0, 0, 0))
    img.save(file, 'png')


def password_generator():
    length = 10
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = string.punctuation
    all = lower + upper + num + symbols
    temp = random.sample(all, length)
    password = "".join(temp)
    return password


def index(request):
    if request.method == 'POST':
        form = UserInformation(request.POST)
        if form.is_valid():
            with TemporaryFile(mode='w+b') as f:
                create_image(form.data['text_information'], f)
                Page.objects.create(image=ImageFile(f, name='test.png'), password=password_generator())
    else:
        form = UserInformation()
    return render(request, 'index.html', {'form': form})
