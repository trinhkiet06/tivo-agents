// Nạp dữ liệu từ các file Excel trong data/ vào Supabase. Chạy: npm run load
// Dùng upsert theo khóa chính nên chạy lại nhiều lần không tạo dòng trùng.
// File Excel chỉ được đọc, không bao giờ bị ghi lại.
import { readdirSync } from 'node:fs';
import path from 'node:path';
import ExcelJS from 'exceljs';
import { createClient } from '@supabase/supabase-js';

const DATA_DIR = path.join(import.meta.dirname, '..', 'data');
const BATCH_SIZE = 200;
const MAX_ATTEMPTS = 6;
const ATTEMPT_TIMEOUT_MS = 30_000;

const SOURCES = {
  products: {
    files: ['THÔNG TIN SẢN PHẨM.xlsx'],
    key: 'sku',
    columns: {
      sku: ['MÃ SP', 'text'],
      name: ['TÊN SẢN PHẨM', 'text'],
      list_price: ['GIÁ NIÊM YẾT', 'int'],
      daily_price: ['GIÁ BÁN DAILY', 'int'],
      camp_price: ['GIÁ BÁN CAMP', 'int'],
      voucher: ['VOUCHER', 'int?'], // ô trống = sản phẩm không có voucher
    },
  },
  orders: {
    // Tên file thực tế là don-hang-thang.xlsx; vẫn nhận tên don-hang-thang-10.xlsx.
    files: ['don-hang-thang.xlsx', 'don-hang-thang-10.xlsx'],
    key: 'order_id',
    columns: {
      order_id: ['Mã đơn hàng', 'text'],
      ordered_at: ['Ngày đặt hàng', 'datetime'],
      sku: ['Mã SP', 'text'],
      product_name: ['Tên sản phẩm', 'text'],
      quantity: ['Số lượng', 'int'],
      unit_price: ['Giá bán (VND)', 'int'],
      shop_voucher: ['Voucher shop (VND)', 'int'],
      total: ['Tổng tiền (VND)', 'int'],
      status: ['Trạng thái', 'text'],
      payment_method: ['Phương thức thanh toán', 'text'],
      province: ['Tỉnh/Thành phố', 'text'],
    },
  },
  stock: {
    files: ['ton-kho.xlsx'],
    key: 'sku',
    columns: {
      sku: ['Mã SP', 'text'],
      stock_now: ['Tồn kho hiện tại', 'int'],
      warn_level: ['Ngưỡng cảnh báo', 'int'],
    },
  },
};

// Tên file tiếng Việt có thể lưu ở dạng Unicode khác nhau (NFC/NFD), dấu cách có thể là "_".
const canonical = (name) => name.normalize('NFC').replaceAll('_', ' ').toLowerCase();

function findFile(candidates) {
  const wanted = new Set(candidates.map(canonical));
  const match = readdirSync(DATA_DIR).find((file) => wanted.has(canonical(file)));
  if (!match) throw new Error(`Không tìm thấy file trong data/: ${candidates.join(' hoặc ')}`);
  return path.join(DATA_DIR, match);
}

// Ô có link trả về object; lấy giá trị hiển thị trong ô.
function cellValue(raw) {
  if (raw && typeof raw === 'object' && !(raw instanceof Date)) {
    if ('result' in raw) return raw.result;
    if ('text' in raw) return raw.text;
    if (raw.richText) return raw.richText.map((part) => part.text).join('');
  }
  return raw ?? null;
}

const headerText = (value) => String(value ?? '').normalize('NFC').trim();

function convert(value, type, where) {
  const isEmpty = value === null || value === '';
  if (type === 'int?' && isEmpty) return null;
  if (isEmpty) throw new Error(`${where}: ô trống`);

  switch (type) {
    case 'text':
      return String(value).normalize('NFC').trim();
    case 'int':
    case 'int?':
      if (!Number.isInteger(value)) throw new Error(`${where}: không phải số nguyên (${value})`);
      return value;
    case 'datetime':
      if (!(value instanceof Date)) throw new Error(`${where}: không phải ngày giờ (${value})`);
      // Excel lưu giờ địa phương, không có múi giờ; ExcelJS trả về dưới dạng UTC.
      // Giữ nguyên giờ trên file vì cột DB là "timestamp without time zone".
      return value.toISOString().slice(0, 19);
    default:
      throw new Error(`Kiểu không hỗ trợ: ${type}`);
  }
}

