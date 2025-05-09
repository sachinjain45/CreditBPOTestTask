import { Suspense } from 'react';
import LoginFormWithParams from './LoginFormWithParams';

export default function LoginPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <LoginFormWithParams />
    </Suspense>
  );
}