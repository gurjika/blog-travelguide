from rest_framework.permissions import BasePermission
from rest_framework import permissions



class IsCreatorOfObjOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.author.user == request.user
    
class IsCurrentUserOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.user == request.user
        