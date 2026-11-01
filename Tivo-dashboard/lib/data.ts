import 'server-only';
import { createClient } from '@supabase/supabase-js';
import { computeMetrics, type Metrics, type Order, type Product, type Stock } from './metrics';

const PAGE_SIZE = 1000;
const MAX_ATTEMPTS = 3;
const ATTEMPT_TIMEOUT_MS = 15_000;

// Supabase đôi khi trả 5xx tạm thời; ở đây chỉ có lệnh đọc nên thử lại an toàn.
async function fetchWithRetry(input: RequestInfo | URL, init?: RequestInit) {
  for (let attempt = 1; ; attempt++) {
    try {
      const response = await fetch(input, { ...init, signal: AbortSignal.timeout(ATTEMPT_TIMEOUT_MS) });
      if (response.status < 500 || attempt === MAX_ATTEMPTS) return response;
    } catch (error) {
      if (attempt === MAX_ATTEMPTS) throw error;
    }
    await new Promise((resolve) => setTimeout(resolve, 1000 * attempt));
  }
}

function client() {
  const { SUPABASE_URL, SUPABASE_SECRET_KEY } = process.env;
  if (!SUPABASE_URL || !SUPABASE_SECRET_KEY) throw new Error('missing_env');
  return createClient(SUPABASE_URL, SUPABASE_SECRET_KEY, {
    auth: { persistSession: false, autoRefreshToken: false },
    global: { fetch: fetchWithRetry },
  });
}

async function readAll<T>(table: string, columns: string, orderBy: string): Promise<T[]> {
  const supabase = client();
  const rows: T[] = [];
  for (let from = 0; ; from += PAGE_SIZE) {
    const { data, error } = await supabase
      .from(table)
      .select(columns)
      .order(orderBy)
      .range(from, from + PAGE_SIZE - 1);
    if (error) {
      // Chỉ ghi mã lỗi: không đưa nội dung phản hồi hay cấu hình vào log.
      console.error(`Không đọc được bảng ${table} (mã lỗi: ${error.code || 'không rõ'})`);
      throw new Error('read_failed');
    }
    rows.push(...(data as T[]));
    if (!data || data.length < PAGE_SIZE) return rows;
  }
}

export async function loadMetrics(): Promise<Metrics | null> {
  const [orders, products, stock] = await Promise.all([
    readAll<Order>('orders', 'order_id,ordered_at,sku,product_name,quantity,total,status', 'order_id'),
    readAll<Product>('products', 'sku,name', 'sku'),
    readAll<Stock>('stock', 'sku,stock_now,warn_level', 'sku'),
  ]);
  return computeMetrics(orders, products, stock);
}
