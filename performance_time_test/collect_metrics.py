"""
Performance Metrics Collection and Analysis Script
Processes exported JSON files from the Performance Logger
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import statistics


def load_metrics(file_path):
    """Load metrics from exported JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        sys.exit(1)


def calculate_statistics(times):
    """Calculate comprehensive statistics for a list of times"""
    if not times:
        return None
    
    return {
        'count': len(times),
        'mean': statistics.mean(times),
        'median': statistics.median(times),
        'stdev': statistics.stdev(times) if len(times) > 1 else 0,
        'min': min(times),
        'max': max(times),
        'range': max(times) - min(times),
        'q1': statistics.quantiles(times, n=4)[0] if len(times) >= 4 else min(times),
        'q3': statistics.quantiles(times, n=4)[2] if len(times) >= 4 else max(times)
    }


def format_time(ms):
    """Format milliseconds for display"""
    if ms < 1:
        return f"{ms:.3f}ms"
    elif ms < 1000:
        return f"{ms:.2f}ms"
    else:
        return f"{ms/1000:.2f}s ({ms:.0f}ms)"


def print_statistics(stats, question_type):
    """Pretty print statistics for a question type"""
    if not stats:
        print(f"  No data collected")
        return
    
    print(f"\n  {'Metric':<15} {'Value':<20}")
    print(f"  {'-'*35}")
    print(f"  {'Sample Count':<15} {stats['count']}")
    print(f"  {'Mean':<15} {format_time(stats['mean'])}")
    print(f"  {'Median':<15} {format_time(stats['median'])}")
    print(f"  {'Std Dev':<15} {format_time(stats['stdev'])}")
    print(f"  {'Min':<15} {format_time(stats['min'])}")
    print(f"  {'Max':<15} {format_time(stats['max'])}")
    print(f"  {'Range':<15} {format_time(stats['range'])}")
    print(f"  {'Q1 (25%)':<15} {format_time(stats['q1'])}")
    print(f"  {'Q3 (75%)':<15} {format_time(stats['q3'])}")


def generate_abstract_text(all_stats):
    """Generate performance text suitable for an abstract"""
    print("\n" + "="*60)
    print("📄 TEXT FOR ABSTRACT/RESEARCH PAPER")
    print("="*60)
    
    text_parts = []
    
    type_names = {
        'one_word': 'one-word matching',
        'list': 'list comparison',
        'numerical': 'numerical validation',
        'short_phrase': 'AI semantic analysis'
    }
    
    for q_type, stats in all_stats.items():
        if stats and stats['count'] > 0:
            type_name = type_names.get(q_type, q_type)
            mean_time = format_time(stats['mean'])
            text_parts.append(f"{type_name}: {mean_time}")
    
    print("\nPerformance Metrics Summary:")
    print("-" * 60)
    for part in text_parts:
        print(f"- {part}")
    
    print("\n\nSample Abstract Text:")
    print("-" * 60)
    print("The grading system demonstrates efficient processing across multiple")
    print("question types:")
    for part in text_parts:
        print(f"  • {part}")
    
    if 'short_phrase' in all_stats and all_stats['short_phrase']:
        print("\n*AI-based grading requires local LLM (Ollama qwen2.5:1.5b) and")
        print("performance varies with hardware specifications.")


def generate_html_report(data, all_stats, output_path):
    """Generate an HTML report with visualizations"""
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>Grading Performance Report</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            max-width: 1200px;
            margin: 40px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
        }
        .metric-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .metric-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 15px;
            color: #333;
        }
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }
        .stat-item {
            background: #f8f9fa;
            padding: 12px;
            border-radius: 6px;
            border-left: 4px solid #667eea;
        }
        .stat-label {
            font-size: 12px;
            color: #666;
            margin-bottom: 4px;
        }
        .stat-value {
            font-size: 20px;
            font-weight: 600;
            color: #333;
        }
        .metadata {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 6px;
            margin-top: 20px;
            font-size: 13px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 AutoGradePro Performance Report</h1>
        <p>Generated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
    </div>
"""
    
    type_names = {
        'one_word': '📝 One-Word Matching',
        'list': '📋 List Comparison',
        'numerical': '🔢 Numerical Validation',
        'short_phrase': '🤖 AI Semantic Analysis'
    }
    
    for q_type, stats in all_stats.items():
        if not stats or stats['count'] == 0:
            continue
            
        html += f"""
    <div class="metric-card">
        <div class="metric-title">{type_names.get(q_type, q_type)}</div>
        <div class="stat-grid">
            <div class="stat-item">
                <div class="stat-label">Samples</div>
                <div class="stat-value">{stats['count']}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Mean</div>
                <div class="stat-value">{format_time(stats['mean'])}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Median</div>
                <div class="stat-value">{format_time(stats['median'])}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Std Dev</div>
                <div class="stat-value">{format_time(stats['stdev'])}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Min</div>
                <div class="stat-value">{format_time(stats['min'])}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Max</div>
                <div class="stat-value">{format_time(stats['max'])}</div>
            </div>
        </div>
    </div>
"""
    
    metadata = data.get('metadata', {})
    html += f"""
    <div class="metadata">
        <strong>Metadata:</strong><br>
        Collected at: {metadata.get('collected_at', 'Unknown')}<br>
        Browser: {metadata.get('browser', 'Unknown')}
    </div>
</body>
</html>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✅ HTML report generated: {output_path}")


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python collect_metrics.py <path_to_exported_json>")
        print("\nExample:")
        print("  python collect_metrics.py grading_performance_1234567890.json")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
    
    print("🔍 Loading metrics from:", file_path)
    data = load_metrics(file_path)
    
    # Extract raw data
    raw_data = data.get('raw_data', {})
    
    # Calculate statistics for each question type
    all_stats = {}
    
    print("\n" + "="*60)
    print("📊 PERFORMANCE ANALYSIS")
    print("="*60)
    
    type_names = {
        'one_word': '📝 One-Word Matching',
        'list': '📋 List Comparison',
        'numerical': '🔢 Numerical Validation',
        'short_phrase': '🤖 AI Semantic Analysis'
    }
    
    for q_type in ['one_word', 'list', 'numerical', 'short_phrase']:
        times = raw_data.get(q_type, [])
        stats = calculate_statistics(times) if times else None
        all_stats[q_type] = stats
        
        print(f"\n{type_names.get(q_type, q_type)}")
        print("-" * 60)
        print_statistics(stats, q_type)
    
    # Generate abstract text
    generate_abstract_text(all_stats)
    
    # Generate HTML report
    output_html = file_path.parent / f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    generate_html_report(data, all_stats, output_html)
    
    print("\n" + "="*60)
    print("✅ Analysis Complete!")
    print("="*60)
    print(f"\nProcessed {sum(len(raw_data.get(t, [])) for t in raw_data)} total samples")
    print(f"Collected at: {data.get('metadata', {}).get('collected_at', 'Unknown')}")


if __name__ == "__main__":
    main()
