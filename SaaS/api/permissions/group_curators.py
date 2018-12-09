from django.contrib.auth.models import Group

from rest_framework import permissions


class IsMemberOfCuratorsGroup(permissions.BasePermission):
    """
    Persmission for members of curators group
    """
    group_curators = []

    def has_permission(self, request, view) -> bool:
        if not self.group_curators:
            self.group_curators = Group.objects.get(name="curators")
        current_user = request.user
        if current_user in self.group_curators.user_set.all():
            return True
        else:
            return False
