# import logging
# from opentelemetry.sdk.resources import SERVICE_NAME
# from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult
# from opentelemetry.trace import Span
# from typing import Optional, Sequence
# import traceback
# logger = logging.getLogger(__name__)

# class DigmaExporter(SpanExporter):

#     def __init__(self) -> None:
#         self._closed = False
#         super().__init__()

#     def export(self, spans: Sequence[Span]) -> SpanExportResult:
        

#         exceptions = []
#         for span in spans:
#             for span_event in span.events:
#                 if span_event.name == 'exception':
#                     exception= {}
#                     exception['type'] = span_event.attributes['exception.type']
#                     exception['trace'] =span_event.attributes['exception.stacktrace']
#                     exception['message']=span_event.attributes['exception.message']
#                     exception['escapted']=span_event.attributes['exception.escaped']

#                     exceptions.append(exception)

#         if self._closed:
#             logger.warning("Exporter already shutdown, ignoring batch")
#             return SpanExportResult.FAILURE

#     def shutdown(self) -> None:
#         self._closed = True