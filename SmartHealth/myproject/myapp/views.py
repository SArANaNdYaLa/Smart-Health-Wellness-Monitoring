from django.shortcuts import render, redirect
import mysql.connector as sql
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import AuthenticationForm

import re


@csrf_protect

def registration(request):
    if request.method == "POST":
        us = request.POST.get('username')
        em = request.POST.get('email')
        ps = request.POST.get('password')
        cpass = request.POST.get('cpassword')

        errors = {}

        try:
            # Open a connection and create a cursor once for both checking and inserting
            conn = sql.connect(host="localhost", user="root", password="******", database="smarthealth")
            cursor = conn.cursor()

            # Check if user already exists in the database
            cursor.execute("SELECT * FROM registration WHERE email = %s", (em,))
            if cursor.fetchone():  # If user already exists
                messages.error(request, "User already registered. Please log in.")
                return redirect('login')  # Redirect to login page if already registered

            # Check if passwords match
            if ps != cpass:
                errors['cpassword_error'] = "Passwords do not match."

            # Shorter password validation checks
            if len(ps) < 6 or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", ps) or not re.search(r"[A-Z]", ps) or not re.search(r"[a-z]", ps) or not re.search(r"[0-9]", ps):
                errors['password_error'] = "Password must be at least 6 characters long, with 1 special character, 1 uppercase letter, 1 lowercase letter, and 1 number."

            # If there are any errors, re-render the registration form with errors
            if errors:
                return render(request, 'registration.html', {'errors': errors})

            # Proceed with inserting user details into the database
            comm = "INSERT INTO registration (username, email, password, cpassword) VALUES (%s, %s, %s, %s)"
            cursor.execute(comm, (us, em, ps, cpass))
            conn.commit()

            # Success message and redirect to login page
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')  # Redirect to the login page

        except sql.Error as e:
            messages.error(request, f"Error: {e}")
        finally:
            # Close cursor and connection at the end to ensure cleanup
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render(request, 'registration.html')


def home(request):
    return render(request, 'home.html')

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_protect
import mysql.connector as sql

@csrf_protect
def register(request):
    error_message = ""

    if request.method == "POST":
        # Get the data from the form
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check if the fields are empty
        if not username or not password:
            error_message = "Username and password are required."
            return render(request, 'registration/register.html', {"error_message": error_message})

        # Hash the password before storing it in the database
        hashed_password = make_password(password)

        # Connect to the database
        conn = None
        cursor = None

        try:
            conn = sql.connect(
                host="localhost",
                user="root",
                password="*21ht1A4342*",
                database="smarthealth"
            )
            cursor = conn.cursor()

            # Check if the username already exists
            query = "SELECT * FROM registration WHERE username = %s"
            cursor.execute(query, (username,))
            if cursor.fetchone():
                error_message = "Username already exists."
                return render(request, 'registration/register.html', {"error_message": error_message})

            # Insert the new user data into the database with the hashed password
            insert_query = "INSERT INTO registration (username, password) VALUES (%s, %s)"
            cursor.execute(insert_query, (username, hashed_password))
            conn.commit()

            return redirect('login')  # Redirect to login page after successful registration

        except sql.Error as e:
            error_message = "An error occurred during registration."
            print(f"Database error: {e}")
        finally:
            # Close the database connection
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render(request, 'registration/register.html', {"error_message": error_message})


@csrf_protect
def login(request):
    error_message = ""
    
    if request.method == "POST":
        # Connect to the database
        try:
            conn = sql.connect(host="localhost", user="root", password="******", database="smarthealth")
            cursor = conn.cursor()
            
            # Get the data from the form
            username = request.POST.get("username")
            password = request.POST.get("password")
            
            print("Login attempt with username:", username, "and password:", password)  # Debugging print statement
            
            # Retrieve the user data from the database
            query = "SELECT password FROM registration WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            
            if result:
                # If a record is found, check if the password matches
                db_password = result[0]
                print("Password in database:", db_password)  # Debugging print statement
                
                if db_password == password:
                    print("Login successful")  # Debugging print statement
                    # Clear any unread results to avoid errors when closing
                    cursor.fetchall()  # Ensures all results are read
                    return redirect('features')  # Redirect to home page on successful login
                else:
                    error_message = "Invalid password."
            else:
                error_message = "Username not found."
                
        except sql.Error as e:
            print("Database error:", e)
            error_message = "Database error. Please try again later."
        
        finally:
            # Ensure all results are processed before closing
            cursor.fetchall()  # Clears any remaining results
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    # Pass the error message to the template if login fails
    return render(request, 'login.html', {"error_message": error_message})


