# Methods Section for Thesis

## Experimental Design and Evaluation Framework

We developed the Trilemma Evaluation Framework 2025 (TEF-2025) to provide a systematic, quantitative assessment of blockchain consensus algorithms across four critical performance dimensions. The framework addresses the classic blockchain trilemma (scalability, security, decentralization) while incorporating energy efficiency as a fourth pillar essential for sustainable blockchain systems.

### Testbed Configuration

Local experiments utilized small-scale Byzantine Fault Tolerant networks with 4-7 validator nodes deployed on identical virtual machines (Ubuntu 20.04, 4 vCPU, 8GB RAM) connected via simulated network conditions. We evaluated two network profiles: LAN (2-5ms latency, 0% loss) and WAN (40-80ms latency, 0-1% loss). Workloads consisted of 90% simple payment transactions and 10% smart contract interactions following Poisson arrival patterns at 80% of theoretical capacity to avoid queue instability (λ ≤ 0.8μ).

Each experimental scenario executed for 5 minutes with a 1-minute warm-up period discarded to ensure steady-state measurements. We conducted three independent runs per configuration and computed 95% confidence intervals using bootstrap resampling (n=1000). Published measurements for protocols requiring extensive infrastructure (PoW, large-scale DPoS, DAG) were normalized from peer-reviewed studies using consistent units and methodological standards.

### Metrics and Normalization

The TEF-2025 framework captures consensus performance through standardized metrics: throughput (transactions per second), latency (95th percentile response time in milliseconds), finality time (seconds to irreversible commitment), energy consumption (watt-hours per transaction), committee size, adversary tolerance, Nakamoto coefficient, and Gini coefficient for stake/power distribution. All metrics undergo min-max normalization to [0,1] intervals using empirically-derived domain thresholds (e.g., TPS: 10-10,000; latency: 50-5,000ms; energy: 0.001-1.0 Wh/tx).

### Mathematical Framework

Committee safety for Byzantine fault tolerant protocols follows the binomial security model where the probability of adversarial control ε = P(X ≥ ⌈k/2⌉) with X ~ Binomial(k, β), representing the likelihood that Byzantine nodes comprise a majority of k committee members when the adversary controls fraction β of the network. The Trilemma Balance Index aggregates normalized pillar scores using weighted summation: TBI = 0.25×Scalability + 0.30×Security + 0.25×Decentralization + 0.20×Energy, with weights reflecting prioritization of security while balancing other dimensions.

### Limitations and Assumptions

Our evaluation operates under several constraints that limit generalizability. Local testbeds necessarily employ small validator sets that may not capture emergent behaviors in large-scale networks. Synthetic transaction workloads, while representative of common patterns, cannot encompass the full diversity of real-world blockchain usage. Energy consumption estimates derive from computational complexity models rather than direct power measurement, introducing potential inaccuracies. Published data integration assumes methodological consistency across studies, though experimental conditions and measurement techniques vary between research groups. Network simulation provides controlled conditions but may not reflect the complexity and heterogeneity of production Internet environments.
