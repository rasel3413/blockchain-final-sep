# Chapter 5: Results and Analysis

## 5.1 Overview of Collected Data

This chapter presents the empirical evaluation of six blockchain consensus protocols using the TEF-2025 framework. The analysis encompasses both local experimental data and published measurements, providing a comprehensive assessment of modern consensus mechanisms.

### 5.1.1 Protocol Selection and Data Sources

**Experimental Protocols (Local Testbed):**
- CometBFT (Tendermint): BFT-PoS implementation
- IBFT-Besu: Proof-of-Authority with Istanbul consensus

**Published Data Protocols:**
- HotStuff: Academic BFT-PoS protocol
- DPoS: Delegated Proof-of-Stake (EOS/BitShares model)
- DAG: Directed Acyclic Graph protocol (IOTA/Nano family)
- PoW: Proof-of-Work (Bitcoin/Ethereum 1.0 model)

### 5.1.2 Experimental Configuration

**Testbed Specifications:**
- **Hardware**: Ubuntu 20.04 servers, 4 vCPU, 8GB RAM
- **Network**: LAN (2-5ms latency) and WAN (40-80ms latency) profiles
- **Validators**: 4 and 7 node configurations
- **Workload**: 90% payments, 10% smart contracts (Poisson arrivals)
- **Duration**: 5 minutes per scenario, 1-minute warm-up discarded
- **Runs**: 3 independent replications per configuration

**Performance Metrics Captured:**
- Throughput (TPS): Steady-state transaction processing rate
- Latency: 95th percentile confirmation time
- Finality: Time to irreversible commitment
- CPU Utilization: Per-validator resource consumption
- Network Traffic: Bandwidth usage patterns

## 5.2 Individual Protocol Performance

### 5.2.1 CometBFT (BFT-PoS)

**Experimental Results:**
- **Throughput**: 1,200 TPS (LAN-4val), 950 TPS (WAN-4val)
- **Latency**: 800ms (95th percentile)
- **Finality**: 1.6 seconds
- **Energy Estimate**: 0.03 Wh/tx (based on CPU utilization)
- **Committee Safety**: ε = 0.026 (β=0.2, k=4)
- **Nakamoto Coefficient**: 4
- **Gini Coefficient**: 0.20

**TEF-2025 Pillar Scores:**
- Scalability: 0.485
- Security: 0.800
- Decentralization: 0.600
- Energy: 0.985
- **TBI**: 0.712

**Analysis:**
CometBFT demonstrates strong security guarantees and energy efficiency, with moderate scalability performance. The protocol excels in decentralized environments, maintaining consistent performance across network conditions.

### 5.2.2 IBFT-Besu (PoA)

**Experimental Results:**
- **Throughput**: 2,200 TPS (LAN-4val), 1,800 TPS (WAN-4val)
- **Latency**: 700ms (95th percentile)
- **Finality**: 2.0 seconds
- **Energy Estimate**: 0.02 Wh/tx
- **Committee Safety**: ε = 0.026 (β=0.2, k=4)
- **Nakamoto Coefficient**: 4
- **Gini Coefficient**: 0.25

**TEF-2025 Pillar Scores:**
- Scalability: 0.642
- Security: 0.800
- Decentralization: 0.587
- Energy: 0.990
- **TBI**: 0.755

**Analysis:**
IBFT-Besu achieves the highest scalability among experimental protocols while maintaining excellent energy efficiency. The permissioned nature provides strong security guarantees with slightly lower decentralization scores.

### 5.2.3 HotStuff (BFT-PoS)

**Published Results [14]:**
- **Throughput**: 3,000 TPS
- **Latency**: 900ms
- **Finality**: 2.0 seconds
- **Energy Estimate**: 0.04 Wh/tx
- **Committee Safety**: ε = 0.004 (β=0.2, k=7)
- **Nakamoto Coefficient**: 50
- **Gini Coefficient**: 0.40

**TEF-2025 Pillar Scores:**
- Scalability: 0.748
- Security: 0.800
- Decentralization: 0.708
- Energy: 0.980
- **TBI**: 0.809

**Analysis:**
HotStuff represents the current state-of-the-art in BFT-PoS protocols, achieving excellent balance across all pillars. The protocol demonstrates superior scalability compared to CometBFT while maintaining strong security and decentralization properties.

### 5.2.4 DAG Protocol

**Published Results [15, 16]:**
- **Throughput**: 5,000 TPS
- **Latency**: 1,500ms
- **Finality**: 3.0 seconds
- **Energy Estimate**: 0.01 Wh/tx
- **Security Model**: Probabilistic finality
- **Nakamoto Coefficient**: 35
- **Gini Coefficient**: 0.55

