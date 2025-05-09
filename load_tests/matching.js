import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');

// Test configuration
export const options = {
  stages: [
    { duration: '1m', target: 30 },  // Ramp up to 30 users
    { duration: '3m', target: 30 },  // Stay at 30 users
    { duration: '1m', target: 0 },   // Ramp down to 0 users
  ],
  thresholds: {
    'errors': ['rate<0.1'],
    'http_req_duration': ['p(95)<800'],  // Matching can be computationally intensive
  },
};

const BASE_URL = __ENV.API_URL || 'http://localhost:8000/api';

// Test data
const testUser = {
  email: `test${__VU}@example.com`,
  password: 'testpass123',
  username: `testuser${__VU}`,
  role: __VU % 2 === 0 ? 'SEEKER' : 'PROVIDER',
};

export function setup() {
  // Register and login
  const registerRes = http.post(`${BASE_URL}/users/register/`, {
    email: testUser.email,
    password: testUser.password,
    username: testUser.username,
    role: testUser.role,
  });

  check(registerRes, {
    'registration successful': (r) => r.status === 201,
  });

  const loginRes = http.post(`${BASE_URL}/users/login/`, {
    email: testUser.email,
    password: testUser.password,
  });

  check(loginRes, {
    'login successful': (r) => r.status === 200,
  });

  const tokens = loginRes.json();

  // Create profile
  const profileRes = http.post(`${BASE_URL}/profiles/`, {
    company_name: `Test Company ${__VU}`,
    industry: 'Technology',
    location: 'New York',
    description: 'Test company description',
  }, {
    headers: {
      'Authorization': `Bearer ${tokens.access}`,
      'Content-Type': 'application/json',
    },
  });

  check(profileRes, {
    'profile creation successful': (r) => r.status === 201,
  });

  return { 
    user: testUser,
    tokens: tokens,
  };
}

export default function(data) {
  const headers = {
    'Authorization': `Bearer ${data.tokens.access}`,
    'Content-Type': 'application/json',
  };

  if (data.user.role === 'SEEKER') {
    // Test basic matching
    const matchesRes = http.get(`${BASE_URL}/matching/matches/?industry=Technology&location=New%20York`, { headers });

    check(matchesRes, {
      'matches fetch successful': (r) => r.status === 200,
      'has matches': (r) => r.json().length > 0,
    }) || errorRate.add(1);

    // Test ML matching
    const mlMatchesRes = http.post(`${BASE_URL}/matching/ml/`, {
      industry: 'Technology',
      location: 'New York',
      preferences: {
        min_rating: 4.0,
        max_distance: 50,
      },
    }, { headers });

    check(mlMatchesRes, {
      'ML matching successful': (r) => r.status === 200,
      'has ML matches': (r) => r.json().length > 0,
    }) || errorRate.add(1);
  } else {
    // Test opportunities for providers
    const opportunitiesRes = http.get(`${BASE_URL}/matching/opportunities/?industry=Technology&location=New%20York`, { headers });

    check(opportunitiesRes, {
      'opportunities fetch successful': (r) => r.status === 200,
      'has opportunities': (r) => r.json().length > 0,
    }) || errorRate.add(1);
  }

  // Test profile search
  const searchRes = http.get(`${BASE_URL}/profiles/search/?q=Technology`, { headers });

  check(searchRes, {
    'profile search successful': (r) => r.status === 200,
    'has search results': (r) => r.json().length > 0,
  }) || errorRate.add(1);

  sleep(1);
} 