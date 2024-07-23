from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Poll


"""
    Standard Django 로 만든 Poll API 
"""
def poll_list(request):
    polls = Poll.objects.all()[:20]
    data = {
        "results": list(polls.values("question", "created_by__username", "pub_date"))
    }
    return JsonResponse(data)


def poll_detail(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    data = {
        "result": {
            "question": poll.question,
            "created_by": poll.created_by.username,
            "pub_date": poll.pub_date,
        }
    }
    return JsonResponse(data)
