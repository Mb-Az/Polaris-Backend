from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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


    @swagger_auto_schema(
        operation_description="Get paginated cell measurements",
        manual_parameters=[
            openapi.Parameter("page", openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter("page_size", openapi.IN_QUERY, description="Items per page", type=openapi.TYPE_INTEGER),
        ],
        responses={200: CellMeasurementSerializer(many=True)}
    )
    def get(self, request):
        queryset = CellMeasurement.objects.all().order_by('-created_at')
        paginator = StandardResultsSetPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)


# -------- GET Test Results --------
class TestResultListView(APIView):
    serializer_class = TestResultSerializer
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get paginated test results",
        manual_parameters=[
            openapi.Parameter("page", openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter("page_size", openapi.IN_QUERY, description="Items per page", type=openapi.TYPE_INTEGER),
        ],
        responses={200: TestResultSerializer(many=True)}
    )
    def get(self, request):
        queryset = TestResult.objects.all().order_by('-created_at')
        paginator = StandardResultsSetPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
