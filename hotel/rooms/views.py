from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q


def index(request):
    return render(request, "index.html")