from django.http import HttpResponseForbidden

def csrf_failure(request, reason=""):
    return HttpResponseForbidden("Custom CSRF failure message.")


from django.shortcuts import render
from .forms import HealthDataForm

def healthinsights(request):
    if request.method == 'POST':
        # If the form is submitted
        form = HealthDataForm(request.POST)
        if form.is_valid():
            # If the form is valid, process the data
            heart_rate = form.cleaned_data['heart_rate']
            sleep_duration = form.cleaned_data['sleep_duration']
            steps = form.cleaned_data['steps']
            calories_burned = form.cleaned_data['calories_burned']
            water_intake = form.cleaned_data['water_intake']
            
            # Pass the data to the template for display
            return render(request, 'healthinsights.html', {
                'form': form,
                'heart_rate': heart_rate,
                'sleep_duration': sleep_duration,
                'steps': steps,
                'calories_burned': calories_burned,
                'water_intake': water_intake,
            })
    else:
        # If it's a GET request, show an empty form
        form = HealthDataForm()

    return render(request, 'healthinsights.html', {'form': form})



from django.shortcuts import render
from .models import Doctor, Patient

from .models import Doctor, Patient, Appointment  # Import the Appointment model

def dashboard(request):
    # Get counts for doctors, patients, and appointments
    total_doctors = Doctor.objects.count()
    total_patients = Patient.objects.count()
    total_appointments = Appointment.objects.count()  # Count of appointments

    # Fetch recent doctors, patients, and appointments with relevant fields
    recent_doctors = Doctor.objects.all().order_by('-id')[:3]  # Limit to the latest 3 doctors
    recent_patients = Patient.objects.all().order_by('-id')[:3]  # Limit to the latest 3 patients
    # recent_appointments = Appointment.objects.all().order_by('-appointment_date')[:3]  # Latest 3 appointments
    recent_appointments = Appointment.objects.all().order_by('-appointment_date')[:3]  # Latest 3 appointments

    # Context to pass to the template
    context = {
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'recent_doctors': recent_doctors,
        'recent_patients': recent_patients,
        'recent_appointments': recent_appointments,
    }

    return render(request, 'dashboard.html', context)

from .models import WellnessTransaction
from django.db.models import Q

