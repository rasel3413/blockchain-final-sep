# TEF-2025: Trilemma Evaluation Framework 2025

A comprehensive evaluation framework for analyzing blockchain consensus algorithms across the classic trilemma dimensions plus energy efficiency.

## 🎯 Overview

TEF-2025 evaluates blockchain protocols across four pillars:
- **Scalability**: Throughput (TPS), latency (p95), finality time
- **Security**: Committee safety risk (Byzantine fault tolerance)
- **Decentralization**: Nakamoto coefficient, Gini inequality
- **Energy**: Energy consumption per transaction

The framework computes a **Trilemma Balance Index (TBI)** that aggregates normalized scores across all pillars.

## 📁 Project Structure

```
tef2025/
├── config.yaml              # TEF-2025 configuration (thresholds, weights)
├── inputs/
│   └── results.csv          # Raw measurement data
├── analysis/
│   ├── tef2025_analysis.py  # Main analysis script
│   └── validate_csv.py      # Data validation utility
├── outputs/                 # Generated results (created after run)
│   ├── results_normalized.csv
│   ├── radar_protocols.png
│   ├── scatter_tps_finality.png
│   ├── safety_curves.png
│   └── report.md
├── scripts/                 # Helper scripts
└── docs/
    └── README.md           # This file
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Navigate to project directory
cd /home/rasel/Documents/blockchain-final-sep/tef2025

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install numpy pandas matplotlib scipy pyyaml seaborn
```

### 2. Validate Your Data

```bash
# Check CSV structure and content
python analysis/validate_csv.py inputs/results.csv
```

### 3. Run Analysis

```bash
# Execute full TEF-2025 analysis
python analysis/tef2025_analysis.py --input inputs/results.csv --outdir outputs
```

### 4. View Results

Results will be saved in the `outputs/` directory:
- `results_normalized.csv` - Normalized data with TBI scores
- `*.png` - Visualization charts
- `report.md` - Comprehensive analysis report

## 📊 Data Schema

Your `inputs/results.csv` must contain these columns:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| protocol | string | Protocol name | "CometBFT" |
| family | string | Algorithm family | "BFT-PoS" |
| scenario | string | Test scenario | "LAN-4val" |
| tps | float | Transactions per second | 1200.0 |
| p95_latency_ms | float | 95th percentile latency (ms) | 800.0 |
| finality_s | float | Time to finality (seconds) | 1.6 |
| energy_wh_tx | float | Energy per transaction (Wh) | 0.03 |
| committee_k | int | Committee size (optional) | 4 |
| adversary_beta | float | Adversary ratio (optional) | 0.2 |
| nakamoto_coef | int | Nakamoto coefficient | 4 |
| gini | float | Gini coefficient [0,1] | 0.20 |
| notes | string | Additional notes | "Local run" |
| source | string | Data source | "Local" |

## 🔧 Configuration

Edit `config.yaml` to customize:

- **Normalization thresholds**: Min/max values for [0,1] mapping
- **Pillar weights**: Relative importance in TBI calculation
- **Security parameters**: Adversary ratios and committee sizes
- **Plot settings**: Colors, DPI, figure sizes

## 📈 Adding Your Data

### Local Experiments

1. Run your consensus protocol with 4-7 validators
2. Measure TPS, latency, finality under realistic load
3. Add new rows to `inputs/results.csv`
4. Re-run analysis

### Published Data

1. Extract metrics from research papers
2. Ensure units match schema (TPS, milliseconds, seconds, Wh)
3. Add appropriate source attribution
4. Re-run analysis

### Example Addition

```csv
MyProtocol,BFT-PoS,LAN-7val,2500,650,1.2,0.025,7,0.2,7,0.15,"My local test","Local-2025"
```

## 🧮 Mathematical Framework

### Committee Safety Risk

For protocols with committee-based consensus:

```
ε = P(X ≥ ⌈k/2⌉) where X ~ Binomial(k, β)
```

Where:
- `k` = committee size
- `β` = adversary ratio (fraction of Byzantine nodes)
- `ε` = probability of Byzantine majority

### Normalization

Each metric is normalized to [0,1]:

```
normalized = (value - min) / (max - min)
```

For "lower is better" metrics, we use: `1 - normalized`

### TBI Calculation

```
TBI = w₁×Scalability + w₂×Security + w₃×Decentralization + w₄×Energy
```

Default weights: 25%, 30%, 25%, 20% respectively.

## 🔍 Quality Checklist

Before submitting results:

- [ ] **Multiple runs**: 3+ independent measurements per scenario
- [ ] **Warm-up period**: Discard initial unstable measurements  
- [ ] **Confidence intervals**: Report 95% CIs for key metrics
- [ ] **Assumptions stated**: Document network conditions, load patterns
- [ ] **Sources cited**: Proper attribution for published data
- [ ] **Reproducible**: Include exact commands and configurations

## ⚠️ Limitations

1. **Scale**: Local testbeds limited to 4-7 validators
2. **Workload**: Synthetic transactions may not reflect real usage
3. **Heterogeneity**: Published data from different methodologies
4. **Energy**: Estimates based on computational models
5. **Network**: Simulated network conditions

## 🛠️ Troubleshooting

### Missing Dependencies

```bash
# If seaborn style fails
pip install seaborn

# If YAML parsing fails  
pip install pyyaml

# If plots don't generate
pip install matplotlib
```

### Data Validation Errors

- Check column names match schema exactly
- Ensure numeric columns contain valid numbers
- Verify Gini coefficients are in [0,1] range
- Check adversary_beta values are in [0,0.5] range

### Plot Generation Issues

- Ensure output directory exists and is writable
- Check matplotlib backend supports PNG output
- Verify sufficient data points for meaningful plots

## 📚 References

- **TEF-2025 Framework**: Original evaluation methodology
- **Committee Safety**: Based on Byzantine fault tolerance theory
- **Trilemma**: Buterin's blockchain trilemma concept
- **Normalization**: Min-max scaling with domain-specific thresholds

---

*For questions or issues, check the generated `outputs/report.md` for detailed results and diagnostics.*
