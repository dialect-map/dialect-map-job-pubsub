# -*- coding: utf-8 -*-

from models import *

from .record_routes import CATEGORY_ROUTE
from .record_routes import GROUP_ROUTE
from .record_routes import JARGON_ROUTE


API_ROUTES = {
    TYPE_CATEGORY.name: CATEGORY_ROUTE,
    TYPE_GROUP.name: GROUP_ROUTE,
    TYPE_JARGON.name: JARGON_ROUTE,
}
