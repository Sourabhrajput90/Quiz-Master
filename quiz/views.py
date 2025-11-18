from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from io import TextIOWrapper
from django.utils.timezone import now
from datetime import timedelta


from quiz.models import Quiz,Leaderboard , Profile ,QuizAttempt

def homepage(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

@login_required
def account(request):
    return render(request, "account.html")

@login_required
def leaderboard(request):
    leaderboard_data = Leaderboard.objects.select_related('user', 'quiz').order_by('-score', '-percentage', '-timestamp')

    return render(request, 'leaderboard.html', {'scores': leaderboard_data, "hide_footer" : True} )




@login_required
def profile(request):
    user = request.user
    
    profile = Profile.objects.filter(user=user).first()

    
    quiz_history = Leaderboard.objects.filter(user=user).order_by('-timestamp')

    return render(request, "profile.html", {
        "user": user,
        "profile": profile,
        "quiz_history": quiz_history,

    })



def loginx(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Minimum length validation
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, "login.html")

        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()
    return render(request, "quiz.html", {"quiz": quiz, "questions": questions})

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

def sign(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Password length check
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, "sign.html")

        # Confirm password check
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "sign.html")

        # Username exists check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, "sign.html")

        # Email exists check
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "sign.html")

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Account created successfully! Please login now.")
        return redirect("login")

    return render(request, "sign.html")



def logout_user(request):
    logout(request)
    return redirect('login')

def submit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    attempt, created = QuizAttempt.objects.get_or_create(user=request.user, quiz=quiz, defaults={'start_time': now()})

    quiz_end_time = attempt.start_time + timedelta(minutes=quiz.duration)
    if now() > quiz_end_time:
        return render(request, 'quiz_result.html', {'message': '⏳ Time is up! Quiz auto-submitted.'})

    score = 0
    total_questions = questions.count()

    for question in questions:
        selected_option = request.POST.get(f'question_{question.id}')
        correct_option = question.correct_option.strip().lower() if question.correct_option else ""

        if selected_option and selected_option.strip().lower() == correct_option:
            score += 1

    attempt.end_time = now()
    attempt.score = score
    attempt.total_questions = total_questions
    attempt.percentage = (score / total_questions) * 100 if total_questions > 0 else 0
    attempt.save()

    leaderboard_entry = Leaderboard.objects.filter(user=request.user, quiz=quiz).first()

    if leaderboard_entry:
        leaderboard_entry.score = score
        leaderboard_entry.total_questions = total_questions
        leaderboard_entry.percentage = attempt.percentage
    else:
        leaderboard_entry = Leaderboard.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            total_questions=total_questions,
            percentage=attempt.percentage
        )

    leaderboard_entry.save()

    return redirect('leaderboard')



@login_required
def quiz_result(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    user_score = Leaderboard.objects.filter(user=request.user, quiz=quiz).order_by('-timestamp').first()

    if not user_score:
        return redirect('quiz_detail', quiz_id=quiz_id)

    return render(request, 'quiz_result.html', {'quiz': quiz, 'user_score': user_score})



def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()  
    return render(request, "quiz.html", {"quiz": quiz, "questions": questions})


@login_required
def update_profile(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        return redirect('profile') 

    return redirect('profile')  


def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Get or create an attempt for the user
    attempt, created = QuizAttempt.objects.get_or_create(user=request.user, quiz=quiz)

    # If the attempt already exists, redirect to the quiz page
    if not created:
        return redirect('quiz_page', quiz_id=quiz.id)  # Ensure 'quiz_page' exists in urls.py

    return render(request, 'quiz/start_quiz.html', {'quiz': quiz, 'attempt': attempt})




def delete_quiz_attempt(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempt = QuizAttempt.objects.filter(user=request.user, quiz=quiz).first()

    if attempt:
        attempt.delete()

        # Also remove from leaderboard
        leaderboard_entry = Leaderboard.objects.filter(user=request.user, quiz=quiz).first()
        if leaderboard_entry:
            leaderboard_entry.delete()

    return redirect('quiz_list')  # Redirect to quiz list after deletion



