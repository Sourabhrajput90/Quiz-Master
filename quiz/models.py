from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="quiz_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(help_text="Duration in minutes", default=10) 
    start_time = models.DateTimeField(default=now, help_text="Quiz Start Time")


    def __str__(self):
        return self.title

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=255)

    def __str__(self):
        return self.question


class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    percentage = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score', '-percentage', '-timestamp']  

    
    def save(self, *args, **kwargs):
        if self.total_questions is None:
            self.total_questions = 0  
        
        if self.score is None:
            self.score = 0  

        if self.total_questions > 0:
            self.percentage = round((self.score / self.total_questions) * 100, 2)
        else:
            self.percentage = 0

        super().save(*args, **kwargs)  
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}/{self.total_questions}"




class Userscore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}"




class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')

    def __str__(self):
        return self.user.username



class QuizAttempt(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"
