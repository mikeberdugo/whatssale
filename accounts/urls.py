from django.urls import path
from .views import login


# afsa fsa asfad 

urlpatterns = [
    path('', login.Login_view , name='login'),

]


urlunpolypatterns =[
        
]

urlpatterns += urlunpolypatterns  
