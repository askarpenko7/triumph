import json
import random

from django.shortcuts import render, get_list_or_404

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

from django.contrib.auth import logout

from triumph_app.models import Challenge


@login_required(login_url='/auth/login/')
def index(request):
    challenges = Challenge.objects.all().filter().order_by('theme__theme_title')
    return render(request, 'index.html', {'challenges': challenges})


@login_required(login_url='/auth/login/')
def challenge_view(request, theme_id, level):
    challenges = get_list_or_404(Challenge, theme_id=theme_id, level=level)
    random_challenge = random.choice(challenges)

    response_data = {
        'result': 'Success',
        'challenge_id': random_challenge.pk,
        'sequence': random_challenge.sequence
    }

    if request.is_ajax():
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        return HttpResponse('Nothing happened. Go away')
