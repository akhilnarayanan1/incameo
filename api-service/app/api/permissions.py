from rest_framework.permissions import IsAuthenticated

class IsOwnerAndAuthenticated(IsAuthenticated):
    """
    Object-level permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.userid
