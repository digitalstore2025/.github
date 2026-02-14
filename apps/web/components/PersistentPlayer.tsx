"use client";

export function PersistentPlayer(): JSX.Element {
  return (
    <div className="player" dir="rtl">
      <strong>الإذاعة المباشرة</strong>
      <audio controls preload="none" style={{ width: "100%", marginTop: 8 }}>
        <source src="/api/stream/live" type="audio/mpeg" />
      </audio>
    </div>
  );
}
