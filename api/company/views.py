from core.views import BaseGenericViewSet
from .models import Department, Employee
from .serializers import ReadOnlyDepartmentSerializer, ReadOnlyEmployeeSerializer, CreateEmployeeSerializer
from .paginations import EmployeePagination
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import mixins, status
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from core.serializers import ExceptionSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated


@method_decorator(
    name='list',
    decorator=extend_schema(
        parameters=[
            OpenApiParameter(
                'department_id',
                OpenApiTypes.INT,
                OpenApiParameter.QUERY,
                description=f'Фильтр по отделу',
            ),
            OpenApiParameter(
                'last_name',
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description=f'Фильтр по фамилии',
            ),
        ],   
        responses={
            '200': ReadOnlyEmployeeSerializer,
            '400': ExceptionSerializer,
            '500': ExceptionSerializer,
        },
    ),
)
@method_decorator(
    name='create',
    decorator=extend_schema(
        responses={
            '201': None,
            '400': ExceptionSerializer,
            '500': ExceptionSerializer,
        },
        request=CreateEmployeeSerializer,
    ),
)
class EmployeeViewSet(
    BaseGenericViewSet,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Employee.objects.all()
    action_serializer_class = {
        'list': ReadOnlyEmployeeSerializer,
        'create': CreateEmployeeSerializer,
    }
    pagination_class = EmployeePagination
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        queryset = super().get_queryset()
        department_id = self.request.query_params.get('department_id')
        last_name = self.request.query_params.get('last_name')

        if department_id:
            queryset = queryset.filter(department_id=department_id)

        if last_name:
            queryset = queryset.filter(full_name__icontains=last_name)

        return queryset
    
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        if 'context' in kwargs:
            kwargs['context'].update(self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        Employee.objects.create(**serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)


class DepartmentViewSet(BaseGenericViewSet, mixins.ListModelMixin):
    queryset = Department.objects.all()
    serializer_class = ReadOnlyDepartmentSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