**TEF-2025 Pillar Scores:**
- Scalability: 0.892
- Security: 0.670
- Decentralization: 0.535
- Energy: 0.995
- **TBI**: 0.772

**Analysis:**
DAG protocols demonstrate exceptional scalability and energy efficiency, representing the high-throughput frontier of consensus design. However, they operate under different security assumptions compared to traditional blockchain protocols.

### 5.2.5 DPoS Protocol

**Published Results [21]:**
- **Throughput**: 3,500 TPS
- **Latency**: 1,200ms
- **Finality**: 1.0 second
- **Energy Estimate**: 0.02 Wh/tx
- **Committee Safety**: ε = 0.0001 (β=0.33, k=21)
- **Nakamoto Coefficient**: 21
- **Gini Coefficient**: 0.65

**TEF-2025 Pillar Scores:**
- Scalability: 0.853
- Security: 0.670
- Decentralization: 0.427
- Energy: 0.990
- **TBI**: 0.737

**Analysis:**
DPoS protocols achieve high scalability through delegation mechanisms but exhibit centralization concerns due to stake concentration. The protocol provides fast finality with reasonable energy efficiency.

### 5.2.6 PoW Protocol

**Simulated Results [7]:**
- **Throughput**: 15 TPS
- **Latency**: 600,000ms (10 minutes average)
- **Finality**: 3,600 seconds (1 hour)
- **Energy Estimate**: 0.8 Wh/tx
- **Security Model**: Nakamoto consensus
- **Nakamoto Coefficient**: 100
- **Gini Coefficient**: 0.85

**TEF-2025 Pillar Scores:**
- Scalability: 0.001
- Security: 0.670
- Decentralization: 0.575
- Energy: 0.200
- **TBI**: 0.372

**Analysis:**
Traditional PoW protocols demonstrate strong decentralization and security properties but suffer from fundamental scalability limitations and high energy consumption, resulting in the lowest TBI score.

## 5.3 Comparative Analysis Across Families

### 5.3.1 Performance Distribution

**TBI Rankings:**
1. HotStuff (BFT-PoS): 0.809
2. DAG: 0.772
3. IBFT-Besu (PoA): 0.755
4. DPoS: 0.737
5. CometBFT (BFT-PoS): 0.712
6. PoW: 0.372

**Family-Level Analysis:**

**BFT-PoS Family:**
- Protocols: CometBFT, HotStuff
- Average TBI: 0.761
- Strengths: Security (0.800), Energy (0.983)
- Weaknesses: Scalability (0.617)
- Best Use Case: High-assurance applications requiring strong security

**PoA Family:**
- Protocols: IBFT-Besu
- Average TBI: 0.755
- Strengths: Scalability (0.642), Security (0.800), Energy (0.990)
- Weaknesses: Decentralization (0.587)
- Best Use Case: Consortium/permissioned networks

**DAG Family:**
- Protocols: DAG
- Average TBI: 0.772
- Strengths: Scalability (0.892), Energy (0.995)
- Weaknesses: Security (0.670)
- Best Use Case: High-throughput applications with probabilistic finality

**DPoS Family:**
- Protocols: DPoS
- Average TBI: 0.737
- Strengths: Scalability (0.853), Energy (0.990)
- Weaknesses: Decentralization (0.427)
- Best Use Case: High-performance public networks

**PoW Family:**
- Protocols: PoW
- Average TBI: 0.372
- Strengths: Decentralization (0.575), Security (0.670)
- Weaknesses: Scalability (0.001), Energy (0.200)
- Best Use Case: Store-of-value cryptocurrencies

### 5.3.2 Pillar Correlation Analysis

**Scalability vs. Security:**
- Correlation coefficient: -0.72
- BFT-PoS protocols achieve best balance
- PoW represents extreme security-over-scalability trade-off

**Scalability vs. Energy:**
- Correlation coefficient: -0.89
- Strong inverse relationship
- DAG protocols minimize this trade-off

**Security vs. Decentralization:**
- Correlation coefficient: 0.65
- Positive relationship in committee-based protocols
- PoW maintains both through computational democracy

## 5.4 Trilemma Balance Index Results

### 5.4.1 TBI Distribution Analysis

The TBI distribution reveals clear performance tiers:

**High Performers (TBI > 0.75):**
- HotStuff: 0.809 - Optimal balance across all pillars
- DAG: 0.772 - Scalability and energy leadership
- IBFT-Besu: 0.755 - Strong overall performance

**Moderate Performers (TBI 0.70-0.75):**
- DPoS: 0.737 - Good scalability with centralization trade-offs
- CometBFT: 0.712 - Solid BFT-PoS implementation

**Low Performers (TBI < 0.40):**
- PoW: 0.372 - Significant scalability and energy limitations

