from django.conf import settings
from django.db import models

# Create your models here.
class Statemodel(models.Model):
    Stateid = models.AutoField(primary_key=True,unique = True)
    States = models.CharField(max_length=100,verbose_name='State Name')
    is_active = models.BooleanField(default=True)
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name='Created On')
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Added By')
    ModifiedDate = models.DateTimeField(blank=True, null=True, verbose_name='Modified On')
    ModifiedBy = models.CharField(max_length=250, blank=True, null=True, verbose_name='Modified By')

    class Meta:
        db_table = 'StateTbl'
        verbose_name = 'State List'
        verbose_name_plural = 'State List'

    def __str__(self):
        return self.States

    def save_model(self, request, obj, form, change):
        obj.added_by = str(request.user)
        super().save_model(request, obj, form, change)

class TournamentModel(models.Model):
    Tourid =  models.AutoField(primary_key=True,unique = True)
    TournamentName = models.CharField(max_length=250,verbose_name='Tournament Name')
    RegStartDate = models.DateField(verbose_name='Registration Start Date')
    RegEndDate = models.DateField(verbose_name='Registration End Date')
    TournamentStartDate = models.DateField(verbose_name='Tournament Start Date')
    TournamentEndDate = models.DateField(verbose_name='Tournament End Date')
    AllowedTeams = models.IntegerField(verbose_name='Team Registration Restriction')
    Venue = models.ForeignKey(Statemodel,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name='Created On')
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Added By')
    ModifiedDate = models.DateTimeField(blank=True, null=True, verbose_name='Modified On')
    ModifiedBy = models.CharField(max_length=250, blank=True, null=True, verbose_name='Modified By')

    class Meta:
        db_table = 'TournamentTbl'
        verbose_name = 'Tournament List'
        verbose_name_plural = 'Tournament List'

    def __str__(self):
        return self.TournamentName

    def save_model(self, request, obj, form, change):
        obj.added_by = str(request.user)
        super().save_model(request, obj, form, change)

class RegisteredTournamentModel(models.Model):
    id =  models.AutoField(primary_key=True,unique = True)
    TournamentName = models.ForeignKey(TournamentModel,on_delete=models.CASCADE)
    TeamName = models.CharField(max_length=255,unique=True,verbose_name='Team Name')
    CoachName = models.CharField(max_length=255,verbose_name='Coach Name')
    ManagerName = models.CharField(max_length=255,verbose_name='Manager Name')
    RegiserStatus = models.BooleanField(default=True,verbose_name='Register Status')
    is_active = models.BooleanField(default=True)
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name='Created On')
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Added By')
    ModifiedDate = models.DateTimeField(blank=True, null=True, verbose_name='Modified On')
    ModifiedBy = models.CharField(max_length=250, blank=True, null=True, verbose_name='Modified By')

    class Meta:
        db_table = 'RegisteredTournamentTbl'
        verbose_name = 'Registered List'
        verbose_name_plural = 'Registered List'

    def __str__(self):
        return self.TeamName

    def save_model(self, request, obj, form, change):
        obj.added_by = str(request.user)
        super().save_model(request, obj, form, change)

class MatchSchedule(models.Model):
    id = models.AutoField(primary_key=True,unique = True)
    TournametId = models.ForeignKey(TournamentModel,on_delete=models.CASCADE,verbose_name="TournamentID",null=True,blank=True)
    Team1 = models.ForeignKey(RegisteredTournamentModel,on_delete=models.CASCADE,verbose_name="Team1 Name",related_name="Team1")
    Team2 = models.ForeignKey(RegisteredTournamentModel,on_delete=models.CASCADE,verbose_name="Team2 Name",related_name="Team2")
    GameDate = models.DateField()
    is_active = models.BooleanField(default=True)
    CreatedDate = models.DateTimeField(auto_now_add=True, verbose_name='Created On')
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Added By')
    ModifiedDate = models.DateTimeField(blank=True, null=True, verbose_name='Modified On')
    ModifiedBy = models.CharField(max_length=250, blank=True, null=True, verbose_name='Modified By')

    class Meta:
        db_table = 'MatchScheduleTbl'
        verbose_name = 'Match Schedule List'
        verbose_name_plural = 'Match Schedule List'

    def __str__(self):
        return str(self.Team1)+"/VS/ "+str(self.Team2)

    def save_model(self, request, obj, form, change):
        obj.added_by = str(request.user)
        super().save_model(request, obj, form, change)
