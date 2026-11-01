import { redirect } from 'next/navigation';
import { loadMetrics } from '@/lib/data';
import type { DayPoint, Metrics } from '@/lib/metrics';
import { endSession, hasValidSession } from '@/lib/session';

export const dynamic = 'force-dynamic';

const number = new Intl.NumberFormat('vi-VN');
const money = (value: number) => `${number.format(value)} ₫`;
const percent = (value: number) =>
  `${new Intl.NumberFormat('vi-VN', { minimumFractionDigits: 1, maximumFractionDigits: 1 }).format(value)}%`;
const shortDay = (day: string) => `${day.slice(8, 10)}/${day.slice(5, 7)}`;
const fullDay = (day: string) => `${shortDay(day)}/${day.slice(0, 4)}`;
const millions = (value: number) =>
  `${new Intl.NumberFormat('vi-VN', { maximumFractionDigits: 1 }).format(value / 1_000_000)} tr`;

async function logout() {
  'use server';
  await endSession();
  redirect('/login');
}

export default async function DashboardPage() {
  // Kiểm tra phiên trước khi đọc dữ liệu: chưa đăng nhập thì không truy vấn gì cả.
  if (!(await hasValidSession())) redirect('/login');

  let metrics: Metrics | null = null;
  let failed = false;
  try {
    metrics = await loadMetrics();
  } catch {
    failed = true;
  }

  return (
    <main className="page">
      <header className="page-header">
        <div>
          <h1>Dashboard bán hàng</h1>
          {metrics && (
            <p className="muted">
              Dữ liệu từ {fullDay(metrics.firstDay)} đến {fullDay(metrics.lastDay)}
            </p>
          )}
        </div>
        <form action={logout}>
          <button type="submit" className="ghost">Đăng xuất</button>
        </form>
      </header>

      {failed && (
        <section className="card" role="alert">
          <h2>Không tải được dữ liệu</h2>
          <p className="muted">Không kết nối hoặc không đọc được Supabase. Hãy tải lại trang sau ít phút.</p>
        </section>
      )}
      {!failed && !metrics && (
        <section className="card">
          <h2>Chưa có dữ liệu</h2>
          <p className="muted">Bảng đơn hàng đang trống. Chạy npm run load để nạp dữ liệu.</p>
        </section>
      )}
      {metrics && <Dashboard metrics={metrics} />}

      <footer className="footer">Dữ liệu mẫu, chỉ dùng để minh họa.</footer>
    </main>
  );
}

