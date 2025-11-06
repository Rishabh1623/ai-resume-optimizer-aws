#!/usr/bin/env python3
"""
AI Resume Optimizer - Visual Architecture Generator
Creates professional architecture diagrams using Python libraries
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_architecture_diagram():
    """Create the main solution architecture diagram"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Title
    ax.text(8, 11.5, 'AI Resume Optimizer - Agentic AI Architecture', 
            fontsize=20, fontweight='bold', ha='center')
    ax.text(8, 11, 'Event-Driven Serverless System on AWS', 
            fontsize=14, ha='center', style='italic')
    
    # Color scheme
    colors = {
        'user': '#FF6B6B',
        'api': '#4ECDC4', 
        'compute': '#45B7D1',
        'ai': '#96CEB4',
        'storage': '#FFEAA7',
        'events': '#DDA0DD',
        'monitoring': '#98D8C8'
    }
    
    # User Layer
    user_box = FancyBboxPatch((0.5, 9.5), 2, 1.5, 
                              boxstyle="round,pad=0.1", 
                              facecolor=colors['user'], 
                              edgecolor='black', linewidth=2)
    ax.add_patch(user_box)
    ax.text(1.5, 10.2, 'USER\n📱 Web App\n📧 Email\n🌐 S3 Console', 
            ha='center', va='center', fontweight='bold')
    
    # API Gateway
    api_box = FancyBboxPatch((4, 9.5), 2, 1.5,
                             boxstyle="round,pad=0.1",
                             facecolor=colors['api'],
                             edgecolor='black', linewidth=2)
    ax.add_patch(api_box)
    ax.text(5, 10.2, 'API GATEWAY\n🌐 REST API\n/health\n/optimize', 
            ha='center', va='center', fontweight='bold')
    
    # Step Functions (Agentic AI)
    step_box = FancyBboxPatch((7.5, 8), 6, 3,
                              boxstyle="round,pad=0.1",
                              facecolor=colors['compute'],
                              edgecolor='black', linewidth=3)
    ax.add_patch(step_box)
    ax.text(10.5, 10, 'STEP FUNCTIONS - AGENTIC AI WORKFLOW', 
            ha='center', va='center', fontweight='bold', fontsize=12)
    
    # Agentic AI phases
    phases = ['PERCEIVE\n(Analyze)', 'PLAN\n(Strategy)', 'ACT\n(Generate)', 
              'EVALUATE\n(Score)', 'LEARN\n(Memory)']
    for i, phase in enumerate(phases):
        phase_box = FancyBboxPatch((8 + i*1, 8.5), 0.8, 0.8,
                                   boxstyle="round,pad=0.05",
                                   facecolor='white',
                                   edgecolor='blue', linewidth=1)
        ax.add_patch(phase_box)
        ax.text(8.4 + i*1, 8.9, phase, ha='center', va='center', fontsize=8)
    
    # EventBridge
    event_box = FancyBboxPatch((0.5, 7), 3, 1.5,
                               boxstyle="round,pad=0.1",
                               facecolor=colors['events'],
                               edgecolor='black', linewidth=2)
    ax.add_patch(event_box)
    ax.text(2, 7.7, 'EVENTBRIDGE\n🔄 Custom Bus\n📡 Event Rules\n⚡ Triggers', 
            ha='center', va='center', fontweight='bold')
    
    # S3 Input
    s3_input_box = FancyBboxPatch((0.5, 5), 2, 1.5,
                                  boxstyle="round,pad=0.1",
                                  facecolor=colors['storage'],
                                  edgecolor='black', linewidth=2)
    ax.add_patch(s3_input_box)
    ax.text(1.5, 5.7, 'S3 INPUT\n📁 Resumes\n📄 Job Desc\n📤 Upload', 
            ha='center', va='center', fontweight='bold')
    
    # Lambda Functions
    lambdas = [
        ('S3 Trigger', 4, 6.5),
        ('Analyze', 6, 6.5),
        ('Plan', 8, 6.5),
        ('Generate', 10, 6.5),
        ('Evaluate', 12, 6.5),
        ('Learn', 14, 6.5)
    ]
    
    for name, x, y in lambdas:
        lambda_box = FancyBboxPatch((x-0.7, y-0.4), 1.4, 0.8,
                                    boxstyle="round,pad=0.05",
                                    facecolor=colors['compute'],
                                    edgecolor='black', linewidth=1)
        ax.add_patch(lambda_box)
        ax.text(x, y, f'λ {name}', ha='center', va='center', fontweight='bold', fontsize=9)
    
    # AI Services
    ai_services = [
        ('BEDROCK\nClaude 3', 2, 4),
        ('TEXTRACT\nPDF OCR', 5, 4),
        ('COMPREHEND\nNLP', 8, 4)
    ]
    
    for service, x, y in ai_services:
        ai_box = FancyBboxPatch((x-0.8, y-0.5), 1.6, 1,
                                boxstyle="round,pad=0.1",
                                facecolor=colors['ai'],
                                edgecolor='black', linewidth=2)
        ax.add_patch(ai_box)
        ax.text(x, y, service, ha='center', va='center', fontweight='bold', fontsize=9)
    
    # DynamoDB Tables
    ddb_tables = [
        ('JOBS\nTABLE', 11, 4),
        ('AGENT\nMEMORY', 13, 4),
        ('ANALYTICS\nTABLE', 15, 4)
    ]
    
    for table, x, y in ddb_tables:
        ddb_box = FancyBboxPatch((x-0.8, y-0.5), 1.6, 1,
                                 boxstyle="round,pad=0.1",
                                 facecolor=colors['storage'],
                                 edgecolor='black', linewidth=2)
        ax.add_patch(ddb_box)
        ax.text(x, y, f'📊 {table}', ha='center', va='center', fontweight='bold', fontsize=9)
    
    # S3 Output & SNS
    s3_output_box = FancyBboxPatch((2, 2), 2, 1,
                                   boxstyle="round,pad=0.1",
                                   facecolor=colors['storage'],
                                   edgecolor='black', linewidth=2)
    ax.add_patch(s3_output_box)
    ax.text(3, 2.5, 'S3 OUTPUT\n📁 Optimized\n📄 Results', 
            ha='center', va='center', fontweight='bold')
    
    sns_box = FancyBboxPatch((6, 2), 2, 1,
                             boxstyle="round,pad=0.1",
                             facecolor=colors['monitoring'],
                             edgecolor='black', linewidth=2)
    ax.add_patch(sns_box)
    ax.text(7, 2.5, 'SNS\n📧 Email\n🔔 Alerts', 
            ha='center', va='center', fontweight='bold')
    
    # Monitoring
    monitoring_box = FancyBboxPatch((10, 2), 4, 1,
                                    boxstyle="round,pad=0.1",
                                    facecolor=colors['monitoring'],
                                    edgecolor='black', linewidth=2)
    ax.add_patch(monitoring_box)
    ax.text(12, 2.5, 'MONITORING\n📊 CloudWatch  🔍 X-Ray  🔐 IAM', 
            ha='center', va='center', fontweight='bold')
    
    # Add arrows for data flow
    arrows = [
        # User to API
        ((2.5, 10.2), (4, 10.2)),
        # API to Step Functions
        ((6, 10.2), (7.5, 9.5)),
        # S3 to EventBridge
        ((1.5, 6.5), (2, 7)),
        # EventBridge to Step Functions
        ((3.5, 7.7), (7.5, 9)),
        # Step Functions to Lambdas
        ((10.5, 8), (10.5, 7)),
        # Output flow
        ((10.5, 8), (7, 3)),
        ((7, 3), (3, 3))
    ]
    
    for start, end in arrows:
        arrow = ConnectionPatch(start, end, "data", "data",
                               arrowstyle="->", shrinkA=5, shrinkB=5,
                               mutation_scale=20, fc="red", ec="red", linewidth=2)
        ax.add_patch(arrow)
    
    # Add legend
    legend_elements = [
        patches.Patch(color=colors['user'], label='User Interface'),
        patches.Patch(color=colors['api'], label='API Layer'),
        patches.Patch(color=colors['compute'], label='Compute Services'),
        patches.Patch(color=colors['ai'], label='AI Services'),
        patches.Patch(color=colors['storage'], label='Storage Services'),
        patches.Patch(color=colors['events'], label='Event Services'),
        patches.Patch(color=colors['monitoring'], label='Monitoring')
    ]
    
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
    
    plt.tight_layout()
    plt.savefig('architecture_diagram.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_agentic_flow_diagram():
    """Create the agentic AI decision flow diagram"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'Agentic AI Decision Flow', 
            fontsize=18, fontweight='bold', ha='center')
    
    # Decision nodes
    nodes = [
        ('START\nResume Upload', 2, 8.5, '#FF6B6B'),
        ('PERCEIVE\nAnalyze Job Type', 2, 7, '#4ECDC4'),
        ('PLAN\nChoose Strategy', 2, 5.5, '#45B7D1'),
        ('ACT\nGenerate 3 Versions', 2, 4, '#96CEB4'),
        ('EVALUATE\nScore Versions', 6, 4, '#FFEAA7'),
        ('DECIDE\nQuality Check', 10, 4, '#DDA0DD'),
        ('ITERATE\nImprove', 10, 6, '#FFB6C1'),
        ('LEARN\nStore Strategy', 10, 2, '#98D8C8'),
        ('COMPLETE\nDeliver Results', 6, 2, '#90EE90')
    ]
    
    for text, x, y, color in nodes:
        node_box = FancyBboxPatch((x-0.8, y-0.4), 1.6, 0.8,
                                  boxstyle="round,pad=0.1",
                                  facecolor=color,
                                  edgecolor='black', linewidth=2)
        ax.add_patch(node_box)
        ax.text(x, y, text, ha='center', va='center', fontweight='bold', fontsize=9)
    
    # Decision paths
    paths = [
        ((2, 8.1), (2, 7.4)),  # START -> PERCEIVE
        ((2, 6.6), (2, 5.9)),  # PERCEIVE -> PLAN
        ((2, 5.1), (2, 4.4)),  # PLAN -> ACT
        ((2.8, 4), (5.2, 4)),  # ACT -> EVALUATE
        ((6.8, 4), (9.2, 4)),  # EVALUATE -> DECIDE
        ((10, 4.4), (10, 5.6)),  # DECIDE -> ITERATE (No)
        ((10, 6.4), (6.8, 4.4)),  # ITERATE -> EVALUATE
        ((10, 3.6), (10, 2.4)),  # DECIDE -> LEARN (Yes)
        ((9.2, 2), (6.8, 2))   # LEARN -> COMPLETE
    ]
    
    for start, end in paths:
        arrow = ConnectionPatch(start, end, "data", "data",
                               arrowstyle="->", shrinkA=5, shrinkB=5,
                               mutation_scale=20, fc="blue", ec="blue", linewidth=2)
        ax.add_patch(arrow)
    
    # Add decision labels
    ax.text(10.5, 5, 'Score < 85\n(Iterate)', ha='center', va='center', 
            fontsize=8, bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow'))
    ax.text(10.5, 3, 'Score ≥ 85\n(Success)', ha='center', va='center', 
            fontsize=8, bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen'))
    
    # Add example scores
    ax.text(12, 7, 'EXAMPLE ITERATION:\n\nIteration 1:\n• Keywords: 78/100\n• Achievement: 82/100\n• Structure: 75/100\n\nBest: 82 < 85 → Iterate\n\nIteration 2:\n• Keywords: 88/100 ✓\n• Achievement: 85/100 ✓\n• Structure: 80/100\n\nBest: 88 ≥ 85 → Success!', 
            ha='left', va='top', fontsize=9,
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('agentic_flow_diagram.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_cost_breakdown_chart():
    """Create cost breakdown visualization"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Per-resume cost breakdown
    services = ['Lambda\nExecution', 'Bedrock\n(Claude)', 'Textract\nOCR', 
                'Comprehend\nNLP', 'Storage\n(S3/DDB)', 'Other\nServices']
    costs = [0.0001, 0.0040, 0.0015, 0.0001, 0.0003, 0.0000]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
    
    wedges, texts, autotexts = ax1.pie(costs, labels=services, colors=colors, 
                                       autopct='%1.1f%%', startangle=90)
    ax1.set_title('Cost per Resume (~$0.006)', fontsize=14, fontweight='bold')
    
    # Monthly scaling
    volumes = [100, 500, 1000, 5000, 10000]
    monthly_costs = [v * 0.006 for v in volumes]
    
    ax2.bar(range(len(volumes)), monthly_costs, color='#45B7D1', alpha=0.7)
    ax2.set_xlabel('Monthly Resume Volume')
    ax2.set_ylabel('Monthly Cost ($)')
    ax2.set_title('Monthly Cost Scaling', fontsize=14, fontweight='bold')
    ax2.set_xticks(range(len(volumes)))
    ax2.set_xticklabels([f'{v:,}' for v in volumes])
    
    # Add cost labels on bars
    for i, cost in enumerate(monthly_costs):
        ax2.text(i, cost + 1, f'${cost:.2f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('cost_breakdown.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    print("🎨 Generating AI Resume Optimizer Architecture Diagrams...")
    
    print("📊 Creating main architecture diagram...")
    create_architecture_diagram()
    
    print("🤖 Creating agentic AI flow diagram...")
    create_agentic_flow_diagram()
    
    print("💰 Creating cost breakdown chart...")
    create_cost_breakdown_chart()
    
    print("✅ All diagrams generated successfully!")
    print("\nGenerated files:")
    print("• architecture_diagram.png - Main solution architecture")
    print("• agentic_flow_diagram.png - AI decision flow")
    print("• cost_breakdown.png - Cost analysis")
    print("\n🚀 Architecture diagrams ready for presentation!")