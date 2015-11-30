# -*- coding: utf-8 -*-
# This file is part of Shoop Gifter Demo.
#
# Copyright (c) 2012-2015, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from django.http import HttpResponse
from django.template.loader import render_to_string

from shoop.core.models import Product, Category


def products(request):
    context = {
        "products": Product.objects.list_visible(
            shop=request.shop,
            customer=request.customer
        ),
        "categories": Category.objects.all_visible(
            customer=request.customer
        )
    }
    return HttpResponse(
        render_to_string(
            "gifter/products_view.jinja",
            context,
            request=request,
        )
    )
