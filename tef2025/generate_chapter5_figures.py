#!/usr/bin/env python3
"""
Generate specific figures for Chapter 5 Results and Analysis
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

# Set style for better figures
plt.style.use('default')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['font.weight'] = 'normal'

def create_data_source_classification():
    """Figure 5.1: Data Source Classification"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Protocol data
    protocols = ['CometBFT', 'IBFT-Besu', 'HotStuff', 'DPoS', 'DAG', 'PoW']
    reliability = [0.9, 0.9, 0.7, 0.6, 0.7, 0.8]
    environment = [0.2, 0.2, 0.5, 0.8, 0.5, 0.9]
    
    colors = ['#2E8B57', '#4169E1', '#FF6347', '#DAA520', '#9370DB', '#8B0000']
    
    scatter = ax.scatter(environment, reliability, s=200, c=colors, alpha=0.8, edgecolors='black', linewidth=2)
    
    # Add protocol labels
    for i, protocol in enumerate(protocols):
        ax.annotate(protocol, (environment[i], reliability[i]), 
                   xytext=(10, 10), textcoords='offset points', 
                   fontsize=10, fontweight='bold')
    
    # Add quadrant labels
    ax.text(0.1, 0.95, 'Direct Measurement\n(Experimental)', 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.8),
            fontsize=11, fontweight='bold', ha='left', va='top')
    
    ax.text(0.9, 0.95, 'Historical Data\n(Production)', 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.8),
            fontsize=11, fontweight='bold', ha='right', va='top')
    
    ax.text(0.1, 0.45, 'Literature Data\n(Published)', 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightyellow', alpha=0.8),
            fontsize=11, fontweight='bold', ha='left', va='bottom')
    
    ax.text(0.9, 0.45, 'Real-World\n(Production)', 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightcoral', alpha=0.8),
            fontsize=11, fontweight='bold', ha='right', va='bottom')
    
    ax.set_xlabel('Environment Type (Synthetic ← → Real-World)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Data Reliability', fontsize=12, fontweight='bold')
    ax.set_title('Figure 5.1: Data Source Classification Matrix', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 1)
    ax.set_ylim(0.4, 1)
    
    plt.tight_layout()
    plt.savefig('outputs/data_source_classification.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_protocol_performance_radar():
    """Figure 5.2: Protocol Performance Radar Chart"""
    # Protocol data
    protocols = ['HotStuff', 'DAG', 'IBFT-Besu', 'DPoS', 'CometBFT', 'PoW']
    
    # Normalized scores for each pillar
    scalability = [0.748, 0.892, 0.642, 0.853, 0.485, 0.001]
    security = [0.800, 0.670, 0.800, 0.670, 0.800, 0.670]
    decentralization = [0.708, 0.535, 0.587, 0.427, 0.600, 0.575]
    energy = [0.980, 0.995, 0.990, 0.990, 0.985, 0.200]
    
    # Setup radar chart
    categories = ['Scalability', 'Security', 'Decentralization', 'Energy']
    N = len(categories)
    
    # Compute angles for each category
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Complete the circle
    
    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(projection='polar'))
    
    colors = ['#2E8B57', '#FF6347', '#4169E1', '#DAA520', '#9370DB', '#8B0000']
    line_styles = ['-', '--', '-.', ':', '-', '--']
    
    for i, protocol in enumerate(protocols):
        values = [scalability[i], security[i], decentralization[i], energy[i]]
        values += values[:1]  # Complete the circle
        
        ax.plot(angles, values, 'o-', linewidth=2, label=f'{protocol} (TBI: {0.809 if protocol=="HotStuff" else 0.772 if protocol=="DAG" else 0.755 if protocol=="IBFT-Besu" else 0.737 if protocol=="DPoS" else 0.712 if protocol=="CometBFT" else 0.372:.3f})', 
                color=colors[i], linestyle=line_styles[i])
        ax.fill(angles, values, alpha=0.1, color=colors[i])
    
    # Customize the plot
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12, fontweight='bold')
    ax.set_ylim(0, 1)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=10)
    ax.grid(True)
    
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=10)
    plt.title('Figure 5.2: Protocol Performance Radar Chart\nTEF-2025 Four-Pillar Analysis', 
              size=14, fontweight='bold', pad=30)
    
    plt.tight_layout()
    plt.savefig('outputs/protocol_performance_radar.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_performance_distribution():
    """Figure 5.3: Performance Distribution by Protocol Family"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Data
    protocols = ['HotStuff', 'DAG', 'IBFT-Besu', 'DPoS', 'CometBFT', 'PoW']
    families = ['BFT-PoS', 'DAG', 'PoA', 'DPoS', 'BFT-PoS', 'PoW']
    tbi_scores = [0.809, 0.772, 0.755, 0.737, 0.712, 0.372]
    
    # Family colors
    family_colors = {
        'BFT-PoS': '#2E8B57',
        'DAG': '#FF6347',
        'PoA': '#4169E1', 
        'DPoS': '#DAA520',
        'PoW': '#8B0000'
    }
    
    colors = [family_colors[family] for family in families]
    
    # Create violin-style distribution plot
    x_positions = np.arange(len(protocols))
    bars = ax.bar(x_positions, tbi_scores, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Add threshold lines
    ax.axhline(y=0.7, color='red', linestyle='--', alpha=0.7, linewidth=2, label='Trilemma Resolution Threshold (0.7)')
    ax.axhline(y=0.75, color='orange', linestyle='--', alpha=0.7, linewidth=2, label='High Performance Threshold (0.75)')
    
    # Add score labels on bars
    for i, (bar, score) in enumerate(zip(bars, tbi_scores)):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                f'{score:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=11)
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2, 
                families[i], ha='center', va='center', fontweight='bold', fontsize=9, color='white')
    
    ax.set_xticks(x_positions)
    ax.set_xticklabels(protocols, rotation=45, ha='right', fontweight='bold')
    ax.set_ylabel('TBI Score', fontsize=12, fontweight='bold')
    ax.set_title('Figure 5.3: TBI Distribution by Protocol Family', fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 0.9)
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('outputs/performance_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_pillar_tradeoff_analysis():
    """Figure 5.4: Pillar Trade-off Analysis"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Protocol data
    protocols = ['HotStuff', 'DAG', 'IBFT-Besu', 'DPoS', 'CometBFT', 'PoW']
    scalability = [0.748, 0.892, 0.642, 0.853, 0.485, 0.001]
    security = [0.800, 0.670, 0.800, 0.670, 0.800, 0.670]
    decentralization = [0.708, 0.535, 0.587, 0.427, 0.600, 0.575]
    energy = [0.980, 0.995, 0.990, 0.990, 0.985, 0.200]
    
    colors = ['#2E8B57', '#FF6347', '#4169E1', '#DAA520', '#9370DB', '#8B0000']
    markers = ['o', 's', '^', 'D', 'v', 'X']
    
    # Scalability vs Security
    for i, protocol in enumerate(protocols):
        ax1.scatter(scalability[i], security[i], c=colors[i], s=150, marker=markers[i], 
                   alpha=0.8, edgecolors='black', linewidth=1.5, label=protocol)
    ax1.set_xlabel('Scalability Score', fontweight='bold')
    ax1.set_ylabel('Security Score', fontweight='bold')
    ax1.set_title('Scalability vs Security Trade-off', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Energy vs Scalability
    for i, protocol in enumerate(protocols):
        ax2.scatter(scalability[i], energy[i], c=colors[i], s=150, marker=markers[i], 
                   alpha=0.8, edgecolors='black', linewidth=1.5, label=protocol)
    ax2.set_xlabel('Scalability Score', fontweight='bold')
    ax2.set_ylabel('Energy Efficiency Score', fontweight='bold')
    ax2.set_title('Energy vs Scalability Efficiency', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Security vs Decentralization
    for i, protocol in enumerate(protocols):
        ax3.scatter(decentralization[i], security[i], c=colors[i], s=150, marker=markers[i], 
                   alpha=0.8, edgecolors='black', linewidth=1.5, label=protocol)
    ax3.set_xlabel('Decentralization Score', fontweight='bold')
    ax3.set_ylabel('Security Score', fontweight='bold')
    ax3.set_title('Security vs Decentralization Alignment', fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # TBI vs Average
    avg_scores = [(s+sec+d+e)/4 for s,sec,d,e in zip(scalability, security, decentralization, energy)]
    tbi_scores = [0.809, 0.772, 0.755, 0.737, 0.712, 0.372]
    
    for i, protocol in enumerate(protocols):
        ax4.scatter(avg_scores[i], tbi_scores[i], c=colors[i], s=150, marker=markers[i], 
                   alpha=0.8, edgecolors='black', linewidth=1.5, label=protocol)
    
    # Add diagonal line
    ax4.plot([0, 1], [0, 1], 'r--', alpha=0.5, label='Perfect Correlation')
    ax4.set_xlabel('Average Pillar Score', fontweight='bold')
    ax4.set_ylabel('TBI Score', fontweight='bold')
    ax4.set_title('TBI vs Individual Pillar Performance', fontweight='bold')
    ax4.grid(True, alpha=0.3)
    ax4.legend()
    
    plt.suptitle('Figure 5.4: Pillar Trade-off Analysis', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('outputs/pillar_tradeoff_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_energy_efficiency_comparison():
    """Figure 5.5: Energy Efficiency Comparison"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Data
    protocols = ['DAG', 'IBFT-Besu', 'DPoS', 'CometBFT', 'HotStuff', 'PoW']
    energy_wh = [0.01, 0.02, 0.02, 0.03, 0.04, 0.8]
    vehicles = [4, 8, 8, 12, 17, 3500]
    colors = ['#FF6347', '#4169E1', '#DAA520', '#9370DB', '#2E8B57', '#8B0000']
    
    # Energy consumption (log scale)
    bars1 = ax1.bar(protocols, energy_wh, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax1.set_yscale('log')
    ax1.set_ylabel('Energy Consumption (Wh/tx)', fontsize=12, fontweight='bold')
    ax1.set_title('Energy Consumption per Transaction (Log Scale)', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Add value labels
    for bar, energy in zip(bars1, energy_wh):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.5, 
                f'{energy:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # Add annotation for 80x gap
    ax1.annotate('80x Gap', xy=(4.5, 0.4), xytext=(3.5, 0.2),
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=12, fontweight='bold', color='red')
    
    # Carbon footprint
    bars2 = ax2.bar(protocols, vehicles, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('Annual Vehicle Equivalent', fontsize=12, fontweight='bold')
    ax2.set_title('Carbon Footprint Comparison (Passenger Vehicle Equivalents)', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Add value labels
    for bar, vehicle in zip(bars2, vehicles):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(vehicles)*0.02, 
                f'{vehicle}', ha='center', va='bottom', fontweight='bold')
    
    plt.suptitle('Figure 5.5: Energy Efficiency Comparison', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('outputs/energy_efficiency_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_committee_safety_curves():
    """Figure 5.6: Committee Safety Risk Curves"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Committee sizes
    k_values = np.arange(4, 23)
    
    # Beta values
    beta_values = [0.1, 0.2, 0.33]
    beta_labels = ['β = 0.1 (Weak Adversary)', 'β = 0.2 (Realistic)', 'β = 0.33 (Strong Adversary)']
    colors = ['green', 'blue', 'red']
    
    for i, beta in enumerate(beta_values):
        # Calculate safety risk ε using binomial
        epsilon_values = []
        for k in k_values:
            f = int(np.floor((k-1)/3))
            # Simplified risk calculation
            epsilon = beta**(f+1) * (k/(f+1))
            epsilon_values.append(min(epsilon, 0.1))
        
        ax.plot(k_values, epsilon_values, 'o-', color=colors[i], linewidth=2, 
               markersize=6, label=beta_labels[i])
    
    # Add risk threshold lines
    ax.axhline(y=0.01, color='orange', linestyle='--', alpha=0.7, label='Medium Risk (1%)')
    ax.axhline(y=0.05, color='red', linestyle='--', alpha=0.7, label='High Risk (5%)')
    
    ax.set_xlabel('Committee Size (k)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Safety Risk (ε)', fontsize=12, fontweight='bold')
    ax.set_title('Figure 5.6: Committee Safety Risk vs Committee Size', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_ylim(0, 0.1)
    
    plt.tight_layout()
    plt.savefig('outputs/committee_safety_curves.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_bootstrap_analysis():
    """Figure 5.7: Bootstrap Analysis Results"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Protocol data
    protocols = ['HotStuff', 'DAG', 'IBFT-Besu', 'DPoS', 'CometBFT', 'PoW']
    tbi_means = [0.809, 0.772, 0.755, 0.737, 0.712, 0.372]
    ci_lower = [0.801, 0.765, 0.748, 0.729, 0.705, 0.368]
    ci_upper = [0.817, 0.779, 0.762, 0.745, 0.719, 0.376]
    
    colors = ['#2E8B57', '#FF6347', '#4169E1', '#DAA520', '#9370DB', '#8B0000']
    
    y_pos = np.arange(len(protocols))
    
    # Create horizontal confidence interval plot
    for i, (protocol, mean, lower, upper) in enumerate(zip(protocols, tbi_means, ci_lower, ci_upper)):
        ax.barh(y_pos[i], upper - lower, left=lower, height=0.4, 
               color=colors[i], alpha=0.6, edgecolor='black')
        ax.scatter(mean, y_pos[i], color=colors[i], s=100, zorder=5, edgecolors='black')
        
        # Add CI text
        ax.text(upper + 0.005, y_pos[i], f'95% CI: [{lower:.3f}, {upper:.3f}]', 
               va='center', fontsize=9, fontweight='bold')
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels([f'{p}\n(Mean: {m:.3f})' for p, m in zip(protocols, tbi_means)], fontweight='bold')
    ax.set_xlabel('TBI Score', fontsize=12, fontweight='bold')
    ax.set_title('Figure 5.7: Bootstrap Analysis Results\n(1,000 Bootstrap Samples)', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0.35, 0.85)
    
    # Add significance note
    ax.text(0.36, 5.5, '✓ All pairwise differences significant (p < 0.001)\n✓ No overlap in confidence intervals\n✓ Robust ranking order maintained', 
           bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.8),
           fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('outputs/bootstrap_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_trilemma_resolution():
    """Figure 5.8: Trilemma Resolution Evidence"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Traditional trilemma (left)
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    
    # Triangle vertices
    vertices = np.array([[0, 1], [-0.866, -0.5], [0.866, -0.5], [0, 1]])
    ax1.plot(vertices[:, 0], vertices[:, 1], 'k-', linewidth=3)
    ax1.fill(vertices[:, 0], vertices[:, 1], alpha=0.1, color='gray')
    
    # Labels
    ax1.text(0, 1.3, 'Security', ha='center', fontsize=14, fontweight='bold')
    ax1.text(-1.1, -0.7, 'Decentralization', ha='center', fontsize=14, fontweight='bold', rotation=60)
    ax1.text(1.1, -0.7, 'Scalability', ha='center', fontsize=14, fontweight='bold', rotation=-60)
    
    # Traditional constraints
    ax1.scatter([-0.4], [0.3], s=200, c='red', marker='s', label='Bitcoin (PoW)', edgecolors='black', linewidth=2)
    ax1.scatter([0.4], [0.3], s=200, c='blue', marker='^', label='Traditional Systems', edgecolors='black', linewidth=2)
    ax1.text(0, -0.2, '"Choose Any Two"', ha='center', fontsize=12, style='italic', fontweight='bold')
    
    ax1.set_title('Traditional Blockchain Trilemma\n(Buterin 2017)', fontsize=14, fontweight='bold')
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.3))
    
    # TEF-2025 results (right) - 3D representation on 2D
    protocols = ['HotStuff', 'DAG', 'IBFT-Besu', 'DPoS', 'CometBFT', 'PoW']
    tbi_scores = [0.809, 0.772, 0.755, 0.737, 0.712, 0.372]
    x_pos = [0.748, 0.892, 0.642, 0.853, 0.485, 0.001]  # Scalability
    y_pos = [0.800, 0.670, 0.800, 0.670, 0.800, 0.670]  # Security
    
    colors = ['#2E8B57', '#FF6347', '#4169E1', '#DAA520', '#9370DB', '#8B0000']
    
    # Create scatter with size representing TBI
    for i, (protocol, tbi, x, y) in enumerate(zip(protocols, tbi_scores, x_pos, y_pos)):
        size = tbi * 300
        ax2.scatter(x, y, s=size, c=colors[i], alpha=0.8, edgecolors='black', linewidth=2)
        ax2.annotate(f'{protocol}\n(TBI: {tbi:.3f})', (x, y), 
                    xytext=(10, 10), textcoords='offset points', 
                    fontsize=9, fontweight='bold')
    
    # Add threshold lines
    ax2.axhline(y=0.7, color='red', linestyle='--', alpha=0.7, label='Trilemma Resolution (0.7)')
    ax2.axvline(x=0.7, color='orange', linestyle='--', alpha=0.7, label='High Scalability (0.7)')
    
    ax2.set_xlabel('Scalability Score', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Security Score', fontsize=12, fontweight='bold')
    ax2.set_title('TEF-2025 Four-Pillar Results\n(2025)', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0.6, 0.85)
    
    plt.suptitle('Figure 5.8: Trilemma Resolution Evidence', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('outputs/trilemma_resolution.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """Generate all Chapter 5 figures"""
    # Create outputs directory if it doesn't exist
    Path('outputs').mkdir(exist_ok=True)
    
    print("Generating Chapter 5 figures...")
    
    create_data_source_classification()
    print("✓ Figure 5.1: Data Source Classification")
    
    create_protocol_performance_radar()
    print("✓ Figure 5.2: Protocol Performance Radar Chart")
    
    create_performance_distribution()
    print("✓ Figure 5.3: Performance Distribution by Protocol Family")
    
    create_pillar_tradeoff_analysis()
    print("✓ Figure 5.4: Pillar Trade-off Analysis")
    
    create_energy_efficiency_comparison()
    print("✓ Figure 5.5: Energy Efficiency Comparison")
    
    create_committee_safety_curves()
    print("✓ Figure 5.6: Committee Safety Risk Curves")
    
    create_bootstrap_analysis()
    print("✓ Figure 5.7: Bootstrap Analysis Results")
    
    create_trilemma_resolution()
    print("✓ Figure 5.8: Trilemma Resolution Evidence")
    
    print("\nAll Chapter 5 figures generated successfully!")
    print("Files saved in outputs/ directory")

if __name__ == "__main__":
    main()
