import django_filters
from .models import CellMeasurement, TestResult

class CellMeasurementFilter(django_filters.FilterSet):
    since = django_filters.DateTimeFilter(field_name="time", lookup_expr="gte")
    till = django_filters.DateTimeFilter(field_name="time", lookup_expr="lte")

    class Meta:
        model = CellMeasurement
        fields = [
            "deviceId",
            "carrier",
            "technology",
            "tac",
            "plmn_id",
            "arfcn",
            "signal_level",
            "rsrq",
            "rsrp",
            "rscp",
            "ec_no",
            "rx_lev",
            "since",  # this allows query param ?since=...
            "till",   # this allows query param ?till=...
        ]


class TestResultFilter(django_filters.FilterSet):
    since = django_filters.DateTimeFilter(field_name="time", lookup_expr="gte")
    till = django_filters.DateTimeFilter(field_name="time", lookup_expr="lte")

    class Meta:
        model = TestResult
        fields = [
            "deviceId",
            "throughput",
            "ping",
            "web",
            "dns",
            "sms",
            "since",
            "till",
        ]
