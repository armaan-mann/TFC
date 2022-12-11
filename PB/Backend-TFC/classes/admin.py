from django.contrib import admin
from classes.models import Class, Enrollment, ClassHistory

# Register your models here.
# admin.site.register(Class)
admin.site.register(Enrollment)
admin.site.register(ClassHistory)


class ClassesAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if change:
            #
            # print(form.changed_data)
            update_data = {}
            # print(form.cleaned_data)
            for i in form.changed_data:

                update_data[i] = form.cleaned_data[i]
            obj.save(update_fields=update_data)
        else:
            super().save_model(request, obj, form, change)


admin.site.register(Class, ClassesAdmin)
