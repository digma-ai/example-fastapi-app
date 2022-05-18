import os

from opentelemetry.instrumentation.digma import digma_opentelemetry_boostrap, DigmaConfiguration
from opentelemetry.instrumentation.digma.django import DigmaIntrumentor
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor


def setup_observability():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'example_django_site.settings')
    digma_opentelemetry_boostrap(service_name='django-ms',
                                 digma_backend='http://localhost:5050',
                                 configuration=DigmaConfiguration()
                                               .trace_this_package()
                                               .set_environment("development")
                                 )
    DjangoInstrumentor().instrument()
    DigmaIntrumentor.instrument()
