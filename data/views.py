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


# Pagination class
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# -------- Combined POST API for Android --------
class AndroidDataUploadView(APIView):
    serializer_class = CombinedDataSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

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


# -------- GET Cell Measurements --------
class CellMeasurementListView(APIView):
    serializer_class = CellMeasurementSerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CellMeasurementFilter

    @swagger_auto_schema(
        operation_description="Get paginated & filtered cell measurements",
        manual_parameters=[
            openapi.Parameter("page", openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter("page_size", openapi.IN_QUERY, description="Items per page", type=openapi.TYPE_INTEGER),
            openapi.Parameter("carrier", openapi.IN_QUERY, description="Filter by carrier", type=openapi.TYPE_STRING),
            openapi.Parameter("technology", openapi.IN_QUERY, description="Filter by technology (e.g., LTE, NR)", type=openapi.TYPE_STRING),
            openapi.Parameter("tac", openapi.IN_QUERY, description="Filter by TAC", type=openapi.TYPE_INTEGER),
            openapi.Parameter("plmnId", openapi.IN_QUERY, description="Filter by PLMN ID", type=openapi.TYPE_STRING),
            openapi.Parameter("start_date", openapi.IN_QUERY, description="Start date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter("end_date", openapi.IN_QUERY, description="End date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
        ],
        responses={200: CellMeasurementSerializer(many=True)}
    )
    def get(self, request):
        queryset = CellMeasurement.objects.all().order_by('-time')
        filtered_queryset = CellMeasurementFilter(request.GET, queryset=queryset).qs
        paginator = StandardResultsSetPagination()
        paginated_queryset = paginator.paginate_queryset(filtered_queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)


# -------- GET Test Results --------
class TestResultListView(APIView):
    serializer_class = TestResultSerializer
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_class = CellMeasurementFilter

    @swagger_auto_schema(
        operation_description="Get paginated & filtered test results",
        manual_parameters=[
            openapi.Parameter("page", openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter("page_size", openapi.IN_QUERY, description="Items per page", type=openapi.TYPE_INTEGER),
            openapi.Parameter("throughput", openapi.IN_QUERY, description="Filter by throughput (KB/s)", type=openapi.TYPE_INTEGER),
            openapi.Parameter("ping", openapi.IN_QUERY, description="Filter by ping time (ms)", type=openapi.TYPE_INTEGER),
            openapi.Parameter("web", openapi.IN_QUERY, description="Filter by web response time (ms)", type=openapi.TYPE_INTEGER),
            openapi.Parameter("dns", openapi.IN_QUERY, description="Filter by DNS resolution time (ms)", type=openapi.TYPE_INTEGER),
            openapi.Parameter("sms", openapi.IN_QUERY, description="Filter by SMS time (ms)", type=openapi.TYPE_INTEGER),
            openapi.Parameter("start_date", openapi.IN_QUERY, description="Start date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter("end_date", openapi.IN_QUERY, description="End date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
        ],
        responses={200: TestResultSerializer(many=True)}
    )
    def get(self, request):
        queryset = TestResult.objects.all().order_by('-time')
        filtered_queryset = TestResultFilter(request.GET, queryset=queryset).qs
        paginator = StandardResultsSetPagination()
        paginated_queryset = paginator.paginate_queryset(filtered_queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
