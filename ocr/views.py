import base64
import datetime

from PIL import Image, ImageEnhance
import pytesseract
import numpy as np
import pytesseract
from django.conf import settings
from django.contrib import messages
from django.core.files.base import ContentFile
from django.shortcuts import render
from PIL import Image
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from googletrans import Translator
from gtts import gTTS
from playsound import playsound
from os import remove, path
import cv2

# you have to install tesseract module too from here - https://github.com/UB-Mannheim/tesseract/wiki
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Path to tesseract.exe
)


def homepage(request):
    if request.method == "POST":
        try:
            image = request.FILES["imagefile"]
            # encode image to base64 string
            image_base64 = base64.b64encode(image.read()).decode("utf-8")
        except:
            messages.add_message(
                request, messages.ERROR, "No image selected or uploaded"
            )
            return render(request, "home.html")
        lang = request.POST["language"]
        img = np.array(Image.open(image))
        text = pytesseract.image_to_string(img, lang=lang)
        # return text to html
        return render(request, "home.html", {"ocr": text, "image": image_base64})

    return render(request, "home.html")


@login_required(login_url='login')
def HomePaged(request):
    return render(request, 'logined.html')


def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')

    return render(request, 'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, 'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('signup')

def Logined(request):
    if request.method == "POST":
        try:
            image = request.FILES["imagefile"]
            # encode image to base64 string
            image_base64 = base64.b64encode(image.read()).decode("utf-8")
        except:
            messages.add_message(
                request, messages.ERROR, "No image selected or uploaded"
            )
            return render(request, "logined.html")
        lang = request.POST["language"]
        img = np.array(Image.open(image))
        text = pytesseract.image_to_string(img, lang=lang)
        # return text to html
        return render(request, "logined.html", {"ocr": text, "image": image_base64})

    return render(request, "logined.html")
def EditPic(request):
        return render(request, 'editpic.html')


def Translate(request):
    return render(request, 'translate.html')


def index(request):
    if request.method == 'POST':
        if request.POST.get('translate'):
            lang = request.POST.get('lang')
            lang1, lang2 = lang.split(',')
            txt = request.POST.get('txt')

            translator = Translator()
            tr = translator.translate(txt, dest=lang1)

            if txt != '':
                speech = gTTS(text=str(tr.text), lang=str(lang2), tld='com')
                if path.isfile('speech.mp3'):
                    remove('speech.mp3')
                speech.save('speech.mp3')
            return render(request, 'translate.html', {'result': tr.text})

        if request.POST.get('sound'):
            if path.isfile('speech.mp3'):
                playsound('speech.mp3')

    return render(request, 'translate.html')

def Contactus(request):
    return render(request, 'contactus.html')
