import os
import numpy as np
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array


def home(request):
    return render(request, 'home1.html')
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('details')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


def registerpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        if password != confirm:
            return render(request, 'register.html', {'result': 'Passwords do not match'})
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'result': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password)
        user.save()
        return redirect('login')

    return render(request, 'register.html')



MODEL_PATH = os.path.join(settings.BASE_DIR, 'final_blood_model.h5')
model = load_model(MODEL_PATH)

CLASS_NAMES = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']




def predict(request):
    result = None
    #name = age = gender = None
    name = request.session.get('name')
    age = request.session.get('age')
    gender = request.session.get('gender')

    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        img_path = os.path.join(settings.MEDIA_ROOT, image_file.name)

        # Save uploaded image
        with open(img_path, 'wb+') as f:
            for chunk in image_file.chunks():
                f.write(chunk)
        
        context = {
        'name': name,
        'age': age,
        'gender': gender,
        'result': result,
    }

        # Preprocess
        img = load_img(img_path, target_size=(224, 224))
        img_array = img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Predict
        preds = model.predict(img_array)
        pred_index = np.argmax(preds)
        result = CLASS_NAMES[pred_index]

    return render(request, 'predict.html', {
    'result': result,
    'name': name,
    'age': age,
    'gender': gender
})




def details(request):
    return render(request, 'details.html')
def save_details(request):
    if request.method == 'POST':
        request.session['name'] = request.POST.get('name')
        request.session['age'] = request.POST.get('age')
        request.session['gender'] = request.POST.get('gender')
        return redirect('predict')
    return redirect('details')

  
