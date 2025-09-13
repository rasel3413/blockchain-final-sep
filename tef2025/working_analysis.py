#!/usr/bin/env python3
"""
TEF-2025: Analysis Script with Fixed Backend
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import yaml
import sys
from pathlib import Path

def main():
    print("🔬 Starting TEF-2025 Analysis")
    print("=" * 40)
    
    try:
        # Load config
        print("📁 Loading configuration...")
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        print("✓ Config loaded")
        
        # Load data
        print("📂 Loading data...")
        df = pd.read_csv('inputs/results.csv')
        print(f"✓ Loaded {len(df)} protocols")
        
        # Create outputs directory
        outputs_dir = Path('outputs')
        outputs_dir.mkdir(exist_ok=True)
        print("✓ Created outputs directory")
        
        # Simple normalization and TBI calculation
        print("🎯 Computing TBI scores...")
        
        # Normalize metrics to [0,1]
        def normalize_metric(values, min_val, max_val, inverse=False):
            clipped = np.clip(values, min_val, max_val)
            normalized = (clipped - min_val) / (max_val - min_val)
            if inverse:
                normalized = 1 - normalized
            return normalized
        
        # Normalize each metric
        tps_norm = normalize_metric(df['tps'], 10, 10000)
        latency_norm = normalize_metric(df['p95_latency_ms'], 50, 5000, inverse=True)
        finality_norm = normalize_metric(df['finality_s'], 0.5, 7200, inverse=True)
        energy_norm = normalize_metric(df['energy_wh_tx'], 0.001, 1.0, inverse=True)
        nakamoto_norm = normalize_metric(df['nakamoto_coef'], 1, 1000)
        gini_norm = normalize_metric(df['gini'], 0, 1, inverse=True)
        
        # Compute pillar scores
        df['scalability'] = (tps_norm + latency_norm + finality_norm) / 3
        df['security'] = 1 - df['adversary_beta'].fillna(0.2)  # Simple security proxy
        df['decentralization'] = (nakamoto_norm + gini_norm) / 2
        df['energy'] = energy_norm
        
        # Compute TBI with weights from config
        weights = config['pillar_weights']
        df['tbi'] = (
            weights['scalability'] * df['scalability'] +
            weights['security'] * df['security'] + 
            weights['decentralization'] * df['decentralization'] +
            weights['energy'] * df['energy']
        )
        
        print("✓ Computed TBI scores")
        
        # Save results
        output_csv = outputs_dir / 'results_normalized.csv'
        df.to_csv(output_csv, index=False)
        print(f"✓ Saved normalized results: {output_csv}")
        
        # Create plots
        print("📈 Generating plots...")
        
        # Scatter plot: TPS vs Finality
        plt.figure(figsize=(10, 8))
        scatter = plt.scatter(df['tps'], df['finality_s'], c=df['tbi'], 
                             cmap='viridis', s=100, alpha=0.7, edgecolors='black')
        
        for i, protocol in enumerate(df['protocol']):
            plt.annotate(protocol, (df.iloc[i]['tps'], df.iloc[i]['finality_s']),
                        xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        plt.xlabel('Throughput (TPS)')
        plt.ylabel('Finality Time (seconds)')
        plt.title('Blockchain Protocol Performance')
        plt.yscale('log')  # Log scale for finality since range is large
        plt.colorbar(scatter, label='TBI Score')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        plot_path = outputs_dir / 'scatter_tps_finality.png'
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Generated scatter plot: {plot_path}")
        
        # Create simple report
        print("📝 Generating report...")
        report_path = outputs_dir / 'report.md'
        
        # Sort by TBI
        top_protocols = df.nlargest(10, 'tbi')
        
        with open(report_path, 'w') as f:
            f.write("# TEF-2025 Analysis Report\n\n")
            f.write(f"*Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            f.write(f"Analyzed **{len(df)} blockchain protocols** using TEF-2025 framework.\n\n")
            
            f.write("## Top Performing Protocols (by TBI)\n\n")
            f.write("| Rank | Protocol | Family | TBI | Scalability | Security | Decentralization | Energy |\n")
            f.write("|------|----------|--------|-----|-------------|----------|------------------|--------|\n")
            
            for i, (_, row) in enumerate(top_protocols.iterrows(), 1):
                f.write(f"| {i} | {row['protocol']} | {row['family']} | {row['tbi']:.3f} | "
                       f"{row['scalability']:.3f} | {row['security']:.3f} | "
                       f"{row['decentralization']:.3f} | {row['energy']:.3f} |\n")
            
            f.write("\n## Key Findings\n\n")
            f.write(f"- **Highest TBI**: {top_protocols.iloc[0]['protocol']} ({top_protocols.iloc[0]['tbi']:.3f})\n")
            f.write(f"- **Most Scalable**: {df.loc[df['scalability'].idxmax(), 'protocol']} ({df['scalability'].max():.3f})\n")
            f.write(f"- **Most Secure**: {df.loc[df['security'].idxmax(), 'protocol']} ({df['security'].max():.3f})\n")
            f.write(f"- **Most Decentralized**: {df.loc[df['decentralization'].idxmax(), 'protocol']} ({df['decentralization'].max():.3f})\n")
            f.write(f"- **Most Energy Efficient**: {df.loc[df['energy'].idxmax(), 'protocol']} ({df['energy'].max():.3f})\n")
            
            f.write("\n## Visualization\n\n")
            f.write("![Performance Analysis](scatter_tps_finality.png)\n")
            
            f.write("\n## Methodology\n\n")
            f.write("- **Framework**: TEF-2025 (Trilemma Evaluation Framework 2025)\n")
            f.write("- **Metrics**: Normalized to [0,1] using configured thresholds\n")
            f.write("- **TBI Weights**: Scalability (25%), Security (30%), Decentralization (25%), Energy (20%)\n")
            f.write("- **Data Sources**: Mix of local experiments and published results\n")
        
        print(f"✓ Generated report: {report_path}")
        
        print("\n✅ TEF-2025 Analysis Complete!")
        print(f"📁 All results saved to: {outputs_dir.resolve()}")
        print(f"📊 View report: {report_path}")
        print(f"📈 View chart: {plot_path}")
        print(f"📄 View data: {output_csv}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
