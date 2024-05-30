import json
from django.shortcuts import render
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
global scaler
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import random
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from django.shortcuts import render
from django.http import JsonResponse
from sklearn.model_selection import train_test_split
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
def HomePage(request):
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('home')
@login_required(login_url='login')
def index(request):
    return render(request, 'chatbot.html')

df = pd.read_csv("data.csv")
X = df['Q']
y = df['A']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the vectorizer and fit it on the training data
vectorizer = TfidfVectorizer(stop_words='english')
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

classifier = MultinomialNB()
c = classifier.fit(X_train_tfidf, y_train)

@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_input = data.get('user_input', '').lower()

        GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey",)
        GREETING_RESPONSES = ["hi there", "hello", "Hi, I am glad! You are talking to me"]

        response_text = None  # Initialize response_text

        for word in user_input.split():
            if word.lower() in GREETING_INPUTS:
                response_text = random.choice(GREETING_RESPONSES)
                break  # Exit the loop if a greeting is detected
        else:  # No greeting detected
            if user_input != 'bye':
                if user_input == 'thanks' or user_input == 'thank you':
                    response_text = "You are welcome."
                elif user_input == 'what is your name?':
                    response_text = "Narendra Modi"
                else:
                    for i, question in enumerate(df['Q']):
                        if question.lower() == user_input: 
                            response_text = df['A'][i] 
                            break
                        else:
                             response_text="Your input not present in dataframe"
            else:
                response_text = "Bye! Take care."

        if response_text is None:
            response_text = "Sorry, I didn't understand that."

        return JsonResponse({'response': response_text})

    return HttpResponseBadRequest()