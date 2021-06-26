from django.shortcuts import render
from django.core.files.images import ImageFile
from tempfile import TemporaryFile
from PIL import Image, ImageDraw
from .forms import UserInformation
from .forms import PasswordForm
from .tasks import delete_expired_images
from .models import Page
from hashids import Hashids
from django.http import Http404
import string
import random
from datetime import datetime

hashids = Hashids('information')


def create_image(text_string, file):
    tmp = Image.new('RGB', (1, 1))
    tmp_d = ImageDraw.Draw(tmp)
    text_width, text_height = tmp_d.textsize(text_string)
    width = text_width + 10
    height = text_height + 10
    img = Image.new('RGB', (width, height), (0, 0, 0))
    d = ImageDraw.Draw(img)
    d.text((5, 5), text_string, fill=(0, 255, 0))
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
    context = {}
    if request.method == 'POST':
        form = UserInformation(request.POST)
        if form.is_valid():
            with TemporaryFile(mode='w+b') as f:
                create_image(form.data['text_information'], f)
                page = Page.objects.create(image=ImageFile(f, name='test.png'), password=password_generator(),
                                           visits_count=0)
                url = '/storage/' + hashids.encode(page.id)
                context['url'] = url
                context['password'] = page.password
    else:
        form = UserInformation()
    context['form'] = form
    return render(request, 'index.html', context)


def get_information(request, url_hash):
    context = {}
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        try:
            id = hashids.decode(url_hash)
            page = Page.objects.get(id=id[0])
        except Exception:
            raise Http404()
        if form.is_valid():
            if form.data['password'] == page.password:
                page.visits_count = page.visits_count + 1
                page.save()
                context['page'] = page
                context['visits'] = page.visits_count
            else:
                context['form'] = form
                context['message'] = 'Wrong password!'
    else:
        form = PasswordForm()
        context['form'] = form
    response = render(request, 'page.html', context)
    response.set_cookie('user_visits', [datetime.now(), f'/{url_hash}'])
    return response
