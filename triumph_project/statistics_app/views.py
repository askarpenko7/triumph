import datetime
import json

from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import render, get_list_or_404, get_object_or_404
from statistics_app.models import StudentAnswer, Session
from triumph_app.models import Challenge, Theme
from django.contrib.auth.decorators import login_required
from django.utils import timezone


@login_required(login_url='/auth/login/')
def empty_statistics(request):
    groups_for_template = []
    all_users = []
    groups = []
    if request.user.is_staff:
        groups_for_template = Group.objects.all()
        groups = Group.objects.all()
        for group in groups:
            all_users = User.objects.filter(groups__pk=group.id)
    else:
        all_users.append(request.user)
        groups.append(request.user.groups)

    return render(request, 'statistics.html', {'users': all_users,
                                               'groups': groups_for_template})


@login_required(login_url='/auth/login/')
def statistics(request, group_id, student_id, date_start, date_end):
    groups_for_template = []
    all_users = []
    groups = []
    if request.user.is_staff:
        groups_for_template = Group.objects.all()
        if group_id == 'g_all':
            groups = Group.objects.all()
        else:
            groups = Group.objects.filter(pk=group_id)
        if student_id == 's_all':
            for group in groups:
                all_users = User.objects.filter(groups__pk=group.id)
        else:
            for group in groups:
                all_users = User.objects.filter(groups__pk=group.id, pk=student_id)
    else:
        all_users.append(request.user)
        groups.append(request.user.groups)

    if date_start == 'm_ago':
        date_start_formatted = timezone.now() - datetime.timedelta(days=30)
    else:
        date_start_formatted = datetime.datetime.strptime(date_start, '%d-%m-%Y')

    if date_end == 'today':
        date_end_formatted = timezone.now()
    else:
        date_end_formatted = datetime.datetime.strptime(date_end, '%d-%m-%Y')

    students = []
    for user in all_users:
        sessions = get_user_sessions(user, date_start_formatted, date_end_formatted)
        if len(sessions) > 0:
            students.append({
                'user_id': user.id,
                'user_name': user.username,
                'user_rows': count_user_rows(sessions),
                'sessions': sessions,
            })
    return render(request, 'statistics.html', {'students': students,
                                               'groups': groups_for_template,
                                               'users': all_users})


def get_user_sessions(user, date_start, date_end):
    result = []
    user_sessions = list(Session.objects.filter(student=user, session_start_at__range=(date_start, date_end)))
    for session in user_sessions:
        themes = get_user_answers_by_sessions(session)
        if len(themes) > 0:
            result.append({
                'session_id': session.id,
                'start_at': session.session_start_at,  # datetime_handler(session.session_start_at),
                'end_at': session.session_end_at,  # datetime_handler(session.session_end_at),
                'session_rows': count_session_rows(themes),
                'themes': themes,
                'total': count_user_totals(themes)
            })
    return result


def get_user_answers_by_sessions(session):
    user_answers = list(StudentAnswer.objects.filter(session=session))
    result = []
    set_themes = set()
    list_themes_level = []

    for answer in user_answers:
        set_themes.add(answer.challenge.theme)
    themes = list(set_themes)

    for theme in themes:
        right_answer_by_theme = 0
        wrong_answer_by_theme = 0
        need_to_add = False
        for answer in user_answers:
            if answer.challenge.theme == theme:
                need_to_add = True
                if answer.is_Right_Answer:
                    right_answer_by_theme += 1
                else:
                    wrong_answer_by_theme += 1

                list_themes_level.append({'theme_id': answer.challenge.theme.id, 'level': answer.challenge.level})

        if need_to_add:
            result.append({
                'theme': {
                    'theme_name': theme.theme_title,
                    'right_answers': right_answer_by_theme,
                    'wrong_answers': wrong_answer_by_theme,
                    'percent': count_percent(right_answer_by_theme, wrong_answer_by_theme),
                    'levels': get_count_answers_by_theme_level(theme.id, get_unique(list_themes_level), user_answers)
                }
            })

    return result


