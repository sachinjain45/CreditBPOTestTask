from django.http import JsonResponse
from django.conf import settings
from django.db import connection
import psutil
import time

def health_check(request):
    """Health check endpoint that checks various system components"""
    start_time = time.time()
    health_status = {
        'status': 'healthy',
        'timestamp': start_time,
        'checks': {}
    }

    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        health_status['checks']['database'] = {
            'status': 'healthy',
            'response_time': time.time() - start_time
        }
    except Exception as e:
        health_status['checks']['database'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
        health_status['status'] = 'unhealthy'

    # Check disk usage
    disk_usage = psutil.disk_usage('/')
    health_status['checks']['disk'] = {
        'status': 'healthy' if disk_usage.percent < settings.HEALTH_CHECK['DISK_USAGE_MAX'] else 'warning',
        'percent_used': disk_usage.percent,
        'free_gb': disk_usage.free / (1024**3)
    }
    if disk_usage.percent >= settings.HEALTH_CHECK['DISK_USAGE_MAX']:
        health_status['status'] = 'warning'

    # Check memory usage
    memory = psutil.virtual_memory()
    health_status['checks']['memory'] = {
        'status': 'healthy' if memory.available > settings.HEALTH_CHECK['MEMORY_MIN'] * 1024 * 1024 else 'warning',
        'available_mb': memory.available / (1024**2),
        'percent_used': memory.percent
    }
    if memory.available <= settings.HEALTH_CHECK['MEMORY_MIN'] * 1024 * 1024:
        health_status['status'] = 'warning'

    # Add response time
    health_status['response_time'] = time.time() - start_time

    return JsonResponse(health_status) 