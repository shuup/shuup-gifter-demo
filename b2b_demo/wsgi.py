# This file is part of Shoop Gifter Demo.
#
# Copyright (c) 2012-2015, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "b2b_demo.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
