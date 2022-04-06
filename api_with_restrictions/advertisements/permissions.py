from rest_framework.permissions import BasePermission


class Owner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # if request.method == 'GET':
        #     print(request.creator)
        #     print(obj.creator)
        #     return True
        # print(f'значение request {request.user}')
        #
        # print(f'значение {obj.creator.first_name}')
        return request.user == obj.creator
