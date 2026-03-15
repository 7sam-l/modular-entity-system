"""
Abstract base serializers for master and mapping entities.

By inheriting these, each app's serializer is reduced to a 5-line Meta class.
All shared validation logic lives here once.
"""

from rest_framework import serializers


class BaseMasterSerializer(serializers.ModelSerializer):
    """
    Base serializer for Vendor, Product, Course, Certification.

    Provides:
        - read_only id / timestamps
        - code auto-uppercase + uniqueness check (update-safe)
        - name non-blank enforcement
    """

    class Meta:
        fields = ['id', 'name', 'code', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    # ── Field-level validation ─────────────────────────────────────────────────

    def validate_name(self, value: str) -> str:
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Name cannot be blank.')
        return value

    def validate_code(self, value: str) -> str:
        """
        Strip, uppercase, and enforce uniqueness across the model.
        Excludes self.instance so PUT/PATCH on the same code succeeds.
        """
        value = value.strip().upper()
        if not value:
            raise serializers.ValidationError('Code cannot be blank.')
        model = self.Meta.model
        qs = model.objects.filter(code=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                f"A {model.__name__} with code '{value}' already exists."
            )
        return value


class BaseMappingSerializer(serializers.ModelSerializer):
    """
    Base serializer for VendorProductMapping, ProductCourseMapping,
    CourseCertificationMapping.

    Subclasses must define:
        - Meta.model
        - Meta.fields  (including the two FK fields + *_detail fields)
        - _parent_field  (str) — name of the FK that is the "parent" for primary_mapping
        - _child_field   (str) — name of the FK that is the "child"
        - _parent_model  (Model class) — for active-status check
        - _child_model   (Model class) — for active-status check

    Provides:
        - FK active-status checks
        - duplicate (parent, child) pair validation
        - single primary_mapping per parent enforcement
    """

    # Subclasses must override these
    _parent_field: str = ''
    _child_field: str = ''
    _parent_model = None
    _child_model = None

    class Meta:
        read_only_fields = ['id', 'created_at', 'updated_at']

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _check_active(self, instance, model, field_label: str):
        """Raise if the FK target is inactive."""
        if instance is None:
            return
        if not model.objects.filter(pk=instance.pk, is_active=True).exists():
            raise serializers.ValidationError(
                f'{field_label} with id {instance.pk} does not exist or is inactive.'
            )

    # ── Cross-field validation ─────────────────────────────────────────────────

    def validate(self, attrs: dict) -> dict:
        parent = attrs.get(self._parent_field, getattr(self.instance, self._parent_field, None))
        child = attrs.get(self._child_field, getattr(self.instance, self._child_field, None))
        primary = attrs.get('primary_mapping', getattr(self.instance, 'primary_mapping', False))

        if parent is None or child is None:
            return attrs  # Field-level errors will handle missing FKs

        model = self.Meta.model
        parent_label = self._parent_model.__name__ if self._parent_model else 'Parent'
        child_label = self._child_model.__name__ if self._child_model else 'Child'

        # 1. FK active-status checks
        self._check_active(parent, self._parent_model, parent_label)
        self._check_active(child, self._child_model, child_label)

        # 2. Duplicate (parent, child) pair check
        qs = model.objects.filter(
            **{self._parent_field: parent, self._child_field: child}
        )
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError({
                'non_field_errors': (
                    f'A mapping between {parent_label}({parent.pk}) and '
                    f'{child_label}({child.pk}) already exists.'
                )
            })

        # 3. Only one primary_mapping per parent
        if primary:
            primary_qs = model.objects.filter(
                **{self._parent_field: parent, 'primary_mapping': True}
            )
            if self.instance:
                primary_qs = primary_qs.exclude(pk=self.instance.pk)
            if primary_qs.exists():
                raise serializers.ValidationError({
                    'primary_mapping': (
                        f'{parent_label}({parent.pk}) already has a primary '
                        f'{child_label} mapping. Only one primary mapping per '
                        f'{parent_label} is allowed.'
                    )
                })

        return attrs
