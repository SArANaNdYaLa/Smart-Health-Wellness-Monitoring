from django import forms

class HealthDataForm(forms.Form):
    heart_rate = forms.IntegerField(label='Heart Rate (bpm)', min_value=0, max_value=200, required=True)
    sleep_duration = forms.FloatField(label='Sleep Duration (hrs)', min_value=0, max_value=24, required=True)
    steps = forms.IntegerField(label='Steps Taken', min_value=0, required=True)
    calories_burned = forms.IntegerField(label='Calories Burned (kcal)', min_value=0, required=True)
    water_intake = forms.FloatField(label='Water Intake (liters)', min_value=0, required=True)

from django import forms

class GoalsForm(forms.Form):
    steps_goal = forms.IntegerField(
        label="Daily Steps Goal",
        min_value=1000,
        max_value=50000,
        initial=10000,
        help_text="Enter your daily steps target (e.g., 10,000)."
    )
    sleep_goal = forms.FloatField(
        label="Sleep Goal (hrs)",
        min_value=4.0,
        max_value=12.0,
        initial=8.0,
        help_text="Enter your sleep target in hours (e.g., 8.0)."
    )
    water_goal = forms.FloatField(
        label="Water Intake Goal (liters)",
        min_value=1.0,
        max_value=5.0,
        initial=2.5,
        help_text="Enter your daily water intake target (e.g., 2.5)."
    )
