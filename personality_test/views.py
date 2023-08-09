from django.shortcuts import render
from django.http import JsonResponse

from .models import Question, UserResponse


def personality_test(request):
    questions = Question.objects.all()

    if request.method == 'POST':
        user = request.user
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

        return JsonResponse(average_scores)

    context = {'questions': questions}
    return render(request, 'personality_test.html', context)
