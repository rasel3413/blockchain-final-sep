#!/usr/bin/env python3
"""
TEF-2025: Trilemma Evaluation Framework 2025
Main analysis script for blockchain consensus algorithm evaluation

This script:
1. Loads configuration and data
2. Computes committee safety (epsilon) where applicable
3. Normalizes all metrics to [0,1]
4. Calculates pillar scores and TBI
5. Generates plots: radar charts, scatter plots, safety curves
6. Exports results and report
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yaml
import argparse
import sys
from pathlib import Path
from scipy.stats import binom
import seaborn as sns

class TEF2025Analyzer:
    """TEF-2025 Analysis Engine"""
    
    def __init__(self, config_path):
        """Initialize with configuration."""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Set plotting style
        try:
            plt.style.use(self.config['plots']['style'])
        except:
            plt.style.use('default')
            print("⚠ Warning: seaborn style not available, using default")
        
        self.colors = self.config['plots']['colors']
        
    def compute_committee_safety(self, k, beta):
        """
        Compute committee safety risk epsilon.
        
        epsilon = P(X >= ceil(k/2)) where X ~ Binomial(k, beta)
        """
        if pd.isna(k) or pd.isna(beta):
            return np.nan
        
        k = int(k)
        threshold = int(np.ceil(k / 2))
        
        # P(X >= threshold) = 1 - P(X <= threshold-1)
        epsilon = 1 - binom.cdf(threshold - 1, k, beta)
        return epsilon
    
    def normalize_metric(self, values, metric_name):
        """Normalize metric to [0,1] based on config."""
        norm_config = self.config['normalization'][metric_name]
        min_val = norm_config['min']
        max_val = norm_config['max']
        inverse = norm_config.get('inverse', False)
        
        # Clip to bounds
        clipped = np.clip(values, min_val, max_val)
        
        # Normalize to [0,1]
        normalized = (clipped - min_val) / (max_val - min_val)
        
        # Invert if lower is better
        if inverse:
            normalized = 1 - normalized
            
        return normalized
    
    def compute_pillars(self, df):
        """Compute the four pillar scores."""
        pillars = pd.DataFrame(index=df.index)
        
        # Scalability: TPS + latency + finality
        tps_norm = self.normalize_metric(df['tps'], 'tps')
        latency_norm = self.normalize_metric(df['p95_latency_ms'], 'p95_latency_ms')
        finality_norm = self.normalize_metric(df['finality_s'], 'finality_s')
        pillars['scalability'] = (tps_norm + latency_norm + finality_norm) / 3
        
        # Security: committee safety (where available)
        if 'epsilon' in df.columns:
            security_norm = self.normalize_metric(df['epsilon'], 'committee_safety_epsilon')
        else:
            # Fallback: use inverse of adversary_beta as proxy
            security_norm = 1 - df['adversary_beta'].fillna(0.2)
        pillars['security'] = security_norm
        
        # Decentralization: Nakamoto + Gini
        nakamoto_norm = self.normalize_metric(df['nakamoto_coef'], 'nakamoto_coef')
        gini_norm = self.normalize_metric(df['gini'], 'gini')
        pillars['decentralization'] = (nakamoto_norm + gini_norm) / 2
        
        # Energy: efficiency
        energy_norm = self.normalize_metric(df['energy_wh_tx'], 'energy_wh_tx')
        pillars['energy'] = energy_norm
        
        return pillars
    
    def compute_tbi(self, pillars):
        """Compute Trilemma Balance Index."""
        weights = self.config['pillar_weights']
        
        tbi = (
            weights['scalability'] * pillars['scalability'] +
            weights['security'] * pillars['security'] + 
            weights['decentralization'] * pillars['decentralization'] +
            weights['energy'] * pillars['energy']
        )
        
        return tbi
    
    def find_pareto_front(self, df, x_col, y_col):
        """Find Pareto frontier points (higher is better for both)."""
        pareto_mask = np.zeros(len(df), dtype=bool)
        
        for i in range(len(df)):
            is_pareto = True
            for j in range(len(df)):
                if i != j:
                    # If another point dominates this one
                    if (df.iloc[j][x_col] >= df.iloc[i][x_col] and 
                        df.iloc[j][y_col] >= df.iloc[i][y_col] and
                        (df.iloc[j][x_col] > df.iloc[i][x_col] or 
                         df.iloc[j][y_col] > df.iloc[i][y_col])):
                        is_pareto = False
                        break
            pareto_mask[i] = is_pareto
        
        return pareto_mask
    
    def plot_radar_chart(self, pillars, protocols, output_dir):
        """Generate radar chart for each protocol."""
        categories = ['Scalability', 'Security', 'Decentralization', 'Energy']
        
        # Number of variables
        N = len(categories)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Complete the circle
        
        fig, axes = plt.subplots(2, 3, figsize=(15, 10), subplot_kw=dict(projection='polar'))
        axes = axes.flatten()
        
        for i, (idx, protocol) in enumerate(protocols.items()):
            if i >= len(axes):
                break
                
            ax = axes[i]
            
            # Values for this protocol
            values = [
                pillars.loc[idx, 'scalability'],
                pillars.loc[idx, 'security'], 
                pillars.loc[idx, 'decentralization'],
                pillars.loc[idx, 'energy']
            ]
            values += values[:1]  # Complete the circle
            
            # Plot
            ax.plot(angles, values, 'o-', linewidth=2, 
                   color=self.colors[i % len(self.colors)], alpha=0.8)
            ax.fill(angles, values, alpha=0.25, 
                   color=self.colors[i % len(self.colors)])
            
            # Customize
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories)
            ax.set_ylim(0, 1)
            ax.set_title(f'{protocol}', size=12, weight='bold', pad=20)
            ax.grid(True)
        
        # Hide unused subplots
        for i in range(len(protocols), len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(output_dir / 'radar_protocols.png', 
                   dpi=self.config['plots']['dpi'], bbox_inches='tight')
        plt.close()
        
        print("✓ Generated radar chart: radar_protocols.png")
    
    def plot_scatter_tps_finality(self, df, output_dir):
        """Generate TPS vs Finality scatter with Pareto front."""
        fig, ax = plt.subplots(figsize=self.config['plots']['figsize'])
        
        # Use inverse finality for "speed" (higher is better)
        finality_speed = 1 / df['finality_s']
        
        # Find Pareto front
        temp_df = pd.DataFrame({
            'tps': df['tps'],
            'finality_speed': finality_speed
        })
        pareto_mask = self.find_pareto_front(temp_df, 'tps', 'finality_speed')
        
        # Plot all points
        scatter = ax.scatter(df['tps'], finality_speed, 
                           c=df['tbi'], cmap='viridis', 
                           s=100, alpha=0.7, edgecolors='black')
        
        # Highlight Pareto front
        pareto_points = temp_df[pareto_mask].sort_values('tps')
        ax.plot(pareto_points['tps'], pareto_points['finality_speed'], 
               'r--', linewidth=2, alpha=0.8, label='Pareto Front')
        
        # Annotations
        for i, protocol in enumerate(df['protocol']):
            ax.annotate(protocol, 
                       (df.iloc[i]['tps'], finality_speed.iloc[i]),
                       xytext=(5, 5), textcoords='offset points',
                       fontsize=8, alpha=0.8)
        
        ax.set_xlabel('Throughput (TPS)')
        ax.set_ylabel('Finality Speed (1/seconds)')
        ax.set_title('Throughput vs Finality Speed\n(with Pareto Frontier)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Colorbar for TBI
        cbar = plt.colorbar(scatter)
        cbar.set_label('TBI Score')
        
        plt.tight_layout()
        plt.savefig(output_dir / 'scatter_tps_finality.png',
                   dpi=self.config['plots']['dpi'], bbox_inches='tight')
        plt.close()
        
        print("✓ Generated scatter plot: scatter_tps_finality.png")
    
    def plot_safety_curves(self, output_dir):
        """Generate committee safety curves."""
        betas = self.config['security']['adversary_betas']
        k_values = self.config['security']['committee_sizes']
        
        fig, ax = plt.subplots(figsize=self.config['plots']['figsize'])
        
        for i, beta in enumerate(betas):
            epsilons = [self.compute_committee_safety(k, beta) for k in k_values]
            ax.plot(k_values, epsilons, 'o-', 
                   color=self.colors[i], linewidth=2, 
                   label=f'β = {beta}', alpha=0.8)
        
        ax.set_xlabel('Committee Size (k)')
        ax.set_ylabel('Safety Risk ε = P(Byzantine Majority)')
        ax.set_title('Committee Safety Risk vs Size')
        ax.set_yscale('log')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Add practical thresholds
        ax.axhline(y=0.01, color='red', linestyle='--', alpha=0.5, label='1% Risk')
        ax.axhline(y=0.001, color='orange', linestyle='--', alpha=0.5, label='0.1% Risk')
        
        plt.tight_layout()
        plt.savefig(output_dir / 'safety_curves.png',
                   dpi=self.config['plots']['dpi'], bbox_inches='tight')
        plt.close()
        
        print("✓ Generated safety curves: safety_curves.png")
    
    def generate_report(self, df, output_dir):
        """Generate markdown report."""
        report_path = output_dir / 'report.md'
        
        # Sort by TBI
        top_protocols = df.nlargest(10, 'tbi')[['protocol', 'family', 'tbi', 'scalability', 'security', 'decentralization', 'energy']]
        
        report = f"""# TEF-2025 Analysis Report
*Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}*

## Executive Summary

This report presents the analysis of {len(df)} blockchain consensus protocols using the Trilemma Evaluation Framework 2025 (TEF-2025). The framework evaluates protocols across four pillars: Scalability, Security, Decentralization, and Energy efficiency.

## Top Performing Protocols (by TBI)

| Rank | Protocol | Family | TBI | Scalability | Security | Decentralization | Energy |
|------|----------|--------|-----|-------------|----------|------------------|--------|
"""
        
        for i, (_, row) in enumerate(top_protocols.iterrows(), 1):
            report += f"| {i} | {row['protocol']} | {row['family']} | {row['tbi']:.3f} | {row['scalability']:.3f} | {row['security']:.3f} | {row['decentralization']:.3f} | {row['energy']:.3f} |\n"
        
        report += f"""
## Key Findings

### Performance Distribution
- **Highest TBI**: {top_protocols.iloc[0]['protocol']} ({top_protocols.iloc[0]['tbi']:.3f})
- **Most Scalable**: {df.loc[df['scalability'].idxmax(), 'protocol']} ({df['scalability'].max():.3f})
- **Most Secure**: {df.loc[df['security'].idxmax(), 'protocol']} ({df['security'].max():.3f})
- **Most Decentralized**: {df.loc[df['decentralization'].idxmax(), 'protocol']} ({df['decentralization'].max():.3f})
- **Most Energy Efficient**: {df.loc[df['energy'].idxmax(), 'protocol']} ({df['energy'].max():.3f})