def wellnesstracking(request):
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        transactions = WellnessTransaction.objects.filter(
            Q(category__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    else:
        transactions = WellnessTransaction.objects.all()

    # Pass transactions to the template
    return render(request, 'wellnesstracking.html', {
        'transactions': transactions,
        'search_query': search_query
    })
    

def features(request):
    return render(request, 'features.html')


import matplotlib
matplotlib.use('Agg')  # This sets the backend to Agg, which doesn't require a GUI

from django.shortcuts import render, redirect
from .forms import HealthDataForm, GoalsForm
import matplotlib.pyplot as plt
import io
import base64
import datetime

# Create charts for the metrics
def create_chart(data, title, labels, colors, chart_type='bar', ylabel=None):
    fig, ax = plt.subplots()
    if chart_type == 'bar':
        ax.bar(labels, data, color=colors)
    elif chart_type == 'plot':
        ax.plot(labels, data, marker='o', color=colors[0])
    if ylabel:
        ax.set_ylabel(ylabel)
    ax.set_title(title)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_str

# Function to generate recommendations based on health data
def generate_recommendations(heart_rate, sleep_duration, steps, water_intake):
    recommendations = []

    # Heart rate recommendations
    if heart_rate < 60:
        recommendations.append("Your heart rate is low. You may want to check with a healthcare provider.")
    elif 60 <= heart_rate <= 100:
        recommendations.append("Your heart rate is in the normal range. Keep up the good work!")
    else:
        recommendations.append("Your heart rate is high. Relaxation exercises or consulting a doctor may help.")

    # Sleep recommendations
    if sleep_duration < 7:
        recommendations.append("You are getting insufficient sleep. Aim for at least 7-8 hours of sleep per night.")
    elif 7 <= sleep_duration <= 9:
        recommendations.append("Your sleep duration is optimal. Maintain your sleep hygiene.")
    else:
        recommendations.append("You are oversleeping. Try to keep a consistent sleep schedule.")

    # Steps recommendations
    if steps < 5000:
        recommendations.append("Your activity level is low. Aim to take at least 10,000 steps daily for better health.")
    elif 5000 <= steps < 10000:
        recommendations.append("You are moderately active. Consider increasing your activity to reach 10,000 steps daily.")
    else:
        recommendations.append("You are very active. Great job maintaining a healthy lifestyle!")

    # Water intake recommendations
    if water_intake < 2:
        recommendations.append("Your water intake is low. Aim to drink at least 2-3 liters of water daily.")
    elif 2 <= water_intake <= 3:
        recommendations.append("Your water intake is sufficient. Stay hydrated!")
    else:
        recommendations.append("Your water intake is high. Ensure you are not overhydrating.")

    return recommendations

# Health insights page for entering data
def healthinsights(request):
    form = HealthDataForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        # Process form and store in session
        request.session['heart_rate'] = form.cleaned_data['heart_rate']
        request.session['sleep_duration'] = form.cleaned_data['sleep_duration']
        request.session['steps'] = form.cleaned_data['steps']
        request.session['calories_burned'] = form.cleaned_data['calories_burned']
        request.session['water_intake'] = form.cleaned_data['water_intake']

        # Set default goals if not set
        request.session.setdefault('steps_goal', 10000)
        request.session.setdefault('sleep_goal', 8.0)
        request.session.setdefault('water_goal', 2.5)

        return redirect('visualizations')  # Redirect to visualizations page
    return render(request, 'healthinsights.html', {'form': form})

# Visualizations page view for displaying charts and health insights
def visualizations(request):
    heart_rate = request.session.get('heart_rate')
    sleep_duration = request.session.get('sleep_duration')
    steps = request.session.get('steps')
    water_intake = request.session.get('water_intake')

    # Generate charts
    heart_rate_chart = create_chart([70, heart_rate], 'Heart Rate', ['Normal Range', 'Your Value'], ['b'])
    sleep_chart = create_chart([8, sleep_duration], 'Sleep Duration', ['Normal Range', 'Your Sleep'], ['g', 'r'])
    steps_chart = create_chart([10000, steps], 'Steps Taken', ['Target Steps', 'Your Steps'], ['g', 'b'])
    water_chart = create_chart([2.5, water_intake], 'Water Intake', ['Normal Intake', 'Your Water'], ['g', 'b'])

    # Generate recommendations
    recommendations = generate_recommendations(heart_rate, sleep_duration, steps, water_intake)

    return render(request, 'visualizations.html', {
        'heart_rate_chart': heart_rate_chart,
        'sleep_chart': sleep_chart,
        'steps_chart': steps_chart,
        'water_chart': water_chart,
        'recommendations': recommendations
    })


# Goal setting and display page view
def set_goals(request):
    # Initialize default goals if not already set
    if 'steps_goal' not in request.session:
        request.session['steps_goal'] = 10000  # Default goal for steps
    if 'sleep_goal' not in request.session:
        request.session['sleep_goal'] = 8.0  # Default goal for sleep
    if 'water_goal' not in request.session:
        request.session['water_goal'] = 2.5  # Default goal for water intake

    form = GoalsForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        # Save goals to the session
        steps_goal = form.cleaned_data['steps_goal']
        sleep_goal = form.cleaned_data['sleep_goal']
        water_goal = form.cleaned_data['water_goal']

        # Get current date
        goal_date = datetime.date.today()

        # Convert the date to string before storing
        goal_date_str = goal_date.strftime('%Y-%m-%d')

        # Append the goals to the session history (convert date to string)
        if 'goal_history' not in request.session:
            request.session['goal_history'] = []

        goal_history = request.session['goal_history']

        # Keep only the last 5 goals
        if len(goal_history) >= 5:
            goal_history.pop(0)

        goal_history.append({
            'steps_goal': steps_goal,
            'sleep_goal': sleep_goal,
            'water_goal': water_goal,
            'date': goal_date_str  # Storing as string
        })

        # Save the updated goal history in session
        request.session['goal_history'] = goal_history

        # Redirect to goals page to display updated goals
        return redirect('goals_page')

    return render(request, 'set_goals.html', {'form': form})

# View to display user's goals in a tabular format
def goals_page(request):
    # Retrieve the last 5 goals from the session
    goal_history = request.session.get('goal_history', [])

    # Convert the stored string date back to a datetime.date object for display
    for goal in goal_history:
        goal['date'] = datetime.datetime.strptime(goal['date'], '%Y-%m-%d').date()

    return render(request, 'goals_page.html', {
        'goal_history': goal_history
    })
