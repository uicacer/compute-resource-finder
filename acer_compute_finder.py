"""
ACER UIC Computational Resource Finder
Aesthetics: clean/minimal to match datastoragefinder.acer.uic.edu
Deploy: GitHub → share.streamlit.io
"""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Computational Resource Finder | ACER UIC",
    page_icon="🔬",
    layout="wide",
)

st.markdown("""
<style>
/* ── Reset & base ─────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1rem 2rem 2rem 2rem !important; max-width: 100% !important; }
html, body, [class*="css"] {
    font-family: Arial, "Helvetica Neue", sans-serif;
    font-size: 14px; color: #222;
}

/* ── Page header ──────────────────────────────── */
.page-header {
    border-bottom: 2px solid #ddd;
    padding-bottom: 10px; margin-bottom: 12px;
}
.page-header h1 {
    font-size: 20px; font-weight: 700; color: #333; margin: 0 0 2px 0;
}
.page-header p { font-size: 13px; color: #666; margin: 0; }

/* ── Info bars ────────────────────────────────── */
.info-bar {
    background: #f0f6ff; border: 1px solid #c5d8f5;
    border-radius: 3px; padding: 8px 12px;
    font-size: 13px; color: #1a3a6b; margin-bottom: 10px;
}
.info-bar a { color: #1a5cb8; }

/* ── Section headings ─────────────────────────── */
.panel-head {
    font-size: 15px; font-weight: 700; color: #333;
    border-bottom: 1px solid #ccc; padding-bottom: 5px; margin-bottom: 10px;
}
.panel-subhead { font-size: 12px; color: #666; margin: -6px 0 10px 0; }

/* ── Service cards ────────────────────────────── */
.svc-card {
    background: #fff; border: 1px solid #d0d0d0;
    border-radius: 3px; padding: 12px 14px; margin-bottom: 10px;
}
.svc-card-sel { border-left: 3px solid #1a5cb8; }
.svc-name { font-size: 14px; font-weight: 700; color: #1a3a6b; margin: 0 0 3px 0; }
.svc-desc { font-size: 13px; color: #444; line-height: 1.45; margin: 3px 0 6px 0; }
.svc-specs {
    font-family: "Courier New", monospace; font-size: 11.5px; color: #555;
    background: #f8f8f8; padding: 6px 8px; border-radius: 2px;
    margin: 5px 0; line-height: 1.6; border: 1px solid #e8e8e8;
}
.svc-storage {
    font-size: 12px; color: #2a5e8a; background: #f0f6ff;
    border: 1px solid #c5d8f5; border-radius: 2px;
    padding: 4px 8px; margin: 5px 0; display: inline-block;
}
.svc-foot { font-size: 12px; color: #555; margin-top: 6px; }
.tag {
    display: inline-block; font-size: 10px; font-weight: 700;
    text-transform: uppercase; letter-spacing: .04em;
    padding: 1px 6px; border-radius: 2px; margin: 0 3px 4px 0;
}
.tag-lakeshore { background: #e8eef8; color: #1a3a6b; border: 1px solid #b8cce8; }
.tag-sce       { background: #fdf4e3; color: #7a4a00; border: 1px solid #f0d090; }
.tag-alcf      { background: #e6f5ee; color: #0a5030; border: 1px solid #a0d8b8; }
.tag-comp      { background: #fde8e8; color: #8b0000; border: 1px solid #f0b0b0; font-size:9px; }
.svc-link {
    display: inline-block; font-size: 12px; font-weight: 600; color: #1a5cb8;
    border: 1px solid #1a5cb8; padding: 3px 10px; border-radius: 2px;
    text-decoration: none; margin: 5px 5px 0 0;
}
.svc-link-ghost {
    display: inline-block; font-size: 12px; color: #666;
    border: 1px solid #aaa; padding: 3px 10px; border-radius: 2px;
    text-decoration: none; margin: 5px 0 0 0;
}
.sce-note {
    background: #fffbe6; border: 1px solid #f0d060;
    border-radius: 2px; padding: 5px 8px;
    font-size: 12px; color: #7a5000; margin: 5px 0;
}

/* ── Node selector section ────────────────────── */
.node-section-head {
    font-size: 13px; font-weight: 700; color: #333;
    border-bottom: 1px solid #ccc; padding-bottom: 4px; margin: 14px 0 8px 0;
}
.node-card {
    border: 1px solid #d0d0d0; border-radius: 3px;
    padding: 10px 12px; margin-bottom: 8px; background: #fff;
}
.node-card-rec { border-left: 3px solid #1a5cb8; background: #f5f8ff; }
.node-name  { font-size: 13px; font-weight: 700; color: #1a3a6b; }
.node-price { font-size: 12px; font-weight: 700; color: #c00; float: right; }
.node-spec  { font-family: monospace; font-size: 11px; color: #555; margin: 3px 0; }
.node-why   { font-size: 12px; color: #333; line-height: 1.45; margin-top: 5px; }
.node-badge {
    display: inline-block; font-size: 10px; font-weight: 700;
    background: #1a5cb8; color: #fff; padding: 1px 7px;
    border-radius: 2px; margin-bottom: 4px;
}
.node-list  { font-size: 12px; color: #444; margin: 4px 0 0 0;
              padding-left: 16px; line-height: 1.6; }
.node-avoid { font-size: 11px; color: #888; margin-top: 4px; font-style: italic; }

/* ── No-match box ─────────────────────────────── */
.no-match {
    background: #fffbe6; border: 1px solid #e8c840;
    border-radius: 3px; padding: 12px;
    font-size: 13px; color: #6b5000; line-height: 1.5;
}

/* ── Footer ───────────────────────────────────── */
.page-footer {
    border-top: 1px solid #ddd; margin-top: 24px; padding-top: 10px;
    font-size: 12px; color: #666; line-height: 1.8;
}
.page-footer a { color: #1a5cb8; }

/* ── Streamlit tweaks ─────────────────────────── */
div[data-testid="stVerticalBlock"] > div { gap: 0.2rem; }
label[data-baseweb="radio"] span { font-size: 13px !important; }
.stTabs [data-baseweb="tab"] { font-size: 13px !important; }
</style>
""", unsafe_allow_html=True)

