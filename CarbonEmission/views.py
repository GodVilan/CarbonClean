from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import PasswordResetToken
from .forms import PasswordResetRequestForm, PasswordResetConfirmForm, UserRegisterForm, UserActivityForm
from .models import UserActivity
from .models import SubCategoryEffect, SubCategorySolution
import random
import string
import json
import os
from .models import StepSubCategory, Step

def home(request):
    return redirect('welcome')

def fetch_users(request):
    users = User.objects.all()
    return render(request, 'CarbonEmission/user_list.html', {'users': users})

def welcome(request):
    return render(request, 'CarbonEmission/welcome.html')

def more_info(request):
    return render(request, 'CarbonEmission/more-info.html')

def register(request):
    register_error = None
    register_success = False

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            register_success = True
        else:
            register_error = 'Registration failed. Please correct the errors below.'

    else:
        form = UserRegisterForm()

    return render(request, 'CarbonEmission/register.html', {
        'form': form,
        'register_error': register_error,
        'register_success': register_success
    })

def user_login(request):
    login_error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            user_auth = authenticate(request, username=username, password=password)
            if user_auth is not None:
                login(request, user_auth)
                return redirect('index')
            else:
                login_error = 'Invalid password. Please try again.'
        except User.DoesNotExist:
            login_error = 'Invalid username. Please try again.'

    return render(request, 'CarbonEmission/login.html', {'login_error': login_error})

def generate_confirmation_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

def password_reset_request(request):
    reset_error = None

    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                confirmation_code = generate_confirmation_code(6)
                PasswordResetToken.objects.create(user=user, token=confirmation_code)
                send_mail(
                    'Password Reset Code',
                    f'Your password reset confirmation code is: {confirmation_code}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )

                messages.success(request, 'Confirmation Sent Successfully')

                return render(request, 'CarbonEmission/password_reset.html', {
                    'form': form,
                    'reset_success': True
                })
            else:
                reset_error = 'No user is associated with this email address.'
                messages.error(request, reset_error)

    else:
        form = PasswordResetRequestForm()

    return render(request, 'CarbonEmission/password_reset.html', {
        'form': form,
        'reset_error': reset_error,
        'reset_success': False
    })

def password_reset_confirm(request):
    confirm_error = None

    if request.method == 'POST':
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            new_password = form.cleaned_data['new_password']
            user_token = PasswordResetToken.objects.filter(token=token).first()

            if user_token and user_token.is_valid():
                user = user_token.user
                user.set_password(new_password)
                user.save()
                user_token.is_used = True
                user_token.save()

                messages.success(request, 'Password Reset Successful!')

                return render(request, 'CarbonEmission/password_reset_confirm.html', {'form': form, 'confirm_success': True})

            else:
                confirm_error = 'Invalid or expired token.'
    else:
        form = PasswordResetConfirmForm()

    return render(request, 'CarbonEmission/password_reset_confirm.html', {
        'form': form,
        'confirm_error': confirm_error,
    })


@login_required
def profile(request):
    return render(request, 'CarbonEmission/profile.html')

@login_required
def index(request):
    return render(request, 'CarbonEmission/index.html')

@login_required
def measure(request):
    return render(request, 'CarbonEmission/measure.html')

@login_required
def manage(request):
    user_activities = UserActivity.objects.filter(user=request.user).order_by('id')  # Keeps original order
    total_emission = sum(activity.calculate_emission() for activity in user_activities)

    ranges_file_path = os.path.join(settings.BASE_DIR, 'CarbonEmission', 'static', 'json', 'ranges.json')
    try:
        with open(ranges_file_path, 'r', encoding='utf-8') as ranges_file:
            ranges = json.load(ranges_file)
    except (FileNotFoundError, json.JSONDecodeError):
        ranges = {}
    sum_of_emissions = 0
    for activity in user_activities:
        category_ranges = ranges.get(activity.category, {})
        subcategory_ranges = category_ranges.get(activity.sub_category, {})

        total_emission = activity.calculate_emission()
        sum_of_emissions += total_emission

        try:
            good_limit = subcategory_ranges.get("Good", float('inf'))
            average_limits = subcategory_ranges.get("Average", [float('-inf'), float('inf')])
            worst_limit = subcategory_ranges.get("Worst", 0)

            if total_emission <= good_limit:
                activity.case = "Good"
                activity.css_class = "table-success"
            elif average_limits[0] <= total_emission <= average_limits[1]:
                activity.case = "Average"
                activity.css_class = "table-warning"
            elif total_emission > worst_limit:
                activity.case = "Worst"
                activity.css_class = "table-danger"
            else:
                activity.case = "Uncategorized"
                activity.css_class = ""
        except Exception as e:
            print(f"Error processing activity {activity.id}: {e}")
            activity.case = "Uncategorized"
            activity.css_class = ""

    sum_of_emissions = round(sum_of_emissions, 2)
    return render(request, 'CarbonEmission/manage.html', {
        'activities': user_activities,
        'total_emission': sum_of_emissions,
        'ranges': ranges,
    })

@login_required
def minimize(request):
    return render(request, 'CarbonEmission/minimize.html')

@login_required
def steps_to_minimize(request, sub_category_name, case):
    sub_category = get_object_or_404(StepSubCategory, name=sub_category_name)
    steps = Step.objects.filter(sub_category=sub_category, case=case)

    return render(request, 'CarbonEmission/steps_to_minimize.html', {
        'sub_category': sub_category,
        'case': case,
        'steps': steps,
    })

@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        logout(request)
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user_activities = UserActivity.objects.filter(user=request.user)
    total_emission = sum(activity.calculate_emission() for activity in user_activities)
    total_emission = round(total_emission, 2)
    return render(request, 'CarbonEmission/dashboard.html', {
        'activities': user_activities,
        'total_emission': total_emission
    })

@login_required
def add_activity(request):
    add_activity_error = None

    if request.method == 'POST':
        form = UserActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
            return render(request, 'CarbonEmission/add_activity.html', {
                'form': form,
                'add_activity_success': True
            })
        else:
            add_activity_error = 'Failed to add activity. Please correct the errors below.'

    else:
        form = UserActivityForm()

    return render(request, 'CarbonEmission/add_activity.html', {
        'form': form,
        'add_activity_error': add_activity_error
    })

@login_required
def delete_activity(request, id):
    activity = get_object_or_404(UserActivity, id=id)

    if request.method == 'POST':
        activity.delete()
        return redirect('manage')

    return redirect('manage')

@login_required
def manage_activity(request, sub_category):
    effects = SubCategoryEffect.objects.filter(sub_category=sub_category)
    solutions = SubCategorySolution.objects.filter(sub_category=sub_category)
    
    if effects.exists():
        effect_list = {effect.effect_title: effect.effect_description for effect in effects}
    else:
        effect_list = "No effects data available."

    if solutions.exists():
        solution_list = {solution.solution_title: solution.solution_description for solution in solutions}
    else:
        solution_list = "No solutions data available."

    context = {
        'sub_category': sub_category,
        'effect': effect_list,
        'solution': solution_list,
    }

    return render(request, 'CarbonEmission/minimize.html', context)
