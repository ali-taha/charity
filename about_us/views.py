from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model()

def about_us(request):
    if request.method == 'GET':
        users = User.objects.all()
        return render(request, 'about_us.html', {'users':users})