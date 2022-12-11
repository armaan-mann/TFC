"""PB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from subscriptions.api.views import PlanAPIView, EditSubscriptionAPIView, EditPlanAPIView, \
    ViewSubscriptionHistoryAPIView
app_name = 'subscriptions'

urlpatterns = [
    path('plans/', PlanAPIView.as_view(), name='plan'),
    path('<int:id>/plans/update-card/', EditSubscriptionAPIView.as_view(), name='update-card_info'),
    path('<int:id>/plans/update-plan/', EditPlanAPIView.as_view(), name='update-plan-type'),
    path('plans/view/<int:id>/', ViewSubscriptionHistoryAPIView.as_view(), name='view'),
]
