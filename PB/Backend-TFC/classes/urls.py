from django.urls import path, re_path
from classes.api.views import ViewClassAPIVIew, EnrollmentAPIView, HistoryAPIView, SearchByName, SearchByCoach, \
    SearchByDate, SearchByTime, FilterView, ScheduleAPIView, ShowEveryClassAPIView, ShowEveryClassPagniatedAPIView

app_name = 'classes'

urlpatterns = [
    path('<int:user_id>/<int:studio_id>/class/all/', ViewClassAPIVIew.as_view(), name='view_all_class'),
    path('all/', ShowEveryClassAPIView.as_view(), name='all'),
    path('paginated-all/', ShowEveryClassPagniatedAPIView.as_view(), name='all'),
    path('<int:user_id>/class/<int:id>/enroll-drop/', EnrollmentAPIView.as_view(), name='enroll'),
    path('<int:user_id>/class/history/', HistoryAPIView.as_view(), name='history'),
    path('<int:user_id>/class/my_schedule/', ScheduleAPIView.as_view(), name='schedule'),
    path('search/<int:studio_id>/name/<str:name>/', SearchByName.as_view(), name='search_name'),
    path('search/<int:studio_id>/coach/<str:coach>/', SearchByCoach.as_view(), name='search_name'),
    path('search/<int:studio_id>/date/<str:date>/', SearchByDate.as_view(), name='search_name'),
    path('search/<int:studio_id>/time/<str:time1>/to/<str:time2>/', SearchByTime.as_view(), name='search_name'),
    # re_path(r'^filter/(?P<studio_id>\w{0,50}/)/$', FilterView.as_view())
    # tr has to be e.g 06x00x00-08x00x00_etc
    path('filter/<int:studio_id>/<slug:class_names>/<slug:coach_names>/<slug:dates>/<slug:tr>/', FilterView.as_view())
]
