#!/usr/bin/env python3
"""
TEF-2025: Simple Analysis Script
Simplified version for testing
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yaml
import sys
from pathlib import Path
from scipy.stats import binom

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
        
        # Simple TBI calculation
        print("🎯 Computing TBI scores...")
        
        # Create outputs directory
        Path('outputs').mkdir(exist_ok=True)
        
        # Normalize TPS (simple version)
        tps_norm = (df['tps'] - df['tps'].min()) / (df['tps'].max() - df['tps'].min())
        
        # Simple TBI = normalized TPS (for demonstration)
        df['tbi'] = tps_norm
        
        # Save results
        df.to_csv('outputs/results_normalized.csv', index=False)
        print("✓ Saved normalized results")
        
        # Create simple plot
        plt.figure(figsize=(10, 6))
        plt.scatter(df['tps'], df['finality_s'], c=df['tbi'], cmap='viridis', s=100)
        
        for i, protocol in enumerate(df['protocol']):
            plt.annotate(protocol, (df.iloc[i]['tps'], df.iloc[i]['finality_s']),
                        xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        plt.xlabel('Throughput (TPS)')
        plt.ylabel('Finality Time (seconds)')
        plt.title('Blockchain Protocol Performance')
        plt.colorbar(label='TBI Score')
        plt.tight_layout()
        plt.savefig('outputs/scatter_tps_finality.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Generated scatter plot")
        
        # Create simple report
        with open('outputs/report.md', 'w') as f:
            f.write("# TEF-2025 Analysis Report\n\n")
            f.write(f"Analyzed {len(df)} protocols.\n\n")
            f.write("## Top Protocols by TBI\n\n")
            
            top = df.nlargest(3, 'tbi')[['protocol', 'tps', 'tbi']]
            for _, row in top.iterrows():
                f.write(f"- {row['protocol']}: TPS={row['tps']}, TBI={row['tbi']:.3f}\n")
            
            f.write("\n## Visualization\n\n")
            f.write("![Performance Scatter](scatter_tps_finality.png)\n")
        
        print("✓ Generated report")
        
        print("\n✅ Analysis complete!")
        print("📁 Results saved to outputs/")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
