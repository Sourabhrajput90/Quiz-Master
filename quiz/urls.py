
from django.urls import path
from quiz import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.homepage, name="home"),
    path("about", views.about, name="about"),
    path("leaderboard", views.leaderboard, name="leaderboard"),
    path("profile", views.profile, name="profile"),
    path("login", views.loginx, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("quiz/", views.quiz_list, name='quiz_list'),
    path("sign", views.sign, name="sign"),
    path("account", views.account, name="account"),
    path("quiz/<int:quiz_id>/", views.quiz_detail, name='quiz_detail'),
    path("quiz/<int:quiz_id>/submit/", views.submit_quiz, name='submit_quiz'),
    path('profile/', views.update_profile, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),  # Correct URL pattern
    path('quiz/<int:quiz_id>/delete/', views.delete_quiz_attempt, name='delete_quiz_attempt'),
    path('quiz/<int:quiz_id>/start/', views.start_quiz, name='start_quiz'),  # Ensure this exists
    
    path("quiz/<int:quiz_id>/result/", views.quiz_result, name='quiz_result'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