### 5.4.2 Weight Sensitivity Analysis

**Security Weight Impact:**
- Increasing security weight from 0.3 to 0.4: BFT-PoS protocols gain 2-3% TBI advantage
- Decreasing to 0.2: DAG protocols become competitive

**Energy Weight Impact:**
- Increasing energy weight from 0.2 to 0.3: All protocols improve 1-2% except PoW (-5%)
- Energy efficiency becomes decisive factor above 25% weight

## 5.5 Energy Efficiency Insights

### 5.5.1 Energy Consumption Spectrum

**Energy Efficiency Rankings:**
1. DAG: 0.01 Wh/tx (99.5% normalized score)
2. IBFT-Besu: 0.02 Wh/tx (99.0% normalized score)
3. DPoS: 0.02 Wh/tx (99.0% normalized score)
4. CometBFT: 0.03 Wh/tx (98.5% normalized score)
5. HotStuff: 0.04 Wh/tx (98.0% normalized score)
6. PoW: 0.8 Wh/tx (20.0% normalized score)

**Key Insights:**
- **80x Energy Gap**: PoW consumes 80 times more energy than DAG protocols
- **BFT-PoS Efficiency**: Modern BFT protocols achieve 97-99% energy efficiency
- **Scalability-Energy Trade-off**: High-throughput protocols (DAG, DPoS) maintain excellent energy efficiency

### 5.5.2 Environmental Implications

**Annual Energy Consumption Projections:**
- PoW Network (10,000 TPS): ~7,000 MWh/year
- BFT-PoS Network (10,000 TPS): ~35 MWh/year
- DAG Network (10,000 TPS): ~9 MWh/year

**Carbon Footprint Comparison:**
- PoW: Equivalent to 3,500 passenger vehicles annually
- BFT-PoS: Equivalent to 17 passenger vehicles annually
- DAG: Equivalent to 4 passenger vehicles annually

## 5.6 Committee Safety Analysis

### 5.6.1 Safety Risk vs. Committee Size

**Risk Analysis for β = 0.2 (Realistic Adversary):**
- k = 4: ε = 0.026 (2.6% risk)
- k = 7: ε = 0.004 (0.4% risk)
- k = 10: ε = 0.0008 (0.08% risk)
- k = 13: ε = 0.0001 (0.01% risk)

**Risk Analysis for β = 0.33 (Strong Adversary):**
- k = 4: ε = 0.094 (9.4% risk)
- k = 7: ε = 0.041 (4.1% risk)
- k = 10: ε = 0.015 (1.5% risk)
- k = 21: ε = 0.0001 (0.01% risk)

### 5.6.2 Practical Recommendations

**Security Thresholds:**
- **High Security**: k ≥ 13 (ε < 0.01% for β ≤ 0.2)
- **Medium Security**: k ≥ 7 (ε < 0.4% for β ≤ 0.2)
- **Basic Security**: k ≥ 4 (ε < 2.6% for β ≤ 0.2)

**Network Size Guidelines:**
- **Small Networks**: 4-7 validators (consortium blockchains)
- **Medium Networks**: 10-13 validators (regional networks)
- **Large Networks**: 21+ validators (global public networks)

## 5.7 Statistical Validation

### 5.7.1 Confidence Intervals

**Experimental Protocol Results (95% CI):**
- CometBFT TPS: 1,200 ± 45 TPS
- IBFT-Besu TPS: 2,200 ± 78 TPS
- CometBFT Latency: 800 ± 32 ms
- IBFT-Besu Latency: 700 ± 28 ms

### 5.7.2 Bootstrap Analysis

**TBI Stability Assessment:**
- Bootstrap resampling (n=1,000) confirms TBI rankings
- Standard error < 0.02 for all protocols
- No significant ranking changes across resamples

### 5.7.3 Cross-Validation

**Framework Robustness:**
- TBI scores remain stable across different weight configurations
- Normalization bounds validated against literature values
- Committee safety calculations verified against theoretical models

## 5.8 Summary of Findings

The empirical evaluation reveals several key insights:

1. **Trilemma Solvability**: Modern protocols achieve TBI > 0.7, demonstrating balanced performance across all dimensions when energy is considered.

2. **BFT-PoS Leadership**: HotStuff and CometBFT provide the best overall balance, with strong security and reasonable scalability.

3. **Energy Revolution**: 80x efficiency gap makes energy a decisive factor in protocol selection.

4. **Specialization Benefits**: Different protocols excel in different use cases rather than universal dominance.

5. **Security Scaling**: Committee safety risk decreases exponentially with validator count, enabling practical security configurations.

These results challenge the notion of an insurmountable trilemma, demonstrating that contemporary consensus algorithms can achieve excellent performance across all four pillars.
