from api.models import Match, Sport, Market, Selection
from rest_framework import serializers

class YourSerializer(serializers.Serializer):
   """Your data serializer, define your fields here."""
   comments = serializers.IntegerField()
   likes = serializers.IntegerField()

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ('id', 'name')

class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ('id', 'name', 'odds')

class MarketSerializer(serializers.ModelSerializer):
    selections = SelectionSerializer(many=True)
    class Meta:
        model = Market
        fields = ('id', 'name','selections')

class MatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('id', 'url', 'name', 'startTime')

class MatchDetailSerializer(serializers.ModelSerializer):
    sport = SportSerializer()
    market = MarketSerializer()
    class Meta:
        model = Match
        fields = ('id', 'url', 'name', 'startTime', 'sport', 'market')

class SampleSerializer(serializers.Serializer):
    field1 = serializers.CharField()
    field2 = serializers.IntegerField()
    # ... other fields



