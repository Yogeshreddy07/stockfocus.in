from django.shortcuts import render

def learn_with_ai_view(request):
    return render(request, 'learn_with_ai/learn_with_ai.html')