function Dashboard({ metrics }: { metrics: Metrics }) {
  const { current, previous, changePct, totalOrders, cancelled, returned } = metrics;
  const rate = (count: number) => (count / totalOrders) * 100;

  return (
    <>
      <section className="tiles">
        <div className="card tile tile-hero">
          <h2>Doanh số 7 ngày gần nhất</h2>
          <p className="hero">{money(current.revenue)}</p>
          <p className="muted">{shortDay(current.from)} – {shortDay(current.to)}</p>
          <Change pct={changePct} />
          <p className="muted">
            7 ngày trước đó ({shortDay(previous.from)} – {shortDay(previous.to)}): {money(previous.revenue)}
          </p>
        </div>
        <div className="card tile">
          <h2>Tỷ lệ đơn hủy</h2>
          <p className="stat">{percent(rate(cancelled))}</p>
          <p className="muted">{number.format(cancelled)} / {number.format(totalOrders)} đơn</p>
        </div>
        <div className="card tile">
          <h2>Tỷ lệ hoàn trả</h2>
          <p className="stat">{percent(rate(returned))}</p>
          <p className="muted">{number.format(returned)} / {number.format(totalOrders)} đơn</p>
        </div>
      </section>

      <section className="card">
        <h2>Doanh số theo ngày</h2>
        <p className="muted">Không tính đơn đã hủy</p>
        <DailyChart points={metrics.daily} />
        <details className="table-view">
          <summary>Xem dạng bảng</summary>
          <div className="table-scroll">
            <table>
              <thead>
                <tr><th>Ngày</th><th className="num">Số đơn</th><th className="num">Doanh số</th></tr>
              </thead>
              <tbody>
                {metrics.daily.map((point) => (
                  <tr key={point.day}>
                    <td>{fullDay(point.day)}</td>
                    <td className="num">{number.format(point.orders)}</td>
                    <td className="num">{money(point.revenue)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </details>
      </section>

      <div className="columns">
        <section className="card">
          <h2>Top 5 sản phẩm bán chạy</h2>
          <p className="muted">Theo số lượng bán, cả kỳ dữ liệu, không tính đơn đã hủy</p>
          <ol className="ranking">
            {metrics.top.map((item) => (
              <li key={item.sku}>
                <div className="ranking-label">
                  <span>{item.name}</span>
                  <span className="muted">{money(item.revenue)}</span>
                </div>
                <div className="ranking-bar">
                  <span className="bar-h" style={{ width: `${(item.quantity / metrics.top[0].quantity) * 85}%` }} />
                  <span className="ranking-value">{number.format(item.quantity)}</span>
                </div>
              </li>
            ))}
          </ol>
        </section>

        <section className="card">
          <h2>Tồn kho dưới ngưỡng cảnh báo</h2>
          {metrics.lowStock.length === 0 ? (
            <p className="muted">Không có sản phẩm nào dưới ngưỡng.</p>
          ) : (
            <>
              <p className="warning-note"><span aria-hidden="true">⚠</span> {metrics.lowStock.length} sản phẩm cần nhập thêm</p>
              <div className="table-scroll">
                <table>
                  <thead>
                    <tr><th>Sản phẩm</th><th className="num">Tồn</th><th className="num">Ngưỡng</th><th className="num">Thiếu</th></tr>
                  </thead>
                  <tbody>
                    {metrics.lowStock.map((item) => (
                      <tr key={item.sku}>
                        <td>{item.name}<br /><span className="muted">{item.sku}</span></td>
                        <td className="num">{number.format(item.stock_now)}</td>
                        <td className="num">{number.format(item.warn_level)}</td>
                        <td className="num">{number.format(item.shortage)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </>
          )}
        </section>
      </div>
    </>
  );
}

function Change({ pct }: { pct: number | null }) {
  if (pct === null) return <p className="muted">Không có dữ liệu kỳ trước để so sánh</p>;
  const up = pct >= 0;
  return (
    <p className={up ? 'delta delta-up' : 'delta delta-down'}>
      <span aria-hidden="true">{up ? '▲' : '▼'}</span> {up ? 'Tăng' : 'Giảm'} {percent(Math.abs(pct))} so với 7 ngày trước đó
    </p>
  );
}

function niceStep(max: number) {
  const rough = Math.max(max, 1) / 4;
  const magnitude = 10 ** Math.floor(Math.log10(rough));
  return [1, 2, 5, 10].map((m) => m * magnitude).find((step) => step >= rough)!;
}

// Biểu đồ cột dựng bằng HTML/CSS: co giãn theo màn hình mà chữ không bị co theo,
// tooltip chạy bằng :hover và :focus nên không cần JavaScript ở trình duyệt.
function DailyChart({ points }: { points: DayPoint[] }) {
  const peak = Math.max(...points.map((p) => p.revenue));
  const step = niceStep(peak);
  const axisMax = Math.max(Math.ceil(peak / step), 1) * step;
  const ticks: number[] = [];
  for (let tick = 0; tick <= axisMax; tick += step) ticks.push(tick);
  const peakDay = points.find((p) => p.revenue === peak)?.day;
  const count = points.length;

  const edge = (i: number) => (i < 4 ? 'at-start' : i >= count - 4 ? 'at-end' : '');

  return (
    <div className="chart">
      <div className="plot">
        {ticks.map((tick) => (
          <div key={tick} className={tick === 0 ? 'grid baseline' : 'grid'} style={{ bottom: `${(tick / axisMax) * 100}%` }}>
            <span>{tick === 0 ? '0' : millions(tick)}</span>
          </div>
        ))}
        <div className="cols">
          {points.map((point, i) => {
            const height = (point.revenue / axisMax) * 100;
            return (
              <div
                key={point.day}
                className={`col ${edge(i)}`}
                tabIndex={0}
                role="img"
                aria-label={`${fullDay(point.day)}: ${money(point.revenue)}, ${point.orders} đơn`}
              >
                <div className="bar" style={{ height: `${height}%` }} />
                {point.day === peakDay && peak > 0 && (
                  <span className="peak" style={{ bottom: `${height}%` }}>{millions(point.revenue)}</span>
                )}
                <div className="tip" style={{ bottom: `${height}%` }}>
                  <strong>{fullDay(point.day)}</strong>
                  <span>{money(point.revenue)}</span>
                  <span>{number.format(point.orders)} đơn</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
      <div className="xaxis" aria-hidden="true">
        {points.map((point, i) => (
          <div key={point.day}>{(count - 1 - i) % 7 === 0 && <span>{shortDay(point.day)}</span>}</div>
        ))}
      </div>
    </div>
  );
}
