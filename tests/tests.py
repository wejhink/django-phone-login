from __future__ import absolute_import, unicode_literals

import sys
import warnings
from unittest import TestCase as UnitTestCase
from unittest import skipIf, skipUnless

import django
import mock
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.management import call_command
from django.db import connection, models
from django.test import TestCase, TransactionTestCase
from django.test.utils import override_settings
from django.utils.encoding import force_text

from .forms import (CustomPKFoodForm, DirectCustomPKFoodForm, DirectFoodForm,
                    FoodForm, OfficialFoodForm)
from .models import (Article, Child, CustomManager, CustomPKFood,
                     CustomPKHousePet, CustomPKPet, DirectCustomPKFood,
                     DirectCustomPKHousePet, DirectCustomPKPet, DirectFood,
                     DirectHousePet, DirectPet, Food, HousePet, Movie,
                     OfficialFood, OfficialHousePet, OfficialPet, OfficialTag,
                     OfficialThroughModel, Pet, Photo, TaggedCustomPK,
                     TaggedCustomPKFood, TaggedFood)

from taggit.managers import TaggableManager, _TaggableManager
from taggit.models import Tag, TaggedItem
from taggit.utils import (_related_model, _remote_field, edit_string_for_tags,
                          parse_tags)
