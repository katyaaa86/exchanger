from rest_framework import serializers

from ads.models import Ad, Category, ExchangeProposal


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class AdSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Ad
        fields = [
            'url',
            'id',
            'user',
            'title',
            'description',
            'image_url',
            'category',
            'condition',
            'created_at',
        ]


class ProposalSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)

    class Meta:
        model = ExchangeProposal
        fields = ['url', 'id', 'ad_sender', 'ad_receiver', 'comment', 'status', 'created_at']

    def validate(self, attrs):
        user = self.context['request'].user
        ad_sender = attrs['ad_sender']
        ad_receiver = attrs['ad_receiver']

        if ad_sender.user != user:
            raise serializers.ValidationError(
                'Вы можете отправлять предложения на обмен только своих вещей'
            )
        if ad_receiver.user == user:
            raise serializers.ValidationError(
                'Вы не можете отправить предложение в обмен на свое же объявление'
            )
        if ad_sender == ad_receiver:
            raise serializers.ValidationError('Нельзя обменять объявление само на себя')

        return attrs


class ProposalStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeProposal
        fields = ['status']

    def validate_status(self, status):
        if status not in ['accept', 'decline']:
            raise serializers.ValidationError('Предложение можно только принять или отклонить')
        return status

    def validate(self, attrs):
        instance = self.instance
        user = self.context['request'].user

        if instance.status != 'pending':
            raise serializers.ValidationError('Нельзя изменить статус предложения')

        if instance.ad_receiver.user != user:
            raise serializers.ValidationError('Вы не можете изменить статус этого предложения')

        return attrs