def get_count_answers_by_theme_level(current_theme, themes_level, user_answers):
    result = []
    list_themes_level = []
    for l in themes_level:
        need_to_add = False
        right_answer = 0
        wrong_answer = 0
        if current_theme == l.get('theme_id'):
            for answer in user_answers:
                if l.get('level') == answer.challenge.level and l.get('theme_id') == answer.challenge.theme.id:
                    need_to_add = True
                    if answer.is_Right_Answer:
                        right_answer += 1
                    else:
                        wrong_answer += 1

                    list_themes_level.append({
                        'theme_id': answer.challenge.theme.id,
                        'level': answer.challenge.level,
                    })

            if need_to_add:
                result.append({
                    'level': l.get('level'),
                    'right_answers': right_answer,
                    'wrong_answers': wrong_answer,
                    'percent': count_percent(right_answer, wrong_answer),
                })

    return result


def count_percent(r, w):
    percent = 0
    if r != 0 or w != 0:
        percent = r / (r + w) * 100

    if percent < 0:
        percent = 0

    return round(percent, 2)


def get_unique(_items):
    result = []
    seen = set()
    for _item in _items:
        t = tuple(_item.items())
        if t not in seen:
            seen.add(t)
            result.append(_item)
    return result


def datetime_handler(dt):
    if isinstance(dt, datetime.datetime):
        return dt.isoformat()
    raise TypeError('Unknown datetime format')


def count_user_rows(sessions):
    rows = 0
    for session in sessions:
        rows += count_session_rows(session['themes'])

    if rows == 0:
        rows = 1
    return rows


def count_session_rows(themes):
    rows = len(themes)  # count themes
    for theme in themes:
        rows += len(theme['theme']['levels'])  # count levels
    if rows == 0:
        rows = 1
    return rows + 1  # count answers +1 totals row


def count_user_totals(themes):
    w = 0
    r = 0

    for theme in themes:
        for level in theme['theme']['levels']:
            r += level['right_answers']
            w += level['wrong_answers']

    result = {
        'total_right_answers': r,
        'total_wrong_answers': w,
        'total_percent': count_percent(r, w)
    }

    return result


@login_required(login_url='/auth/login/')
def start_statistic(request):
    if request.method == 'POST':
        session_start_at = request.POST.get('session_start_at')
        session_end_at = request.POST.get('session_end_at')
        session = Session(student=request.user, session_start_at=session_start_at, session_end_at=session_end_at)
        session.save()

        response_data = {'result': 'Session created successful', 'session_id': session.pk,
                         'start_at': session.session_start_at, 'end_at': session.session_end_at}

        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json'
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


@login_required(login_url='/auth/login/')
def update_statistic_time(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        session_end_at = request.POST.get('session_end_at')

        session = get_object_or_404(Session, pk=session_id)
        session.session_end_at = session_end_at
        session.save(update_fields=["session_end_at"])

        response_data = {'result': 'Session updated successful'}

        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json'
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


@login_required(login_url='/auth/login/')
def add_answer(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        challenge_id = request.POST.get('challenge_id')
        is_right_answer = request.POST.get('is_right')
        session = get_object_or_404(Session, pk=session_id)
        challenge = get_object_or_404(Challenge, pk=challenge_id)
        answer = StudentAnswer(session=session, challenge=challenge, is_Right_Answer=is_right_answer)
        answer.save()

        response_data = {'result': 'Answer saved successful'}

        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json'
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


@login_required(login_url='/auth/login/')
def get_filters_data(request, group_id):
    users = []
    if request.user.is_staff:
        if group_id == 'g_all':
            groups = Group.objects.all()
        else:
            groups = Group.objects.filter(pk=group_id)

        for group in groups:
            users = User.objects.filter(groups__pk=group.id)
    else:
        users.append(request.user)

    students = []
    for user in users:
        students.append({
            'user_id': user.id,
            'user_name': user.username,
        })

    response_data = {
        'result': 'Success',
        'users': students
    }

    if request.is_ajax():
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        return HttpResponse('Nothing happened. Go away')
