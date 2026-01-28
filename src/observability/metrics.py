from prometheus_client import Counter, Histogram


# Request level metrics
REQUESTS_TOTAL = Counter(
    "requests_total",
    "Total number of requests processed"
)

REQUESTS_SUCCESS = Counter(
    "requests_success_total",
    "Total number of successful requests"
)

REQUESTS_FAILURE = Counter(
    "requests_failure_total",
    "Total number of failed requests"
)

REQUEST_LATENCY = Histogram(
    "request_latency_ms",
    "Latency of full request in milliseconds",
    buckets=(500, 1000, 2000, 4000, 8000, 12000, 20000)
)


# Agent-Level metrics
AGENT_LATENCY = Histogram(
    "agent_latency_ms",
    "Latency per agent in milliseconds",
    ["agent_name"],
    buckets=(200, 500, 1000, 2000, 4000, 8000)
)

AGENT_ERRORS = Counter(
    "agent_errors_total",
    "Total number of agent errors",
    ["agent_name"]
)