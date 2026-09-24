from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from ads.models import Ad, Review
from .forms import AdForm, ReviewForm, RegisterForm, LoginForm


def index(request):
    """Главная страница."""
    ads = Ad.objects.all()[:6]
    return render(request, 'index.html', {'ads': ads})


def ad_list(request):
    queryset = Ad.objects.all()

    search = request.GET.get('search', '').strip()
    if search:
        queryset = queryset.filter(Q(title__icontains=search))

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        queryset = queryset.filter(price__gte=min_price)
    if max_price:
        queryset = queryset.filter(price__lte=max_price)

    ad_type = request.GET.get('type')
    if ad_type:
        queryset = queryset.filter(type=ad_type)

    paginator = Paginator(queryset, 4)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search': search,
        'min_price': min_price or '',
        'max_price': max_price or '',
        'ad_type': ad_type or '',
    }
    return render(request, 'ads/list.html', context)


def ad_detail(request, pk):
    """Одно объявление с отзывами."""
    ad = get_object_or_404(Ad, pk=pk)
    reviews = ad.reviews.all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Войдите, чтобы оставить отзыв')
            return redirect('web:login')

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.ad = ad
            review.save()
            messages.success(request, 'Отзыв добавлен')
            return redirect('web:ad-detail', pk=pk)
    else:
        form = ReviewForm()

    return render(request, 'ads/detail.html', {
        'ad': ad,
        'reviews': reviews,
        'form': form,
    })


@login_required
def ad_create(request):
    """Создание объявления."""
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()
            messages.success(request, 'Объявление создано')
            return redirect('web:ad-detail', pk=ad.pk)
    else:
        form = AdForm()

    return render(request, 'ads/form.html', {'form': form, 'action': 'Создать'})


@login_required
def ad_update(request, pk):
    """Редактирование объявления."""
    ad = get_object_or_404(Ad, pk=pk)

    if ad.author != request.user and request.user.role != 'admin':
        messages.error(request, 'Нет прав')
        return redirect('web:ad-detail', pk=pk)

    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Объявление обновлено')
            return redirect('web:ad-detail', pk=pk)
    else:
        form = AdForm(instance=ad)

    return render(request, 'ads/form.html', {'form': form, 'action': 'Редактировать'})


@login_required
def ad_delete(request, pk):
    """Удаление объявления."""
    ad = get_object_or_404(Ad, pk=pk)

    if ad.author != request.user and request.user.role != 'admin':
        messages.error(request, 'Нет прав')
        return redirect('web:ad-detail', pk=pk)

    if request.method == 'POST':
        ad.delete()
        messages.success(request, 'Объявление удалено')
        return redirect('web:ad-list')

    return render(request, 'ads/confirm_delete.html', {'ad': ad})


def register(request):
    """Регистрация."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна')
            return redirect('web:index')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    """Вход."""
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы вошли')
            return redirect('web:index')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    """Выход."""
    logout(request)
    messages.success(request, 'Вы вышли')
    return redirect('web:index')


@login_required
def profile(request):
    """Профиль пользователя."""
    my_ads = Ad.objects.filter(author=request.user)
    return render(request, 'users/profile.html', {'my_ads': my_ads})
