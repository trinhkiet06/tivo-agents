import { redirect } from 'next/navigation';
import { hasValidSession, isCorrectPassword, startSession } from '@/lib/session';

export const dynamic = 'force-dynamic';

async function login(formData: FormData) {
  'use server';
  const password = formData.get('password');
  if (typeof password !== 'string' || !isCorrectPassword(password)) {
    await new Promise((resolve) => setTimeout(resolve, 1000)); // làm chậm việc dò mật khẩu
    redirect('/login?error=1');
  }
  await startSession();
  redirect('/');
}

export default async function LoginPage({
  searchParams,
}: {
  searchParams: Promise<{ error?: string }>;
}) {
  if (await hasValidSession()) redirect('/');
  const { error } = await searchParams;

  return (
    <main className="login">
      <form action={login} className="card login-card">
        <h1>Dashboard bán hàng</h1>
        <label htmlFor="password">Mật khẩu</label>
        <input id="password" name="password" type="password" autoComplete="current-password" required autoFocus />
        {error && <p className="form-error" role="alert">Mật khẩu không đúng.</p>}
        <button type="submit">Xem dữ liệu</button>
      </form>
    </main>
  );
}
