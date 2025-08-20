from rest_framework import serializers
from data.models import CellMeasurement, TestResult


class CellMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CellMeasurement
        fields = '__all__'


class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = '__all__'


class CombinedDataSerializer(serializers.Serializer):
    cell_measurements = CellMeasurementSerializer(many=True)
    test_results = TestResultSerializer(many=True)

    def create(self, validated_data):
        cell_data = validated_data.get("cell_measurements", [])
        test_data = validated_data.get("test_results", [])

        # Save multiple cell measurements
        cell_measurements = [CellMeasurement(**cell) for cell in cell_data]
        CellMeasurement.objects.bulk_create(cell_measurements)

        # Save multiple test results
        test_results = [TestResult(**test) for test in test_data]
        TestResult.objects.bulk_create(test_results)

        return {
            "cell_measurements": cell_measurements,
            "test_results": test_results
        }
