from django.shortcuts import render, redirect
from .forms import TeamForm, MatchForm, RegisterForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Team, Match
from collections import defaultdict

def standings_view(request):
    teams = Team.objects.all()
    matches = Match.objects.all().order_by('-date')

    # Struktur data klasemen
    table = defaultdict(lambda: {
        'name': '',
        'played': 0,
        'wins': 0,
        'draws': 0,
        'losses': 0,
        'goals_for': 0,
        'goals_against': 0,
        'goal_diff': 0,
        'points': 0
    })

    for team in teams:
        table[team.id]['name'] = team.name
        table[team.id]['manager'] = team.manager

    for match in matches:
        home = match.home_team
        away = match.away_team
        hs = match.home_score
        as_ = match.away_score

        # Update home team
        table[home.id]['played'] += 1
        table[home.id]['goals_for'] += hs
        table[home.id]['goals_against'] += as_
        if hs > as_:
            table[home.id]['wins'] += 1
            table[home.id]['points'] += 3
        elif hs == as_:
            table[home.id]['draws'] += 1
            table[home.id]['points'] += 1
        else:
            table[home.id]['losses'] += 1

        # Update away team
        table[away.id]['played'] += 1
        table[away.id]['goals_for'] += as_
        table[away.id]['goals_against'] += hs
        if as_ > hs:
            table[away.id]['wins'] += 1
            table[away.id]['points'] += 3
        elif hs == as_:
            table[away.id]['draws'] += 1
            table[away.id]['points'] += 1
        else:
            table[away.id]['losses'] += 1

    # Hitung selisih gol dan ubah ke list
    standings = []
    for team_data in table.values():
        team_data['goal_diff'] = team_data['goals_for'] - team_data['goals_against']
        standings.append(team_data)

    # Urutkan berdasarkan poin, selisih gol, dan gol
    standings.sort(key=lambda x: (x['points'], x['goal_diff'], x['goals_for']), reverse=True)

    return render(request, 'standings.html', {'standings': standings, 'matches': matches})

@login_required
def add_team_view(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('standings')
    else:
        form = TeamForm()
    return render(request, 'add_team.html', {'form': form})

@login_required
def add_match_view(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('standings')
    else:
        form = MatchForm()
    return render(request, 'add_match.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login setelah daftar
            return redirect('standings')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# reset button
from django.contrib import messages

@login_required
def reset_confirm_view(request):
    # Halaman konfirmasi reset
    return render(request, 'reset_confirm.html')

@login_required
def reset_all_view(request):
    if request.method == 'POST':
        Match.objects.all().delete()
        Team.objects.all().delete()
        messages.success(request, 'Semua data telah direset.')
        return redirect('standings')
    else:
        return redirect('reset_confirm')
