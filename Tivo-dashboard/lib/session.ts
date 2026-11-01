import 'server-only';
import { createHash, createHmac, timingSafeEqual } from 'node:crypto';
import { cookies } from 'next/headers';

const COOKIE_NAME = 'dashboard_session';
const SESSION_SECONDS = 8 * 60 * 60;

const sha256 = (text: string) => createHash('sha256').update(text).digest();

// Khóa ký phụ thuộc mật khẩu, nên đổi DASHBOARD_PASSWORD sẽ hủy mọi phiên đang mở.
function signature(expires: string): Buffer | null {
  const { DASHBOARD_PASSWORD, SUPABASE_SECRET_KEY } = process.env;
  if (!DASHBOARD_PASSWORD || !SUPABASE_SECRET_KEY) return null;
  return createHmac('sha256', sha256(`${SUPABASE_SECRET_KEY}\0${DASHBOARD_PASSWORD}`))
    .update(expires)
    .digest();
}

export function isCorrectPassword(input: string) {
  const { DASHBOARD_PASSWORD } = process.env;
  if (!DASHBOARD_PASSWORD) return false; // chưa đặt mật khẩu thì không ai vào được
  return timingSafeEqual(sha256(input), sha256(DASHBOARD_PASSWORD));
}

export async function startSession() {
  const expires = String(Math.floor(Date.now() / 1000) + SESSION_SECONDS);
  const signed = signature(expires);
  if (!signed) throw new Error('missing_env');
  (await cookies()).set(COOKIE_NAME, `${expires}.${signed.toString('base64url')}`, {
    httpOnly: true,
    sameSite: 'strict',
    secure: process.env.NODE_ENV === 'production',
    path: '/',
    maxAge: SESSION_SECONDS,
  });
}

export async function endSession() {
  (await cookies()).delete(COOKIE_NAME);
}

export async function hasValidSession() {
  const value = (await cookies()).get(COOKIE_NAME)?.value;
  if (!value) return false;

  const [expires, signed] = value.split('.');
  if (!expires || !signed || Number(expires) * 1000 <= Date.now()) return false;

  const expected = signature(expires);
  const actual = Buffer.from(signed, 'base64url');
  return !!expected && actual.length === expected.length && timingSafeEqual(actual, expected);
}
