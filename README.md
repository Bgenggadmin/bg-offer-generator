# B&G Engineering — Offer Generator

A separate Streamlit application for generating branded techno-commercial offer documents.
Produces DOCX files matching the 11-part B&G offer template, using B&G logo, tagline, and brand colors.

## Features

- **Branded DOCX output** — B&G logo, red/pink colors (#C7203E / #E91E63), "Responsible towards water" tagline, alternating pink table rows, red section headers
- **Full 11-part offer structure** — Executive Summary, Process Description, PFD, Economics, Technical Details, Scope of Supply, Battery Limits, Scope Matrix, Commissioning, Pricing, General T&C
- **Edit flexibility** — Every text section is editable in the UI; equipment lists are editable data tables
- **Form template download** — Excel template trainee engineers can fill offline, then upload back
- **Bridge from process design** — Upload JSON from bg_process_design to auto-populate technical specs, utilities, and economics
- **Two-option pricing** — Titanium & Duplex 2205 (premium) vs SS 316Ti & SS 316L (economy)
- **AI-friendly structure** — Clean hierarchy so when clients use AI summarizers, they get coherent output

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the app

```bash
streamlit run app/main.py
```

### 3. Workflow

1. **Import from process design (optional)**: On the "Templates / Bridge" tab, upload the `full_project.json` exported from `bg_process_design`. Technical specs, utilities, and economics get auto-filled.
2. **Or start from scratch**: The form is pre-populated with a 100 KLD template. Edit per client.
3. **Or fill Excel template offline**: Download the Excel template, fill with a trainee engineer, then upload the filled version via the bridge tab.
4. **Review & customize**: Go through tabs 1–8 to customize executive summary, process descriptions, pricing, scope, etc.
5. **Generate**: Tab 🚀 — click "Generate Offer DOCX", download the file.

## Project Structure

```
bg_offer_generator/
├── app/
│   ├── main.py                 # Streamlit UI entry
│   ├── modules/
│   │   └── docx_generator.py   # python-docx DOCX builder
│   ├── utils/
│   │   ├── brand.py            # Brand colors, fonts, company info
│   │   ├── default_data.py     # 100 KLD template defaults
│   │   ├── form_template.py    # Excel template generator
│   │   └── bridge.py           # Process design JSON → offer bridge
│   └── assets/
│       ├── bg_logo.png         # B&G logo
│       ├── bg_tagline.png      # "Responsible towards water"
│       └── bg_hero_plant.png   # Plant photo for cover
├── .streamlit/
│   └── config.toml             # Streamlit theme
├── requirements.txt
└── README.md
```

## Brand Assets

- **Primary Red**: `#C7203E`
- **Accent Pink**: `#E91E63`
- **Water Blue**: `#2E75B6`
- **Table Header Red**: `#C7203E`
- **Alt Row Tint**: `#FDECEF`

## Tips for AI-Friendly Offers

The offer structure is designed so that when a client pastes it into Claude/ChatGPT,
the AI gets a coherent executive summary. Key design choices:

1. **Clear PART I — Executive Summary** at the top (the AI focuses here first)
2. **Consistent table structure** with headers for easy parsing
3. **Numeric specs separated from narrative** — AI can extract both
4. **ECOX-ZLD Advantage table** highlights savings prominently
5. **Performance Guarantee bullets** are structured for easy extraction

## License

Proprietary — B&G Engineering Industries
