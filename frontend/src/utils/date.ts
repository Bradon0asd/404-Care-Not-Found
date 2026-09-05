const WEEKDAYS = ['日', '一', '二', '三', '四', '五', '六']

export function toMinguoDate(date: Date): string {
  const year = date.getFullYear() - 1911
  const month = date.getMonth() + 1
  const day = date.getDate()
  const weekday = WEEKDAYS[date.getDay()]
  return `民國${year}年${month}月${day}日（星期${weekday}）`
}
