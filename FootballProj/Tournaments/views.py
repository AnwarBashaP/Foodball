import itertools
from datetime import datetime, timedelta

from django.db.models import Q
from django.db.models.sql import Query
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import Response
from rest_framework.views import APIView

from .models import TournamentModel, RegisteredTournamentModel, Statemodel, MatchSchedule
from .serializer import TournamentSerializer, TournamentRegisterSerializer, MatchSeralizer


@permission_classes((AllowAny,))
# @permission_classes([IsAuthenticated])
class TournamentDetails(APIView):

    def get(self, request):
        today = datetime.today()
        outputdata = TournamentModel.objects.filter(RegEndDate__gte=today, is_active=True).values('Tourid',
                                                                                                  'TournamentName',
                                                                                                  'RegStartDate',
                                                                                                  'RegEndDate',
                                                                                                  'TournamentStartDate',
                                                                                                  'TournamentEndDate',
                                                                                                  'AllowedTeams',
                                                                                                  'Venue')

        data = []
        if outputdata:
            for values in outputdata:
                Tourid = values['Tourid']
                AllowedTeams = values['AllowedTeams']
                venue = Statemodel.objects.filter(Stateid=values['Venue']).values('States')
                data.append(
                    {"Tourid": Tourid, "AllowedTeams": AllowedTeams, "TournamentName": values['TournamentName'],
                     "RegStartDate": values['RegStartDate'], "RegEndDate": values['RegEndDate'],
                     'TournamentStartDate': values['TournamentStartDate'],
                     'TournamentEndDate': values['TournamentEndDate'], "Venue": venue[0]['States']})

        return Response({"message": data}, status=status.HTTP_200_OK)


@permission_classes((AllowAny,))
# @permission_classes([IsAuthenticated])
class InduvialTournamentDetails(APIView):

    def get(self, request, tourid):
        data = TournamentModel.objects.filter(Tourid=tourid, is_active=True).values('Tourid',
                                                                                    'TournamentName',
                                                                                    'RegStartDate',
                                                                                    'RegEndDate',
                                                                                    'TournamentStartDate',
                                                                                    'TournamentEndDate',
                                                                                    'AllowedTeams', 'Venue')
        registeropenstatus = RegisteredTournamentModel.objects.filter(TournamentName__Tourid=tourid).count()
        register = False
        if data[0]['AllowedTeams'] > registeropenstatus:
            register = True

        return Response({"message": data, "registerstatus": register}, status=status.HTTP_200_OK)


# @permission_classes([IsAuthenticated])
@permission_classes((AllowAny,))
class RegisterTournamentView(generics.ListAPIView):
    today = datetime.today()
    serializer_class = TournamentRegisterSerializer
    queryset = RegisteredTournamentModel.objects.filter(is_active=True).all()

    def post(self, request):
        # try:

            request.POST._mutable = True

            print(request.data)
            # request.data = request.data['data']
            request.data['is_active'] = True
            request.data['RegiserStatus'] = True

            data = TournamentRegisterSerializer(data=request.data['data'])
            if data.is_valid():
                instance = data.save()
                read_serializer = TournamentRegisterSerializer(instance)
            else:
                print("da",data.errors)
                return Response(data.errors,
                                status=status.HTTP_200_OK)

        # except data.DoesNotExist:
        #     return Response({"message": "Some data is missing. please check the datas.","status":"fail"},
        #                     status=status.HTTP_200_OK)

            return Response({"data": read_serializer.data,"status":"pass"}, status=status.HTTP_200_OK)


