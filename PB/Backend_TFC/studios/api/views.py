from rest_framework.generics import get_object_or_404, RetrieveAPIView, ListAPIView
from studios.api.serializers import StudioSerializer, StudioPageSerializer, AmenitiesSerializer, ClassSerializer
from studios.api.pagination import FilterPagination, ListPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from studios.models import Studio, Amenities, Image
from classes.models import Class
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import filters

from math import sin, cos, sqrt, atan2, radians

class SearchCoachAPIView(ListAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['coach']

class SearchClassAPIView(ListAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class SearchAmenityAPIView(ListAPIView):
    queryset = Amenities.objects.all()
    serializer_class = AmenitiesSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['type']

class SearchStudioAPIView(ListAPIView):
    queryset = Studio.objects.all()
    serializer_class = StudioPageSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class FilterStudioAPIView(ListAPIView):
    pagination_class = FilterPagination
    serializer_class = StudioSerializer
    #permission_classes = [IsAuthenticated, ]
    
    def get_queryset(self):
        all_studios = Studio.objects.all()
        return all_studios

    def get(self, request, *args, **kwargs):
        all_ids = Studio.objects.values_list('id')

        studio_names = (self.kwargs['studio_name']).replace('_', ' ').split("-")
        amenities = (self.kwargs['types']).replace('_', ' ').split("-")
        class_names = (self.kwargs['class_names']).replace('_', ' ').split("-")
        coaches = (self.kwargs['coaches']).replace('_', ' ').split("-")

        if amenities == ['', '']:
            studio_ids_amenities = all_ids
        else:
            filter_amenities = {}
            for i in range(len(amenities)):
                filter_amenities[i] = Amenities.objects.filter(type=amenities[i]).values_list('studio')
            filter_amenities[len(amenities)] = filter_amenities[len(amenities)-1] 
            for i in range(len(amenities)):
                filter_amenities[i+1] = set(filter_amenities[i]) & set(filter_amenities[i+1])
            studio_ids_amenities = filter_amenities[len(amenities)]

        if studio_names == ['', '']:
            studio_ids_snames = all_ids
        else:
            filter_snames = {}
            for i in range(len(studio_names)):
                filter_snames[i] = Studio.objects.filter(name=studio_names[i]).values_list('id')
            filter_snames[len(studio_names)] = filter_snames[len(studio_names)-1] 
            for i in range(len(studio_names)):
                filter_snames[i+1] = set(filter_snames[i]) | set(filter_snames[i+1])
            studio_ids_snames = filter_snames[len(studio_names)]

        if class_names == ['', '']:
            studio_ids_cnames = all_ids
        else:
            filter_cnames = {}
            for i in range(len(class_names)):
                filter_cnames[i] = Class.objects.filter(name=class_names[i]).values_list('studio')
            filter_cnames[len(class_names)] = filter_cnames[len(class_names)-1] 
            for i in range(len(class_names)):
                filter_cnames[i+1] = set(filter_cnames[i]) | set(filter_cnames[i+1])
            studio_ids_cnames = filter_cnames[len(class_names)]
        
        if coaches == ['', '']:
            studio_ids_coaches = all_ids
        else:
            filter_coaches = {}
            for i in range(len(coaches)):
                filter_coaches[i] = Class.objects.filter(coach=coaches[i]).values_list('studio')
            filter_coaches[len(coaches)] = filter_coaches[len(coaches)-1] 
            for i in range(len(coaches)):
                filter_coaches[i+1] = set(filter_coaches[i]) | set(filter_coaches[i+1])
            studio_ids_coaches = filter_coaches[len(coaches)]

        data = set(studio_ids_snames) & set(studio_ids_cnames) & set(studio_ids_amenities) & set(studio_ids_coaches) 
        filtered_studios = []
        for x in data:
            filtered_studios.append(Studio.objects.get(id=x[0]))

        return Response(StudioPageSerializer(filtered_studios, many=True).data)
        #return self.get_paginated_response(self.paginate_queryset(StudioPageSerializer(filtered_studios, many=True).data))


class ViewStudioAPIView(RetrieveAPIView):
    queryset = Studio.objects.all()
    serializer_class = StudioPageSerializer
    #permission_classes = [IsAuthenticated, AllowAny]

    def get_queryset(self):
        all_studios = Studio.objects.all()
        return all_studios

    def get(self, request, *args, **kwargs):
        studio_for_page = get_object_or_404(Studio, pk=self.kwargs['studio_id'])

        data = {}
        data['name'] = studio_for_page.name
        data['address'] = studio_for_page.address
        data['latitude'] = str(studio_for_page.latitude)
        data['longitude'] = str(studio_for_page.longitude)

        try:
            studio_image = Image.objects.filter(studio=studio_for_page)
        except Image.DoesNotExist:
            data['image'] = "No Images"

        else:
            set_of_images = {"http://127.0.0.1:8000"+i.image.url for i in studio_image}
            data['image'] = set_of_images

        try:
            studio_ammenities = Amenities.objects.filter(studio=studio_for_page)
        except Amenities.DoesNotExist:
            data['type'] = "No Ammenities"
            return Response(data)

        else: 
            set_of_ammenities = {(i.type, i.quantity) for i in studio_ammenities}
            data['ammenities'] = set_of_ammenities

        data['directions'] = "https://www.google.com/maps/dir/?api=1&origin="+str(studio_for_page.longitude)+","+str(studio_for_page.latitude)+"&destination="

        return Response(data)

class StudiosByProximityAPIView(ListAPIView):

    serializer_class = StudioSerializer
    #permission_classes = [IsAuthenticated, AllowAny]
    permission_classes = [AllowAny]
    pagination_class = ListPagination
    lookup_field = 'user_id'

    def get_queryset(self):
        all_studios = Studio.objects.all()
        return all_studios

    def get(self, request, *args, **kwargs):
        longitude = kwargs['longitude']
        latitude = kwargs['latitude']

        R = 6373.0

        lat1 = radians(52.2296756)
        lon1 = radians(21.0122287)
        lat2 = radians(52.406374)
        lon2 = radians(16.9251681)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        ids = (kwargs['ids']).split("-")
        #print(ids)
        queryset = Studio.objects.filter(id__in=ids).values_list('name', 'longitude', 'latitude', 'address', 'id', flat=False)

        qs = list(queryset)
        
        for x in range (len(qs)):

            R = 6373.0

            lat1 = radians(float(qs[x][2]))
            lon1 = radians(float(qs[x][1]))
            lat2 = radians(float(latitude))
            lon2 = radians(float(longitude))

            dlon = lon2 - lon1
            dlat = lat2 - lat1

            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            distance = R * c
            qs[x] = qs[x] + (str(distance),)

        sorted_by_prox = sorted(qs, key=lambda tup: float(tup[5]))
        ordered_studios = []
        
        for i in range(len(sorted_by_prox)):
            d = {}
            d['id'] = sorted_by_prox[i][4]
            d['name'] = sorted_by_prox[i][0]
            d['address'] = sorted_by_prox[i][3]
            dis = float(sorted_by_prox[i][5])
            dis = str(round(dis, 2))

            d['distance'] = dis
            d['latitude'] = sorted_by_prox[i][2]
            d['longitude'] = sorted_by_prox[i][1]
            ordered_studios.append(d)

        #return Response(StudioSerializer(ordered_studios, many=True).data)
        return self.get_paginated_response(self.paginate_queryset(StudioSerializer(ordered_studios, many=True).data))