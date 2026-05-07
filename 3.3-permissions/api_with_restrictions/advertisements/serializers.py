from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Advertisement, AdvertisementStatusChoices


class AdvertisementSerializer(serializers.ModelSerializer):
    """Сериализатор для объявлений"""
    
    creator = serializers.ReadOnlyField(source='creator.username')
    
    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'description', 'status', 'creator', 'created_at', 'updated_at']
        read_only_fields = ['id', 'creator', 'created_at', 'updated_at']
    
    def validate_status(self, value):
        """Валидация: не больше 10 открытых объявлений у пользователя"""
        request = self.context.get('request')
        
        # Проверяем только при создании или изменении статуса на OPEN
        if value == AdvertisementStatusChoices.OPEN and request and hasattr(request, 'user'):
            # Считаем открытые объявления пользователя (исключая текущее при обновлении)
            open_count = Advertisement.objects.filter(
                creator=request.user,
                status=AdvertisementStatusChoices.OPEN
            ).exclude(pk=self.instance.pk if self.instance else None).count()
            
            if open_count >= 10:
                raise ValidationError('У вас не может быть больше 10 открытых объявлений.')
        
        return value
    
    def validate(self, attrs):
        """Дополнительная валидация всего объекта"""
        request = self.context.get('request')
        
        # При создании проверяем лимит открытых объявлений
        if not self.instance and request and hasattr(request, 'user'):
            if attrs.get('status') == AdvertisementStatusChoices.OPEN:
                open_count = Advertisement.objects.filter(
                    creator=request.user,
                    status=AdvertisementStatusChoices.OPEN
                ).count()
                
                if open_count >= 10:
                    raise ValidationError({'status': 'У вас не может быть больше 10 открытых объявлений.'})
        
        return attrs