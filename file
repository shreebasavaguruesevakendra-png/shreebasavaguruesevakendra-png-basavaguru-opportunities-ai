# Basavaguru Opportunities AI

An AI-powered digital employee for Shree Basavaguru eSeva Kendra.

Every day, this worker can wake up on GitHub Actions, check government websites, collect new opportunities, organize them by citizen category, and store them in a database. Later, the same database can power Telegram, WhatsApp, Instagram, YouTube Shorts, a website dashboard, and an AI search assistant.

The mission is simple: help Karnataka citizens discover scholarships, schemes, jobs, admissions, welfare benefits, subsidies, and public service notifications without manually searching dozens of government websites.

## What It Does Now

- Reads government/source websites from `config/sources.json`
- Extracts likely opportunity links using scholarship, scheme, recruitment, admission, welfare, subsidy, and deadline keywords
- Categorizes likely opportunities for students, job seekers, women, labour workers, farmers, senior citizens, and public services
- Saves unique opportunities into `data/opportunities.sqlite`
- Exports a readable JSON copy to `data/opportunities.json`
- Runs automatically every day at 8:00 AM India time using GitHub Actions

## Product Vision

Basavaguru Opportunities AI should become a trusted opportunity platform for:

- Students
- Job seekers
- Farmers
- Labour workers
- Women
- Senior citizens
- General public service users

The opportunity is not the final business by itself. The business path is:

```text
Opportunity found
Citizen sees it
Citizen needs help
Basavaguru eSeva Kendra helps
Revenue
```

## Project Structure

```text
.
|-- .github/workflows/daily-worker.yml
|-- config/categories.json
|-- config/sources.json
|-- data/.gitkeep
|-- docs/product_spec.md
|-- prompts/content_generation.md
|-- scripts/run_worker.py
`-- src/basavaguru_worker/
    |-- __init__.py
    |-- scraper.py
    `-- storage.py
```

## Run Locally

```bash
python scripts/run_worker.py
```

The worker will create:

```text
data/opportunities.sqlite
data/opportunities.json
```

## Add More Websites

Edit `config/sources.json`:

```json
{
  "name": "SSP Karnataka",
  "url": "https://ssp.postmatric.karnataka.gov.in/",
  "type": "website",
  "category_hint": "students",
  "enabled": true
}
```

Keep `enabled` as `true` for active sources. Set it to `false` when a source should be skipped temporarily.

## GitHub Actions

The worker runs daily at:

```text
8:00 AM IST
2:30 AM UTC
```

GitHub Actions uses UTC, so the cron expression is:

```text
30 2 * * *
```

You can also run it manually from the GitHub Actions tab.

## Next Phases

1. Improve extraction for each important government website
2. Add eligibility, documents, last date, and application link extraction
3. Send Telegram and WhatsApp updates
4. Generate Instagram captions and poster text
5. Generate YouTube Shorts scripts
6. Launch website dashboard
7. Add a RAG/search assistant over the opportunity database
