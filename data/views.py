from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django_filters.rest_framework import DjangoFilterBackend
from .filters import CellMeasurementFilter, TestResultFilter
from .models import CellMeasurement, TestResult
from .serializers import (
    CellMeasurementSerializer,
    TestResultSerializer,
    CombinedDataSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CellMeasurementFilter, TestResultFilter


# Pagination class
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# -------- Combined POST API for Android --------
class AndroidDataUploadView(APIView):
    serializer_class = CombinedDataSerializer
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Upload cell measurements and test results together",
        request_body=CombinedDataSerializer,
        responses={
            201: openapi.Response(
                description="Data saved successfully",
                examples={
                    "application/json": {
                        "message": "Data saved successfully",
                        "cell_measurements_saved": 2,
                        "test_results_saved": 2
                    }
                }
            ),
            400: "Invalid data"
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(
                {
                    "message": "Data saved successfully",
                    "cell_measurements_saved": len(result["cell_measurements"]),
                    "test_results_saved": len(result["test_results"]),
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# Pagination class
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# -------- Combined GET API --------
class DataListView(APIView):
    permission_classes = [IsAuthenticated]  # Or IsAuthenticated
    filter_backends = [DjangoFilterBackend]

    @swagger_auto_schema(
        operation_description="Get paginated & filtered cell measurements and test results together",
        manual_parameters=[
            # Cell measurement filters
            openapi.Parameter("cm_carrier", openapi.IN_QUERY, description="Filter by carrier", type=openapi.TYPE_STRING),
            openapi.Parameter("cm_technology", openapi.IN_QUERY, description="Filter by technology (e.g., LTE, NR)", type=openapi.TYPE_STRING),
            openapi.Parameter("cm_tac", openapi.IN_QUERY, description="Filter by TAC", type=openapi.TYPE_INTEGER),
            openapi.Parameter("cm_plmnId", openapi.IN_QUERY, description="Filter by PLMN ID", type=openapi.TYPE_STRING),
            openapi.Parameter("cm_start_date", openapi.IN_QUERY, description="Cell measurement start date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter("cm_end_date", openapi.IN_QUERY, description="Cell measurement end date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            # Test result filters
            openapi.Parameter("tr_throughput", openapi.IN_QUERY, description="Filter by throughput (KB/s)", type=openapi.TYPE_INTEGER),
            openapi.Parameter("tr_ping", openapi.IN_QUERY, description="Filter by ping time (ms)", type=openapi.TYPE_INTEGER),
            openapi.Parameter("tr_web", openapi.IN_QUERY, description="Filter by web response time (ms)", type=openapi.TYPE_INTEGER),
            openapi.Parameter("tr_dns", openapi.IN_QUERY, description="Filter by DNS resolution time (ms)", type=openapi.TYPE_INTEGER),
            openapi.Parameter("tr_sms", openapi.IN_QUERY, description="Filter by SMS time (ms)", type=openapi.TYPE_INTEGER),
            openapi.Parameter("tr_start_date", openapi.IN_QUERY, description="Test result start date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter("tr_end_date", openapi.IN_QUERY, description="Test result end date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            # Pagination
            openapi.Parameter("page", openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter("page_size", openapi.IN_QUERY, description="Items per page", type=openapi.TYPE_INTEGER),
        ]
    )
    def get(self, request):
        allowed_sort_fields_test = ['deviceId','time','throughput', 'ping', 'web', 'dns', 'sms','latitude','longitude']
        sort_param_test= request.GET.get('sort')
        if sort_param_test is None or sort_param_test.lstrip('-') not in allowed_sort_fields_test :
            sort_param_test = '-time'

        allowed_sort_fields_measure = ['deviceId','time', 'rsrp', 'rsrq','rx_lev','rscp','ec_no','plmn_id','tac','arfcn','signal_level','latitude','longitude']
        sort_param_measure = request.GET.get('sort')
    
        if sort_param_measure is None or sort_param_measure.lstrip('-') not in allowed_sort_fields_measure :
            sort_param_measure = '-time'

        # ---------- Cell Measurements ----------
        cm_queryset = CellMeasurement.objects.all().order_by(sort_param_measure)
        cm_filtered = CellMeasurementFilter(request.GET, queryset=cm_queryset).qs
        cm_paginator = StandardResultsSetPagination()
        cm_paginated = cm_paginator.paginate_queryset(cm_filtered, request)
        cm_serializer = CellMeasurementSerializer(cm_paginated, many=True)

        # ---------- Test Results ----------
        tr_queryset = TestResult.objects.all().order_by(sort_param_test)
        tr_filtered = TestResultFilter(request.GET, queryset=tr_queryset).qs
        tr_paginator = StandardResultsSetPagination()
        tr_paginated = tr_paginator.paginate_queryset(tr_filtered, request)
        tr_serializer = TestResultSerializer(tr_paginated, many=True)

        # Return both in one response
        return Response({
            "cell_measurements": {
                "count": cm_filtered.count(),
                "next": cm_paginator.get_next_link(),
                "previous": cm_paginator.get_previous_link(),
                "results": cm_serializer.data
            },
            "test_results": {
                "count": tr_filtered.count(),
                "next": tr_paginator.get_next_link(),
                "previous": tr_paginator.get_previous_link(),
                "results": tr_serializer.data
            }
        }, status=status.HTTP_200_OK)

