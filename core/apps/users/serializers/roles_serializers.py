from rest_framework import serializers

from apps.users.models import Roles


class RolesSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(
        default="",
        required=False,
    )
    url = serializers.HyperlinkedIdentityField(
        view_name="role-detail",
        lookup_field="name",
        read_only=True,
    )

    class Meta:
        model = Roles
        fields = (
            "name",
            "description",
            "url",
        )

    def to_representation(self, instance):
        instance.name = instance.name.upper()
        return super().to_representation(instance)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance
