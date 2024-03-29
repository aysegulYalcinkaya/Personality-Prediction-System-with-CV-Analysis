from django.shortcuts import render
from django.http import JsonResponse

from .models import Question, UserResponse, UserScore


def personality_test(request):
    questions = Question.objects.all()
    user = request.user
    personality_test_score=UserScore.objects.filter(user__id=user.id)

    if request.method == 'POST':

        responses = {}

        for question in questions:
            response_key = f'response-{question.id}'
            response_value = request.POST.get(response_key)

            if response_value:
                score = int(response_value)
                category = question.category

                if category not in responses:
                    responses[category] = {'total_score': 0, 'count': 0}

                responses[category]['total_score'] += score
                responses[category]['count'] += 1

                UserResponse.objects.create(user=user, question=question, response=score)

        # Calculate average scores for each category
        average_scores = {category: (data['total_score'] / data['count']) if data['count'] > 0 else 0 for
                          category, data in responses.items()}
        userScore=UserScore()
        userScore.user=user
        userScore.neuroticism=average_scores["neuroticism"]
        userScore.extroversion = average_scores["extroversion"]
        userScore.openness = average_scores["openness"]
        userScore.agreeableness = average_scores["agreeableness"]
        userScore.conscientiousness = average_scores["conscientiousness"]
        print (userScore)
        userScore.save()
        return JsonResponse({"msg":"Personality Test saved"})

    context = {'questions': questions,'personality':(len(personality_test_score))}
    return render(request, 'personality_test.html', context)
