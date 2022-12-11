from django.http import JsonResponse, Http404
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from subscriptions.api.pagination import CustomPagination
from subscriptions.models import UserMemberships, UserPayHistory
from rest_framework.permissions import AllowAny, IsAuthenticated

from subscriptions.api.serializer import UserMembershipSerialization, \
    EditUserMembershipSerialization, EditUserPlanSerialization, UserPayHistorySerializer

newData = {"15": "Monthly", "150": "Annually"}


class PlanAPIView(CreateAPIView):
    serializer_class = UserMembershipSerialization
    permission_classes = (AllowAny, IsAuthenticated)
    queryset = UserMemberships.objects.all()

    def post(self, request, *args, **kwargs):
        # print(request.data)
        _id = request.user.id
        serializer = UserMembershipSerialization(data=request.data)
        data = {}
        if serializer.is_valid():
            userMembership = serializer.save(_id)
            data['response'] = 'Subscription Added Successfully'
            data['membership_type'] = userMembership.membership.membership_type
            data['duration'] = userMembership.membership.duration
            data["card_info"] = userMembership.card_info
            data['registration_date'] = (userMembership.membership.registration_date).date()
            data['amount'] = str(userMembership.amount)
            data["next_payment"] = userMembership.next_payment
        else:
            data = serializer.errors
        return Response(data)


class ViewSubscriptionHistoryAPIView(ListAPIView):
    page_size = 1
    serializer_class = UserPayHistorySerializer
    permission_classes = [IsAuthenticated, AllowAny]
    pagination_class = CustomPagination

    def get_queryset(self):
        try:
            new_user_mem = UserMemberships.objects.get(user=self.kwargs['id'])
            users_mem = UserPayHistory.objects.filter(User=new_user_mem.id)
            return users_mem
        except (UserMemberships.DoesNotExist, UserPayHistory.DoesNotExist):
            raise Http404({"Message": "User Does not exist"})


class EditSubscriptionAPIView(RetrieveUpdateAPIView):
    serializer_class = EditUserMembershipSerialization
    permission_classes = [IsAuthenticated, ]
    queryset = UserMemberships.objects.all()
    lookup_field = 'id'

    def perform_update(self, serializer):
        return serializer.save(self.kwargs['id'])

    def update(self, request, *args, **kwargs):
        print("update request")
        partial = kwargs.pop('partial', False)
        instance = UserMemberships.objects.filter(user=self.kwargs['id'])

        if not instance:
            return Response({"Message": "User Does not Exist"}, status=404)

        # serializer = UserMembershipSerialization(data=request.data)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            instance = self.perform_update(serializer)
            _ = EditUserMembershipSerialization(instance)
        else:
            data = serializer.errors
        return Response({"Message": "Update was successful!"})


class EditPlanAPIView(RetrieveUpdateAPIView):
    serializer_class = EditUserPlanSerialization
    permission_classes = [IsAuthenticated, ]
    queryset = UserMemberships.objects.all()
    lookup_field = 'id'

    def perform_update(self, serializer):
        return serializer.save(self.kwargs['id'])

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = UserMemberships.objects.filter(user=self.kwargs['id'])
        if not instance:
            return Response({"Message": "User Does not Exist"}, status=404)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=True):
            instance = self.perform_update(serializer)
            _ = EditUserPlanSerialization(instance)
        return Response({"Message": "Update was successful!"})
