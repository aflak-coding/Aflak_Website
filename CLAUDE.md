# CLAUDE.md — Aflak Recruitment website (شركة أفلاك للاستقدام)

Read this first. The owner (Medo / ميدو) is not a developer and is worried about breaking the live site. Be careful, explain simply.

## How to talk to Medo
- Reply in **Egyptian Arabic** for normal chat; keep code, file names and commands in English.
- Short, step-by-step answers. No jargon without a one-line explanation.
- **Tell him BEFORE adding anything he did not ask for** (new features, extra pages, extra buttons). Do only what he asked.
- If something is unclear, ask one short question instead of guessing.

## SAFETY RULES (most important)
1. **Never push to `main` directly.** Work on a branch named `work/<short-topic>` (e.g. `work/tailoring-job`).
2. When done: commit, push the branch, and tell Medo exactly what changed in plain Arabic. He merges it on GitHub (Pull request → Merge). If `gh` is available, open the pull request for him.
3. Only push to `main` if he says explicitly "ادفع على main". Never force-push. Never delete branches, files in `cvs/`, or `data/*.json` unless asked.
4. Before editing `data/cvs-*.json`, `cvs/` PDFs, or `.github/workflows/*`, ask first. CVs and the parsed JSON are the company's real data.
5. Test before saying "done": run the local checks below. Show him what was tested.
6. If something goes wrong, stop, explain, and offer `git restore` / `git revert`. Do not improvise destructive commands.

## What this project is
- Arabic-first (RTL) static site with AR/EN toggle. Live: https://aflakrecruitment.com (GitHub Pages, repo `aflak-coding/Aflak_Website`, branch `main`).
- Pure HTML/CSS/vanilla JS. **No build step, no npm.** Deployed by `.github/workflows/jekyll-gh-pages.yml` on every push to `main`.
- Content editing: **Pages CMS** (`.pages.yml`) — the team uploads CV PDFs there.
- CV pipeline: GitHub Action `.github/workflows/process-cvs.yml` runs `scripts/process_cvs.py` which reads new PDFs (text layer via pdftotext, OCR via tesseract for scans), fills `data/cvs-<country>.json`, and crops photos with `scripts/cvphoto.py`.
- Sub-pages (`services/`, `nationalities/`, `privacy.html`, `sitemap.xml`) are **generated** by `scripts/build_pages.py`. Do not hand-edit generated pages; edit the script and regenerate.

## Key files
| File | Purpose |
|---|---|
| `index.html` | Main page. Asset links carry cache-busting `?v=N` (currently 36). **Bump N whenever `assets/app.js` or `assets/style.css` change**, otherwise visitors see old files. |
| `assets/app.js` | All behaviour + i18n dictionary `D{ar,en}`, CV list/filters/pagination (8 per page desktop, 4 mobile), share bar, CV viewer dialog, order form. |
| `assets/style.css` | All styling. |
| `.pages.yml` | CMS config. Job/nationality select options exist in **six collections** — a new option must be added to all six. |
| `scripts/process_cvs.py` | CV parser (job, age, religion, status, experience, passport-hash dedupe). |
| `scripts/cvphoto.py` | Photo cropper (embedded images, scans, and the "Tawasul" template). |
| `data/cvs-<country>.json` | `{"cvs":[...]}` one file per nationality. |

## Data model (each CV in `data/cvs-*.json`)
`nat` (n1 Kenya, n2 Bangladesh, n3 Philippines, n4 Ethiopia, n5 Sri Lanka, n6 Uganda — currently hidden), `name`, `ref`, `job`, `age`, `rel`, `st`, `exp`, `status`, `file`, `photo`.
- `job`: svc1 housemaid · svc2 driver · svc3 cook · svc4 nurse · svc5 personal assistant · **svc7 tailor/seamstress**. (`svc6` = "طلب تفويض" authorization request: only an order-form option, NOT a CV job.)
- `rel`: m = مسلم, o = غير مسلم. `st`: marital status. `exp`: `new` (first timer) or `prev` (has experience). `status`: `available` | `reserved` | `hidden`.
- Hidden auto fields: `pp` (passport hash), `xc`, `xd`, `xe` (one-time recheck flags) — never edit by hand.
- Adding a new job: update `svcs` in both languages, `JOBS` array, `pendingJob` check in `goNat`, the job icon map in `app.js`; all six places in `.pages.yml`; job detection in `process_cvs.py`.

## Known CV template quirks
- Experienced CVs have a table `COUNTRY / PROFESSION / FOR YEARS` with a country row → `prev`. `FIRST TIMER` alone → `new`. Do not treat "FIRST TIME" in a language table as experience.
- `NON-MUSLIM` must map to `rel: "o"` (check it BEFORE `MUSLIM`).
- Tawasul-template CVs are image-only PDFs (OCR path). Name is white-on-blue and not OCR-readable → name comes from the file name (`FIRST_LAST.pdf`). Page 2 is the passport: never use it for photos or data.

## Local checks before every commit
```bash
node --check assets/app.js
python -I -c "import ast;ast.parse(open('scripts/process_cvs.py',encoding='utf-8').read())"
python scripts/build_pages.py   # only if services/nationalities pages are affected
python -m http.server 8000      # then open http://localhost:8000 and click through
```
Test the page at desktop width AND phone width (390px): hero fills the screen, nationality flags, "ابحث في كل الجنسيات" button, CV filters, CV viewer, reserved CVs (button must be disabled), order form, language toggle, no horizontal scrolling.

## Don't touch without asking
`CNAME`, `robots.txt`, `sitemap.xml` (generated), Google Search Console / Analytics tags, `.github/workflows/*`, the domain settings.

## Open items
Uganda still hidden · "كيف تتم الخدمة؟" content not written · service sub-pages' own WhatsApp buttons unchanged · optional: hide the share bar.