@permission_classes((AllowAny,))
class TournamentGenerate(APIView):
    def get(self, request):

        startdate = datetime.strptime(str('2020/08/20'),
                                      "%Y/%m/%d")

        outputdata = TournamentModel.objects.filter(is_active=True).values('Tourid', 'AllowedTeams', 'Venue')

        if outputdata:
            for i in outputdata:
                tourid = i['Tourid']
                allowedTeams = i['AllowedTeams']
                registeropenstatus = RegisteredTournamentModel.objects.filter(TournamentName__Tourid=tourid).count()
                registeropenIDs = RegisteredTournamentModel.objects.filter(TournamentName__Tourid=tourid).values_list(
                    'id', flat=True)
                if not MatchSchedule.objects.filter(TournametId=TournamentModel.objects.get(
                        Tourid=tourid)):
                    if registeropenstatus > 0:
                        if allowedTeams == registeropenstatus:
                            combinations = list(itertools.combinations(registeropenIDs, 2))
                            i = 1
                            while len(combinations) > 0:
                                today = startdate
                                previousDay = datetime.strftime(startdate - timedelta(1), '%Y-%m-%d')
                                tomorow = datetime.strftime(startdate + timedelta(1), '%Y-%m-%d')

                                for j in combinations:
                                    val1 = RegisteredTournamentModel.objects.get(id=j[0])
                                    val2 = RegisteredTournamentModel.objects.get(id=j[1])
                                    Matchstatus = MatchSchedule.objects.filter(GameDate=today)

                                    if not Matchstatus:

                                        if not MatchSchedule.objects.filter(Q(
                                                Team2__TeamName=val1) | Q(
                                            Team1__TeamName=val1) | Q(
                                            Team1__TeamName=val2) | Q(
                                            Team2__TeamName=val2), GameDate=previousDay):
                                            MatchSchedule.objects.create(Team1=val1, Team2=val2, GameDate=today,
                                                                         TournametId=TournamentModel.objects.get(
                                                                             Tourid=tourid))
                                            combinations.remove(j)

                                        # else:
                                        #
                                        #     MatchSchedule.objects.create(Team1=val1, Team2=val2, GameDate=tomorow,
                                        #                                  TournametId=TournamentModel.objects.get(
                                        #                                      Tourid=tourid))
                                        #     print(val1, val2, tomorow, today)
                                        #     combinations.remove(j)
                                    else:
                                        i = i + 1
                                        today = datetime.strftime(startdate + timedelta(i), '%Y-%m-%d')
                                        today = datetime.strptime(str(today), "%Y-%m-%d")
                                        previousDay = datetime.strftime(today - timedelta(1), '%Y-%m-%d')
                                        tomorow = datetime.strftime(today + timedelta(1), '%Y-%m-%d')
                                        if not MatchSchedule.objects.filter(Q(
                                                Team2__TeamName=val1) | Q(
                                            Team1__TeamName=val1) | Q(
                                            Team1__TeamName=val2) | Q(
                                            Team2__TeamName=val2), (Q(GameDate=previousDay) | Q(GameDate=today))):

                                            MatchSchedule.objects.create(Team1=val1, Team2=val2, GameDate=today,
                                                                         TournametId=TournamentModel.objects.get(
                                                                             Tourid=tourid))

                                            combinations.remove(j)
                                            i = i - 1
                                        else:
                                            if MatchSchedule.objects.filter(Q(
                                                    Team2__TeamName=val1) | Q(
                                                Team1__TeamName=val1) | Q(
                                                Team1__TeamName=val2) | Q(
                                                Team2__TeamName=val2), (Q(GameDate=previousDay) | Q(GameDate=today))):
                                                tomorow = datetime.strftime(today + timedelta(2), '%Y-%m-%d')
                                                MatchSchedule.objects.create(Team1=val1, Team2=val2, GameDate=tomorow,
                                                                             TournametId=TournamentModel.objects.get(
                                                                                 Tourid=tourid))

                                                combinations.remove(j)
                                            else:
                                                MatchSchedule.objects.create(Team1=val1, Team2=val2, GameDate=tomorow,
                                                                             TournametId=TournamentModel.objects.get(
                                                                                 Tourid=tourid))
                                                i = i + 1
                                                combinations.remove(j)
                # else:
                #     return  Response({"message":"Tournament Match schedule is already created"})
        datas = MatchSchedule.objects.values('TournametId', 'Team1', 'Team2', 'GameDate')
        output = []
        for i in datas:
            Tourid = i['TournametId']
            Team1 = i['Team1']
            Team2 = i['Team2']
            GameDate = i['GameDate']
            Tournamentid = TournamentModel.objects.filter(Tourid=Tourid).values('TournamentName')
            Team1Name = RegisteredTournamentModel.objects.filter(id=Team1).values('TeamName')
            Team2Name = RegisteredTournamentModel.objects.filter(id=Team2).values('TeamName')
            output.append({"Tournamentid": Tournamentid[0]['TournamentName'], "Team1Name": Team1Name[0]['TeamName'],
                           "Team2Name": Team2Name[0]['TeamName'],"GameDate":GameDate})

        return Response({"message": "Tournament Match schedule is created", "data": output})
