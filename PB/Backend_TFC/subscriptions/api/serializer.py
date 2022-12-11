import re
from django.db import IntegrityError
import datetime as dt
from django.http import Http404, response
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from accounts.models import User
from classes.models import Enrollment
from subscriptions.models import Plans, UserMemberships, UserPayHistory

credit_card_regex = r"\d{4}[\s\-]*\d{4}[\s\-]*\d{4}[\s\-]*\d{4}"

new = {"15": 'Monthly Plan: $15', "150": "Annually Plan: $150", "200": "Premium Annual Plan"}


class PlanSerialization(serializers.ModelSerializer):
    membership_type = serializers.ChoiceField(
        choices=(("15", 'Monthly Plan: $15'), ("150", "Annually Plan: $150"),
                 ("200", "Premium Annual Panel: $200")))

    class Meta:
        model = Plans
        fields = ('membership_type',)


class UserMembershipSerialization(serializers.ModelSerializer):
    membership = PlanSerialization()
    card_info = serializers.CharField(label='Payment Method', )

    class Meta:
        model = UserMemberships
        fields = ("membership", "card_info")
        depth = 1

    def save(self, _id):
        try:
            print("here")
            user = get_object_or_404(User, pk=_id)
            plan = Plans.objects.create(membership_type=self.validated_data["membership"]['membership_type'])

            if plan.membership_type == '150' or plan.membership_type == '200':
                plan.duration = 365
            else:
                plan.duration = 30

            plan.save()

            new_arr = self.validated_data['card_info'].split("-")
            credit_card = "".join(new_arr)
            if re.match(credit_card_regex, self.validated_data['card_info']) and len(credit_card) <= 16:
                userMembership = UserMemberships.objects.create(user=user,
                                                                membership=plan,
                                                                card_info=self.validated_data["card_info"],
                                                                amount=plan.membership_type,
                                                                next_payment=(plan.registration_date +
                                                                              dt.timedelta(days=plan.duration)).date())

                userMembership.save()

                history = UserPayHistory.objects.create(User=userMembership,
                                                        username=user.username,
                                                        Membership=new[plan.membership_type],
                                                        Card_info=self.validated_data["card_info"],
                                                        IsActiveMembership=True,
                                                        amount=plan.membership_type,
                                                        Next_payment=((plan.registration_date +
                                                                       dt.timedelta(days=plan.duration)).date())
                                                        )
                history.save()
            else:
                raise serializers.ValidationError("Credit Card Information is Not Valid")
        except (IntegrityError, Http404):
            raise serializers.ValidationError("The user has already been registered to a membership")

        plan.save(), userMembership.save()
        return userMembership


class EditUserMembershipSerialization(serializers.ModelSerializer):
    isActiveMembership = serializers.BooleanField(label="Membership Status \n (Active/Inactive)")
    card_info = serializers.CharField(label='Payment Method', )

    class Meta:
        model = UserMemberships
        fields = ("card_info", "isActiveMembership")

    def save(self, _id):
        print("here")
        correspondingType = {"15": 'Monthly Plan: $15', "150": "Annually Plan: $150", "200": "Premium Annual Plan"}
        user = User.objects.filter(id=_id)
        if not user:
            raise serializers.ValidationError({"Message": "User Does not exist"})
        try:
            membershipStatus = self.validated_data['isActiveMembership']

            if user:
                user_mem = get_object_or_404(UserMemberships, pk=user[0].id)
                plan = user_mem.membership

                if user_mem:
                    if re.match(credit_card_regex, self.validated_data['card_info']) is not None:
                        print("IS valid")
                        user_mem.card_info = self.validated_data['card_info']
                        history = UserPayHistory.objects.create(User=user_mem,
                                                                username=user[0].username,
                                                                Membership=correspondingType
                                                                [user_mem.membership.membership_type],
                                                                Card_info=self.validated_data["card_info"],
                                                                IsActiveMembership=membershipStatus,
                                                                amount=plan.membership_type,
                                                                Next_payment=(plan.registration_date +
                                                                              dt.timedelta(
                                                                                  days=plan.duration)).date()
                                                                )
                        history.save()
                    else:
                        raise serializers.ValidationError("Credit Card Information is Not Valid")

                if not membershipStatus:
                    user_future_classes = Enrollment.objects.filter(_user=user[0].id)
                    for c in user_future_classes:
                        print(c)
                        if c._start_recursion >= history.Next_payment:
                            c._is_active = False
                            c.save()

                if membershipStatus:
                    user_future_classes = Enrollment.objects.filter(_user=user[0].id)
                    for c in user_future_classes:
                        print(c)
                        if c._start_recursion >= history.Next_payment:
                            c._is_active = True
                            c.save()

                user_mem.save()
                return user_mem

        except (IntegrityError, Http404):
            raise serializers.ValidationError("Invalid")


class EditUserPlanSerialization(serializers.ModelSerializer):
    class Meta:
        model = Plans
        fields = ("membership_type",)

    def save(self, _id):
        try:
            user = get_object_or_404(User, pk=_id)
            if user.is_authenticated:
                if user:
                    user_mem = get_object_or_404(UserMemberships, pk=user.id)
                    plan = get_object_or_404(Plans, pk=user_mem.id)
                    if user_mem and plan:
                        if self.validated_data['membership_type'] != "":
                            plan.membership_type = self.validated_data["membership_type"]
                            if plan.membership_type == 150:
                                plan.duration = 365
                            else:
                                plan.duration = 30
                            history = UserPayHistory.objects.create(User=user_mem,
                                                                    username=user.username,
                                                                    Membership=new[
                                                                        self.validated_data["membership_type"]],
                                                                    Card_info=user_mem.card_info,
                                                                    IsActiveMembership=user_mem.isActiveMembership,
                                                                    amount=plan.membership_type,
                                                                    Next_payment=(plan.registration_date +
                                                                                  dt.timedelta(
                                                                                      days=plan.duration)).date()
                                                                    )

                        history.save()
                        plan.save()
                        user_mem.save()
                        user.save()
                        return user_mem
        except (IntegrityError, Http404):
            raise serializers.ValidationError("User not Found")


class UserPayHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPayHistory
        fields = ("username", "Membership", "amount", "Card_info", "IsActiveMembership", "Next_payment",
                  "last_modified")
