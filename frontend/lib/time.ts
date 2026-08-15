// Turkish relative time formatter — small, no deps.

export function formatRelativeTime(ts: number): string {
  const now = Date.now();
  const diffSec = Math.max(0, Math.round((now - ts) / 1000));

  if (diffSec < 15) return "az önce";
  if (diffSec < 60) return `${diffSec} sn önce`;

  const min = Math.round(diffSec / 60);
  if (min < 60) return `${min} dk önce`;

  const hour = Math.round(min / 60);
  if (hour < 24) return `${hour} sa önce`;

  const day = Math.round(hour / 24);
  if (day < 7) return `${day} gün önce`;

  const d = new Date(ts);
  return d.toLocaleDateString("tr-TR", {
    day: "numeric",
    month: "short",
  });
}
