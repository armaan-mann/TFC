from django.http import Http404
from classes.api.pagination import FilterPagination
from rest_framework.pagination import LimitOffsetPagination
from accounts.models import User
from rest_framework.generics import CreateAPIView, get_object_or_404, ListAPIView, RetrieveAPIView, \
    RetrieveUpdateAPIView
from classes.api.serializers import ClassSerializer, EnrolUserSerializer, HistorySerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from classes.models import Class, Enrollment, ClassHistory
from studios.models import Studio
from itertools import chain
from django.db.models import Q, F


# Create your views here.

class ViewClassAPIVIew(ListAPIView):
    serializer_class = ClassSerializer
    queryset = Class.objects.all()
    permission_classes = (AllowAny, IsAuthenticated)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        try:
            user = get_object_or_404(User, pk=self.kwargs['user_id'])
            studio = get_object_or_404(Studio, pk=self.kwargs['studio_id'])
            print(studio)
            if user and studio:
                all_class_times = Class.objects.filter(studio=studio.id).order_by('start_time')
                if all_class_times:
                    return all_class_times
                else:
                    return Response({"Message": "OR No class is registered within the studio"}, status=403)
        except Http404:
            return Response({"Message", "User or Studio not registered "},
                            status=404)


class EnrollmentAPIView(RetrieveUpdateAPIView):
    serializer_class = EnrolUserSerializer
    queryset = Class.objects.all()
    permission_classes = (AllowAny, IsAuthenticated)
    lookup_field = 'id'

    def perform_update(self, serializer):
        c = Class.objects.filter(id=self.kwargs['id'])
        # print("C", c)
        if not c:
            raise Http404("Class doesnt exist")
        return serializer.save(self.kwargs['user_id'], self.kwargs['id'])

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = get_object_or_404(self.get_queryset(), pk=self.kwargs['id'])
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            instance = self.perform_update(serializer)
            _ = EnrolUserSerializer(instance)
        return Response({"Success": "Drop or Enrolled was Successful!"})


class HistoryAPIView(ListAPIView):
    serializer_class = HistorySerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        user = User.objects.filter(id=self.kwargs['user_id'])
        if not user:
            raise Http404

        enrollment = Enrollment.objects.filter(_user=user[0].id).order_by('_start_recursion', '_start_time')
        if not enrollment:
            if not user:
                raise Http404
        class_history = []
        for e in enrollment:
            check = ClassHistory.objects.filter(User=e.id)
            if check:
                class_history += ClassHistory.objects.filter(User=e.id).order_by('Name')
        return class_history


class ScheduleAPIView(ListAPIView):
    serializer_class = HistorySerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        user = User.objects.filter(id=self.kwargs['user_id'])
        if not user:
            raise Http404

        enrollment = Enrollment.objects.filter(_user=user[0].id, _is_active=True).order_by('_start_recursion',
                                                                                           '_start_time')
        if not enrollment:
            if not user:
                raise Http404
        class_history = []
        for e in enrollment:
            check = ClassHistory.objects.filter(User=e.id)
            if check:
                class_history += ClassHistory.objects.filter(User=e.id).order_by('Name')
        return class_history


class SearchByName(ListAPIView):
    serializer_class = ClassSerializer
    permission = [AllowAny, ]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        studio = Studio.objects.filter(id=self.kwargs['studio_id'])

        if not studio:
            raise Http404({"Message": "Wrong studio id"})
        class_search = Class.objects.filter(studio=studio[0], name=self.kwargs['name']).order_by('start_recursion',
                                                                                                 'start_time')
        return class_search


class SearchByCoach(ListAPIView):
    serializer_class = ClassSerializer
    permission = [AllowAny, ]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        studio = Studio.objects.filter(id=self.kwargs['studio_id'])
        if not studio:
            raise Http404({"Message": "Wrong studio id"})
        class_search = Class.objects.filter(studio=studio[0], coach=self.kwargs['coach']).order_by('start_recursion',
                                                                                                   'start_time')
        return class_search


class SearchByDate(ListAPIView):
    serializer_class = ClassSerializer
    permission = [AllowAny, ]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        studio = Studio.objects.filter(id=self.kwargs['studio_id'])
        if not studio:
            raise Http404({"Message": "Wrong studio id"})
        class_search1 = Class.objects.filter(studio=studio[0], start_recursion=self.kwargs['date']).order_by(
            'start_recursion',
            'start_time')
        return class_search1


