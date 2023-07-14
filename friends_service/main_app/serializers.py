from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User, FriendRequest


class FriendsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class RequestsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendsListSerializer
        fields = ['to_user', 'from_user']


class SendRequestSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        from_user = self.context['request'].user
        if from_user == attrs['to_user']:
            raise ValidationError('Cannot add to friends yourself')
        if from_user.friends.contains(attrs['to_user']):
            raise ValidationError('Already friends.')
        if FriendRequest.objects.filter(to_user=attrs['to_user'], from_user=from_user).exists():
            raise ValidationError('Request already sent.')
        return attrs

    def create(self, validated_data):
        from_user = self.context['request'].user
        try:
            reversed_friend_request = FriendRequest.objects.get(
                to_user=from_user,
                from_user=validated_data['to_user']
            )
            from_user.friends.add(validated_data['to_user'])
            reversed_friend_request.delete()
            return reversed_friend_request
        except FriendRequest.DoesNotExist:
            return FriendRequest.objects.create(from_user=from_user, **validated_data)

    class Meta:
        model = FriendRequest
        fields = ['to_user']
