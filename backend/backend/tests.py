from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
import json
from unittest.mock import patch
import psutil

class HealthCheckTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.health_url = reverse('health-check')

    def test_health_check_success(self):
        response = self.client.get(self.health_url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        # Check response structure
        self.assertIn('status', data)
        self.assertIn('timestamp', data)
        self.assertIn('checks', data)
        
        # Check individual health checks
        checks = data['checks']
        self.assertIn('database', checks)
        self.assertIn('disk', checks)
        self.assertIn('memory', checks)
        
        # Verify database check
        self.assertEqual(checks['database']['status'], 'healthy')
        
        # Verify disk check
        self.assertIn('percent_used', checks['disk'])
        self.assertIn('free_gb', checks['disk'])
        
        # Verify memory check
        self.assertIn('available_mb', checks['memory'])
        self.assertIn('percent_used', checks['memory'])

    @patch('psutil.disk_usage')
    def test_health_check_disk_warning(self, mock_disk_usage):
        # Mock disk usage above threshold
        mock_disk_usage.return_value = psutil._pslinux.sdiskusage(
            total=1000000000,
            used=950000000,
            free=50000000,
            percent=95
        )
        
        response = self.client.get(self.health_url)
        data = json.loads(response.content)
        
        self.assertEqual(data['status'], 'warning')
        self.assertEqual(data['checks']['disk']['status'], 'warning')

    @patch('psutil.virtual_memory')
    def test_health_check_memory_warning(self, mock_virtual_memory):
        # Mock low memory
        mock_virtual_memory.return_value = psutil._pslinux.svmem(
            total=1000000000,
            available=50000000,  # 50MB available
            percent=95,
            used=950000000,
            free=50000000,
            active=800000000,
            inactive=150000000,
            buffers=10000000,
            cached=20000000,
            shared=10000000,
            slab=5000000
        )
        
        response = self.client.get(self.health_url)
        data = json.loads(response.content)
        
        self.assertEqual(data['status'], 'warning')
        self.assertEqual(data['checks']['memory']['status'], 'warning')

    @patch('django.db.connection.cursor')
    def test_health_check_database_error(self, mock_cursor):
        # Mock database error
        mock_cursor.side_effect = Exception('Database connection failed')
        
        response = self.client.get(self.health_url)
        data = json.loads(response.content)
        
        self.assertEqual(data['status'], 'unhealthy')
        self.assertEqual(data['checks']['database']['status'], 'unhealthy')
        self.assertIn('error', data['checks']['database']) 