from django.db import models
from django.utils import timezone

class Warrior(models.Model):
    name = models.CharField(max_length=100, default="Döyüşçü")
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    coins = models.IntegerField(default=100)
    
    # Bacarıqlar
    analytic_power = models.IntegerField(default=1)
    quick_think = models.IntegerField(default=1)
    word_mastery = models.IntegerField(default=1)
    research_skill = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.name} (Səviyyə {self.level})"
    
    def add_experience(self, points):
        self.experience += points
        level_up_threshold = self.level * 100
        if self.experience >= level_up_threshold:
            self.level += 1
            self.experience = 0
            return True
        return False

class Question(models.Model):
    SUBJECT_CHOICES = [
        ('math', 'Riyaziyyat'),
        ('literature', 'Ədəbiyyat'),
        ('science', 'Elm'),
        ('history', 'Tarix'),
    ]
    
    text = models.TextField()
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    difficulty = models.IntegerField(default=1)  # 1-5 arası
    
    def __str__(self):
        return f"{self.get_subject_display()} sualı (Çətinlik: {self.difficulty})"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.text

class Battle(models.Model):
    warrior = models.ForeignKey(Warrior, on_delete=models.CASCADE, null=True, blank=True)
    questions = models.ManyToManyField(Question)
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)  # auto_now_add əvəzinə default
    
    def __str__(self):
        return f"{self.warrior.name} döyüşü ({self.score} xal)"