# ── Page header ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
  <h1>Computational Resource Finder</h1>
  <p>Advanced Cyberinfrastructure for Education and Research (ACER) ·
     University of Illinois Chicago</p>
</div>
<div class="info-bar">
  This tool is intended to help you choose among ACER computational services.
  All services are vetted and supported by the University of Illinois at Chicago.
  For data <em>storage</em> recommendations, use the
  <a href="https://datastoragefinder.acer.uic.edu" target="_blank">Data Storage Finder ↗</a>
  · Questions? <a href="https://acer.uic.edu/services/consulting-outreach/office-hours/"
  target="_blank">ACER Office Hours ↗</a>
</div>
""", unsafe_allow_html=True)

# ── Data definitions ───────────────────────────────────────────────────────────

CPU_NODES = {
    "standard": dict(
        name="Standard Memory Node",
        price="$11,900 / node",
        spec="2× Intel Xeon Gold 6548Y+  ·  64 cores  ·  256 GB DDR5  ·  5-yr warranty",
        why="Best value for most HPC workloads — parallel batch jobs, genomics pipelines, MPI simulation, statistical computing. 256 GB covers the large majority of per-node memory needs.",
        ideal=["General-purpose batch HPC & MPI simulation",
               "Genomics pipelines (GATK, Nextflow, Snakemake)",
               "Statistical computing (R, Python, Julia)",
               "Machine learning preprocessing / CPU inference"],
        avoid="Avoid when individual jobs require > 256 GB RAM on a single node.",
    ),
    "midmem": dict(
        name="Mid-Memory Node",
        price="$16,000 / node",
        spec="2× Intel Xeon Gold 6548Y+  ·  64 cores  ·  1 TB DDR5  ·  5-yr warranty",
        why="When jobs must hold large datasets or graphs entirely in RAM. Common for de novo genome/metagenome assembly, large sparse matrix operations, in-memory analytics, large databases.",
        ideal=["De novo genome/metagenome assembly (SPAdes, Hifiasm, Flye)",
               "Large-scale graph analytics (single-node)",
               "In-memory analytics on datasets > 256 GB",
               "Large database servers with big buffer pools"],
        avoid="Avoid when jobs fit in 256 GB — standard nodes offer better cost-per-core.",
    ),
    "highmem": dict(
        name="High-Memory Node",
        price="$52,000 / node",
        spec="2× Intel Xeon Gold 6548Y+  ·  64 cores  ·  4 TB DDR5  ·  5-yr warranty",
        why="For workloads where 1 TB is not enough: very large reference genome databases, extreme-scale MD with explicit solvent, or data that cannot be distributed across nodes.",
        ideal=["Extremely large in-memory databases (> 1 TB buffer)",
               "Very large reference genome indices",
               "Large-scale Monte Carlo / structural biology",
               "Workloads that cannot tolerate MPI communication overhead"],
        avoid="Avoid when 1 TB nodes cover your use case — costs 3.25× more per node.",
    ),
}

GPU_NODES = {
    "l40s": dict(
        name="NVIDIA L40S GPU Node",
        price="$37,681 / node",
        spec="4× NVIDIA L40S  ·  48 GB GDDR6 / GPU  ·  64 cores  ·  512 GB DDR5",
        why="Best all-rounder at this price tier. Strong FP32 throughput makes it ideal for inference, rendering, and mixed-precision training. 512 GB system RAM supports multiple concurrent users and jobs.",
        ideal=["Model inference and serving (PyTorch, TensorRT, ONNX)",
               "Medium-scale deep learning training (single- or multi-GPU)",
               "3D scientific visualization and GPU rendering",
               "RAPIDS GPU analytics (cuDF, cuML)",
               "GPU-accelerated MD / molecular docking (AMBER, GROMACS)",
               "Shared lab node — multiple concurrent users"],
        avoid="Avoid for training very large models where 48 GB VRAM is insufficient and NVLink bandwidth is critical — use H100 instead.",
        mem_gb=48, fp16_tf=733, fp32_tf=91.6,
    ),
    "h100": dict(
        name="NVIDIA H100 GPU Node",
        price="$98,681 / node",
        spec="4× NVIDIA H100 SXM5  ·  94 GB HBM3 / GPU  ·  64 cores  ·  1 TB DDR5",
        why="H100 HBM3 delivers ~3.5× the memory bandwidth of L40S (3.35 TB/s vs 0.96 TB/s per GPU), critical for large model training. 94 GB VRAM supports models too large for L40S. FP8 Tensor Cores provide extreme throughput for transformer training.",
        ideal=["LLM and foundation model training",
               "Large-scale deep learning with FP8 / BF16 precision",
               "GPU-accelerated HPC simulation at scale (NAMD, LAMMPS, OpenFOAM)",
               "Quantum chemistry / DFT (VASP, NWChem, CP2K)",
               "Models or datasets requiring > 48 GB VRAM per GPU"],
        avoid="Avoid when workloads fit in 48 GB VRAM and don't need H100's memory bandwidth — L40S gives equivalent or better throughput at 38% of the cost.",
        mem_gb=94, fp16_tf=1979, fp32_tf=67.0,
    ),
}

RESOURCES = {
    "chicago_computes": dict(
        name="Lakeshore HPC — Chicago Computes",
        tag="Lakeshore", tag_cls="tag-lakeshore",
        compliance=[], gpu=True,
        roles=["pi"], sensitivities=["none"],
        workloads=["cpu_batch", "gpu"], sce_resource=False,
        desc="Free batch HPC allocation for UIC faculty PIs funded through the Forward Initiative. SLURM-scheduled AMD CPU and NVIDIA A100 GPU nodes on Lakeshore.",
        specs="20 AMD standard nodes — 128 cores, 256 GB RAM\n2 A100 GPU nodes — 4× NVIDIA A100 40 GB, 64 cores, 256 GB RAM\nScheduler: SLURM  ·  Interconnect: InfiniBand",
        storage="1 TB Research Data Rapids (Lustre/GPFS) included free. Additional storage purchasable.",
        storage_url="https://acer.uic.edu/services/research-data-storage/research-data-rapids/",
        cost="Free for UIC faculty PIs",
        who="UIC faculty PIs only",
        cta="Request Access", url="https://acer.uic.edu/get-started/request-access/",
        info_url="https://acer.uic.edu/services/hpc/lakeshore/",
        has_node_selector=False,
    ),
    "hpc_partnership": dict(
        name="Lakeshore HPC — HPC Partnership",
        tag="Lakeshore · Condo", tag_cls="tag-lakeshore",
        compliance=[], gpu=True,
        roles=["pi", "student_staff"], sensitivities=["none"],
        workloads=["cpu_batch", "gpu"], sce_resource=False,
        desc="Buy-in condo model giving 24/7 priority access to purchased Intel nodes on Lakeshore. Choose CPU or GPU nodes based on your research needs. 5-year warranty included.",
        specs="CPU: Standard (256 GB · $11,900), Mid-Memory (1 TB · $16,000), High-Memory (4 TB · $52,000)\nGPU: NVIDIA L40S (48 GB/GPU · $37,681), NVIDIA H100 (94 GB/GPU · $98,681)\nScheduler: SLURM  ·  Interconnect: InfiniBand",
        storage="1 TB Research Data Rapids (Lustre/GPFS) included. Additional storage purchasable.",
        storage_url="https://acer.uic.edu/services/research-data-storage/research-data-rapids/",
        cost="Per-node purchase — CPU from $11,900 · GPU from $37,681 · 5-yr warranty",
        who="Any PI, or student/staff with PI sponsorship",
        cta="Order Nodes", url="https://help.uillinois.edu/TDClient/37/uic/Requests/ServiceDet?ID=479",
        info_url="https://acer.uic.edu/get-started/resource-pricing/",
        has_node_selector=True,
    ),
    "sce_onprem": dict(
        name="Secure Computing Environment — On-Premises",
        tag="SCE · On-Premises", tag_cls="tag-sce",
        compliance=["HIPAA", "FERPA", "PIPA"], gpu=False,
        roles=["pi", "student_staff"], sensitivities=["ferpa", "hipaa"],
        workloads=["cpu_batch", "vm"], sce_resource=True,
        desc="On-premises secure VM service for HIPAA, FERPA, and PIPA-regulated research. Fixed monthly pricing. Supports web servers, databases, and computation. ACER staff assists with configuration.",
        specs="8 levels: 1–6 CPUs, 2–64 GB RAM\nOS: Rocky Linux · Windows Server 2022\nLocation: UIC campus · fulfills grants requiring local compute",
        storage="$0.10/GB/month including 90-day backups. 40 GB OS disk included in VM cost.",
        storage_url="https://acer.uic.edu/services/sce/on-prem/",
        cost="$41–$204/month (fixed, level-based) + $0.10/GB/month storage",
        who="Any UIC researcher",
        cta="Request SCE", url="https://help.uillinois.edu/TDClient/37/uic/Requests/TicketRequests/NewForm?ID=XyFNsqMR16k_&RequestorType=Service",
        info_url="https://acer.uic.edu/services/sce/on-prem/",
        has_node_selector=False,
    ),
    "sce_azure": dict(
        name="Secure Computing Environment — Azure",
        tag="SCE · Cloud", tag_cls="tag-sce",
        compliance=["NIST 800-171", "HIPAA", "FERPA", "PIPA"], gpu=True,
        roles=["pi", "student_staff"], sensitivities=["ferpa", "hipaa", "nist"],
        workloads=["gpu", "vm", "cpu_batch"], sce_resource=True,
        desc="Cloud-based secure VM on Microsoft Azure. Adds GPU options and NIST 800-171 compliance. Hourly billing — best when workload is intermittent or NIST 800-171 compliance is required.",
        specs="CPU VMs: 1–8 CPUs, 2–32 GB RAM — from $0.025/hr\nGPU VMs: NVIDIA T4, V100, 4× A100 — from $0.71/hr\nOS: Rocky Linux · Windows Server 2022",
        storage="From $9.60/month (128 GB) + backup ($14–$18/month). First 100 GB/month egress free.",
        storage_url="https://acer.uic.edu/services/sce/azure/",
        cost="Hourly, usage-dependent (Azure rates) + storage/backup",
        who="Any UIC researcher",
        cta="Request Azure SCE", url="https://help.uillinois.edu/TDClient/37/uic/Requests/TicketRequests/NewForm?ID=XyFNsqMR16k_&RequestorType=Service",
        info_url="https://acer.uic.edu/services/sce/azure/",
        has_node_selector=False,
    ),
    "alcf_lighthouse": dict(
        name="ALCF Lighthouse — Aurora, Polaris & AI Testbeds",
        tag="ALCF · National Lab", tag_cls="tag-alcf",
        compliance=[], gpu=True,
        roles=["pi", "student_staff"], sensitivities=["none"],
        workloads=["gpu", "ai_scale"], sce_resource=False,
        desc="UIC's shared allocation on Argonne Leadership Computing Facility systems (DOE). Designed for porting, testing, and scaling toward leadership-class computing. Not for production runs or sensitive/export-controlled data.",
        specs="Aurora: 10,624 nodes · 63,744 Intel GPUs · 2 Exaflop/s (#3 Top500)\nPolaris: 560 nodes · 2,240 NVIDIA A100s · 44 PFlop/s\nAI Testbeds: Cerebras CS-2 · SambaNova · Graphcore · Groq\nScheduler: PBS · Project: lighthouse-uic",
        storage="Home dir + Eagle & Grand filesystems (100 PB Lustre, 650 GB/s each). Project path: /lus/eagle/projects/lighthouse-uic/ · Do NOT store sensitive data.",
        storage_url="https://docs.alcf.anl.gov/",
        cost="Free via UIC's shared allocation — contact acer@uic.edu",
        who="Any UIC researcher · no sensitive or export-controlled data",
        cta="Contact ACER", url="mailto:acer@uic.edu",
        info_url="https://acer.uic.edu/services/argonne-leadership-computing-facility-lighthouse-initiative/",
        has_node_selector=False,
    ),
}

WORKLOAD_LABELS = {
    "cpu_batch": "Batch HPC — CPU-intensive scheduled jobs",
    "gpu":       "GPU-accelerated computing",
    "vm":        "Interactive / persistent virtual machine",
    "ai_scale":  "AI / ML at leadership scale",
}

def matches(res_key, res, role, sensitivity, workload):
    if role not in res["roles"]: return False
    if sensitivity not in res["sensitivities"]: return False
    if res["sce_resource"] and sensitivity != "none": return True
    return workload in res["workloads"]

# ── Read session state before layout (needed for left-panel conditional) ───────
_role = st.session_state.get("q_role", "pi")
_sens = st.session_state.get("q_sensitivity", "none")
_work = st.session_state.get("q_workload", "cpu_batch")
_show_nodes = matches("hpc_partnership", RESOURCES["hpc_partnership"], _role, _sens, _work)

# ── GPU/CPU recommendation logic (reads session state, no widgets) ─────────────
def gpu_recommendation():
    q1 = st.session_state.get("ns_gpu_q1", "Training deep learning / AI models")
    q2 = st.session_state.get("ns_gpu_q2", "Less than 48 GB")
    q3 = st.session_state.get("ns_gpu_q3", "Shared")
    needs_h100 = ("48–94 GB" in q2 or "More than 94 GB" in q2 or
                  ("Training" in q1 and "Dedicated" in q3))
    return "h100" if needs_h100 else "l40s"

def cpu_recommendation():
    cq1 = st.session_state.get("ns_cpu_q1", "General batch HPC")
    cq2 = st.session_state.get("ns_cpu_q2", "Less than 256 GB")
    cq3 = st.session_state.get("ns_cpu_q3", "Many concurrent")
    if "More than 1 TB" in cq2: return "highmem"
    if ("256 GB to 1 TB" in cq2 or "assembly" in cq1.lower()
            or "large in-memory" in cq1.lower() or "Fewer" in cq3):
        return "midmem"
    return "standard"

# ── Layout ─────────────────────────────────────────────────────────────────────
left_col, spacer, right_col = st.columns([1.15, 0.05, 2.0])

# ══════════════════════ LEFT PANEL ════════════════════════════════════════════
with left_col:
    st.markdown('<div class="panel-head">Describe your research needs</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-subhead">Identify resources by answering the questions below.</div>', unsafe_allow_html=True)

    st.markdown("**1. Who are you?**")
    role = st.radio("role",
        ["pi", "student_staff"],
        format_func=lambda x: "Faculty PI (Principal Investigator)"
                               if x == "pi" else "Student / Staff (with PI sponsorship)",
        label_visibility="collapsed", key="q_role",
    )
    st.markdown("**2. Does your research data have regulatory requirements?**")
    sensitivity = st.radio("sens",
        ["none", "ferpa", "hipaa", "nist"],
        format_func=lambda x: {
            "none":  "No restrictions (public / unrestricted)",
            "ferpa": "FERPA — student education records",
            "hipaa": "HIPAA — protected health information",
            "nist":  "NIST 800-171 — export controlled / CUI",
        }[x],
        label_visibility="collapsed", key="q_sensitivity",
    )
    st.markdown("**3. What type of computational work?**")
    workload = st.radio("work",
        ["cpu_batch", "gpu", "vm", "ai_scale"],
        format_func=lambda x: WORKLOAD_LABELS[x],
        label_visibility="collapsed", key="q_workload",
    )

    # ── Node purchase questions (appear only when HPC Partnership matches) ─────
    if _show_nodes:
        st.markdown('<div class="node-section-head">4. Which node type to purchase? (HPC Partnership)</div>', unsafe_allow_html=True)
        st.caption("Answers drive the recommendation shown on the right.")

        tab_gpu, tab_cpu = st.tabs(["GPU nodes", "CPU nodes"])

        with tab_gpu:
            st.radio("Primary use case:",
                ["Training deep learning / AI models",
                 "Running inference / serving models",
                 "Scientific simulation (MD, CFD, DFT, quantum chem)",
                 "Data analytics, visualization, or rendering"],
                key="ns_gpu_q1",
            )
            st.radio("GPU memory needed per job (per GPU):",
                ["Less than 48 GB  (most workloads)",
                 "48–94 GB  (large models or big datasets)",
                 "More than 94 GB  (need multi-GPU tensor parallelism)"],
                key="ns_gpu_q2",
            )
            st.radio("How will the node be used?",
                ["Shared — multiple users / concurrent jobs",
                 "Dedicated — one project or tightly coupled training"],
                key="ns_gpu_q3",
            )

        with tab_cpu:
            st.radio("What best describes your workload?",
                ["General batch HPC — MPI jobs, simulations, pipelines",
                 "Genomics / bioinformatics — assembly, variant calling, RNA-seq",
                 "Data analytics — large in-memory datasets or databases",
                 "Other / not sure"],
                key="ns_cpu_q1",
            )
            st.radio("RAM needed per job on a single node:",
                ["Less than 256 GB",
                 "256 GB to 1 TB",
                 "More than 1 TB",
                 "Not sure yet"],
                key="ns_cpu_q2",
            )
            st.radio("Usage pattern:",
                ["Many concurrent medium-sized jobs",
                 "Fewer large-memory jobs"],
                key="ns_cpu_q3",
            )

    st.markdown("")
    if st.button("Clear answers", use_container_width=True):
        for k in ["q_role", "q_sensitivity", "q_workload", "sel",
                  "ns_gpu_q1", "ns_gpu_q2", "ns_gpu_q3",
                  "ns_cpu_q1", "ns_cpu_q2", "ns_cpu_q3"]:
            st.session_state.pop(k, None)
        st.rerun()

# ── Recompute matching after widgets render ────────────────────────────────────
matching = {k: v for k, v in RESOURCES.items()
            if matches(k, v, role, sensitivity, workload)}

# ══════════════════════ RIGHT PANEL ═══════════════════════════════════════════
with right_col:
    st.markdown('<div class="panel-head">Services</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-subhead">Select services you would like to compare.</div>', unsafe_allow_html=True)

    if not matching:
        st.markdown("""
        <div class="no-match">
          <strong>No services match all selected criteria.</strong><br>
          Contact <a href="mailto:acer@uic.edu">acer@uic.edu</a> or attend
          <a href="https://acer.uic.edu/services/consulting-outreach/office-hours/"
             target="_blank">ACER Office Hours ↗</a>
        </div>""", unsafe_allow_html=True)

    else:
        if "sel" not in st.session_state:
            st.session_state.sel = []

        ba, bb = st.columns(2)
        with ba:
            if st.button("Select All", use_container_width=True):
                st.session_state.sel = list(matching.keys()); st.rerun()
        with bb:
            if st.button("Clear Selections", use_container_width=True):
                st.session_state.sel = []; st.rerun()

        for res_key, res in matching.items():
            is_sel = res_key in st.session_state.sel
            card_cls = "svc-card svc-card-sel" if is_sel else "svc-card"
            comp_tags = "".join(f'<span class="tag tag-comp">{c}</span>' for c in res["compliance"])
            specs_html = res["specs"].replace("\n", "<br>")
            gpu_txt = "✅ GPU available" if res["gpu"] else "❌ No GPU"
            sce_note = (
                '<div class="sce-note">⚠️ SCE is required for regulated data and '
                'supports any workload type (batch jobs, interactive analysis, '
                'databases, web servers).</div>'
                if res["sce_resource"] and sensitivity != "none" else ""
            )

            st.markdown(f"""
            <div class="{card_cls}">
              <div class="svc-name">{res['name']}</div>
              <span class="tag {res['tag_cls']}">{res['tag']}</span>{comp_tags}
              <div class="svc-desc">{res['desc']}</div>
              {sce_note}
              <div class="svc-specs">{specs_html}</div>
              <div class="svc-storage">
                🗄️ <strong>Storage:</strong> {res['storage']}
                &nbsp;<a href="{res['storage_url']}" target="_blank">details ↗</a>
              </div>
              <div class="svc-foot">
                <strong>Cost:</strong> {res['cost']} &nbsp;·&nbsp;
                {gpu_txt} &nbsp;·&nbsp;
                <strong>Eligible:</strong> {res['who']}
              </div>
              <a href="{res['url']}" target="_blank" class="svc-link">{res['cta']} →</a>
              <a href="{res['info_url']}" target="_blank" class="svc-link-ghost">More info ↗</a>
            </div>
            """, unsafe_allow_html=True)

            # ── Node recommendation (right panel, reads left-panel answers) ────
            if res_key == "hpc_partnership" and res["has_node_selector"] and _show_nodes:
                grec = gpu_recommendation()
                crec = cpu_recommendation()
                gn = GPU_NODES[grec]
                cn = CPU_NODES[crec]

                st.markdown('<div class="node-section-head">💡 Node purchase recommendation</div>', unsafe_allow_html=True)
                nc1, nc2 = st.columns(2)
                with nc1:
                    st.markdown(f"""
                    <div class="node-card node-card-rec">
                      <span class="node-badge">GPU — recommended</span>
                      <span class="node-price">{gn['price']}</span>
                      <div class="node-name">{gn['name']}</div>
                      <div class="node-spec">{gn['spec']}</div>
                      <div class="node-why">{gn['why']}</div>
                      <div class="node-avoid">↳ {gn['avoid']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    with st.expander("All GPU node options"):
                        for k, n in GPU_NODES.items():
                            lbl = "✔ Recommended" if k == grec else "Alternative"
                            st.markdown(f"""
                            <div class="node-card {'node-card-rec' if k==grec else ''}">
                              <strong>{n['name']}</strong> &nbsp; <em style="color:#c00">{n['price']}</em><br>
                              <span style="font-family:monospace;font-size:11px">{n['spec']}</span><br>
                              <em style="font-size:11px;color:#555">{n['why']}</em>
                              <ul class="node-list">{''.join(f'<li>{w}</li>' for w in n['ideal'])}</ul>
                            </div>""", unsafe_allow_html=True)

                with nc2:
                    st.markdown(f"""
                    <div class="node-card node-card-rec">
                      <span class="node-badge">CPU — recommended</span>
                      <span class="node-price">{cn['price']}</span>
                      <div class="node-name">{cn['name']}</div>
                      <div class="node-spec">{cn['spec']}</div>
                      <div class="node-why">{cn['why']}</div>
                      <div class="node-avoid">↳ {cn['avoid']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    with st.expander("All CPU node options"):
                        for k, n in CPU_NODES.items():
                            st.markdown(f"""
                            <div class="node-card {'node-card-rec' if k==crec else ''}">
                              <strong>{n['name']}</strong> &nbsp; <em style="color:#c00">{n['price']}</em><br>
                              <span style="font-family:monospace;font-size:11px">{n['spec']}</span><br>
                              <em style="font-size:11px;color:#555">{n['why']}</em>
                              <ul class="node-list">{''.join(f'<li>{w}</li>' for w in n['ideal'])}</ul>
                            </div>""", unsafe_allow_html=True)

                with st.expander("GPU vs CPU spec comparison table"):
                    gpu_df = pd.DataFrame({
                        "": ["VRAM / GPU", "Memory BW / GPU", "Peak FP16 (4 GPUs)", "Peak FP32 (4 GPUs)", "System RAM", "Price / node"],
                        "L40S": ["48 GB GDDR6", "0.96 TB/s", "733 TF", "91.6 TF", "512 GB", "$37,681"],
                        "H100": ["94 GB HBM3", "3.35 TB/s", "1,979 TF", "67.0 TF", "1 TB", "$98,681"],
                    }).set_index("")
                    st.dataframe(gpu_df, use_container_width=True)
                    cpu_df = pd.DataFrame({
                        "": ["Cores", "RAM", "RAM/core", "Price / node"],
                        "Standard": ["64", "256 GB", "4 GB", "$11,900"],
                        "Mid-Memory": ["64", "1 TB", "16 GB", "$16,000"],
                        "High-Memory": ["64", "4 TB", "64 GB", "$52,000"],
                    }).set_index("")
                    st.dataframe(cpu_df, use_container_width=True)

            checked = st.checkbox(
                f"Add to comparison: **{res['name']}**",
                value=is_sel, key=f"chk_{res_key}",
            )
            if checked and res_key not in st.session_state.sel:
                st.session_state.sel.append(res_key); st.rerun()
            if not checked and res_key in st.session_state.sel:
                st.session_state.sel.remove(res_key); st.rerun()

        # ── Comparison table ───────────────────────────────────────────────────
        sel_keys = [k for k in st.session_state.sel if k in matching]
        st.caption(f"{len(sel_keys)} service{'s' if len(sel_keys) != 1 else ''} selected")

        if len(sel_keys) >= 2:
            st.markdown("---")
            st.markdown("**Compare the services which match your selected criteria.**")
            attrs = ["Cost", "Compliance", "GPU", "Storage included", "Eligible users"]
            def get_attr(res, a):
                if a == "Cost":             return res["cost"]
                if a == "Compliance":       return ", ".join(res["compliance"]) or "None required"
                if a == "GPU":              return "Yes" if res["gpu"] else "No"
                if a == "Storage included": return res["storage"]
                if a == "Eligible users":   return res["who"]
                return ""
            table = {"": attrs}
            for k in sel_keys:
                r = RESOURCES[k]
                col_name = r["name"].split("—")[-1].strip() if "—" in r["name"] else r["name"]
                table[col_name] = [get_attr(r, a) for a in attrs]
            st.dataframe(pd.DataFrame(table).set_index(""), use_container_width=True)
            lcs = st.columns(len(sel_keys))
            for i, k in enumerate(sel_keys):
                r = RESOURCES[k]
                short = r["name"].split("—")[-1].strip() if "—" in r["name"] else r["name"]
                with lcs[i]:
                    st.markdown(
                        f'<a href="{r["url"]}" target="_blank" class="svc-link">{r["cta"]} →</a>',
                        unsafe_allow_html=True,
                    )
        elif len(sel_keys) == 1:
            st.info("Select at least two services to compare.", icon="ℹ️")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-footer">
  <strong>Advanced Cyberinfrastructure for Education and Research (ACER)</strong>
  · University of Illinois Chicago<br>
  728 W. Roosevelt Rd., 215A RRB, Chicago IL 60607
  · (312) 413-4149
  · <a href="mailto:acer@uic.edu">acer@uic.edu</a>
  · <a href="https://acer.uic.edu">acer.uic.edu</a><br>
  Data storage finder: <a href="https://datastoragefinder.acer.uic.edu">datastoragefinder.acer.uic.edu</a>
  &nbsp;·&nbsp;
  Consulting: <a href="https://acer.uic.edu/services/consulting-outreach/office-hours/">ACER Office Hours</a>
  &nbsp;·&nbsp;
  All services: <a href="https://acer.uic.edu/services/">acer.uic.edu/services</a>
</div>
""", unsafe_allow_html=True)
