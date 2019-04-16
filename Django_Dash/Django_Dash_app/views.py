from django.shortcuts import render
import Django_Dash_app.dashplotly.dashboard_app

# Create your views here.
def index(request):
    return render(request, "index.html")
