# Why did the 2025 M5.5+ earthquake count spike in July?

A global catalog can have a busy month because activity rose across many regions, or because many events were concentrated near one rupture. I used Avaloka to compute the monthly counts and investigated how much of July’s peak came from a short window near Kamchatka.

## Findings

- The [USGS ComCat export](https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2025-01-01&endtime=2025-12-31T23:59:59.999&minmagnitude=5.5&eventtype=earthquake) contains 514 unique event IDs. The query covers worldwide earthquakes of catalog magnitude 5.5 or greater in calendar year 2025 UTC.
- July had **97 events**, compared with a monthly median of **39**. The next-highest counts were 52 in August and October.
- **28** July events occurred within **500 km** of the [July 29 M8.8 Kamchatka mainshock](https://earthquake.usgs.gov/earthquakes/eventpage/us6000qw60/executive) during July 30–31 UTC. Removing those 28 leaves **69**, still the busiest month.
- The 28 events represent **29% of July's count** and **48% of its excess over the median**. The calculation excludes the July 29 mainshock from the group being removed.
- Avaloka's profile reported a median catalog magnitude of 5.7 and a range of 5.5–8.8. Those are descriptive properties of this magnitude-filtered file.

| UTC month | Distinct events |
| --- | ---: |
| January | 31 |
| February | 24 |
| March | 31 |
| April | 39 |
| May | 41 |
| June | 29 |
| **July** | **97** |
| August | 52 |
| September | 39 |
| October | 52 |
| November | 40 |
| December | 39 |

## Avaloka workflow

The working prompt was: “Create a table and a bar chart of earthquake counts by month. Parse the time column as UTC. Group by UTC month (YYYY-MM) and count distinct id in each group. Return exactly one row per month with columns month and event_count, sorted by month. Use the full dataset.” Avaloka returned all 12 rows, and each count matched the independent computation. A combined aggregation and distance prompt failed its output validation, so the 500 km calculation below comes from the separate verification script.

## Method and limits

I used the full export. There were no missing fields for the requested aggregation and distance check, and no duplicate IDs. The distance uses a Haversine great circle on a 6,371.0088 km sphere, centered on the mainshock epicenter at 52.4948° N, 160.2395° E. The window begins July 30 at 00:00 UTC and ends August 1 at 00:00 UTC, exclusive.

The spatial and time cut describes concentration. Aftershock attribution would require a different analysis. A sample selected by magnitude and time cannot estimate future hazard. July's remaining count also depends on the window and radius chosen.

Run `python3 verify.py` for the independent cross-check against the saved public USGS extract.
