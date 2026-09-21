const mcWeekdays = ['CN', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7'];
const mcMonthNames = [
  'Tháng 1', 'Tháng 2', 'Tháng 3', 'Tháng 4', 'Tháng 5', 'Tháng 6',
  'Tháng 7', 'Tháng 8', 'Tháng 9', 'Tháng 10', 'Tháng 11', 'Tháng 12'
];
    
const mcToday = new Date();
let mcViewYear = mcToday.getFullYear();
let mcViewMonth = mcToday.getMonth();
let mcSelectedDate = new Date(mcToday);

const mcTitleEl = document.getElementById('mcTitle');
const mcGridEl = document.getElementById('mcGrid');

function mcRender() {
  mcTitleEl.textContent = `${mcMonthNames[mcViewMonth]} ${mcViewYear}`;
  mcGridEl.innerHTML = '';

  mcWeekdays.forEach(w => {
    const el = document.createElement('div');
    el.className = 'mc-weekday';
    el.textContent = w;
    mcGridEl.appendChild(el);
  });

  const firstDay = new Date(mcViewYear, mcViewMonth, 1);
  const startOffset = firstDay.getDay();
  const daysInMonth = new Date(mcViewYear, mcViewMonth + 1, 0).getDate();
  const daysInPrevMonth = new Date(mcViewYear, mcViewMonth, 0).getDate();

  const cells = [];

  for (let i = startOffset - 1; i >= 0; i--) {
    cells.push({ day: daysInPrevMonth - i, otherMonth: true });
  }
  for (let d = 1; d <= daysInMonth; d++) {
    cells.push({ day: d, otherMonth: false });
  }
  while (cells.length % 7 !== 0) {
    cells.push({ day: cells.length - (startOffset + daysInMonth) + 1, otherMonth: true });
  }

  cells.forEach(cell => {
    const el = document.createElement('div');
    el.className = 'mc-day';
    el.textContent = cell.day;

    if (cell.otherMonth) {
      el.classList.add('other-month');
    } else {
      const isToday =
        mcViewYear === mcToday.getFullYear() &&
        mcViewMonth === mcToday.getMonth() &&
        cell.day === mcToday.getDate();

      const isSelected =
        mcViewYear === mcSelectedDate.getFullYear() &&
        mcViewMonth === mcSelectedDate.getMonth() &&
        cell.day === mcSelectedDate.getDate();

      if (isToday) el.classList.add('today');
      else if (isSelected) el.classList.add('selected');

      el.addEventListener('click', () => {
        mcSelectedDate = new Date(mcViewYear, mcViewMonth, cell.day);
        mcRender();
      });
    }

    mcGridEl.appendChild(el);
  });
}

document.getElementById('mcPrevBtn').addEventListener('click', () => {
  mcViewMonth--;
  if (mcViewMonth < 0) { mcViewMonth = 11; mcViewYear--; }
  mcRender();
});

document.getElementById('mcNextBtn').addEventListener('click', () => {
  mcViewMonth++;
  if (mcViewMonth > 11) { mcViewMonth = 0; mcViewYear++; }
  mcRender();
});

document.getElementById('mcTodayBtn').addEventListener('click', () => {
  mcViewYear = mcToday.getFullYear();
  mcViewMonth = mcToday.getMonth();
  mcSelectedDate = new Date(mcToday);
  mcRender();
});

mcRender();