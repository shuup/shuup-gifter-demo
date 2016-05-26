# This file is part of Shoop Gifter Demo.
#
# Copyright (c) 2012-2015, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.core.management.commands.migrate import Command as MigrateCommand
from django.db.transaction import atomic
from django.utils import translation

from shoop.core.models import (
    CustomCarrier, CustomPaymentProcessor, PaymentMethod, ProductType,
    SalesUnit, ShippingMethod, Shop, ShopStatus, TaxClass
)
from shoop.testing.factories import create_default_order_statuses, get_default_supplier
from shoop.xtheme import set_current_theme

from b2b_demo_content.importer import import_categories, import_products, import_cms_content


class Command(BaseCommand):
    def seed_default(self):
        migrator = MigrateCommand()
        migrator.stdout = self.stdout
        migrator.handle(database="default", verbosity=1, noinput=True, app_label=None, migration_name=None)

        if not Shop.objects.exists():
            shop = Shop.objects.create(name="B2B", identifier="default", status=ShopStatus.ENABLED)
            try:
                tax_class = TaxClass.objects.create(identifier="default", tax_rate=0)
            except:
                tax_class = TaxClass.objects.create(identifier="default")

            custom_carrier = CustomCarrier.objects.first()
            custom_carrier.create_service(
                choice_identifier="manual",
                identifier="default",
                shop=shop,
                enabled=True,
                name="Post Parcel",
                tax_class=tax_class
            )
            payment_processor = CustomPaymentProcessor.objects.first()
            payment_processor.create_service(choice_identifier="manual",
                identifier="default",
                shop=shop,
                enabled=True,
                name="Invoice",
                tax_class=tax_class
            )
            create_default_order_statuses()
            get_default_supplier()
            ProductType.objects.create(identifier="default")
            SalesUnit.objects.create(identifier="pcs", short_name="pcs", name="pieces")
            print("Seeded basic shop information")
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@b2b.shoop.io",
                password="admin",
            )
            print("Superuser created: admin / admin")

    def import_data(self):
        this_dir = os.path.dirname(__file__)
        data_path = os.path.realpath(os.path.join(this_dir, "..", "..", "data"))
        img_path = os.path.realpath(os.path.join(this_dir, "..", "..", "data", "images"))
        print("Importing categories...")
        import_categories(os.path.join(data_path, "categories.yaml"))
        print("Importing products...")
        import_products(os.path.join(data_path, "products.yaml"), img_path)
        print("Importing Simple CMS pages...")
        import_cms_content(os.path.join(data_path, "cms.yaml"))

    @atomic
    def handle(self, *args, **options):
        translation.activate("en")
        self.seed_default()
        self.import_data()
        set_current_theme("shoop_beauty_theme")
