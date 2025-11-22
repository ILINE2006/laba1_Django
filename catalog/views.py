from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Question, Vote, Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, QuestionForm


def home(request):
    questions = Question.objects.filter(
        is_active=True,
        expires_at__gt=timezone.now()
    ).order_by('-created_at')

    context = {
        'questions': questions,
    }
    return render(request, 'catalog/home.html', context)


@login_required
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    has_voted = Vote.objects.filter(user=request.user, question=question).exists()

    total_users = User.objects.count()
    vote_percent = (question.votes_count / total_users * 100) if total_users > 0 else 0

    context = {
        'question': question,
        'has_voted': has_voted,
        'vote_percent': round(vote_percent, 1),
        'total_users': total_users,
    }
    return render(request, 'catalog/question_detail.html', context)


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if Vote.objects.filter(user=request.user, question=question).exists():
        messages.error(request, 'Вы уже голосовали за этот вопрос!')
        return redirect('question_detail', pk=question_id)

    Vote.objects.create(user=request.user, question=question)
    question.votes_count += 1
    question.save()

    messages.success(request, 'Ваш голос учтен!')
    return redirect('question_detail', pk=question_id)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            Profile.objects.create(
                user=user,
                avatar=form.cleaned_data['avatar']
            )

            messages.success(request, 'Аккаунт создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'catalog/register.html', {'form': form})


@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Ваш профиль обновлен!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'catalog/profile.html', context)


@login_required
def delete_profile(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Ваш профиль удален.')
        return redirect('home')
    return render(request, 'catalog/delete_profile.html')


@login_required
def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.created_by = request.user
            question.save()

            messages.success(request, 'Вопрос создан!')
            return redirect('home')
    else:
        form = QuestionForm()

    return render(request, 'catalog/create_question.html', {'form': form})