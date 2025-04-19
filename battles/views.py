from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Warrior, Question, Answer, Battle
import random

def index(request):
    warrior = Warrior.objects.first()
    if not warrior:
        warrior = Warrior.objects.create(name="Sənin Döyüşçü")
    
    context = {
        'warrior': warrior,
        'battles': Battle.objects.filter(warrior=warrior).order_by('-created_at')[:5]
    }
    return render(request, 'battles/index.html', context)

def arena(request):
    warrior = Warrior.objects.first()
    return render(request, 'battles/arena.html', {'warrior': warrior})

from django.shortcuts import redirect

def start_battle(request):
    warrior = Warrior.objects.first()
    questions = list(Question.objects.all())
    
    if len(questions) < 5:
        # Əgər kifayət qədər sual yoxdursa, nümunə suallar yaradırıq
        sample_questions = [
            {
                'text': '2 + 2 neçə edir?',
                'subject': 'math',
                'difficulty': 1,
                'answers': [
                    {'text': '3', 'correct': False},
                    {'text': '4', 'correct': True},
                    {'text': '5', 'correct': False},
                ]
            },
            # Daha çox nümunə suallar əlavə edə bilərsiniz
        ]
        
        for q in sample_questions:
            question = Question.objects.create(
                text=q['text'],
                subject=q['subject'],
                difficulty=q['difficulty']
            )
            for a in q['answers']:
                Answer.objects.create(
                    question=question,
                    text=a['text'],
                    is_correct=a['correct']
                )
        
        questions = list(Question.objects.all())
    
    selected_questions = random.sample(questions, min(5, len(questions)))
    battle = Battle.objects.create(warrior=warrior)
    battle.questions.set(selected_questions)
    battle.save()
    
    # Yeni döyüşə yönləndir
    return redirect('get_question', battle_id=battle.id, question_num=1)

def get_question(request, battle_id, question_num):
    battle = get_object_or_404(Battle, id=battle_id)
    questions = battle.questions.all()
    
    if question_num < 1 or question_num > len(questions):
        return JsonResponse({'error': 'Invalid question number'}, status=400)
    
    question = questions[question_num-1]
    answers = list(question.answer_set.all())

    context = {
        'battle': battle,
        'question': question,
        'answers': answers,
        'question_num': question_num,
        'total_questions': len(questions),
    }

    return render(request, 'battles/battle.html', context)


def submit_answer(request, battle_id, question_num):
    if request.method == 'POST':
        battle = get_object_or_404(Battle, id=battle_id)
        answer_id = request.POST.get('answer_id')
        
        try:
            answer = Answer.objects.get(id=answer_id)
            is_correct = answer.is_correct
            
            if is_correct:
                battle.score += 10 * answer.question.difficulty
                battle.save()
            
            return JsonResponse({
                'correct': is_correct,
                'score': battle.score
            })
        except Answer.DoesNotExist:
            return JsonResponse({'error': 'Invalid answer'}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def complete_battle(request, battle_id):
    battle = get_object_or_404(Battle, id=battle_id)
    warrior = battle.warrior
    
    if not battle.completed:
        battle.completed = True
        battle.save()
        
        # Təcrübə və coin əlavə et
        experience_gained = battle.score // 2
        coins_gained = battle.score // 5
        
        warrior.experience += experience_gained
        warrior.coins += coins_gained
        leveled_up = warrior.add_experience(experience_gained)
        warrior.save()
        
        return JsonResponse({
            'status': 'completed',
            'score': battle.score,
            'experience_gained': experience_gained,
            'coins_gained': coins_gained,
            'leveled_up': leveled_up
        })
    
    return JsonResponse({'status': 'already_completed'})