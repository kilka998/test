from rest_framework.viewsets import GenericViewSet


class BaseGenericViewSet(GenericViewSet):
    action_serializer_class = None
    action_queryset = None
    action_permission_classes = None
    action_search_fields = None

    def get_serializer_class(self):
        if self.action_serializer_class is None:
            return super().get_serializer_class()

        serializer_class = self.action_serializer_class.get(self.action)
        return serializer_class or super().get_serializer_class()

    def get_queryset(self):
        if self.action_queryset is not None and self.action in self.action_queryset.keys():
            return self.action_queryset.get(self.action)
        return super().get_queryset()

    def get_permissions(self):
        if self.action_permission_classes is None:
            return super().get_permissions()

        permission_classes = self.action_permission_classes.get(self.action) or []
        return [permission() for permission in permission_classes] or super().get_permissions()