class SearchByTime(ListAPIView):
    serializer_class = ClassSerializer
    permission = [AllowAny, ]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        studio = Studio.objects.filter(id=self.kwargs['studio_id'])
        # print(self.kwargs)
        if not studio:
            raise Http404({"Message": "Wrong studio id"})
        class_search1 = Class.objects.filter(studio=studio[0], start_time=self.kwargs['time1'])
        class_search2 = Class.objects.filter(studio=studio[0], start_time=self.kwargs['time2'])
        combine = class_search1.union(class_search2).order_by('start_recursion',
                                                              'start_time')
        return combine


class FilterView(ListAPIView):
    serializer_class = ClassSerializer
    permission = [AllowAny, ]
    pagination_class = FilterPagination

    def get_queryset(self):
        all_classes = Class.objects.filter(id=self.kwargs['studio_id'])
        return all_classes

    def get(self, request, *args, **kwargs):

        all_classes = Class.objects.filter(studio=self.kwargs['studio_id'])

        class_names = (self.kwargs['class_names']).split("_")
        coache_names = (self.kwargs['coach_names']).split("_")
        dates = (self.kwargs['dates']).split("_")
        tr = (self.kwargs['tr']).replace('x', ':').split("_")
        if class_names == ['', '']:
            studio_ids_class_names = all_classes.values_list('id')
        else:
            filter_class_name = {}
            for i in range(len(class_names)):
                filter_class_name[i] = all_classes.filter(name=class_names[i]).values_list('id')
            filter_class_name[len(class_names)] = filter_class_name[len(class_names) - 1]

            for i in range(len(class_names)):
                filter_class_name[i + 1] = set(filter_class_name[i]) | set(filter_class_name[i + 1])
            studio_ids_class_names = filter_class_name[len(class_names)]

        if coache_names == ['', '']:
            studio_ids_coache_names = all_classes.values_list('id')
        else:
            filter_coache_names = {}
            for i in range(len(coache_names)):
                filter_coache_names[i] = all_classes.filter(coach=coache_names[i]).values_list('id')
            filter_coache_names[len(coache_names)] = filter_coache_names[len(coache_names) - 1]
            for i in range(len(coache_names)):
                filter_coache_names[i + 1] = set(filter_coache_names[i]) | set(filter_coache_names[i + 1])
            studio_ids_coache_names = filter_coache_names[len(coache_names)]

        if dates == ['', '']:
            studio_ids_dates = all_classes.values_list('id')
        else:
            filter_dates = {}
            for i in range(len(dates)):
                filter_dates[i] = all_classes.filter(start_recursion=dates[i]).values_list('id')
            filter_dates[len(dates)] = filter_dates[len(dates) - 1]
            for i in range(len(dates)):
                filter_dates[i + 1] = set(filter_dates[i]) | set(filter_dates[i + 1])
            studio_ids_dates = filter_dates[len(dates)]

        if tr == ['', '']:
            studio_ids_tr = all_classes.values_list('id')
        else:
            filter_tr = {}
            for i in range(len(tr)):
                time_range = tr[i].split('-')
                start_time = time_range[0]
                end_time = time_range[1]
                intermediate = all_classes.filter(Q(end_time__lte=F('end_time')),
                                                  Q(end_time__lte=end_time))

                filter_tr[i] = intermediate.filter(Q(start_time__gte=F('start_time')),
                                                   Q(start_time__gte=start_time)).values_list('id')
            filter_tr[len(tr)] = filter_tr[len(tr) - 1]
            for i in range(len(tr)):
                filter_tr[i + 1] = set(filter_tr[i]) | set(filter_tr[i + 1])
            studio_ids_tr = filter_tr[len(tr)]

        data = set(studio_ids_class_names) & set(studio_ids_coache_names) & set(studio_ids_dates) & set(studio_ids_tr)
        filtered_studios = []
        for x in data:
            filtered_studios.append(all_classes.get(id=x[0]))

        return self.get_paginated_response(self.paginate_queryset(ClassSerializer(filtered_studios, many=True).data))
