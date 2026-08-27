from rest_framework.permissions import BasePermission


class IsAdminOrSupervisor(BasePermission):

    message = "Only administrators and supervisors can perform this action."

    def has_permission(self, request, view):
        return (request.user
            and request.user.is_authenticated
            and request.user.role in ["ADMIN", "SUPERVISOR"]
        )
    
class IsCustomer(BasePermission):

    message = "Only customers can perform this action."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "CUSTOMER"
        )
    
class IsPacker(BasePermission):

    message = "Only packers can perform this action."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "PACKER"
        )
    
class IsTakeawayStaff(BasePermission):
    message = "Only takeaway staff can perform this action."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "TAKEAWAY_STAFF"
        )
    
class IsPackerOrAdminOrSupervisor(BasePermission):
    message = "Only packers, admin, and supervisors can perform this action."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ["PACKER", "ADMIN", "SUPERVISOR"]
        )
    
class IsTakeawayStaffOrAdminOrSupervisor(BaseException):
    message = "Only takeaway_staff, admin and supervisors can perform this action."

    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated
            and request.user.role in ["TAKEAWAY_STAFF", "ADMIN", "SUPERVISOR"]
        )
    
class IsSupervisorOrAdmin(BasePermission):
    message = "Only supervisors and administrators can perform this action."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ["SUPERVISOR", "ADMIN"]
        )