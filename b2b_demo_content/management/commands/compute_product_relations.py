# This file is part of Shoop Gifter Demo.
#
# Copyright (c) 2012-2015, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
import random

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from shoop.core.models import Category, Product, ProductCrossSell, ProductCrossSellType


def add_cross_sell_products(type, product, products):
    count = random.randint(5, 8)
    product_count = len(products)
    if count > product_count:
        count = product_count
    related_products = random.sample(products, count)
    for i, related_product in enumerate(related_products):
        if related_product != product:
            ProductCrossSell.objects.create(product1_id=product, product2_id=related_product, weight=i, type=type)


def handle_category(category):
    print("Starting to handle category %s" % category)
    category_products = Product.objects.filter(category=category).values_list("id", flat=True)
    for product in category_products:
        add_cross_sell_products(ProductCrossSellType.COMPUTED, product, category_products)
        add_cross_sell_products(ProductCrossSellType.RECOMMENDED, product, category_products)
        add_cross_sell_products(ProductCrossSellType.RELATED, product, category_products)


class Command(BaseCommand):

    @atomic
    def handle(self, *args, **options):
        # Clear all existing ProductCrossSell objects
        print("Deleting old product cross sells")
        ProductCrossSell.objects.all().delete()

        print("Starting to create no product relations")
        for category in Category.objects.all():
            handle_category(category)
