#!/usr/bin/env python3
"""
Generate interactive dashboard showing all work items organized by sprint.
Creates both HTML and Markdown dashboards with charts and metrics.
"""

import os
import sys
import json
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict


class DashboardGenerator:
    def __init__(self, organization: str, project: str, pat: str):
        self.organization = organization
        self.project = project
        self.pat = pat
        self.base_url = f"https://dev.azure.com/{organization}/{project}/_apis"
        self.auth = HTTPBasicAuth('', pat)
        self.api_version = "7.0"
    
    def test_connection(self) -> bool:
        """Test connection to Azure DevOps."""
        url = f"https://dev.azure.com/{self.organization}/_apis/projects?api-version={self.api_version}"
        try:
            response = requests.get(url, auth=self.auth)
            if response.status_code == 200:
                print(f"✓ Connected to Azure DevOps")
                return True
            return False
        except:
            return False
    
    def get_all_work_items(self) -> List[Dict]:
        """Fetch all work items with their details."""
        print("📥 Fetching all work items...")
        
        url = f"{self.base_url}/wit/wiql?api-version={self.api_version}"
        query = {
            "query": """
                SELECT [System.Id]
                FROM WorkItems
                WHERE [System.TeamProject] = @project
                ORDER BY [System.Id]
            """
        }
        
        try:
            response = requests.post(url, json=query, auth=self.auth)
            response.raise_for_status()
            
            work_item_ids = [item['id'] for item in response.json().get('workItems', [])]
            print(f"✓ Found {len(work_item_ids)} work items")
            
            # Fetch details in batches
            work_items = []
            batch_size = 200
            
            for i in range(0, len(work_item_ids), batch_size):
                batch = work_item_ids[i:i+batch_size]
                ids = ','.join(map(str, batch))
                
                details_url = f"{self.base_url}/wit/workitems?ids={ids}&api-version={self.api_version}"
                details_response = requests.get(details_url, auth=self.auth)
                details_response.raise_for_status()
                
                work_items.extend(details_response.json().get('value', []))
            
            print(f"✓ Loaded {len(work_items)} work item details")
            return work_items
            
        except Exception as e:
            print(f"✗ Error fetching work items: {e}")
            return []
    
    def organize_by_sprint(self, work_items: List[Dict]) -> Dict[str, Dict]:
        """Organize work items by sprint."""
        print("📊 Organizing by sprint...")
        
        sprints = defaultdict(lambda: {
            'epics': [],
            'stories': [],
            'tasks': [],
            'total_story_points': 0
        })
        
        for item in work_items:
            fields = item['fields']
            work_type = fields.get('System.WorkItemType', '')
            iteration = fields.get('System.IterationPath', 'Unassigned')
            
            # Extract sprint name from iteration path
            sprint = iteration.split('\\')[-1] if '\\' in iteration else iteration
            
            item_data = {
                'id': item['id'],
                'title': fields.get('System.Title', ''),
                'state': fields.get('System.State', ''),
                'tags': fields.get('System.Tags', ''),
                'assigned_to': fields.get('System.AssignedTo', {}).get('displayName', 'Unassigned'),
                'story_points': fields.get('Microsoft.VSTS.Scheduling.StoryPoints', 0)
            }
            
            if work_type == 'Epic':
                sprints[sprint]['epics'].append(item_data)
            elif work_type == 'User Story':
                sprints[sprint]['stories'].append(item_data)
                sprints[sprint]['total_story_points'] += item_data['story_points'] or 0
            elif work_type == 'Task':
                sprints[sprint]['tasks'].append(item_data)
        
        print(f"✓ Organized into {len(sprints)} sprints")
        return dict(sprints)
    
    def calculate_metrics(self, sprint_data: Dict) -> Dict:
        """Calculate metrics for a sprint."""
        stories = sprint_data['stories']
        tasks = sprint_data['tasks']
        
        # Count by state
        story_states = defaultdict(int)
        task_states = defaultdict(int)
        
        for story in stories:
            story_states[story['state']] += 1
        
        for task in tasks:
            task_states[task['state']] += 1
        
        # Calculate completion percentage
        total_stories = len(stories)
        completed_stories = story_states.get('Closed', 0) + story_states.get('Done', 0)
        story_completion = (completed_stories / total_stories * 100) if total_stories > 0 else 0
        
        total_tasks = len(tasks)
        completed_tasks = task_states.get('Closed', 0) + task_states.get('Done', 0)
        task_completion = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            'total_epics': len(sprint_data['epics']),
            'total_stories': total_stories,
            'total_tasks': total_tasks,
            'total_story_points': sprint_data['total_story_points'],
            'story_completion': story_completion,
            'task_completion': task_completion,
            'story_states': dict(story_states),
            'task_states': dict(task_states)
        }
    
    def generate_html_dashboard(self, sprints: Dict[str, Dict], output_file: str):
        """Generate HTML dashboard with charts."""
        print("🎨 Generating HTML dashboard...")
        
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Odoo Microservices - Sprint Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            text-align: center;
        }
        h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #666;
            font-size: 1.1em;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            text-align: center;
        }
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label {
            color: #666;
            margin-top: 5px;
        }
        .sprint-section {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .sprint-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
        }
        .sprint-title {
            color: #667eea;
            font-size: 1.8em;
        }
        .sprint-badge {
            background: #667eea;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 25px;
        }
        .metric {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        .metric-value {
            font-size: 1.8em;
            font-weight: bold;
            color: #667eea;
        }
        .metric-label {
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }
        .progress-bar {
            background: #e9ecef;
            height: 30px;
            border-radius: 15px;
            overflow: hidden;
            margin: 15px 0;
        }
        .progress-fill {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            transition: width 0.3s ease;
        }
        .work-items-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .work-item-section {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
        }
        .work-item-section h4 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        .work-item {
            background: white;
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 6px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .work-item-id {
            color: #999;
            font-size: 0.9em;
        }
        .work-item-title {
            color: #333;
            margin: 5px 0;
        }
        .work-item-meta {
            display: flex;
            gap: 10px;
            margin-top: 8px;
            font-size: 0.85em;
        }
        .badge {
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.85em;
        }
        .badge-new { background: #e3f2fd; color: #1976d2; }
        .badge-active { background: #fff3e0; color: #f57c00; }
        .badge-done { background: #e8f5e9; color: #388e3c; }
        .badge-closed { background: #e8f5e9; color: #388e3c; }
        .chart-container {
            margin: 30px 0;
            max-height: 400px;
        }
        footer {
            text-align: center;
            color: white;
            margin-top: 30px;
            padding: 20px;
        }
        @media print {
            body { background: white; }
            .sprint-section { page-break-inside: avoid; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 Odoo Microservices Sprint Dashboard</h1>
            <p class="subtitle">Project Overview & Sprint Progress Tracking</p>
            <p style="color: #999; margin-top: 10px;">Generated: """ + datetime.now().strftime('%B %d, %Y at %H:%M') + """</p>
        </header>
"""
        
        # Calculate overall stats
        total_epics = sum(len(s['epics']) for s in sprints.values())
        total_stories = sum(len(s['stories']) for s in sprints.values())
        total_tasks = sum(len(s['tasks']) for s in sprints.values())
        total_points = sum(s['total_story_points'] for s in sprints.values())
        
        # Overall stats
        html += f"""
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{len(sprints)}</div>
                <div class="stat-label">Total Sprints</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{total_epics}</div>
                <div class="stat-label">Epics</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{total_stories}</div>
                <div class="stat-label">User Stories</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{total_tasks}</div>
                <div class="stat-label">Tasks</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{int(total_points)}</div>
                <div class="stat-label">Story Points</div>
            </div>
        </div>
"""
        
        # Sprint sections
        for sprint_name in sorted(sprints.keys()):
            if sprint_name == 'Unassigned':
                continue
                
            sprint_data = sprints[sprint_name]
            metrics = self.calculate_metrics(sprint_data)
            
            html += f"""
        <div class="sprint-section">
            <div class="sprint-header">
                <h2 class="sprint-title">{sprint_name}</h2>
                <span class="sprint-badge">{metrics['total_story_points']} Story Points</span>
            </div>
            
            <div class="metrics-grid">
                <div class="metric">
                    <div class="metric-value">{metrics['total_epics']}</div>
                    <div class="metric-label">Epics</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{metrics['total_stories']}</div>
                    <div class="metric-label">User Stories</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{metrics['total_tasks']}</div>
                    <div class="metric-label">Tasks</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{int(metrics['story_completion'])}%</div>
                    <div class="metric-label">Story Completion</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{int(metrics['task_completion'])}%</div>
                    <div class="metric-label">Task Completion</div>
                </div>
            </div>
            
            <div>
                <strong>Story Progress:</strong>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {metrics['story_completion']}%">
                        {int(metrics['story_completion'])}%
                    </div>
                </div>
            </div>
            
            <div>
                <strong>Task Progress:</strong>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {metrics['task_completion']}%">
                        {int(metrics['task_completion'])}%
                    </div>
                </div>
            </div>
            
            <div class="work-items-grid">
                <div class="work-item-section">
                    <h4>📋 Epics ({len(sprint_data['epics'])})</h4>
"""
            
            for epic in sprint_data['epics'][:10]:  # Show first 10
                state_class = epic['state'].lower().replace(' ', '-')
                html += f"""
                    <div class="work-item">
                        <span class="work-item-id">#{epic['id']}</span>
                        <div class="work-item-title">{epic['title']}</div>
                        <div class="work-item-meta">
                            <span class="badge badge-{state_class}">{epic['state']}</span>
                        </div>
                    </div>
"""
            
            if len(sprint_data['epics']) > 10:
                html += f"<p style='text-align: center; color: #999; margin-top: 10px;'>+ {len(sprint_data['epics']) - 10} more epics</p>"
            
            html += """
                </div>
                <div class="work-item-section">
                    <h4>📖 User Stories (""" + str(len(sprint_data['stories'])) + """)</h4>
"""
            
            for story in sprint_data['stories'][:10]:  # Show first 10
                state_class = story['state'].lower().replace(' ', '-')
                html += f"""
                    <div class="work-item">
                        <span class="work-item-id">#{story['id']}</span>
                        <div class="work-item-title">{story['title']}</div>
                        <div class="work-item-meta">
                            <span class="badge badge-{state_class}">{story['state']}</span>
                            {f"<span>SP: {int(story['story_points'])}</span>" if story['story_points'] else ""}
                        </div>
                    </div>
"""
            
            if len(sprint_data['stories']) > 10:
                html += f"<p style='text-align: center; color: #999; margin-top: 10px;'>+ {len(sprint_data['stories']) - 10} more stories</p>"
            
            html += """
                </div>
                <div class="work-item-section">
                    <h4>✅ Tasks (""" + str(len(sprint_data['tasks'])) + """)</h4>
"""
            
            for task in sprint_data['tasks'][:10]:  # Show first 10
                state_class = task['state'].lower().replace(' ', '-')
                html += f"""
                    <div class="work-item">
                        <span class="work-item-id">#{task['id']}</span>
                        <div class="work-item-title">{task['title']}</div>
                        <div class="work-item-meta">
                            <span class="badge badge-{state_class}">{task['state']}</span>
                        </div>
                    </div>
"""
            
            if len(sprint_data['tasks']) > 10:
                html += f"<p style='text-align: center; color: #999; margin-top: 10px;'>+ {len(sprint_data['tasks']) - 10} more tasks</p>"
            
            html += """
                </div>
            </div>
        </div>
"""
        
        html += """
        <footer>
            <p>🚀 Odoo 19 Microservices Project | Azure DevOps Dashboard</p>
            <p style="margin-top: 10px; font-size: 0.9em;">
                <a href="https://dev.azure.com/Aries-Test/Odoo-Microservices" style="color: white;">View in Azure DevOps</a>
            </p>
        </footer>
    </div>
</body>
</html>
"""
        
        with open(output_file, 'w') as f:
            f.write(html)
        
        print(f"✓ HTML dashboard saved to: {output_file}")
    
    def generate_markdown_dashboard(self, sprints: Dict[str, Dict], output_file: str):
        """Generate Markdown dashboard."""
        print("📝 Generating Markdown dashboard...")
        
        md = f"""# 🚀 Odoo Microservices Sprint Dashboard

**Generated**: {datetime.now().strftime('%B %d, %Y at %H:%M')}

---

## 📊 Project Overview

"""
        
        # Calculate overall stats
        total_epics = sum(len(s['epics']) for s in sprints.values())
        total_stories = sum(len(s['stories']) for s in sprints.values())
        total_tasks = sum(len(s['tasks']) for s in sprints.values())
        total_points = sum(s['total_story_points'] for s in sprints.values())
        
        md += f"""| Metric | Count |
|--------|-------|
| **Total Sprints** | {len([s for s in sprints.keys() if s != 'Unassigned'])} |
| **Total Epics** | {total_epics} |
| **Total User Stories** | {total_stories} |
| **Total Tasks** | {total_tasks} |
| **Total Story Points** | {int(total_points)} |

---

"""
        
        # Sprint sections
        for sprint_name in sorted(sprints.keys()):
            if sprint_name == 'Unassigned':
                continue
            
            sprint_data = sprints[sprint_name]
            metrics = self.calculate_metrics(sprint_data)
            
            md += f"""## {sprint_name}

**Story Points**: {int(metrics['total_story_points'])}

### Metrics

| Metric | Value |
|--------|-------|
| Epics | {metrics['total_epics']} |
| User Stories | {metrics['total_stories']} |
| Tasks | {metrics['total_tasks']} |
| Story Completion | {int(metrics['story_completion'])}% |
| Task Completion | {int(metrics['task_completion'])}% |

### Progress

**Stories**: {int(metrics['story_completion'])}% Complete
```
{"█" * int(metrics['story_completion'] / 5)}{"░" * (20 - int(metrics['story_completion'] / 5))}
```

**Tasks**: {int(metrics['task_completion'])}% Complete
```
{"█" * int(metrics['task_completion'] / 5)}{"░" * (20 - int(metrics['task_completion'] / 5))}
```

### Epics ({len(sprint_data['epics'])})

"""
            
            for epic in sprint_data['epics']:
                md += f"- [#{epic['id']}] **{epic['title']}** - {epic['state']}\n"
            
            md += f"\n### User Stories ({len(sprint_data['stories'])})\n\n"
            
            for story in sprint_data['stories'][:20]:  # Show first 20
                points = f" ({int(story['story_points'])} SP)" if story['story_points'] else ""
                md += f"- [#{story['id']}] **{story['title']}** - {story['state']}{points}\n"
            
            if len(sprint_data['stories']) > 20:
                md += f"\n*... and {len(sprint_data['stories']) - 20} more user stories*\n"
            
            md += f"\n### Tasks Summary\n\n"
            md += f"**Total Tasks**: {len(sprint_data['tasks'])}\n\n"
            
            # Task state breakdown
            if metrics['task_states']:
                md += "**Task States**:\n"
                for state, count in sorted(metrics['task_states'].items()):
                    md += f"- {state}: {count}\n"
            
            md += "\n---\n\n"
        
        md += """## 🔗 Quick Links

- **Azure DevOps Project**: [Odoo-Microservices](https://dev.azure.com/Aries-Test/Odoo-Microservices)
- **Boards**: [View Boards](https://dev.azure.com/Aries-Test/Odoo-Microservices/_boards)
- **Backlogs**: [View Backlogs](https://dev.azure.com/Aries-Test/Odoo-Microservices/_backlogs)

---

*Dashboard generated by Azure DevOps Dashboard Generator*
"""
        
        with open(output_file, 'w') as f:
            f.write(md)
        
        print(f"✓ Markdown dashboard saved to: {output_file}")


def main():
    print("="*70)
    print("📊 Azure DevOps Dashboard Generator")
    print("="*70)
    
    # Load environment variables
    org = os.getenv('AZURE_DEVOPS_ORG')
    project = os.getenv('AZURE_DEVOPS_PROJECT')
    pat = os.getenv('AZURE_DEVOPS_PAT')
    
    if not all([org, project, pat]):
        print("\n❌ Missing required environment variables")
        print("Make sure to source .env file:")
        print("  source azure-devops-setup/.env")
        sys.exit(1)
    
    generator = DashboardGenerator(org, project, pat)
    
    # Test connection
    if not generator.test_connection():
        print("❌ Failed to connect to Azure DevOps")
        sys.exit(1)
    
    # Get all work items
    work_items = generator.get_all_work_items()
    if not work_items:
        print("❌ No work items found")
        sys.exit(1)
    
    # Organize by sprint
    sprints = generator.organize_by_sprint(work_items)
    
    # Generate dashboards
    html_file = "sprint-dashboard.html"
    md_file = "sprint-dashboard.md"
    
    generator.generate_html_dashboard(sprints, html_file)
    generator.generate_markdown_dashboard(sprints, md_file)
    
    print("\n" + "="*70)
    print("✅ Dashboards generated successfully!")
    print("="*70)
    print(f"\n📄 Files created:")
    print(f"  - {html_file} (Open in browser)")
    print(f"  - {md_file} (View in editor)")
    print()


if __name__ == "__main__":
    main()
