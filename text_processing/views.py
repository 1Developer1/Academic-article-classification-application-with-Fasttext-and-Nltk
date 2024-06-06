from django.shortcuts import render,redirect
from text_processing.models import Users,Article
from django.contrib.auth import authenticate,login,logout 
from django.contrib.auth.models import User
from TextProcessing import TextVectorizer
import pickle
import numpy as np
import json


def login_request(request):
    if request.method == "POST":
        print(request.user)
        username = request.POST.get("username")
        password = request.POST.get("password")

        user=authenticate(request,username=username,password=password)
       
        
        if user is not None:
            login(request, user)
            print(f"Giriş yapan kullanıcının ID'si: {request.user.id}")

            
            return redirect("texts")
            
        else:
            return render(request,"login.html",{"error":"username ya da parola yanlış"})
             

    return render(request, "login.html")

def logout_request(request):
    logout(request)
    return redirect("login") 

def interests_request(request):
    if request.method == "POST":
        user_=request.user
        username = request.POST.get("name")
        phone = request.POST.get("phone")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        location = request.POST.get("location")
        interest1 = request.POST.get("interest1")
        interest2 = request.POST.get("interest2")
        interest3 = request.POST.get("interest3")

        existing_user = Users.objects.filter(user=user_).first()

        if existing_user:
            existing_user.phone = phone
            existing_user.age = age
            existing_user.gender = gender
            existing_user.location = location
            existing_user.interest1 = interest1
            existing_user.interest2 = interest2
            existing_user.interest3 = interest3
            existing_user.save()
        else:
            new_user = Users.objects.create(
                user=user_,
                username=username,
                phone=phone,
                age=age,
                gender=gender,
                location=location,
                interest1=interest1,
                interest2=interest2,
                interest3=interest3
            )
            new_user.save()

        return redirect('texts')  

    return render(request, "interests.html")


def search(request):
    if request.method == "POST":
        print(request.user.id)
        query = request.POST.get('query', '')
        articles_dir = "C:/Users/XMG/Desktop/python/Metin İşleme/krapivin-2009-pre-master/krapivin-2009-pre-master/src/all_docs_abstacts_refined/all_docs_abstacts_refined"
        model_path = "C:/Users/XMG/Desktop/python/Metin İşleme/cc.en.300.bin"
        
        text_processor = TextVectorizer(model_path, articles_dir)

        # Veritabanından makale verilerini al
        articles = Article.objects.all()
        article_texts = [(article.filename, article.content, article.vector) for article in articles]
        article_vectors = [np.array(json.loads(article[2])) for article in article_texts]


        if query=='':
            print('1')
            # Kullanıcının ilgi alanlarını veritabanından al
            user_interests = Users.objects.get(user=request.user.id)
            interests = [user_interests.interest1, user_interests.interest2, user_interests.interest3]

            # Ilgi alanlarının vektörlerini oluştur
            interest_vectors = text_processor.get_interest_vectors(interests)

            # Ilgi alanları ile benzerlikleri hesapla
            similarities = text_processor.calculate_similarity(interest_vectors, article_vectors)
           
        else:
            print('2')
            # Query vektörünü oluştur
            query_vector = text_processor.get_query_vector(query)

            # Query ile benzerlikleri hesapla
            similarities = text_processor.calculate_query_similarity(query_vector, article_vectors)

        # En yakın 5 makaleyi bul
        top_articles = text_processor.get_top_n_articles(similarities,article_texts)



         # Sonuçları yazdır
        search_results = {
            "top_articles": top_articles,
        }
        return render(request, 'texts.html', {'search_results': search_results})
    else:
        return render(request, 'texts.html', {'search_results': []})

def register_request(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        verify_password = request.POST.get("verify_password")

        if password== verify_password:
            if User.objects.filter(username=username).exists():
                return render(request,"register.html",{"error":"Username kullanılıyor."})
            else:
                user=User.objects.create_user(username=username,password=password)
                user.save()
                return redirect("login")
        else:
            return render(request,"register.html",{"error":"parola eşleşmiyor."})

    return render(request, "register.html")


def my_view(request):
    articles_dir = "C:/Users/XMG/Desktop/python/Metin İşleme/krapivin-2009-pre-master/krapivin-2009-pre-master/src/all_docs_abstacts_refined/all_docs_abstacts_refined"
    model_path = "C:/Users/XMG/Desktop/python/Metin İşleme/cc.en.300.bin"
    
    text_processor = TextVectorizer(model_path, articles_dir)

    # Kullanıcının ilgi alanlarını veritabanından al
    user_interests = Users.objects.get(user=request.user)
    interests = [user_interests.interest1, user_interests.interest2, user_interests.interest3]

    # Ilgi alanlarının vektörlerini oluştur
    interest_vectors = text_processor.get_interest_vectors(interests)
    
    # Veritabanından makale verilerini al
    articles = Article.objects.all()
    article_texts = [(article.filename, article.content, pickle.loads(article.vector)) for article in articles]
    article_vectors = [article[2] for article in article_texts]

    # Benzerlikleri hesapla
    similarities = text_processor.calculate_similarity(interest_vectors, article_vectors)

    # En yakın 5 makaleyi bul
    top_articles = text_processor.get_top_n_articles(similarities, article_texts)

    # Sonuçları yazdır
    context = {
        "top_articles": top_articles
    }

    return render(request, 'results.html', context)

def save_articles(request):
    articles_dir = "C:/Users/XMG/Desktop/python/Metin İşleme/krapivin-2009-pre-master/krapivin-2009-pre-master/src/all_docs_abstacts_refined/all_docs_abstacts_refined"
    model_path = "C:/Users/XMG/Desktop/python/Metin İşleme/cc.en.300.bin"
    
    text_processor = TextVectorizer(model_path, articles_dir)
    article_data = text_processor.get_article_vectors()
    
    for filename, content, vector in article_data:
        # Save each article and its vector to the database
        article = Article(filename=filename, content=content, vector=np.array(vector).tobytes())
        article.save()
    
    return render(request, 'texts.html', {"message": "Articles saved to database."})