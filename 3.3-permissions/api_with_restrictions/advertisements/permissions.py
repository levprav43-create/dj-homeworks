from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение: только владелец может редактировать/удалять.
    Остальные — только чтение.
    """
    
    def has_object_permission(self, request, view, obj):
        # Безопасные методы (GET, HEAD, OPTIONS) — разрешены всем
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Для остальных методов: только если пользователь — владелец
        return obj.creator == request.user