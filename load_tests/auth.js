import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');

// Test configuration
export const options = {
  stages: [
    { duration: '1m', target: 50 },  // Ramp up to 50 users
    { duration: '3m', target: 50 },  // Stay at 50 users
    { duration: '1m', target: 0 },   // Ramp down to 0 users
  ],
  thresholds: {
    'errors': ['rate<0.1'],  // Error rate should be less than 10%
    'http_req_duration': ['p(95)<500'],  // 95% of requests should be below 500ms
  },
};

const BASE_URL = __ENV.API_URL || 'http://localhost:8000/api';

// Test data
const testUser = {
  email: `test${__VU}@example.com`,
  password: 'testpass123',
  username: `testuser${__VU}`,
};

export function setup() {
  // Register a new user
  const registerRes = http.post(`${BASE_URL}/users/register/`, {
    email: testUser.email,
    password: testUser.password,
    username: testUser.username,
  });

  check(registerRes, {
    'registration successful': (r) => r.status === 201,
  });

  return { user: testUser };
}

export default function(data) {
  // Login
  const loginRes = http.post(`${BASE_URL}/users/login/`, {
    email: data.user.email,
    password: data.user.password,
  });

  check(loginRes, {
    'login successful': (r) => r.status === 200,
    'has access token': (r) => r.json('access') !== undefined,
    'has refresh token': (r) => r.json('refresh') !== undefined,
  }) || errorRate.add(1);

  if (loginRes.status === 200) {
    const tokens = loginRes.json();
    
    // Test token refresh
    const refreshRes = http.post(`${BASE_URL}/users/login/refresh/`, {
      refresh: tokens.refresh,
    });

    check(refreshRes, {
      'refresh successful': (r) => r.status === 200,
      'has new access token': (r) => r.json('access') !== undefined,
    }) || errorRate.add(1);

    // Test protected endpoint
    const headers = {
      'Authorization': `Bearer ${tokens.access}`,
    };

    const profileRes = http.get(`${BASE_URL}/users/me/`, { headers });

    check(profileRes, {
      'profile fetch successful': (r) => r.status === 200,
      'has correct email': (r) => r.json('email') === data.user.email,
    }) || errorRate.add(1);
  }

  sleep(1);
} 