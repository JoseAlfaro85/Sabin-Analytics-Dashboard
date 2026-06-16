# Sabin Dashboard Handoff

## Folder

This handoff file lives in:

`C:\Users\JAlfaro\OneDrive - Albert B. Sabin Vaccine Institute\Sabin Communications - Performance Dashboard`

## What changed

This round focused on stabilizing the May 2026 dashboard snapshot and aligning the social + web reporting logic.

### 1. May 2026 social metrics

- `Tracked Link Clicks` now uses the Ow.ly / tracked URL export as the main click metric.
- The dashboard no longer treats post link clicks and Ow.ly tracked clicks as two separate report-facing stories.
- May 2026 now shows:
  - `42,457` total followers
  - `+1,727` net new followers
  - `3,038` total engagements
  - `5,663` tracked link clicks

### 2. May 2026 web analytics

- The saved GA4 fallback now loads correctly from the archived monthly GA4 raw extract.
- May 2026 web analytics now shows:
  - `13,173` sessions
  - `10,954` total users
  - `10,378` new users
  - `95.67%` engagement rate
  - `23s` average engagement time

### 3. Local server fix

- The local dashboard server now supports:
  - `/` as home
  - `/app` as home
  - no-cache headers so the browser stops showing stale HTML

Use:

`http://127.0.0.1:8765/`

## Files changed

### Source / pipeline files

These are the main logic changes:

- `C:\Users\JAlfaro\OneDrive - Albert B. Sabin Vaccine Institute\Desktop\Python Scripts\reporting_framework.py`
- `C:\Users\JAlfaro\OneDrive - Albert B. Sabin Vaccine Institute\Desktop\Python Scripts\dashboard_preview_builder.py`
- `C:\Users\JAlfaro\OneDrive - Albert B. Sabin Vaccine Institute\Desktop\Python Scripts\hootsuite_to_dashboard.py`

### Dashboard/server files

- `C:\Users\JAlfaro\OneDrive - Albert B. Sabin Vaccine Institute\Sabin Communications - Performance Dashboard\dashboard_server.py`
- `C:\Users\JAlfaro\OneDrive - Albert B. Sabin Vaccine Institute\Desktop\SharePoint - Sabin Communications\Digital Comms Team\Social & Digital Analytics\Performance Dashboards\dashboard_server.py`

### Optional hosting scaffold added

These were added while preparing for a public deployment:

- `.openai\hosting.json`
- `package.json`
- `vite.config.ts`
- `next.config.ts`
- `tsconfig.json`
- `postcss.config.mjs`
- `build\sites-vite-plugin.ts`
- `worker\index.ts`
- `app\layout.tsx`
- `app\page.tsx`
- `app\globals.css`
- `scripts\sync-dashboard-public.mjs`
- `public\...`

## Important note on public deployment

I prepared the dashboard root so it can be wrapped and deployed through Sites, but the actual Sites deployment was blocked because:

`Sites is not yet enabled for this workspace.`

So the dashboard is locally ready, but there is not yet a true hosted production URL from the Sites connector.

## Recommended Git structure

There are really two buckets of work:

### Commit 1: reporting logic + dashboard refresh

Include:

- `Desktop Python Scripts\reporting_framework.py`
- `Desktop Python Scripts\dashboard_preview_builder.py`
- `Desktop Python Scripts\hootsuite_to_dashboard.py`
- refreshed dashboard HTML / JSON in `Sabin Communications - Performance Dashboard`

Suggested commit message:

`Align May dashboard metrics and restore GA4 fallback`

### Commit 2: optional hosting scaffold

Include:

- `.openai`
- `app`
- `build`
- `worker`
- `public`
- `package.json`
- `vite.config.ts`
- `next.config.ts`
- `tsconfig.json`
- `postcss.config.mjs`
- `scripts\sync-dashboard-public.mjs`

Suggested commit message:

`Prepare dashboard wrapper for hosted deployment`

If you do not want to keep the hosting experiment yet, review those files before committing them.

## How to rebuild

### Full pipeline rebuild

Run:

`C:\Users\JAlfaro\OneDrive - Albert B. Sabin Vaccine Institute\Desktop\Python Scripts\hootsuite_to_dashboard.py`

This refreshes the monthly JSON package and syncs dashboard files to the SharePoint-synced dashboard folder.

### HTML-only refresh from saved JSON

Run:

`C:\Users\JAlfaro\OneDrive - Albert B. Sabin Vaccine Institute\Desktop\Python Scripts\update_dashboard.py --default-month 2026-05`

## Local run

Preferred local entry:

`http://127.0.0.1:8765/`

If you restart manually, use the dashboard server from:

`C:\Users\JAlfaro\OneDrive - Albert B. Sabin Vaccine Institute\Desktop\SharePoint - Sabin Communications\Digital Comms Team\Social & Digital Analytics\Performance Dashboards\dashboard_server.py`

## Open follow-ups

### Part 2

Planned next item:

- add an `LLM Visibility` monthly layer to the dashboard using a monthly JSON input, similar to `talkwalker_insights.json`

### Public link

Still needed:

- either enable the Sites connector in this workspace
- or choose another approved hosting method for a true team-facing public URL
