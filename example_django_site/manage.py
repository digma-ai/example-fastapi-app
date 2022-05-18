#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from opentelemetry.instrumentation.digma import digma_opentelemetry_boostrap
from opentelemetry.instrumentation.digma.digma_configuration import DigmaConfiguration
from opentelemetry.instrumentation.digma.django import DigmaIntrumentor
from opentelemetry.instrumentation.django import DjangoInstrumentor

from observability import setup_observability


def main():
    setup_observability()
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
