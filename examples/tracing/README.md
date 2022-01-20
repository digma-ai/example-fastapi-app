# OpenTelemetry Collector Demo

This demo is a sample app to build the collector and exercise its tracing functionality.

To build and run the demo, switch to this directory and run

`docker-compose up`


You should be able to browse different components of the application by using the below URLs :

```
Zipkin     : http://localhost:9411/
Jaeger     : http://localhost:16686/
Prometheus : http://localhost:9090/
```
for sending traces to opentelemetry collector do the following:
set environment variable OTELE_TRACE=True (.env file) when running the fastapi example,
