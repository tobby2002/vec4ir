import os, sys
from api.models import Match, Sport, Selection, Market
from api.serializers import MatchListSerializer, MatchDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
import config
from ltr.ltrmanager import restore_lr, predict_lr

class MatchViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given match.

    list:
    Return a list of all the existing matches.

    create:
    Create a new match instance.
    """
    queryset = Match.objects.all()
    serializer_class = MatchListSerializer  # for list view
    detail_serializer_class = MatchDetailSerializer  # for detail view
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    ordering_fields = '__all__'

    def get_serializer_class(self):
        """
        Determins which serializer to user `list` or `detail`
        """
        if self.action == 'retrieve':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class
        return super().get_serializer_class()


    def get_queryset(self):
        """
        Optionally restricts the returned queries by filtering against
        a `sport` and `name` query parameter in the URL.
        """
        queryset = Match.objects.all()
        sport = self.request.query_params.get('sport', None)
        name = self.request.query_params.get('name', None)
        if sport is not None:
            sport = sport.title()
            queryset = queryset.filter(sport__name=sport)
        if name is not None:
            queryset = queryset.filter(name=name)
        return queryset


    def create(self, request):
        """
        to parse the incoming request and create a new match or update
        existing odds.
        """
        message = request.data.pop('message_type')

        # check if incoming api request is for new event creation
        if message == "NewEvent":
            event = request.data.pop('event')
            sport = event.pop('sport')
            markets = event.pop('markets')[0] # for now we have only one market
            selections = markets.pop('selections')
            sport = Sport.objects.create(**sport)
            markets = Market.objects.create(**markets, sport=sport)
            for selection in selections:
                markets.selections.create(**selection)
            match = Match.objects.create(**event, sport=sport, market=markets)
            return Response(status=status.HTTP_201_CREATED)

        # check if incoming api request is for updation of odds
        elif message == "UpdateOdds":
            event = request.data.pop('event')
            markets = event.pop('markets')[0]
            selections = markets.pop('selections')
            for selection in selections:
                s = Selection.objects.get(id=selection['id'])
                s.odds = selection['odds']
                s.save()
            match = Match.objects.get(id=event['id'])
            return Response(status=status.HTTP_201_CREATED)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)




from . import scheduler
sc = scheduler.Scheduler()
ir_model_dic = sc.irmodel_dic

class QueryViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given match.

    list:
    Return a list of all the existing matches.

    create:
    Create a new match instance.
    """
    queryset = Match.objects.all()
    serializer_class = MatchListSerializer  # for list view
    detail_serializer_class = MatchDetailSerializer  # for detail view
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    ordering_fields = '__all__'

    def get_serializer_class(self):
        """
        Determins which serializer to user `list` or `detail`
        """
        if self.action == 'retrieve':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class
        return super().get_serializer_class()


    def get_queryset(self):
        """
        Optionally restricts the returned queries by filtering against
        a `sport` and `name` query parameter in the URL.
        """
        print('======================= start get_queryset ========================')

        print('timeinstance in get_queryset:', sc.get_timeinstance())
        ir_model_dic = sc.get_irmodels()

        if ir_model_dic:
            irmodel_title = ir_model_dic['w2v_title']
            irmodel_authors = ir_model_dic['w2v_authors']
            print('get_irmodel in get_queryset:%s, %s' % (irmodel_title, irmodel_authors))
        else:
            print('get_irmodel in get_queryset: None, None')

        c = sc.get_ltrmodel()
        if c:
            print('get_ltrmodel in get_queryset:%s' % c)
        else:
            print('get_ltrmodel in No ltrmodel')

        model = restore_lr(None)
        y_pred = predict_lr(model)
        print(y_pred)
        print('======================= end get_queryset ========================')

        queryset = Match.objects.all()
        sport = self.request.query_params.get('sport', None)
        name = self.request.query_params.get('name', None)
        if sport is not None:
            sport = sport.title()
            queryset = queryset.filter(sport__name=sport)
        if name is not None:
            queryset = queryset.filter(name=name)
        return queryset


    def qltr(self, request):
        """
        to parse the incoming request and create a new match or update
        existing odds.
        """
        message = request.data.pop('message_type')

        # check if incoming api request is for new event creation
        if message == "NewEvent":
            event = request.data.pop('event')
            sport = event.pop('sport')
            markets = event.pop('markets')[0] # for now we have only one market
            selections = markets.pop('selections')
            sport = Sport.objects.create(**sport)
            markets = Market.objects.create(**markets, sport=sport)
            for selection in selections:
                markets.selections.create(**selection)
            match = Match.objects.create(**event, sport=sport, market=markets)
            return Response(status=status.HTTP_201_CREATED)

        # check if incoming api request is for updation of odds
        elif message == "UpdateOdds":
            event = request.data.pop('event')
            markets = event.pop('markets')[0]
            selections = markets.pop('selections')
            for selection in selections:
                s = Selection.objects.get(id=selection['id'])
                s.odds = selection['odds']
                s.save()
            match = Match.objects.get(id=event['id'])
            return Response(status=status.HTTP_201_CREATED)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
