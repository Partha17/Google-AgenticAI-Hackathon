"""
Google Charts Integration for Enhanced Financial Dashboard
Advanced visualizations using Google Charts API
"""

import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import plotly.graph_objects as go
import plotly.express as px

from config import settings

class GoogleChartsIntegration:
    """Google Charts integration for advanced financial visualizations"""
    
    def __init__(self):
        self.charts_api_key = settings.google_charts_api_key
        self.real_time_enabled = settings.google_charts_enable_real_time
    
    def create_portfolio_treemap(self, portfolio_data: Dict[str, Any]) -> str:
        """Create interactive portfolio treemap using Google Charts"""
        
        # Prepare data for treemap
        treemap_data = []
        if 'holdings' in portfolio_data:
            for holding in portfolio_data['holdings']:
                treemap_data.append([
                    holding.get('name', 'Unknown'),
                    holding.get('sector', 'Other'),
                    holding.get('value', 0),
                    holding.get('change_percent', 0)
                ])
        
        chart_html = f"""
        <html>
        <head>
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <script type="text/javascript">
                google.charts.load('current', {{'packages':['treemap']}});
                google.charts.setOnLoadCallback(drawChart);
                
                function drawChart() {{
                    var data = google.visualization.arrayToDataTable([
                        ['Asset', 'Sector', 'Value', 'Change %'],
                        {json.dumps(treemap_data)[1:-1]}
                    ]);
                    
                    var options = {{
                        title: 'Portfolio Allocation Treemap',
                        minColor: '#ff4444',
                        midColor: '#ffff44',
                        maxColor: '#44ff44',
                        headerHeight: 15,
                        fontColor: 'black',
                        showScale: true,
                        generateTooltip: showFullTooltip
                    }};
                    
                    var tree = new google.visualization.TreeMap(document.getElementById('treemap_div'));
                    tree.draw(data, options);
                }}
                
                function showFullTooltip(row, size, value) {{
                    return '<div style="background:#fd9; padding:10px; border-style:solid">' +
                           '<span style="font-family:Courier">' + data.getValue(row, 0) + 
                           '</span><br/>' + 'Value: $' + size.toLocaleString() + 
                           '<br/>Change: ' + value.toFixed(2) + '%</div>';
                }}
            </script>
        </head>
        <body>
            <div id="treemap_div" style="width: 100%; height: 400px;"></div>
        </body>
        </html>
        """
        
        return chart_html
    
    def create_risk_gauge_chart(self, risk_score: float, risk_level: str) -> str:
        """Create risk assessment gauge chart"""
        
        chart_html = f"""
        <html>
        <head>
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <script type="text/javascript">
                google.charts.load('current', {{'packages':['gauge']}});
                google.charts.setOnLoadCallback(drawChart);
                
                function drawChart() {{
                    var data = google.visualization.arrayToDataTable([
                        ['Label', 'Value'],
                        ['Risk Score', {risk_score}]
                    ]);
                    
                    var options = {{
                        width: 400, height: 300,
                        redFrom: 75, redTo: 100,
                        yellowFrom: 50, yellowTo: 75,
                        greenFrom: 0, greenTo: 50,
                        minorTicks: 5,
                        max: 100
                    }};
                    
                    var chart = new google.visualization.Gauge(document.getElementById('gauge_div'));
                    chart.draw(data, options);
                    
                    // Real-time updates if enabled
                    {self._get_realtime_update_script() if self.real_time_enabled else ""}
                }}
            </script>
        </head>
        <body>
            <div id="gauge_div" style="width: 100%; height: 300px;"></div>
            <div style="text-align: center; margin-top: 10px;">
                <strong>Risk Level: {risk_level}</strong>
            </div>
        </body>
        </html>
        """
        
        return chart_html
    
    def create_performance_timeline(self, performance_data: List[Dict[str, Any]]) -> str:
        """Create interactive performance timeline chart"""
        
        # Prepare timeline data
        timeline_data = []
        for point in performance_data:
            timeline_data.append([
                f"new Date('{point.get('date', datetime.now().isoformat())}')",
                point.get('portfolio_value', 0),
                point.get('benchmark_value', 0)
            ])
        
        chart_html = f"""
        <html>
        <head>
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <script type="text/javascript">
                google.charts.load('current', {{'packages':['line']}});
                google.charts.setOnLoadCallback(drawChart);
                
                function drawChart() {{
                    var data = new google.visualization.DataTable();
                    data.addColumn('date', 'Date');
                    data.addColumn('number', 'Portfolio Value');
                    data.addColumn('number', 'Benchmark');
                    
                    data.addRows([
                        {str(timeline_data).replace("'new Date(", "new Date(").replace(")'", ")")}
                    ]);
                    
                    var options = {{
                        chart: {{
                            title: 'Portfolio Performance vs Benchmark',
                            subtitle: 'Track your investment performance over time'
                        }},
                        width: '100%',
                        height: 400,
                        series: {{
                            0: {{color: '#1f77b4', lineWidth: 3}},
                            1: {{color: '#ff7f0e', lineWidth: 2, lineDashStyle: [10, 2]}}
                        }},
                        vAxis: {{
                            format: 'currency'
                        }},
                        hAxis: {{
                            format: 'MMM yyyy'
                        }}
                    }};
                    
                    var chart = new google.charts.Line(document.getElementById('timeline_div'));
                    chart.draw(data, google.charts.Line.convertOptions(options));
                }}
            </script>
        </head>
        <body>
            <div id="timeline_div" style="width: 100%; height: 400px;"></div>
        </body>
        </html>
        """
        
        return chart_html
    
    def create_sector_allocation_pie(self, sector_data: Dict[str, float]) -> str:
        """Create interactive sector allocation pie chart"""
        
        pie_data = [[sector, value] for sector, value in sector_data.items()]
        
        chart_html = f"""
        <html>
        <head>
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <script type="text/javascript">
                google.charts.load('current', {{'packages':['corechart']}});
                google.charts.setOnLoadCallback(drawChart);
                
                function drawChart() {{
                    var data = google.visualization.arrayToDataTable([
                        ['Sector', 'Allocation %'],
                        {json.dumps(pie_data)[1:-1]}
                    ]);
                    
                    var options = {{
                        title: 'Sector Allocation',
                        titleTextStyle: {{fontSize: 18, bold: true}},
                        pieHole: 0.4,
                        colors: ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                                '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'],
                        chartArea: {{width: '90%', height: '80%'}},
                        legend: {{position: 'right', textStyle: {{fontSize: 12}}}},
                        pieSliceText: 'percentage',
                        sliceVisibilityThreshold: 0.02,
                        tooltip: {{
                            showColorCode: true,
                            trigger: 'both'
                        }}
                    }};
                    
                    var chart = new google.visualization.PieChart(document.getElementById('pie_div'));
                    chart.draw(data, options);
                    
                    // Add click handler for drill-down
                    google.visualization.events.addListener(chart, 'select', function() {{
                        var selectedItem = chart.getSelection()[0];
                        if (selectedItem) {{
                            var sector = data.getValue(selectedItem.row, 0);
                            alert('Selected sector: ' + sector + '\\nClick for detailed analysis');
                        }}
                    }});
                }}
            </script>
        </head>
        <body>
            <div id="pie_div" style="width: 100%; height: 400px;"></div>
        </body>
        </html>
        """
        
        return chart_html
    
    def create_correlation_heatmap(self, correlation_matrix: Dict[str, Dict[str, float]]) -> str:
        """Create correlation heatmap using Google Charts"""
        
        assets = list(correlation_matrix.keys())
        heatmap_data = [[''] + assets]
        
        for asset1 in assets:
            row = [asset1]
            for asset2 in assets:
                correlation = correlation_matrix.get(asset1, {}).get(asset2, 0)
                row.append(correlation)
            heatmap_data.append(row)
        
        chart_html = f"""
        <html>
        <head>
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <script type="text/javascript">
                google.charts.load('current', {{'packages':['table']}});
                google.charts.setOnLoadCallback(drawChart);
                
                function drawChart() {{
                    var data = google.visualization.arrayToDataTable({json.dumps(heatmap_data)});
                    
                    var options = {{
                        title: 'Asset Correlation Matrix',
                        width: '100%',
                        height: 400,
                        allowHtml: true,
                        cssClassNames: {{
                            'headerRow': 'header-row',
                            'tableRow': 'table-row',
                            'oddTableRow': 'odd-row'
                        }}
                    }};
                    
                    var table = new google.visualization.Table(document.getElementById('heatmap_div'));
                    table.draw(data, options);
                }}
            </script>
            <style>
                .header-row {{
                    background-color: #4285f4;
                    color: white;
                    font-weight: bold;
                }}
                .table-row {{
                    background-color: #f9f9f9;
                }}
                .odd-row {{
                    background-color: #ffffff;
                }}
                .google-visualization-table-table td {{
                    text-align: center;
                    padding: 8px;
                }}
            </style>
        </head>
        <body>
            <div id="heatmap_div" style="width: 100%; height: 400px;"></div>
        </body>
        </html>
        """
        
        return chart_html
    
    def create_real_time_metrics_dashboard(self, metrics: List[Dict[str, Any]]) -> str:
        """Create real-time metrics dashboard"""
        
        # Prepare metrics data
        metrics_data = []
        for metric in metrics:
            metrics_data.append([
                metric.get('name', 'Unknown'),
                metric.get('current_value', 0),
                metric.get('target_value', 0),
                metric.get('status', 'normal')
            ])
        
        chart_html = f"""
        <html>
        <head>
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <script type="text/javascript">
                google.charts.load('current', {{'packages':['table', 'gauge']}});
                google.charts.setOnLoadCallback(drawCharts);
                
                var metricsData = {json.dumps(metrics_data)};
                
                function drawCharts() {{
                    drawMetricsTable();
                    drawMetricsGauges();
                    
                    // Set up real-time updates
                    {self._get_realtime_update_script() if self.real_time_enabled else ""}
                }}
                
                function drawMetricsTable() {{
                    var data = google.visualization.arrayToDataTable([
                        ['Metric', 'Current', 'Target', 'Status'],
                        ...metricsData
                    ]);
                    
                    var options = {{
                        title: 'Real-time Financial Metrics',
                        width: '100%',
                        height: 300,
                        allowHtml: true
                    }};
                    
                    var table = new google.visualization.Table(document.getElementById('metrics_table'));
                    table.draw(data, options);
                }}
                
                function drawMetricsGauges() {{
                    for (let i = 0; i < metricsData.length && i < 4; i++) {{
                        var data = google.visualization.arrayToDataTable([
                            ['Label', 'Value'],
                            [metricsData[i][0], metricsData[i][1]]
                        ]);
                        
                        var options = {{
                            width: 200, height: 200,
                            redFrom: 80, redTo: 100,
                            yellowFrom: 60, yellowTo: 80,
                            greenFrom: 0, greenTo: 60,
                            minorTicks: 5,
                            max: 100
                        }};
                        
                        var chart = new google.visualization.Gauge(document.getElementById('gauge_' + i));
                        chart.draw(data, options);
                    }}
                }}
                
                // Update function for real-time data
                function updateMetrics(newData) {{
                    metricsData = newData;
                    drawCharts();
                }}
            </script>
        </head>
        <body>
            <div style="display: flex; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 300px;">
                    <div id="metrics_table"></div>
                </div>
                <div style="flex: 1; min-width: 400px;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <div id="gauge_0"></div>
                        <div id="gauge_1"></div>
                        <div id="gauge_2"></div>
                        <div id="gauge_3"></div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        return chart_html
    
    def create_market_overview_chart(self, market_data: Dict[str, Any]) -> str:
        """Create comprehensive market overview chart"""
        
        # Prepare market indices data
        indices_data = []
        if 'indices' in market_data:
            for index in market_data['indices']:
                indices_data.append([
                    index.get('name', 'Unknown'),
                    index.get('value', 0),
                    index.get('change', 0),
                    index.get('change_percent', 0)
                ])
        
        chart_html = f"""
        <html>
        <head>
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <script type="text/javascript">
                google.charts.load('current', {{'packages':['corechart', 'bar']}});
                google.charts.setOnLoadCallback(drawCharts);
                
                function drawCharts() {{
                    drawIndicesChart();
                    drawVolatilityChart();
                }}
                
                function drawIndicesChart() {{
                    var data = google.visualization.arrayToDataTable([
                        ['Index', 'Value', 'Change', 'Change %'],
                        {json.dumps(indices_data)[1:-1]}
                    ]);
                    
                    var options = {{
                        title: 'Market Indices Overview',
                        titleTextStyle: {{fontSize: 16, bold: true}},
                        chartArea: {{width: '80%', height: '70%'}},
                        colors: ['#1f77b4', '#ff7f0e'],
                        vAxis: {{
                            title: 'Index Value',
                            format: 'short'
                        }},
                        hAxis: {{
                            title: 'Market Indices'
                        }},
                        legend: {{position: 'top', maxLines: 3}},
                        bar: {{groupWidth: '75%'}},
                        isStacked: false
                    }};
                    
                    var chart = new google.visualization.ColumnChart(document.getElementById('indices_div'));
                    chart.draw(data, options);
                }}
                
                function drawVolatilityChart() {{
                    var volatilityData = google.visualization.arrayToDataTable([
                        ['Asset Class', 'Volatility %'],
                        ['Stocks', 15.2],
                        ['Bonds', 4.8],
                        ['Commodities', 22.1],
                        ['REITs', 18.6],
                        ['Crypto', 45.3]
                    ]);
                    
                    var options = {{
                        title: 'Asset Class Volatility',
                        chartArea: {{width: '80%', height: '70%'}},
                        colors: ['#ff4444', '#ffaa44', '#44ff44', '#4444ff', '#ff44ff'],
                        vAxis: {{
                            title: 'Volatility (%)',
                            minValue: 0
                        }},
                        hAxis: {{
                            title: 'Asset Classes'
                        }}
                    }};
                    
                    var chart = new google.visualization.ColumnChart(document.getElementById('volatility_div'));
                    chart.draw(data, options);
                }}
            </script>
        </head>
        <body>
            <div style="display: flex; flex-direction: column;">
                <div id="indices_div" style="width: 100%; height: 300px;"></div>
                <div id="volatility_div" style="width: 100%; height: 300px; margin-top: 20px;"></div>
            </div>
        </body>
        </html>
        """
        
        return chart_html
    
    def _get_realtime_update_script(self) -> str:
        """Generate real-time update JavaScript"""
        if not self.real_time_enabled:
            return ""
        
        return """
        setInterval(function() {
            // Simulate real-time data updates
            // In production, this would connect to your real-time data stream
            var randomFactor = 0.95 + Math.random() * 0.1; // ±5% variation
            
            // Update gauge values
            var currentValue = data.getValue(0, 1);
            var newValue = Math.round(currentValue * randomFactor);
            data.setValue(0, 1, newValue);
            
            // Redraw chart
            chart.draw(data, options);
        }, 5000); // Update every 5 seconds
        """
    
    # === Streamlit Integration Methods ===
    
    def render_in_streamlit(self, chart_html: str, height: int = 400):
        """Render Google Chart in Streamlit"""
        st.components.v1.html(chart_html, height=height, scrolling=True)
    
    def create_advanced_analytics_suite(self, financial_data: Dict[str, Any]) -> Dict[str, str]:
        """Create a complete suite of advanced analytics charts"""
        
        charts = {}
        
        # Portfolio treemap
        if 'portfolio' in financial_data:
            charts['portfolio_treemap'] = self.create_portfolio_treemap(financial_data['portfolio'])
        
        # Risk gauge
        if 'risk_assessment' in financial_data:
            risk_data = financial_data['risk_assessment']
            charts['risk_gauge'] = self.create_risk_gauge_chart(
                risk_data.get('risk_score', 50),
                risk_data.get('risk_level', 'Medium')
            )
        
        # Performance timeline
        if 'performance_history' in financial_data:
            charts['performance_timeline'] = self.create_performance_timeline(financial_data['performance_history'])
        
        # Sector allocation
        if 'sector_allocation' in financial_data:
            charts['sector_pie'] = self.create_sector_allocation_pie(financial_data['sector_allocation'])
        
        # Correlation matrix
        if 'correlation_matrix' in financial_data:
            charts['correlation_heatmap'] = self.create_correlation_heatmap(financial_data['correlation_matrix'])
        
        # Real-time metrics
        if 'metrics' in financial_data:
            charts['metrics_dashboard'] = self.create_real_time_metrics_dashboard(financial_data['metrics'])
        
        # Market overview
        if 'market_data' in financial_data:
            charts['market_overview'] = self.create_market_overview_chart(financial_data['market_data'])
        
        return charts

# Global instance
google_charts = GoogleChartsIntegration() 