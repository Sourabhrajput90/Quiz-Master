from django.contrib import admin
from  quiz.models import Quiz, QuizQuestion , Profile

class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ("question", "quiz", "correct_option")
    search_fields = ("question",)
    list_filter = ("quiz",)

admin.site.register(Quiz)
admin.site.register(QuizQuestion, QuizQuestionAdmin)
admin.site.register(Profile)
