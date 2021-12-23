# SPDX-License-Identifier: MPL-2.0
# Copyright (C) 2019 - 2021 Gemeente Amsterdam
from django.conf import settings
from rest_framework.fields import JSONField

from signals.apps.questionnaires.services import SessionService


class SignalExtraPropertiesField(JSONField):
    def __init__(self, *args, **kwargs):
        self.instance = None
        super().__init__(*args, **kwargs)

    def get_attribute(self, instance):
        self.instance = instance
        return self.to_representation(instance.extra_properties)

    def to_representation(self, value):
        representation = super().to_representation(value=value)
        if representation is None:
            representation = []

        session_extra_properties = []
        session_qs = self.instance.session_set.filter(questionnaire__category__isnull=False)
        if session_qs.exists():
            """
            If there are connected sessions that have questionnaires belonging to categories we want to extract the
            extra_properties and add them to the representation
            """
            for session in session_qs:
                session_service = SessionService(session)
                session_extra_properties += session_service.get_extra_properties()
            representation = session_extra_properties

        if not settings.FEATURE_FLAGS.get('API_FILTER_EXTRA_PROPERTIES', False):
            return representation + session_extra_properties

        category_url = self.instance.category_assignment.category.get_absolute_url()
        category_urls = [category_url, f'{category_url}/']
        if self.instance.category_assignment.category.is_child():
            parent_category_url = self.instance.category_assignment.category.parent.get_absolute_url()
            category_urls += [parent_category_url, f'{parent_category_url}/']

        return list(filter(
            lambda x: 'category_url' in x and x['category_url'] in category_urls, representation
        )) + session_extra_properties
