from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import models
import datetime as dt
from accounts.models import User
from classes.models import Class, Enrollment, ClassHistory
from studios.models import Studio
from subscriptions.models import UserMemberships


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'


class EnrolUserSerializer(serializers.ModelSerializer):
    # CLASSES = Class.objects.values_list('name', 'name').distinct()
    # dummy = [["1", "2"], ["2", "3"]]
    options = [
        ['enroll', "Enroll"], ["drop", "Drop"], ["drop_all", "Drop All"], ["enroll_all", "Enroll All"]
    ]
    _enrolled = serializers.CharField(default="None", max_length=30)
    _enroll_or_drop = serializers.ChoiceField(choices=options, default="None")

    class Meta:
        model = Enrollment
        fields = ('_enrolled', '_enroll_or_drop')

    def save(self, user_id, class_id):
        print(self.validated_data)
        try:
            _c2 = Class.objects.filter(id=class_id)
            _c = Class.objects.filter(name=self.validated_data['_enrolled'])
            if not _c:
                raise serializers.ValidationError({"Message": "Wrong Class Name or ID"})

            if _c[0].name != _c2[0].name:
                raise serializers.ValidationError({"Message": "Wrong Class Name or ID"})

            user = User.objects.filter(id=user_id)
            if not user:
                raise serializers.ValidationError({"Message": "User does not exist"})

            user_mem = UserMemberships.objects.filter(user=user[0].id)
            if not user_mem:
                raise serializers.ValidationError({"Message": "User Membership does not exist"})

            # Case for enroll
            if self.validated_data['_enroll_or_drop'] == 'enroll':
                c = Class.objects.get(id=class_id)  # Every object that has the name gym
                # if user and studio and _class and user_mem and user_mem.isActiveMembership:
                if user_mem[0].isActiveMembership:
                    check_space = c.capacity
                    if check_space - 1 >= 0:
                        e = Enrollment.objects.create(_user=user[0], _enrolled=c,
                                                      _enroll_or_drop=self.validated_data['_enroll_or_drop'],
                                                      _start_time=c.start_time,
                                                      _start_recursion=c.start_recursion)
                        e.save()
                        h = ClassHistory.objects.create(User=e,
                                                        Enrollment_Status=self.validated_data['_enroll_or_drop'],
                                                        Name=c.name, Coach=c.coach, Keywords=c.keywords,
                                                        Studio=studio[0], Start_Time=c.start_time,
                                                        End_Time=c.end_time, Start_Recursion=c.start_recursion,
                                                        End_Recursion=c.end_recursion)
                        h.save()
                        c.capacity -= 1
                        c.save(update_fields={'capacity': c.capacity})
                        return e
                else:
                    raise serializers.ValidationError({"Message": "Full Class"})
            # Case for enroll_all
            elif self.validated_data['_enroll_or_drop'] == 'enroll_all':
                if user_mem[0].isActiveMembership:
                    single = Class.objects.get(id=class_id)
                    many = Class.objects.filter(name=single.name)
                    for c in many:
                        check = c.capacity
                        if check - 1 >= 0:
                            e = Enrollment.objects.create(_user=user[0], _enrolled=c,
                                                          _enroll_or_drop=self.validated_data['_enroll_or_drop'],
                                                          _start_time=c.start_time,
                                                          _start_recursion=c.start_recursion)
                            e.save()
                            h = ClassHistory.objects.create(User=e,
                                                            Enrollment_Status=self.validated_data['_enroll_or_drop'],
                                                            Name=c.name, Coach=c.coach, Keywords=c.keywords,
                                                            Studio=studio[0], Start_Time=c.start_time,
                                                            End_Time=c.end_time, Start_Recursion=c.start_recursion,
                                                            End_Recursion=c.end_recursion)
                            h.save()
                            c.capacity -= 1
                        else:
                            raise serializers.ValidationError({"Message": "Full Class"})
                        c.save(update_fields={'capacity': c.capacity})
            # drop
            elif self.validated_data['_enroll_or_drop'] == 'drop':
                c = Class.objects.get(id=class_id)  # Every object that has the name gym

                eligible_for_drop = Enrollment.objects.filter(_user=user[0].id)
                if not eligible_for_drop:
                    raise serializers.ValidationError({"Message": "You are not Enrolled in this Class!"})

                if user_mem[0].isActiveMembership:
                    print(self.validated_data['_enroll_or_drop'])
                    e = Enrollment.objects.create(_user=user[0], _enrolled=c,
                                                  _enroll_or_drop=self.validated_data['_enroll_or_drop'],
                                                  _start_time=c.start_time,
                                                  _start_recursion=c.start_recursion)
                    e.save()
                    h = ClassHistory.objects.create(User=e,
                                                    Enrollment_Status=self.validated_data['_enroll_or_drop'],
                                                    Name=c.name, Coach=c.coach, Keywords=c.keywords,
                                                    Studio=studio[0], Start_Time=c.start_time,
                                                    End_Time=c.end_time, Start_Recursion=c.start_recursion,
                                                    End_Recursion=c.end_recursion)
                    h.save()
                    c.capacity += 1
                    c.save(update_fields={'capacity': c.capacity})
                    return e
            else:
                if user_mem[0].isActiveMembership:

                    eligible_for_drop = Enrollment.objects.filter(_user=user[0].id)
                    if not eligible_for_drop:
                        raise serializers.ValidationError({"Message": "You are not Enrolled in this Class!"})

                    single = Class.objects.get(id=class_id)
                    many = Class.objects.filter(name=single.name)
                    for c in many:
                        e = Enrollment.objects.create(_user=user[0], _enrolled=c,
                                                      _enroll_or_drop=self.validated_data['_enroll_or_drop'],
                                                      _start_time=c.start_time,
                                                      _start_recursion=c.start_recursion
                                                      )
                        e.save()
                        h = ClassHistory.objects.create(User=e,
                                                        Enrollment_Status=self.validated_data['_enroll_or_drop'],
                                                        Name=c.name, Coach=c.coach, Keywords=c.keywords,
                                                        Studio=studio[0], Start_Time=c.start_time,
                                                        End_Time=c.end_time, Start_Recursion=c.start_recursion,
                                                        End_Recursion=c.end_recursion)
                        h.save()
                        c.capacity += 1
                        c.save(update_fields={'capacity': c.capacity})
            return
        except Http404:
            raise serializers.ValidationError('Class doesnt exist!')


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassHistory
        fields = '__all__'