async function readTable({ files, key, columns }) {
  const file = findFile(files);
  const workbook = new ExcelJS.Workbook();
  await workbook.xlsx.readFile(file);
  const sheet = workbook.worksheets[0];

  // Dòng tiêu đề không cố định (file sản phẩm có dòng tiêu đề lớn ở trên),
  // nên tìm dòng đầu tiên chứa đủ các cột cần thiết.
  const required = Object.values(columns).map(([header]) => header);
  let headerRow = 0;
  const position = new Map();
  for (let r = 1; r <= Math.min(sheet.rowCount, 20) && !headerRow; r++) {
    const row = sheet.getRow(r);
    const found = new Map();
    row.eachCell((cell, c) => {
      const text = headerText(cellValue(cell.value));
      if (!found.has(text)) found.set(text, c);
    });
    if (required.every((h) => found.has(h.normalize('NFC')))) {
      headerRow = r;
      found.forEach((c, text) => position.set(text, c));
    }
  }
  if (!headerRow) throw new Error(`${path.basename(file)}: không tìm thấy dòng tiêu đề`);

  const keyColumn = position.get(columns[key][0].normalize('NFC'));
  const rows = [];
  const seen = new Set();
  for (let r = headerRow + 1; r <= sheet.rowCount; r++) {
    const row = sheet.getRow(r);
    if (headerText(cellValue(row.getCell(keyColumn).value)) === '') continue; // dòng trống

    const record = {};
    for (const [column, [header, type]] of Object.entries(columns)) {
      const raw = cellValue(row.getCell(position.get(header.normalize('NFC'))).value);
      record[column] = convert(raw, type, `${path.basename(file)} dòng ${r}, cột "${header}"`);
    }
    if (seen.has(record[key])) {
      throw new Error(`${path.basename(file)} dòng ${r}: trùng ${key} = ${record[key]}`);
    }
    seen.add(record[key]);
    rows.push(record);
  }
  return { file: path.basename(file), rows };
}

// Supabase đôi khi trả 5xx tạm thời. Mọi lệnh ở đây là upsert/đếm nên thử lại an toàn.
async function fetchWithRetry(input, init) {
  for (let attempt = 1; ; attempt++) {
    try {
      const response = await fetch(input, { ...init, signal: AbortSignal.timeout(ATTEMPT_TIMEOUT_MS) });
      if (response.status < 500 || attempt === MAX_ATTEMPTS) return response;
      console.log(`  Supabase trả ${response.status}, thử lại (${attempt}/${MAX_ATTEMPTS - 1})...`);
    } catch (error) {
      if (attempt === MAX_ATTEMPTS) throw error;
      console.log(`  Lỗi kết nối, thử lại (${attempt}/${MAX_ATTEMPTS - 1})...`);
    }
    await new Promise((resolve) => setTimeout(resolve, 2000 * attempt));
  }
}

function describe(error) {
  // Chuỗi lỗi HTML từ gateway rất dài và không có ích; chỉ giữ phần ngắn.
  const message = String(error?.message ?? error).split('\n')[0].slice(0, 200);
  return error?.code ? `${error.code}: ${message}` : message;
}

async function main() {
  const { SUPABASE_URL, SUPABASE_SECRET_KEY } = process.env;
  if (!SUPABASE_URL || !SUPABASE_SECRET_KEY) {
    throw new Error('Thiếu SUPABASE_URL hoặc SUPABASE_SECRET_KEY trong .env.local');
  }

  // Đọc và kiểm tra cả 3 file trước khi ghi, để file lỗi không gây nạp dở dang.
  const tables = {};
  for (const [table, source] of Object.entries(SOURCES)) {
    tables[table] = await readTable(source);
    console.log(`Đọc ${tables[table].file}: ${tables[table].rows.length} dòng`);
  }

  const supabase = createClient(SUPABASE_URL, SUPABASE_SECRET_KEY, {
    auth: { persistSession: false, autoRefreshToken: false },
    global: { fetch: fetchWithRetry },
  });

  // Thứ tự của SOURCES: products trước, vì orders và stock tham chiếu sku.
  for (const [table, source] of Object.entries(SOURCES)) {
    const { rows } = tables[table];
    for (let i = 0; i < rows.length; i += BATCH_SIZE) {
      const { error } = await supabase
        .from(table)
        .upsert(rows.slice(i, i + BATCH_SIZE), { onConflict: source.key });
      if (error) throw new Error(`Nạp bảng ${table} thất bại - ${describe(error)}`);
    }
    console.log(`Đã nạp bảng ${table}`);
  }

  console.log('\nSố dòng hiện có trong Supabase:');
  for (const table of Object.keys(SOURCES)) {
    const { count, error } = await supabase.from(table).select('*', { count: 'exact', head: true });
    if (error) throw new Error(`Đếm bảng ${table} thất bại - ${describe(error)}`);
    console.log(`  ${table}: ${count}`);
  }
}

main().catch((error) => {
  console.error(`\nLỖI: ${describe(error)}`);
  process.exitCode = 1;
});
