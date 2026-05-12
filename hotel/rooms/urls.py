from . import views
from django.urls import path
app_name = 'rooms'


from django.urls import path
from . import views

urlpatterns = [
	path(
        "",
        views.index,
        name="index"
    ),
	path(
        "generate/",
        views.generate_variants,
        name="generate_variants"
    ),
]
