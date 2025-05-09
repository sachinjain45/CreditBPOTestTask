from django.http import JsonResponse
from django.views import View
from django.db import connections
from django.db.utils import OperationalError
import logging

logger = logging.getLogger(__name__)

class HealthCheckView(View):
    def get(self, request, *args, **kwargs):
        db_conn = connections['default']
        db_status = "ok"
        try:
            db_conn.cursor()
        except OperationalError:
            db_status = "error"
            logger.error("Database connection failed during health check.")

        # Basic metrics stub
        metrics = {
            "request_count_placeholder": 1234, 
            "error_count_placeholder": 5, 
        }

        data = {
            "status": "ok",
            "services": {
                "database": db_status,
            },
            "metrics_stub": metrics,
        }
        if db_status != "ok":
            return JsonResponse(data, status=503)
        return JsonResponse(data)