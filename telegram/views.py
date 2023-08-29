from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate
from django.contrib import messages
from django.urls import reverse_lazy
from .models import TelegramUser
from django.http import HttpResponse
import json
# Create your views here.


@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "GET":
        return render(request, template_name='telegram/sign-in.html')

    if request.method == "POST":
        print(request.body)
        data = json.loads(request.body)
        tg_id = data.get('tg_id')
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            tg_user = get_object_or_404(TelegramUser, telegram_id=tg_id)
            tg_user.user_id = user
            tg_user.save()
            return HttpResponse(f"Congrats")  # перенаправление на успешную страницу
        else:
            # Если аутентификация не удалась, можно добавить сообщение об ошибке
            messages.error(request, 'Invalid username or password')
            return redirect(reverse_lazy('telegram:login'))
