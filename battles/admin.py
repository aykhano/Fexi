from django.contrib import admin
from .models import Warrior, Question, Answer, Battle

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1
    min_num = 2  # Hər sual üçün ən az 2 cavab tələb olunur

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'subject', 'difficulty', 'answer_count')
    list_filter = ('subject', 'difficulty')
    search_fields = ('text',)
    inlines = [AnswerInline]
    
    def answer_count(self, obj):
        return obj.answer_set.count()
    answer_count.short_description = 'Cavab Sayı'

@admin.register(Warrior)
class WarriorAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'experience', 'coins', 'power_score')
    list_filter = ('level',)
    search_fields = ('name',)
    readonly_fields = ('power_score',)
    
    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': ('name', 'level', 'experience', 'coins')
        }),
        ('Bacarıqlar', {
            'fields': ('analytic_power', 'quick_think', 'word_mastery', 'research_skill')
        }),
        ('Statistika', {
            'fields': ('power_score',),
            'classes': ('collapse',)
        })
    )
    
    def power_score(self, obj):
        return (obj.analytic_power + obj.quick_think + 
                obj.word_mastery + obj.research_skill) * obj.level
    power_score.short_description = 'Ümumi Güc'

@admin.register(Battle)
class BattleAdmin(admin.ModelAdmin):
    list_display = ('warrior', 'score', 'completed', 'created_at', 'question_count')
    list_filter = ('completed', 'created_at')
    date_hierarchy = 'created_at'
    filter_horizontal = ('questions',)
    
    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Sual Sayı'

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_correct', 'question_text', 'question_subject')
    list_filter = ('is_correct', 'question__subject')
    search_fields = ('text', 'question__text')
    
    def question_text(self, obj):
        return obj.question.text[:50] + '...' if len(obj.question.text) > 50 else obj.question.text
    question_text.short_description = 'Sual'
    
    def question_subject(self, obj):
        return obj.question.get_subject_display()
    question_subject.short_description = 'Fənn'