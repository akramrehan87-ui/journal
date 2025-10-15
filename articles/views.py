from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Category
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms_auth import RegisterForm
# 1. Browsing articles
def article_list(request):
    articles = Article.objects.filter().order_by('-created_at')
    return render(request, 'articles/article_list.html', {'articles': articles})


# 2. Reading full article
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'articles/article_detail.html', {'article': article})


# 3. Searching and filtering (bonus)
def article_search(request):
    query = request.GET.get('q')
    articles = Article.objects.filter()
    if query:
        articles = articles.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )
    return render(request, 'articles/article_search.html', {'articles': articles, 'query': query})


# 4. Creating article (Author)
@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'articles/article_form.html', {'form': form})


# 5. Editing article (Author)
@login_required
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk, author=request.user)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/article_form.html', {'form': form})

# 6. Deleting article (Author)
@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk, author=request.user)
    if request.method == 'POST':
        article.delete()
        return redirect('article_list')
    return render(request, 'articles/article_confirm_delete.html', {'article': article})

# Register
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('article_list')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


# Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('article_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# Logout
def logout_view(request):
    logout(request)
    return redirect('article_list')