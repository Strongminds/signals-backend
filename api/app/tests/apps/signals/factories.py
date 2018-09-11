import random
import string
import uuid
from datetime import datetime

import factory
import pytz
from django.contrib.gis.geos import Point
from factory import fuzzy

from signals.apps.signals.models import (
    GEMELD,
    STADSDELEN,
    Category,
    Location,
    Reporter,
    Signal,
    Status,
    Priority)

# Amsterdam.
BBOX = [52.03560, 4.58565, 52.48769, 5.31360]


def get_puntje():

    lat = fuzzy.FuzzyFloat(BBOX[0], BBOX[2]).fuzz()
    lon = fuzzy.FuzzyFloat(BBOX[1], BBOX[3]).fuzz()
    return Point(float(lat), float(lon))


class SignalFactory(factory.DjangoModelFactory):

    class Meta:
        model = Signal

    signal_id = fuzzy.FuzzyAttribute(uuid.uuid4)
    text = fuzzy.FuzzyText(length=100)
    text_extra = fuzzy.FuzzyText(length=100)

    # Creating (reverse FK) related objects after this `Signal` is created.
    locations = factory.RelatedFactory('tests.apps.signals.factories.LocationFactory', '_signal')
    statuses = factory.RelatedFactory('tests.apps.signals.factories.StatusFactory', '_signal')
    categories = factory.RelatedFactory('tests.apps.signals.factories.CategoryFactory', '_signal')
    reporters = factory.RelatedFactory('tests.apps.signals.factories.ReporterFactory', '_signal')
    priorities = factory.RelatedFactory('tests.apps.signals.factories.PriorityFactory', '_signal')

    incident_date_start = fuzzy.FuzzyDateTime(
        datetime(2017, 11, 1, tzinfo=pytz.UTC),
        datetime(2018, 2, 1, tzinfo=pytz.UTC),
    )
    incident_date_end = fuzzy.FuzzyDateTime(
        datetime(2018, 2, 2, tzinfo=pytz.UTC),
        datetime(2019, 2, 2, tzinfo=pytz.UTC)
    )
    extra_properties = {}

    @factory.post_generation
    def set_one_to_one_relations(self, create, extracted, **kwargs):
        """Set o2o relations on given `Signal` object."""
        self.location = self.locations.first()
        self.status = self.statuses.first()
        self.category = self.categories.first()
        self.reporter = self.reporters.first()
        self.priority = self.priorities.first()


class LocationFactory(factory.DjangoModelFactory):

    class Meta:
        model = Location

    _signal = factory.SubFactory(SignalFactory, locations=None)

    buurt_code = fuzzy.FuzzyText(length=4)
    stadsdeel = fuzzy.FuzzyChoice(choices=(s[0] for s in STADSDELEN))
    geometrie = get_puntje()
    address = {'straat': 'Sesamstraat',
               'huisnummer': 666,
               'postcode': '1011AA',
               'openbare_ruimte': 'Ergens'}

    @factory.post_generation
    def set_one_to_one_relation(self, create, extracted, **kwargs):
        self.signal = self._signal


class ReporterFactory(factory.DjangoModelFactory):

    class Meta:
        model = Reporter

    _signal = factory.SubFactory(SignalFactory, reporters=None)

    phone = fuzzy.FuzzyText(length=10, chars=string.digits)
    email = 'john%d@example.org' % (int(random.random() * 100))

    @factory.post_generation
    def set_one_to_one_relation(self, create, extracted, **kwargs):
        self.signal = self._signal


class CategoryFactory(factory.DjangoModelFactory):

    class Meta:
        model = Category

    _signal = factory.SubFactory(SignalFactory, categories=None)

    main = fuzzy.FuzzyText(length=10)
    sub = fuzzy.FuzzyText(length=10)

    @factory.post_generation
    def set_one_to_one_relation(self, create, extracted, **kwargs):
        self.signal = self._signal


class StatusFactory(factory.DjangoModelFactory):

    class Meta:
        model = Status

    _signal = factory.SubFactory(SignalFactory, statuses=None)

    text = fuzzy.FuzzyText(length=400)
    user = 'kees%s@amsterdam.nl' % (int(random.random() * 100))
    state = GEMELD  # Initial state is always 'm'
    extern = fuzzy.FuzzyChoice((True, False))

    @factory.post_generation
    def set_one_to_one_relation(self, create, extracted, **kwargs):
        self.signal = self._signal


class PriorityFactory(factory.DjangoModelFactory):

    class Meta:
        model = Priority

    _signal = factory.SubFactory(SignalFactory, priorities=None)

    @factory.post_generation
    def set_one_to_one_relation(self, create, extracted, **kwargs):
        self.signal = self._signal
