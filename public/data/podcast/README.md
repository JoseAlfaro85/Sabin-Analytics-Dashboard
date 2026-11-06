# Podcast report refresh

The report reads `data/<latest dashboard month>/<latest dashboard month>_podcast_analytics.csv`. The refresh job rebuilds that file from the canonical daily table at `data/podcast/podcast_daily.csv` and then regenerates the dashboard HTML.

## Add platform exports

Drop CSV exports into the matching folder and run `scripts/refresh_podcast_report.py`:

- `data/podcast/inbox/apple/`
- `data/podcast/inbox/spotify/`
- `data/podcast/inbox/youtube/`

The job accepts either a long format with fields such as `date`, `episode`, `platform`, `metric`, and `value`, or a wide format with `Episode`, `Published`, and one column per `YYYY-MM-DD` date. The platform folder is used when the file does not include a platform column.

The existing manually entered file is used as the seed. When an export includes a platform-specific row for the same episode and date, the platform rows replace the combined seed for that date so the dashboard does not add the same activity twice.

The dashboard measure is intentionally named “reported listening activity.” Apple Podcasts, Spotify, and YouTube do not define or expose an identical deduplicated listening-session metric, so the source metric is retained in `podcast_daily.csv` and the report footnote explains the additive treatment.

## Run the refresh

```text
python scripts/refresh_podcast_report.py
```

The job writes `podcast_refresh_status.json` with the last refresh time, date-through, source files, row counts, and platform coverage. It also rebuilds the local HTML package and synchronizes the `public` folder when Node.js is available.