### Algorithm Family Analysis
"""
        
        # Add family analysis
        family_stats = df.groupby('family').agg({'tbi': ['mean', 'std', 'count']}).round(3)
        report += family_stats.to_string()
        
        report += """

## Visualizations

### Protocol Comparison (Radar Chart)
![Radar Chart](radar_protocols.png)

### Throughput vs Finality Trade-off
![TPS vs Finality](scatter_tps_finality.png)

### Committee Safety Analysis
![Safety Curves](safety_curves.png)

## Methodology Notes

- **Normalization**: All metrics normalized to [0,1] using configured thresholds
- **TBI Weights**: Scalability (25%), Security (30%), Decentralization (25%), Energy (20%)
- **Committee Safety**: Computed as ε = P(X ≥ ⌈k/2⌉) where X ~ Binomial(k, β)
- **Data Sources**: Mix of local experiments and published results

## Limitations

- Small-scale local testbeds (4-7 validators)
- Synthetic workloads may not reflect real-world usage
- Published data from different studies may have varying methodologies
- Energy estimates based on computational models, not direct measurement

---
*Analysis performed using TEF-2025 framework*
"""
        
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(f"✓ Generated report: {report_path}")
    
    def analyze(self, input_csv, output_dir):
        """Main analysis pipeline."""
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        print("🔬 Starting TEF-2025 Analysis")
        print("=" * 40)
        
        # Load data
        print(f"📂 Loading data from {input_csv}")
        df = pd.read_csv(input_csv)
        print(f"   Loaded {len(df)} protocols")
        
        # Compute committee safety where possible
        print("🛡️  Computing committee safety risks...")
        df['epsilon'] = df.apply(
            lambda row: self.compute_committee_safety(row['committee_k'], row['adversary_beta']),
            axis=1
        )
        
        # Compute pillar scores
        print("📊 Computing pillar scores...")
        pillars = self.compute_pillars(df)
        
        # Add pillars to dataframe
        for col in pillars.columns:
            df[col] = pillars[col]
        
        # Compute TBI
        print("🎯 Computing Trilemma Balance Index...")
        df['tbi'] = self.compute_tbi(pillars)
        
        # Save normalized results
        output_csv = output_dir / 'results_normalized.csv'
        df.to_csv(output_csv, index=False)
        print(f"💾 Saved normalized results: {output_csv}")
        
        # Generate plots
        print("📈 Generating visualizations...")
        protocols = dict(zip(df.index, df['protocol']))
        
        self.plot_radar_chart(pillars, protocols, output_dir)
        self.plot_scatter_tps_finality(df, output_dir)
        self.plot_safety_curves(output_dir)
        
        # Generate report
        print("📝 Generating report...")
        self.generate_report(df, output_dir)
        
        print("\n✅ Analysis complete!")
        print(f"📁 Results saved to: {output_dir}")
        
        return df

def main():
    """Main function with CLI."""
    parser = argparse.ArgumentParser(description='TEF-2025 Blockchain Analysis')
    parser.add_argument('--input', required=True, help='Input CSV file path')
    parser.add_argument('--outdir', required=True, help='Output directory')
    parser.add_argument('--config', default='config.yaml', help='Config file path')
    
    args = parser.parse_args()
    
    try:
        analyzer = TEF2025Analyzer(args.config)
        analyzer.analyze(args.input, args.outdir)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
