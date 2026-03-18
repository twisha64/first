from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .sudoku import generate_sudoku
from .models import GameScore
import json
from .solver import solve

# ===============================
# DASHBOARD
# ===============================
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")

    scores = GameScore.objects.filter(user=request.user).order_by("-score")

    return render(request, "dashboard.html", {
        "scores": scores
    })

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "Username already exists"
            })

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect("dashboard")

    return render(request, "signup.html")


# ===============================
# LOGIN
# ===============================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, "login.html", {
                "error": "Invalid login"
            })

        login(request, user)
        return redirect("dashboard")

    return render(request, "login.html")


# ===============================
# LOGOUT
# ===============================
def logout_view(request):
    logout(request)
    return redirect("login")


# ===============================
# HOME (GAME PAGE)
# ===============================
def home(request):
    level = request.GET.get("level", "easy")

    puzzle, solution = generate_sudoku(level=level)

    highscore = None
    if request.user.is_authenticated:
        best = GameScore.objects.filter(user=request.user).order_by("-score").first()
        if best:
            highscore = best.score

    request.session["puzzle"] = puzzle
    request.session["solution"] = solution
    request.session["score"] = 0
    request.session["hints_left"] = 3
    request.session["level"] = level
    request.session.modified = True

    return render(request, "index.html", {
        "board": puzzle,
        "hints_left": 3,
        "score": 0,
        "highscore": highscore,
        "level": level
    })


# ===============================
# CHECK SOLUTION
# ===============================
def check_solution(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"})

    try:
        user_board = json.loads(request.POST.get("board"))
    except:
        return JsonResponse({"error": "Invalid board data"})

    solution = request.session.get("solution")
    puzzle = request.session.get("puzzle")

    if not solution or not puzzle:
        return JsonResponse({"error": "Game session expired"})

    result = []

    for r in range(9):
        row = []
        for c in range(9):

            if puzzle[r][c] != 0:
                row.append("fixed")

            elif user_board[r][c] == 0:
                row.append("empty")

            elif user_board[r][c] == solution[r][c]:
                row.append("correct")

            else:
                row.append("wrong")

        result.append(row)

    return JsonResponse({"result": result})


# ===============================
# HINT SYSTEM
# ===============================
@csrf_exempt
def hint(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"})

    hints_left = request.session.get("hints_left", 0)

    if hints_left <= 0:
        return JsonResponse({"error": "No hints left"})

    try:
        row = int(request.POST.get("row"))
        col = int(request.POST.get("col"))
    except:
        return JsonResponse({"error": "Invalid cell"})

    puzzle = request.session.get("puzzle")
    solution = request.session.get("solution")

    if not puzzle or not solution:
        return JsonResponse({"error": "Game session expired"})

    if puzzle[row][col] != 0:
        return JsonResponse({"error": "Fixed cell"})

    # reduce hints
    request.session["hints_left"] -= 1

    # deduct score
    score = request.session.get("score", 0) - 10
    request.session["score"] = score
    request.session.modified = True

    return JsonResponse({
        "value": solution[row][col],
        "hints_left": request.session["hints_left"],
        "score": score
    })


# ===============================
# UPDATE SCORE
# ===============================
@csrf_exempt
def update_score(request):
    if request.method == "POST":

        try:
            data = json.loads(request.body)
            change = int(data.get("change", 0))
        except:
            change = int(request.POST.get("change", 0))

        current_score = request.session.get("score", 0)
        current_score += change

        request.session["score"] = current_score
        request.session.modified = True

        return JsonResponse({"score": current_score})

    return JsonResponse({"error": "Invalid request"})

# ===============================
# SAVE SCORE TO DATABASE
# ===============================
@csrf_exempt
@csrf_exempt
def save_score(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"})

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"})

    score = request.session.get("score", 0)
    level = request.session.get("level", "easy")
    time_taken = int(request.POST.get("time", 0))

    print("Saving score:", score)  # DEBUG

    GameScore.objects.create(
        user=request.user,
        score=score,
        time_taken=time_taken,
        level=level
    )

    return JsonResponse({"status": "saved"})

def solve_board(request):
    if request.method == "POST":
        board = json.loads(request.POST.get("board"))
        solve(board)
        return JsonResponse({"solution": board})
