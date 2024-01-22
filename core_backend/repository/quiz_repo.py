from django.shortcuts import get_object_or_404
from core_backend.models import QuizModel



def get_quiz_by_id(quiz_id):
    quiz = get_object_or_404(QuizModel, id=quiz_id)
    return quiz


def update_quiz_by_id(quiz_id, data):
    try:
        instance = QuizModel.objects.get(id=quiz_id)
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return True, instance
    except QuizModel.DoesNotExist:
        return False, None