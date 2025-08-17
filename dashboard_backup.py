#!/usr/bin/env python3
"""
Interactive Dashboard for Obsidian Vault Analysis
"""

import json
import panel as pn
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pyvis.network import Network
from datetime import datetime
import tempfile
import os

pn.extension('plotly', 'tabulator')


class ObsidianDashboard:
    """Interactive dashboard for vault analysis"""
    
    def __init__(self, data_file: str = "vault_analysis.json"):
        # Load analysis data
        with open(data_file, 'r') as f:
            self.data = json.load(f)
        
        # Initialize Panel
        self.template = pn.template.MaterialTemplate(
            title="Obsidian Vault Analyzer",
            sidebar=[self.create_sidebar()],
        )
        
        # Create main content
        self.template.main.append(
            pn.Tabs(
                ("Overview", self.create_overview_tab()),
                ("Timeline", self.create_timeline_tab()),
                ("Important Notes", self.create_important_notes_tab()),
                ("Orphaned Notes", self.create_orphaned_notes_tab()),
                ("Hashtags", self.create_hashtag_tab()),
                ("Network Graph", self.create_network_tab()),
                ("Analysis", self.create_analysis_tab())
            )
        )
    
    def create_sidebar(self):
        """Create sidebar with vault statistics"""
        stats = self.data["stats"]
        
        stats_html = f"""
        <h3>Vault Statistics</h3>
        <ul style="list-style-type: none; padding: 0;">
            <li>📝 <b>Total Notes:</b> {stats['total_notes']}</li>
            <li>📄 <b>Markdown:</b> {stats['markdown_count']}</li>
            <li>🎨 <b>Excalidraw:</b> {stats['excalidraw_count']}</li>
            <li>🔗 <b>Connections:</b> {stats['graph_edges']}</li>
            <li>🏝️ <b>Orphaned:</b> {stats['orphaned_count']}</li>
        </ul>
        """
        
        return pn.pane.HTML(stats_html, width=250)
    
    def create_overview_tab(self):
        """Create overview tab with key metrics"""
        stats = self.data["stats"]
        
        # Create metric cards
        metrics = pn.Row(
            pn.indicators.Number(
                value=stats['total_notes'],
                name='Total Notes',
                format='{value:,}',
                font_size='24pt',
                title_size='14pt'
            ),
            pn.indicators.Number(
                value=stats['graph_edges'],
                name='Connections',
                format='{value:,}',
                font_size='24pt',
                title_size='14pt'
            ),
            pn.indicators.Number(
                value=stats['orphaned_count'],
                name='Orphaned Notes',
                format='{value:,}',
                font_size='24pt',
                title_size='14pt'
            )
        )
        
        # File type distribution
        file_types = pd.DataFrame([
            {'Type': 'Markdown', 'Count': stats['markdown_count']},
            {'Type': 'Excalidraw', 'Count': stats['excalidraw_count']}
        ])
        
        pie_chart = px.pie(
            file_types, 
            values='Count', 
            names='Type',
            title='File Type Distribution'
        )
        
        # Recent activity - show more notes
        recent_df = pd.DataFrame(self.data['timeline']['modified'][-50:])  # Show last 50 notes
        recent_df['modified'] = pd.to_datetime(recent_df['modified'], format='mixed')
        recent_df = recent_df.sort_values('modified', ascending=False)  # Most recent first
        
        # Format the table with more columns and full height
        display_df = recent_df[['path', 'modified', 'type', 'importance_score']].copy()
        display_df['modified'] = display_df['modified'].dt.strftime('%Y-%m-%d %H:%M')
        
        recent_table = pn.widgets.Tabulator(
            display_df,
            pagination='local',
            page_size=25,  # Show 25 rows per page
            sizing_mode='stretch_both',  # Stretch both width and height
            height=800,  # Much taller to use full dashboard height
            name='Recently Modified Notes',
            formatters={
                'path': {'type': 'link', 'urlPrefix': 'obsidian://open?path='},
                'importance_score': {'type': 'progress', 'max': 50}
            },
            sorters=[{'field': 'modified', 'dir': 'desc'}]
        )
        
        return pn.Column(
            "# Vault Overview",
            metrics,
            pn.Row(
                pn.Column(
                    pn.pane.Plotly(pie_chart, height=350),
                    width=400,
                    sizing_mode='fixed'
                ),
                recent_table,
                sizing_mode='stretch_both'
            ),
            sizing_mode='stretch_both'
        )
    
    def create_timeline_tab(self):
        """Create timeline visualizations"""
        # Prepare data
        created_df = pd.DataFrame(self.data['timeline']['created'])
        created_df['created'] = pd.to_datetime(created_df['created'], format='mixed')
        
        modified_df = pd.DataFrame(self.data['timeline']['modified'])
        modified_df['modified'] = pd.to_datetime(modified_df['modified'], format='mixed')
        
        # Creation timeline
        creation_fig = px.scatter(
            created_df,
            x='created',
            y='importance_score',
            hover_data=['path', 'type'],
            color='type',
            title='Note Creation Timeline',
            labels={'created': 'Creation Date', 'importance_score': 'Importance Score'}
        )
        
        # Modification timeline with histogram
        mod_hist = px.histogram(
            modified_df,
            x='modified',
            nbins=50,
            title='Modification Activity Over Time'
        )
        
        # Activity heatmap (by day of week and hour)
        modified_df['hour'] = modified_df['modified'].dt.hour
        modified_df['day_of_week'] = modified_df['modified'].dt.day_name()
        
        activity_pivot = modified_df.pivot_table(
            index='hour',
            columns='day_of_week',
            values='path',
            aggfunc='count',
            fill_value=0
        )
        
        heatmap = px.imshow(
            activity_pivot,
            labels=dict(x="Day of Week", y="Hour of Day", color="Notes Modified"),
            title="Activity Heatmap",
            aspect="auto"
        )
        
        return pn.Column(
            "# Timeline Analysis",
            pn.pane.Plotly(creation_fig, height=400),
            pn.pane.Plotly(mod_hist, height=300),
            pn.pane.Plotly(heatmap, height=400)
        )
    
    def create_important_notes_tab(self):
        """Create tab for important notes"""
        important_df = pd.DataFrame(self.data['important_notes'])
        
        # Prepare display columns
        display_df = important_df[[
            'path', 'importance_score', 'in_degree', 'out_degree', 
            'word_count', 'modified', 'type'
        ]].copy()
        
        display_df['modified'] = pd.to_datetime(display_df['modified'], format='mixed').dt.strftime('%Y-%m-%d')
        display_df['importance_score'] = display_df['importance_score'].round(2)
        
        # Create interactive table
        table = pn.widgets.Tabulator(
            display_df,
            pagination='local',
            page_size=20,
            sizing_mode='stretch_width',
            height=600,
            sorters=[{'field': 'importance_score', 'dir': 'desc'}],
            formatters={
                'importance_score': {'type': 'progress', 'max': display_df['importance_score'].max()},
                'path': {'type': 'link', 'urlPrefix': 'obsidian://open?path='}
            }
        )
        
        # Importance factors breakdown
        factors_fig = go.Figure()
        
        for _, note in important_df.head(10).iterrows():
            factors_fig.add_trace(go.Bar(
                name=note['path'].split('/')[-1][:20] + '...',
                x=['PageRank', 'In Links', 'Out Links', 'Content'],
                y=[
                    note['pagerank'] * 30,  # Scaled to match importance calculation
                    note['in_degree'] * 0.25,
                    note['out_degree'] * 0.25,
                    min(note['word_count'] / 1000 + len(note.get('images', [])) * 0.5, 10) * 0.15
                ]
            ))
        
        factors_fig.update_layout(
            title="Importance Score Breakdown (Top 10 Notes)",
            barmode='group',
            height=400
        )
        
        return pn.Column(
            "# Important Notes",
            "Notes ranked by their importance score (links, content, and network position)",
            table,
            pn.pane.Plotly(factors_fig)
        )
    
    def create_orphaned_notes_tab(self):
        """Create tab for orphaned notes"""
        orphaned_df = pd.DataFrame(self.data['orphaned_notes'])
        
        if len(orphaned_df) > 0:
            # Prepare display
            display_df = orphaned_df[['path', 'modified', 'word_count', 'type']].copy()
            display_df['modified'] = pd.to_datetime(display_df['modified'], format='mixed').dt.strftime('%Y-%m-%d')
            
            table = pn.widgets.Tabulator(
                display_df,
                pagination='local',
                page_size=20,
                sizing_mode='stretch_width',
                height=500,
                formatters={
                    'path': {'type': 'link', 'urlPrefix': 'obsidian://open?path='}
                }
            )
            
            # Orphan statistics
            orphan_stats = f"""
            <div style="background-color: #f0f0f0; padding: 20px; border-radius: 5px;">
                <h3>Orphaned Notes Analysis</h3>
                <p><b>Total Orphaned Notes:</b> {len(orphaned_df)}</p>
                <p><b>Percentage of Vault:</b> {len(orphaned_df) / self.data['stats']['total_notes'] * 100:.1f}%</p>
                <p><b>Total Word Count:</b> {orphaned_df['word_count'].sum():,}</p>
                <p><i>Orphaned notes have no incoming or outgoing links.</i></p>
            </div>
            """
            
            content = pn.Column(
                pn.pane.HTML(orphan_stats),
                table
            )
        else:
            content = pn.pane.Alert(
                "No orphaned notes found! All notes are connected.",
                alert_type="success"
            )
        
        return pn.Column(
            "# Orphaned Notes",
            content
        )
    
    def create_hashtag_tab(self):
        """Create hashtag browsing tab"""
        # Get hashtag data
        hashtags_data = self.data.get('hashtags', [])
        notes_metadata = self.data.get('notes_metadata', {})
        
        # Create hashtag selector with fuzzy search
        hashtag_options = [h['hashtag'] for h in hashtags_data]
        hashtag_selector = pn.widgets.AutocompleteInput(
            name='Search Hashtags',
            options=hashtag_options,
            placeholder='Type to search hashtags...',
            case_sensitive=False,
            min_characters=1,
            value=hashtag_options[0] if hashtag_options else None
        )
        
        # Create row count selector
        row_count_selector = pn.widgets.Select(
            name='Rows per page:',
            value=10,
            options=[10, 20, 50, 100],
            width=150
        )
        
        # Extract top-level folders from notes metadata
        top_folders = set()
        for metadata in notes_metadata.values():
            path = metadata.get('path', '')
            if path and '/' in path:
                top_folder = path.split('/')[0]
                top_folders.add(top_folder)
        
        # Sort folders, prioritizing numbered folders
        sorted_folders = sorted(top_folders, key=lambda x: (not x[0].isdigit(), x))
        
        # Create folder filter checkboxes
        folder_filter = pn.widgets.CheckBoxGroup(
            name='Include folders:',
            value=sorted_folders,  # All folders included by default
            options=sorted_folders,
            inline=False,
            width=200
        )
        
        # Create notes table
        notes_table = pn.widgets.Tabulator(
            pd.DataFrame(),
            pagination='local',
            page_size=10,  # Start with 10 rows
            sizing_mode='stretch_width',
            height=400,  # Reduced height to make room for AI summary
            formatters={
                'path': {'type': 'link', 'urlPrefix': 'obsidian://open?path='}
            },
            selectable=1  # Enable single row selection
        )
        
        # Hashtag statistics
        hashtag_stats = pn.pane.HTML("")
        
        # AI Summary panel
        ai_summary_panel = pn.pane.HTML(
            "<div style='background-color: #f9f9f9; padding: 20px; border-radius: 5px; min-height: 150px;'>"
            "<h4>AI Summary</h4>"
            "<p style='color: #666;'>Select a note to view its AI summary</p>"
            "</div>",
            sizing_mode='stretch_width'
        )
        
        # Store filtered notes metadata for AI summary lookup
        current_notes_metadata = {}
        
        def update_notes(event=None):
            """Update notes table when hashtag is selected or filters change"""
            selected_hashtag = hashtag_selector.value
            if not selected_hashtag or selected_hashtag not in hashtag_options:
                return
            
            # Get included folders
            included_folders = folder_filter.value
            
            # Clear current metadata
            current_notes_metadata.clear()
            
            # Filter notes by hashtag and folder inclusions
            filtered_notes = []
            for note_id, metadata in notes_metadata.items():
                if selected_hashtag in metadata.get('auto_hashtags', []):
                    # Check if note is in an included folder
                    path = metadata.get('path', '')
                    if path and '/' in path:
                        top_folder = path.split('/')[0]
                        if top_folder not in included_folders:
                            continue  # Skip this note
                    elif not path or '/' not in path:
                        # Skip notes without proper path structure
                        continue
                    
                    # Store full metadata for AI summary lookup
                    current_notes_metadata[metadata.get('path', '')] = metadata
                    
                    filtered_notes.append({
                        'path': metadata.get('path', ''),
                        'type': metadata.get('type', ''),
                        'importance_score': metadata.get('importance_score', 0),
                        'word_count': metadata.get('word_count', 0),
                        'modified': pd.to_datetime(metadata.get('modified', ''), format='mixed').strftime('%Y-%m-%d') if metadata.get('modified') else '',
                        'keywords': ', '.join(metadata.get('keywords', [])[:5])  # Show first 5 keywords
                    })
            
            if filtered_notes:
                df = pd.DataFrame(filtered_notes)
                df = df.sort_values('importance_score', ascending=False)
                notes_table.value = df
                
                # Update statistics
                hashtag_count = next((h['count'] for h in hashtags_data if h['hashtag'] == selected_hashtag), 0)
                filtered_count = len(df)
                stats_html = f"""
                <div style="background-color: #f0f0f0; padding: 20px; border-radius: 5px; margin-bottom: 20px;">
                    <h3>{selected_hashtag}</h3>
                    <p><b>Total Notes:</b> {hashtag_count}</p>
                    <p><b>Displayed Notes:</b> {filtered_count} {f'(filtered from {hashtag_count})' if filtered_count < hashtag_count else ''}</p>
                    <p><b>Average Importance:</b> {df['importance_score'].mean():.2f}</p>
                    <p><b>Total Word Count:</b> {df['word_count'].sum():,}</p>
                </div>
                """
                hashtag_stats.object = stats_html
            else:
                notes_table.value = pd.DataFrame()
                hashtag_stats.object = "<p>No notes found for this hashtag.</p>"
                
            # Reset AI summary panel
            ai_summary_panel.object = (
                "<div style='background-color: #f9f9f9; padding: 20px; border-radius: 5px; min-height: 150px;'>"
                "<h4>AI Summary</h4>"
                "<p style='color: #666;'>Select a note to view its AI summary</p>"
                "</div>"
            )
        
        # Bind update function
        hashtag_selector.param.watch(update_notes, 'value')
        
        # Bind folder filter changes
        folder_filter.param.watch(update_notes, 'value')
        
        # Handle row selection in notes table
        def on_row_select(event):
            """Update AI summary when a row is selected"""
            if event.new and len(event.new) > 0:
                # Get the selected row index
                selected_idx = event.new[0]
                if selected_idx < len(notes_table.value):
                    # Get the path of the selected note
                    selected_path = notes_table.value.iloc[selected_idx]['path']
                    
                    # Look up the full metadata
                    if selected_path in current_notes_metadata:
                        metadata = current_notes_metadata[selected_path]
                        ai_summary = metadata.get('ai_summary', None)
                        
                        if ai_summary:
                            # Format the AI summary nicely
                            summary_html = f"""
                            <div style='background-color: #f9f9f9; padding: 20px; border-radius: 5px;'>
                                <h4>AI Summary for: {selected_path.split('/')[-1]}</h4>
                                <div style='margin-top: 15px; line-height: 1.6;'>
                                    {ai_summary}
                                </div>
                                <div style='margin-top: 15px; color: #666; font-size: 0.9em;'>
                                    <b>Keywords:</b> {', '.join(metadata.get('keywords', [])[:10])}
                                </div>
                            </div>
                            """
                        else:
                            summary_html = f"""
                            <div style='background-color: #f9f9f9; padding: 20px; border-radius: 5px;'>
                                <h4>AI Summary for: {selected_path.split('/')[-1]}</h4>
                                <p style='color: #999; font-style: italic;'>No AI summary available for this note</p>
                            </div>
                            """
                        
                        ai_summary_panel.object = summary_html
            else:
                # No selection, reset to default
                ai_summary_panel.object = (
                    "<div style='background-color: #f9f9f9; padding: 20px; border-radius: 5px; min-height: 150px;'>"
                    "<h4>AI Summary</h4>"
                    "<p style='color: #666;'>Select a note to view its AI summary</p>"
                    "</div>"
                )
        
        # Bind selection handler
        notes_table.param.watch(on_row_select, 'selection')
        
        # Handle row count changes
        def on_row_count_change(event):
            """Update page size when row count is changed"""
            notes_table.page_size = event.new
        
        # Bind row count handler
        row_count_selector.param.watch(on_row_count_change, 'value')
        
        # Initialize with first hashtag after binding the update function
        # (moved to after param.watch)
        
        # Hashtag cloud
        hashtag_df = pd.DataFrame(hashtags_data)
        if len(hashtag_df) > 0:
            fig = px.treemap(
                hashtag_df.head(20),
                path=[px.Constant("All Hashtags"), 'hashtag'],
                values='count',
                title="Top 20 Hashtags by Note Count (Click to select)"
            )
            fig.update_traces(textinfo="label+value")
            fig.update_layout(height=400)
            
            # Create plotly pane with click event handling
            hashtag_cloud = pn.pane.Plotly(fig)
            
            # Handle clicks on the treemap
            def handle_treemap_click(event):
                if event and 'points' in event and event['points']:
                    point = event['points'][0]
                    if 'label' in point and point['label'] != 'All Hashtags':
                        # Update the hashtag selector
                        hashtag_selector.value = point['label']
            
            hashtag_cloud.param.watch(handle_treemap_click, 'click_data')
        else:
            hashtag_cloud = pn.pane.Alert("No hashtags found in the vault.", alert_type="info")
        
        # Initialize with first hashtag after everything is set up
        if hashtag_options:
            hashtag_selector.value = hashtag_options[0]
        
        return pn.Column(
            "# Hashtag Browser",
            pn.Row(
                pn.Column(
                    hashtag_selector,
                    pn.pane.Markdown("### Filter Options"),
                    folder_filter,
                    width=300
                ),
                pn.Spacer(width=50),
                hashtag_cloud
            ),
            hashtag_stats,
            pn.Row(
                pn.pane.Markdown("## Notes with Selected Hashtag"),
                pn.Spacer(),
                row_count_selector
            ),
            notes_table,
            "## AI Summary",
            ai_summary_panel
        )
    
    def create_network_tab(self):
        """Create network visualization tab"""
        # Create network
        net = Network(height="600px", width="100%", notebook=False)
        
        # Configure physics
        net.set_options("""
        {
            "physics": {
                "enabled": true,
                "stabilization": {
                    "enabled": true,
                    "iterations": 100
                },
                "barnesHut": {
                    "gravitationalConstant": -8000,
                    "springConstant": 0.001,
                    "springLength": 200
                }
            },
            "interaction": {
                "hover": true,
                "tooltipDelay": 200
            }
        }
        """)
        
        # Add nodes
        for node in self.data['graph']['nodes']:
            net.add_node(
                node['id'],
                label=node['label'],
                title=node['title'],
                value=node['value'],
                group=node['group']
            )
        
        # Add edges
        for edge in self.data['graph']['edges']:
            net.add_edge(edge['from'], edge['to'])
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            net.save_graph(f.name)
            temp_path = f.name
        
        # Read the HTML
        with open(temp_path, 'r') as f:
            network_html = f.read()
        
        # Clean up
        os.unlink(temp_path)
        
        return pn.Column(
            "# Network Graph",
            "Interactive visualization of note connections (may take a moment to stabilize)",
            pn.pane.HTML(network_html, height=600, sizing_mode='stretch_width')
        )
    
    def create_analysis_tab(self):
        """Create additional analysis tab"""
        # Prepare data
        all_notes_df = pd.DataFrame(
            [{"id": k, **v} for k, v in self.data.get('notes_metadata', {}).items()]
            if 'notes_metadata' in self.data 
            else self.data['important_notes'] + self.data['orphaned_notes']
        )
        
        # Link distribution
        link_dist = px.histogram(
            all_notes_df,
            x='out_degree',
            nbins=30,
            title='Outgoing Links Distribution',
            labels={'out_degree': 'Number of Outgoing Links', 'count': 'Number of Notes'}
        )
        
        # Word count distribution
        word_dist = px.histogram(
            all_notes_df[all_notes_df['word_count'] > 0],
            x='word_count',
            nbins=50,
            title='Word Count Distribution',
            labels={'word_count': 'Word Count', 'count': 'Number of Notes'}
        )
        word_dist.update_xaxes(range=[0, all_notes_df['word_count'].quantile(0.95)])
        
        # Tag analysis (if available)
        if 'tags' in all_notes_df.columns:
            all_tags = []
            for tags in all_notes_df['tags']:
                if isinstance(tags, list):
                    all_tags.extend(tags)
            
            if all_tags:
                tag_counts = pd.Series(all_tags).value_counts().head(20)
                tag_fig = px.bar(
                    x=tag_counts.values,
                    y=tag_counts.index,
                    orientation='h',
                    title='Top 20 Tags',
                    labels={'x': 'Count', 'y': 'Tag'}
                )
            else:
                tag_fig = None
        else:
            tag_fig = None
        
        return pn.Column(
            "# Additional Analysis",
            pn.Row(
                pn.pane.Plotly(link_dist, height=400),
                pn.pane.Plotly(word_dist, height=400)
            ),
            pn.pane.Plotly(tag_fig, height=400) if tag_fig else pn.pane.Markdown("No tag data available")
        )
    
    def serve(self):
        """Serve the dashboard"""
        self.template.servable()
        return self.template


def main():
    """Main entry point"""
    dashboard = ObsidianDashboard()
    dashboard.serve().show(port=5006, address="0.0.0.0", open=False)


if __name__ == "__main__":
    main()