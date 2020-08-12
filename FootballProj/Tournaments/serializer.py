from rest_framework import serializers


from .models import Statemodel, TournamentModel, RegisteredTournamentModel, MatchSchedule


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statemodel
        exclude = ('is_active', 'CreatedDate', 'added_by', 'ModifiedDate', 'ModifiedBy',)


class TournamentSerializer(serializers.ModelSerializer):
    Venue = StateSerializer()
    class Meta:
        model = TournamentModel
        fields = '__all__'

class TournamentviewSerializer(serializers.ModelSerializer):
    Venue = StateSerializer()
    class Meta:
        model = TournamentModel
        exclude = ('is_active', 'CreatedDate', 'added_by', 'ModifiedDate', 'ModifiedBy',)

class TournamentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredTournamentModel
        exclude = ('CreatedDate', 'added_by', 'ModifiedDate', 'ModifiedBy',)

class RegisterTournamentSerailizer(serializers.ModelSerializer):
    TournamentName = TournamentviewSerializer()
    class Meta:
        model = RegisteredTournamentModel
        exclude = ('CreatedDate', 'added_by', 'ModifiedDate', 'ModifiedBy',)


class MatchSeralizer(serializers.ModelSerializer):
    # TournametId = TournamentRegisterSerializer()
    # Team1 = RegisterTournamentSerailizer()
    # Team2 = RegisterTournamentSerailizer()
    class Meta:
        model = MatchSchedule
        exclude = ('CreatedDate', 'added_by', 'ModifiedDate', 'ModifiedBy',)