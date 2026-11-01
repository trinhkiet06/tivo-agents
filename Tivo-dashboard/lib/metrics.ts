// Tính các chỉ số của dashboard. Không truy cập mạng, chỉ làm việc trên dữ liệu đã tải.

export type Order = {
  order_id: string;
  ordered_at: string;
  sku: string;
  product_name: string;
  quantity: number;
  total: number;
  status: string;
};
export type Product = { sku: string; name: string };
export type Stock = { sku: string; stock_now: number; warn_level: number };

const CANCELLED = 'Đã hủy';
const RETURNED = 'Hoàn trả';

// ordered_at là "timestamp without time zone": 10 ký tự đầu chính là ngày trên file gốc,
// không cần đổi múi giờ.
const dayOf = (order: Order) => order.ordered_at.slice(0, 10);

function shiftDay(day: string, delta: number) {
  const date = new Date(`${day}T00:00:00Z`);
  date.setUTCDate(date.getUTCDate() + delta);
  return date.toISOString().slice(0, 10);
}

export type DayPoint = { day: string; revenue: number; orders: number };
export type TopProduct = { sku: string; name: string; quantity: number; revenue: number };
export type LowStock = Stock & { name: string; shortage: number };

export type Metrics = {
  firstDay: string;
  lastDay: string;
  current: { from: string; to: string; revenue: number };
  previous: { from: string; to: string; revenue: number };
  changePct: number | null;
  daily: DayPoint[];
  top: TopProduct[];
  lowStock: LowStock[];
  totalOrders: number;
  cancelled: number;
  returned: number;
};

export function computeMetrics(orders: Order[], products: Product[], stock: Stock[]): Metrics | null {
  if (orders.length === 0) return null;

  const days = orders.map(dayOf).sort();
  const firstDay = days[0];
  const lastDay = days[days.length - 1];

  // Doanh số không tính đơn đã hủy; đơn hoàn trả vẫn được tính theo yêu cầu.
  const sold = orders.filter((order) => order.status !== CANCELLED);

  const byDay = new Map<string, DayPoint>();
  for (let day = firstDay; day <= lastDay; day = shiftDay(day, 1)) {
    byDay.set(day, { day, revenue: 0, orders: 0 });
  }
  for (const order of sold) {
    const point = byDay.get(dayOf(order))!;
    point.revenue += order.total;
    point.orders += 1;
  }

  const revenueBetween = (from: string, to: string) =>
    sold.reduce((sum, o) => (dayOf(o) >= from && dayOf(o) <= to ? sum + o.total : sum), 0);

  // Mốc "7 ngày gần nhất" là ngày có đơn mới nhất, vì dữ liệu là một tháng cố định
  // chứ không cập nhật tới hôm nay.
  const current = { from: shiftDay(lastDay, -6), to: lastDay, revenue: 0 };
  const previous = { from: shiftDay(lastDay, -13), to: shiftDay(lastDay, -7), revenue: 0 };
  current.revenue = revenueBetween(current.from, current.to);
  previous.revenue = revenueBetween(previous.from, previous.to);

  const names = new Map(products.map((p) => [p.sku, p.name]));

  const bySku = new Map<string, TopProduct>();
  for (const order of sold) {
    const item = bySku.get(order.sku) ?? {
      sku: order.sku,
      name: names.get(order.sku) ?? order.product_name,
      quantity: 0,
      revenue: 0,
    };
    item.quantity += order.quantity;
    item.revenue += order.total;
    bySku.set(order.sku, item);
  }

  return {
    firstDay,
    lastDay,
    current,
    previous,
    changePct: previous.revenue > 0 ? ((current.revenue - previous.revenue) / previous.revenue) * 100 : null,
    daily: [...byDay.values()],
    top: [...bySku.values()].sort((a, b) => b.quantity - a.quantity || b.revenue - a.revenue).slice(0, 5),
    lowStock: stock
      .filter((s) => s.stock_now < s.warn_level)
      .map((s) => ({ ...s, name: names.get(s.sku) ?? s.sku, shortage: s.warn_level - s.stock_now }))
      .sort((a, b) => b.shortage - a.shortage),
    totalOrders: orders.length,
    cancelled: orders.filter((o) => o.status === CANCELLED).length,
    returned: orders.filter((o) => o.status === RETURNED).length,
  };
}
