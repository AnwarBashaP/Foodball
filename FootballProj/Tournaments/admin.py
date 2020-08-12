from datetime import datetime

from django.contrib import admin

# Register your models here.
from .models import Statemodel, TournamentModel, RegisteredTournamentModel, MatchSchedule


class StateModalAdmin(admin.ModelAdmin):
    list_display = ('Stateid',
        'States',
        'is_active',
        'ModifiedDate',
        'CreatedDate',
        'ModifiedBy',)

    search_fields = (
        'Stateid',
        'States',
        'is_active',
        'ModifiedDate',
        'CreatedDate',
        'ModifiedBy')

    exclude = ('ModifiedDate', 'added_by', 'ModifiedBy',)

    def save_model(self, request, obj, form, change):
        obj.ModifiedBy = str(request.user)
        obj.ModifiedDate = datetime.now()
        obj.save()

    def has_delete_permission(self, request, obj=None):

        # years = str(obj).split('-')
        #
        if obj != None:

            data = Statemodel.objects.filter(States= obj).values('is_active')
            if data[0]['is_active']:
                return True
        return False

    def delete_model(modeladmin, request, queryset):
        queryset.is_active = False
        queryset.save()


class TournamentModalAdmin(admin.ModelAdmin):
    list_display = ('Tourid',
        'TournamentName','RegStartDate','RegEndDate','TournamentStartDate','TournamentEndDate','AllowedTeams','Venue',
        'is_active',
        'ModifiedDate',
        'CreatedDate',
        'ModifiedBy',)

    search_fields = (
        'Tourid',
        'TournamentName','RegStartDate','RegEndDate','TournamentStartDate','TournamentEndDate','AllowedTeams','Venue',
        'is_active',
        'ModifiedDate',
        'CreatedDate',
        'ModifiedBy',)

    exclude = ('ModifiedDate', 'added_by', 'ModifiedBy',)

    def save_model(self, request, obj, form, change):
        obj.ModifiedBy = str(request.user)
        obj.ModifiedDate = datetime.now()
        obj.save()

    def has_delete_permission(self, request, obj=None):

        # years = str(obj).split('-')
        #
        if obj != None:

            data = TournamentModel.objects.filter(TournamentName= obj).values('is_active')
            if data[0]['is_active']:
                return True
        return False

    def delete_model(modeladmin, request, queryset):
        queryset.is_active = False
        queryset.save()



class RegisteredTournamentModelAdmin(admin.ModelAdmin):
    list_display = ('id',
        'TournamentName','TeamName','CoachName','ManagerName','RegiserStatus',
        'is_active',
        'ModifiedDate',
        'CreatedDate',
        'ModifiedBy',)

    search_fields = ('id',
        'TournamentName','TeamName','CoachName','ManagerName','RegiserStatus',
        'is_active',
        'ModifiedDate',
        'CreatedDate',
        'ModifiedBy',)

    exclude = ('ModifiedDate', 'added_by', 'ModifiedBy',)

    def save_model(self, request, obj, form, change):
        obj.ModifiedBy = str(request.user)
        obj.ModifiedDate = datetime.now()
        obj.save()


    def delete_model(modeladmin, request, queryset):
        queryset.is_active = False
        queryset.save()

class MatchScheduleAdmin(admin.ModelAdmin):
    list_display = ('id','TournametId',
        'Team1','Team2','GameDate',
        'is_active',
        'ModifiedDate',
        'CreatedDate',
        'ModifiedBy',)

    search_fields = ('id','TournametId',
        'Team1','Team2','GameDate',
        'is_active',
        'ModifiedDate',
        'CreatedDate',
        'ModifiedBy',)

    exclude = ('ModifiedDate', 'added_by', 'ModifiedBy',)

    def save_model(self, request, obj, form, change):
        obj.ModifiedBy = str(request.user)
        obj.ModifiedDate = datetime.now()
        obj.save()

admin.site.register(MatchSchedule, MatchScheduleAdmin)
admin.site.register(RegisteredTournamentModel, RegisteredTournamentModelAdmin)
admin.site.register(Statemodel, StateModalAdmin)
admin.site.register(TournamentModel, TournamentModalAdmin)