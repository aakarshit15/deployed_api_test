from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path(
        'get_balance_sheet/<str:ticker>/',
        views.get_balance_sheet,
        name="get-balance-sheet"
    ),
    path(
        'get_cash_flow/<str:ticker>/',
        views.get_cash_flow,
        name="get-cash-flow"
    ),
    path(
        'get_historical_data/<str:ticker>/',
        views.get_historical_data,
        name="get-historical-data"
    ),
    path(
        'get_sector_and_industry/<str:ticker>/',
        views.get_sector_and_industry,
        name="get-sector-and-industry"
    ),
    path(
        'get_calendar/<str:ticker>/',
        views.get_calendar,
        name="get-calendar"
    ),
    path(
        'get_news/<str:ticker>/',
        views.get_news,
        name="get-news"
    ),
    path(
        'get_profile/<str:ticker>/',
        views.get_profile,
        name="get-profile"
    ),
]
