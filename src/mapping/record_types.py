# -*- coding: utf-8 -*-

import re
from ..models import DataType


TYPE_CATEGORY = DataType(
    name="Category",
    regex=re.compile(
        r"^"
        r"("
        r"(astro)|(cond)|(cs)|(econ)|(eess)|(gr)|(hep)|"
        r"(math)|(nlin)|(nucl)|(physics)|(q)|(quant)|(stat)"
        r")"
        r"(-\w+)?"
        r"(\.\w+)?"
        r"(-\w+)?"
        r"$"
    ),
)

TYPE_GROUP = DataType(
    name="JargonGroup",
    regex=re.compile(r"^group-\d+$"),
)

TYPE_JARGON = DataType(
    name="Jargon",
    regex=re.compile(r"^group-\d+-jargon-\d+$"),
)
