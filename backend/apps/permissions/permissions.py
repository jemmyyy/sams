from apps.common.thread_local import get_current_academy_id
from apps.permissions.models import Role
from rest_framework import permissions


class RolePermission(permissions.BasePermission):
    required_roles = []

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        academy_id = get_current_academy_id()
        if not academy_id:
            return False
        return request.user.user_roles.filter(
            academy_id=academy_id, role__name__in=self.required_roles
        ).exists()

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        academy_id = get_current_academy_id()
        if hasattr(obj, "academy_id") and str(obj.academy_id) != academy_id:
            return False
        return True


class IsSuperAdmin(RolePermission):
    required_roles = [Role.SUPER_ADMIN]


class IsAdmin(RolePermission):
    required_roles = [Role.ADMIN, Role.SUPER_ADMIN]


class IsOperations(RolePermission):
    required_roles = [Role.OPERATIONS, Role.ADMIN, Role.SUPER_ADMIN]


class IsCoach(RolePermission):
    required_roles = [Role.COACH, Role.OPERATIONS, Role.ADMIN, Role.SUPER_ADMIN]

    def has_object_permission(self, request, view, obj):
        if not super().has_object_permission(request, view, obj):
            return False
        academy_id = get_current_academy_id()
        user_roles = request.user.user_roles.filter(academy_id=academy_id).values_list(
            "role__name", flat=True
        )
        if any(r in [Role.OPERATIONS, Role.ADMIN, Role.SUPER_ADMIN] for r in user_roles):
            return True
        # Coach can access their own coach profile
        if hasattr(obj, "user_id") and str(obj.user_id) == str(request.user.id):
            return True
        # Coach can access sessions they are assigned to
        if hasattr(obj, "coach_id") and str(obj.coach_id) == str(request.user.id):
            return True
        if obj.__class__.__name__ == "SessionOccurrence":
            return obj.coaches.filter(coach_id=request.user.id).exists()
        return False


class IsCustomer(RolePermission):
    required_roles = [
        Role.CUSTOMER,
        Role.COACH,
        Role.OPERATIONS,
        Role.ADMIN,
        Role.SUPER_ADMIN,
    ]

    def has_object_permission(self, request, view, obj):
        if not super().has_object_permission(request, view, obj):
            return False
        academy_id = get_current_academy_id()
        user_roles = request.user.user_roles.filter(academy_id=academy_id).values_list(
            "role__name", flat=True
        )
        if any(r in [Role.COACH, Role.OPERATIONS, Role.ADMIN, Role.SUPER_ADMIN] for r in user_roles):
            return True
        # Customer can access their own player children
        if hasattr(obj, "parent_id") and str(obj.parent_id) == str(request.user.id):
            return True
        # Customer can access their own enrollments
        if hasattr(obj, "player") and hasattr(obj.player, "parent_id"):
            return str(obj.player.parent_id) == str(request.user.id)
        return False
