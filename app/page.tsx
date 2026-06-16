"use client";

import { useEffect } from "react";

export default function Home() {
  useEffect(() => {
    const target = new URL("/DASHBOARD_PREVIEW.html", window.location.href);
    const currentParams = new URLSearchParams(window.location.search);
    currentParams.forEach((value, key) => target.searchParams.set(key, value));
    if (!target.searchParams.has("month")) {
      target.searchParams.set("month", "2026-05");
    }
    if (!target.searchParams.has("mode")) {
      target.searchParams.set("mode", "month");
    }
    window.location.replace(target.toString());
  }, []);

  return (
    <main className="min-h-screen bg-white px-6 py-16 text-slate-900">
      <div className="mx-auto flex max-w-2xl flex-col gap-4">
        <p className="text-sm font-semibold uppercase tracking-[0.18em] text-slate-500">
          Sabin Vaccine Institute
        </p>
        <h1 className="text-3xl font-semibold tracking-tight">
          Opening the dashboard...
        </h1>
        <p className="text-base leading-7 text-slate-600">
          If the dashboard does not open automatically, use the link below.
        </p>
        <a
          className="inline-flex w-fit items-center rounded-md bg-[#196BAC] px-4 py-2 text-sm font-semibold text-white"
          href="/DASHBOARD_PREVIEW.html?month=2026-05&mode=month"
        >
          Open dashboard
        </a>
      </div>
    </main>
  );
}
