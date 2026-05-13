from rest_framework import permissions
from apps.common.thread_local import get_current_academy_id
from apps.permissions.models import Role

class RolePermission(permissions.BasePermission):
    """
    Base permission for role-based access.
    """
    required_roles = []

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
            
        if request.user.is_superuser:
            return True

        academy_id = get_current_academy_id()
        if not academy_id:
            return False

        # Check if user has any of the required roles in the current academy
        return request.user.user_roles.filter(
            academy_id=academy_id,
            role__name__in=self.required_roles
        ).exists()

class IsSuperAdmin(RolePermission):
    required_roles = [Role.SUPER_ADMIN]

class IsAdmin(RolePermission):
    required_roles = [Role.ADMIN, Role.SUPER_ADMIN]

class IsOperations(RolePermission):
    required_roles = [Role.OPERATIONS, Role.ADMIN, Role.SUPER_ADMIN]

class IsCoach(RolePermission):
    required_roles = [Role.COACH, Role.OPERATIONS, Role.ADMIN, Role.SUPER_ADMIN]

class IsCustomer(RolePermission):
    required_roles = [Role.CUSTOMER, Role.COACH, Role.OPERATIONS, Role.ADMIN, Role.SUPER_ADMIN]
