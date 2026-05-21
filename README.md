# compute-resource-finder
Interactive tool to help UIC researchers find the right ACER computational resource

# ACER Computational Resource Finder

An interactive tool to help UIC researchers identify the right computational resource from ACER's portfolio.

**Live app:** [[computefinder.acer.uic.edu](https://acer-compute-finder.streamlit.app) *(update after deploy)*](https://acer-compute-finder.streamlit.app/)

## What it covers

- **Lakeshore HPC — Chicago Computes** — free allocation for faculty PIs
- **Lakeshore HPC — HPC Partnership** — condo/purchase model with GPU and CPU node advisor
- **Secure Computing Environment — On-Premises** — HIPAA/FERPA/PIPA regulated research
- **Secure Computing Environment — Azure** — cloud SCE with NIST 800-171 + GPU options
- **ALCF Lighthouse** — Aurora, Polaris, and AI Testbeds at Argonne National Laboratory

For data storage recommendations, see the companion tool:
[datastoragefinder.acer.uic.edu](https://datastoragefinder.acer.uic.edu)

## Files

| File | Purpose |
|---|---|
| `acer_compute_finder.py` | Main Streamlit app |
| `requirements.txt` | Python dependencies |
| `README.md` | This file |

## Updating resource information

All resource data is in the `RESOURCES`, `GPU_NODES`, and `CPU_NODES` dictionaries near the top of `acer_compute_finder.py`. To update pricing, specs, or descriptions, edit those dictionaries and push to GitHub — Streamlit redeploys automatically.

## Local development

```bash
pip install streamlit pandas
streamlit run acer_compute_finder.py
```

## Contact

ACER · acer@uic.edu · 
