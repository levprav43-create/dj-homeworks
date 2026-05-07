from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from .models import Advertisement
from .serializers import AdvertisementSerializer
from .filters import AdvertisementFilter
from .permissions import IsOwnerOrReadOnly


class AdvertisementViewSet(viewsets.ModelViewSet):
    """ViewSet для объявлений с доступом и фильтрацией"""
    
    queryset = Advertisement.objects.select_related('creator').all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    
    def get_permissions(self):
        """Динамическое назначение прав доступа"""
        if self.action in ['create']:
            # Создавать могут только авторизованные
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Редактировать/удалять — только владелец
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        # Просмотр — всем (по умолчанию IsAuthenticatedOrReadOnly)
        return [IsAuthenticatedOrReadOnly()]
    
    def get_throttles(self):
        """Возвращаем нужный троттл в зависимости от авторизации"""
        if self.request.user and self.request.user.is_authenticated:
            return [UserRateThrottle()]  # 20/min для авторизованных
        return [AnonRateThrottle()]  # 10/min для анонимов
    
    def perform_create(self, serializer):
        """Автоматически проставляем создателя"""
        serializer.save(creator=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        """Дополнительная проверка при удалении (дублирующая для надёжности)"""
        instance = self.get_object()
        
        # Если пользователь не владелец — запрещаем удаление
        if instance.creator != request.user:
            return Response(
                {'detail': 'Удаление чужого объявления запрещено.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().destroy(request, *args, **kwargs)