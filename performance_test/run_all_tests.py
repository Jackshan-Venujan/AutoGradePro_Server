"""
Master Test Runner
Runs all tests (accuracy and performance) and generates comprehensive reports.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from test_accuracy import AccuracyTester
from test_performance import PerformanceTester

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    class Fore:
        CYAN = GREEN = YELLOW = RED = BLUE = MAGENTA = ""
    class Style:
        RESET_ALL = BRIGHT = ""


def print_header():
    """Print fancy header"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}║{'':^68}║")
    print(f"{Fore.CYAN}║{Fore.GREEN}    AutoGradePro Grading Methods Testing Framework    {Fore.CYAN}║")
    print(f"{Fore.CYAN}║{'':^68}║")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")


def print_section(title):
    """Print section header"""
    print(f"\n{Fore.YELLOW}{'='*70}")
    print(f"{title}")
    print(f"{'='*70}{Style.RESET_ALL}\n")


def generate_html_report(accuracy_results, performance_results):
    """Generate a comprehensive HTML report"""
    
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AutoGradePro Grading Methods Test Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section-title {{
            font-size: 1.8em;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        
        .grading-type {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 20px;
            border-left: 5px solid #667eea;
        }}
        
        .grading-type h3 {{
            color: #764ba2;
            font-size: 1.5em;
            margin-bottom: 15px;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        
        .metric {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        
        .metric-label {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 5px;
        }}
        
        .metric-value {{
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .metric-value.good {{
            color: #28a745;
        }}
        
        .metric-value.warning {{
            color: #ffc107;
        }}
        
        .metric-value.bad {{
            color: #dc3545;
        }}
        
        .summary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        
        .summary h2 {{
            font-size: 2em;
            margin-bottom: 20px;
        }}
        
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }}
        
        .summary-card {{
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        
        .summary-card h3 {{
            font-size: 1.2em;
            margin-bottom: 10px;
            opacity: 0.9;
        }}
        
        .summary-card .value {{
            font-size: 2.5em;
            font-weight: bold;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
        
        .badge {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
            margin-left: 10px;
        }}
        
        .badge.pass {{
            background: #28a745;
            color: white;
        }}
        
        .badge.warning {{
            background: #ffc107;
            color: #333;
        }}
        
        .badge.fail {{
            background: #dc3545;
            color: white;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        
        th {{
            background: #667eea;
            color: white;
            font-weight: bold;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 AutoGradePro</h1>
            <p>Grading Methods Testing Report</p>
            <p style="font-size: 0.9em; margin-top: 10px;">Generated: {timestamp}</p>
        </div>
        
        <div class="content">
            <div class="summary">
                <h2>Executive Summary</h2>
                <div class="summary-grid">
                    <div class="summary-card">
                        <h3>Total Tests</h3>
                        <div class="value">{total_tests}</div>
                    </div>
                    <div class="summary-card">
                        <h3>Overall Accuracy</h3>
                        <div class="value">{overall_accuracy}%</div>
                    </div>
                    <div class="summary-card">
                        <h3>Avg Response Time</h3>
                        <div class="value">{avg_time} ms</div>
                    </div>
                    <div class="summary-card">
                        <h3>Status</h3>
                        <div class="value">✅</div>
                    </div>
                </div>
            </div>
            
            {grading_sections}
            
            <div class="section">
                <div class="section-title">📊 Detailed Comparison Table</div>
                <table>
                    <thead>
                        <tr>
                            <th>Grading Method</th>
                            <th>Accuracy</th>
                            <th>Avg Time (ms)</th>
                            <th>Throughput (ops/s)</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {comparison_rows}
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="footer">
            <p>AutoGradePro Testing Framework v1.0</p>
            <p>© 2025 AutoGradePro. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
    """
    
    # Calculate summary statistics
    total_tests = sum(accuracy_results.get(gt, {}).get("total", 0) 
                     for gt in ["one_word", "short_phrase", "list", "numerical"])
    
    accuracies = []
    times = []
    
    for gt in ["one_word", "short_phrase", "list", "numerical"]:
        acc_data = accuracy_results.get(gt, {})
        perf_data = performance_results.get(gt, {})
        
        if "accuracy" in acc_data:
            accuracies.append(acc_data["accuracy"])
        
        if "aggregate" in perf_data:
            times.append(perf_data["aggregate"]["mean_ms"])
    
    overall_accuracy = f"{sum(accuracies) / len(accuracies):.1f}" if accuracies else "N/A"
    avg_time = f"{sum(times) / len(times):.2f}" if times else "N/A"
    
    # Generate grading method sections
    grading_sections = ""
    comparison_rows = ""
    
    method_names = {
        "one_word": "One-Word Grading",
        "short_phrase": "Short-Phrase (AI) Grading",
        "list": "List Grading",
        "numerical": "Numerical Grading"
    }
    
    for gt_key in ["one_word", "short_phrase", "list", "numerical"]:
        acc_data = accuracy_results.get(gt_key, {})
        perf_data = performance_results.get(gt_key, {})
        
        if not acc_data or acc_data.get("total", 0) == 0:
            continue
        
        method_name = method_names[gt_key]
        accuracy = acc_data.get("accuracy", 0)
        
        # Determine status badge
        if accuracy >= 95:
            badge_class = "pass"
            badge_text = "EXCELLENT"
        elif accuracy >= 85:
            badge_class = "warning"
            badge_text = "GOOD"
        else:
            badge_class = "fail"
            badge_text = "NEEDS IMPROVEMENT"
        
        # Build metrics HTML
        metrics_html = ""
        
        # Accuracy metrics
        if "accuracy" in acc_data:
            metrics_html += f"""
            <div class="metric">
                <div class="metric-label">Accuracy</div>
                <div class="metric-value {'good' if accuracy >= 95 else 'warning' if accuracy >= 85 else 'bad'}">{accuracy:.1f}%</div>
            </div>
            """
        
        if "precision" in acc_data:
            metrics_html += f"""
            <div class="metric">
                <div class="metric-label">Precision</div>
                <div class="metric-value">{acc_data['precision']:.1f}%</div>
            </div>
            """
        
        if "recall" in acc_data:
            metrics_html += f"""
            <div class="metric">
                <div class="metric-label">Recall</div>
                <div class="metric-value">{acc_data['recall']:.1f}%</div>
            </div>
            """
        
        # Performance metrics
        if "aggregate" in perf_data:
            agg = perf_data["aggregate"]
            mean_time = agg["mean_ms"]
            
            metrics_html += f"""
            <div class="metric">
                <div class="metric-label">Avg Response Time</div>
                <div class="metric-value {'good' if mean_time < 10 else 'warning' if mean_time < 100 else 'bad'}">{mean_time:.2f} ms</div>
            </div>
            <div class="metric">
                <div class="metric-label">Min Time</div>
                <div class="metric-value">{agg['min_ms']:.2f} ms</div>
            </div>
            <div class="metric">
                <div class="metric-label">Max Time</div>
                <div class="metric-value">{agg['max_ms']:.2f} ms</div>
            </div>
            """
            
            ops_per_sec = 1000 / mean_time if mean_time > 0 else 0
            metrics_html += f"""
            <div class="metric">
                <div class="metric-label">Throughput</div>
                <div class="metric-value">{ops_per_sec:.0f} ops/s</div>
            </div>
            """
        
        # Error metrics
        if "false_positives" in acc_data:
            metrics_html += f"""
            <div class="metric">
                <div class="metric-label">False Positives</div>
                <div class="metric-value {'good' if acc_data['false_positives'] == 0 else 'bad'}">{acc_data['false_positives']}</div>
            </div>
            """
        
        if "false_negatives" in acc_data:
            metrics_html += f"""
            <div class="metric">
                <div class="metric-label">False Negatives</div>
                <div class="metric-value {'good' if acc_data['false_negatives'] == 0 else 'bad'}">{acc_data['false_negatives']}</div>
            </div>
            """
        
        grading_sections += f"""
        <div class="section">
            <div class="grading-type">
                <h3>{method_name} <span class="badge {badge_class}">{badge_text}</span></h3>
                <div class="metrics-grid">
                    {metrics_html}
                </div>
            </div>
        </div>
        """
        
        # Add comparison row
        status_icon = "✅" if accuracy >= 95 else "⚠️" if accuracy >= 85 else "❌"
        
        # Format timing and throughput
        if 'aggregate' in perf_data:
            mean_time_str = f"{agg['mean_ms']:.2f}"
            ops_str = f"{ops_per_sec:.0f}"
        else:
            mean_time_str = "N/A"
            ops_str = "N/A"
        
        comparison_rows += f"""
        <tr>
            <td><strong>{method_name}</strong></td>
            <td>{accuracy:.1f}%</td>
            <td>{mean_time_str}</td>
            <td>{ops_str}</td>
            <td>{status_icon} {badge_text}</td>
        </tr>
        """
    
    # Fill in template
    html = html_template.format(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_tests=total_tests,
        overall_accuracy=overall_accuracy,
        avg_time=avg_time,
        grading_sections=grading_sections,
        comparison_rows=comparison_rows
    )
    
    return html


def main():
    """Main entry point"""
    print_header()
    
    print(f"{Fore.CYAN}Starting comprehensive testing suite...{Style.RESET_ALL}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check test data exists
    test_data_path = Path(__file__).parent / "test_data" / "grading_test_cases.json"
    if not test_data_path.exists():
        print(f"{Fore.RED}❌ Error: Test data file not found: {test_data_path}{Style.RESET_ALL}")
        return 1
    
    # Run accuracy tests
    print_section("Phase 1: Accuracy Testing")
    accuracy_tester = AccuracyTester(test_data_path)
    accuracy_results = accuracy_tester.run_all_tests()
    
    if not accuracy_results:
        print(f"{Fore.RED}❌ Accuracy testing failed{Style.RESET_ALL}")
        return 1
    
    # Run performance tests
    print_section("Phase 2: Performance Benchmarking")
    performance_tester = PerformanceTester(iterations=100)
    performance_results = performance_tester.run_all_tests()
    
    if not performance_results:
        print(f"{Fore.RED}❌ Performance testing failed{Style.RESET_ALL}")
        return 1
    
    # Generate HTML report
    print_section("Phase 3: Generating HTML Report")
    
    try:
        html_report = generate_html_report(accuracy_results, performance_results)
        
        output_path = Path(__file__).parent / "results" / "summary_report.html"
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        print(f"{Fore.GREEN}✓ HTML report generated: {output_path}{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}To view the report, open: {output_path}{Style.RESET_ALL}")
    
    except Exception as e:
        print(f"{Fore.RED}❌ Error generating HTML report: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
    
    # Final summary
    print(f"\n\n{Fore.GREEN}{'='*70}")
    print(f"{Fore.GREEN}✓ ALL TESTS COMPLETED SUCCESSFULLY!")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print("📁 Generated Reports:")
    print(f"  • Accuracy Report:     results/accuracy_report.json")
    print(f"  • Performance Report:  results/performance_report.json")
    print(f"  • HTML Summary:        results/summary_report.html")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
