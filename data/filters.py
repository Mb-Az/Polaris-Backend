import django_filters
from .models import CellMeasurement, TestResult

class CellMeasurementFilter(django_filters.FilterSet):
    # Filtering by date ranges
    start_date = django_filters.DateTimeFilter(field_name="time", lookup_expr="gte")
    end_date = django_filters.DateTimeFilter(field_name="time", lookup_expr="lte")

    class Meta:
        model = CellMeasurement
        fields = [
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
        ]

class TestResultFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name="time", lookup_expr="gte")
    end_date = django_filters.DateTimeFilter(field_name="time", lookup_expr="lte")

    class Meta:
        model = TestResult
        fields = [
            "throughput",
            "ping",
            "web",
            "dns",
            "sms",
        ]
