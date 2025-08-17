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
    
    def __init__(self, data_file: str = "vault_analysis_with_git.json"):
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
                ("Images", self.create_images_tab()),
                ("Network Graph", self.create_network_tab()),
                ("Analysis", self.create_analysis_tab())
            )
        )
    
    def create_scrollable_table(self, dataframe, page_size=20, height=400, selectable=True, hidden_columns=None):
        """
        Create a common scrollable and sortable table component
        
        Args:
            dataframe: pandas DataFrame to display
            page_size: Initial page size (default 20)
            height: Table height in pixels (default 400)
            selectable: Whether rows are selectable (default True)
            hidden_columns: List of column names to hide (default None)
        
        Returns:
            table: Tabulator widget
            row_selector: Row count selector widget
        """
        # Create row count selector
        row_selector = pn.widgets.Select(
            name='Rows per page',
            value=page_size,
            options=[10, 20, 50, 100],
            width=150
        )
        
        # Configure table settings
        configuration = {
            'columnDefaults': {
                'headerSort': True,
                'resizable': True,
                'headerTooltip': True,
                'tooltip': True,
                'minWidth': 100,  # Minimum column width
                'maxWidth': 500,  # Maximum column width to prevent overly wide columns
                'editor': False,  # Make all columns read-only
                'widthGrow': 1,  # Allow columns to grow proportionally
                'editable': False,  # Explicitly disable editing
                'clickable': False  # Disable cell clicking
            },
            'movableColumns': True,  # Allow column reordering
            'autoColumns': False,  # Don't auto-size columns
            'responsiveLayout': False,  # Disable responsive layout to ensure scrolling
            'selectable': selectable,  # Control row selection
            'layout': 'fitData',  # Fit data with scrolling
            'placeholder': 'No data available',  # Show message when empty
            'headerVisible': True,  # Always show header
            'virtualDom': True,  # Enable virtual DOM for performance
            'virtualDomBuffer': 50,  # Buffer size for virtual DOM
            'cellClick': False,  # Disable cell click events
            'cellDblClick': False,  # Disable cell double-click events
            'cellContext': False,  # Disable cell context menu
            'cellEdited': False  # Disable cell edit events
        }
        
        # Handle hidden columns first
        if hidden_columns:
            if 'columns' not in configuration:
                configuration['columns'] = []
            for col in dataframe.columns:
                if col in hidden_columns:
                    configuration['columns'].append({'field': col, 'visible': False})
        
        # Special configuration for specific columns
        if 'columns' not in configuration:
            configuration['columns'] = []
        
        # Check if dataframe has keywords column and configure it specially
        if 'keywords' in dataframe.columns:
            # Check if keywords column already exists in configuration
            keywords_config_exists = any(col.get('field') == 'keywords' for col in configuration['columns'])
            if not keywords_config_exists:
                configuration['columns'].append({
                    'field': 'keywords',
                    'title': 'Keywords',
                    'minWidth': 250,  # Wider minimum for keywords
                    'maxWidth': None,  # No max width for keywords
                    'tooltip': True,  # Show full content on hover
                    'formatter': 'plaintext',  # Plain text display
                    'cssClass': 'keywords-cell'  # Custom CSS class
                })
        
        # Create table with horizontal scrolling enabled
        table = pn.widgets.Tabulator(
            dataframe,
            pagination='local',
            page_size=page_size,
            height=height,
            width_policy='max',  # Limit to container width
            sizing_mode='stretch_width',  # Stretch to fill available width
            layout='fit_data_table',  # Allow columns to size naturally
            show_index=False,
            selectable=1 if selectable else False,
            configuration=configuration,
            disabled=False  # Table is interactive but cells are not editable
        )
        
        # Add custom CSS to ensure horizontal scrolling and read-only appearance
        table.stylesheets = ["""
        /* Container constraints */
        :host {
            display: block !important;
            width: 100% !important;
            overflow: hidden !important;
        }
        
        /* Table holder with scrollbars */
        .tabulator-tableholder {
            overflow-x: auto !important;
            overflow-y: auto !important;
            max-width: 100% !important;
        }
        
        /* Table sizing */
        .tabulator-table {
            width: auto !important;
            min-width: 100% !important;
        }
        
        /* Header styling */
        .tabulator-header {
            overflow: hidden !important;
        }
        
        /* Cell styling for read-only */
        .tabulator-cell {
            user-select: none !important;  /* Disable text selection */
            cursor: default !important;  /* Default cursor, not text cursor */
            white-space: nowrap !important;  /* Prevent text wrapping by default */
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            pointer-events: auto !important;  /* Keep pointer events for hover */
            -webkit-user-select: none !important;
            -moz-user-select: none !important;
            -ms-user-select: none !important;
        }
        
        /* Disable input appearance for all cells */
        .tabulator-cell input,
        .tabulator-cell textarea,
        .tabulator-cell select {
            display: none !important;  /* Hide any input elements */
        }
        
        /* Disable cell editing styles */
        .tabulator-cell.tabulator-editing {
            border: none !important;
            background: inherit !important;
        }
        
        /* Special styling for keywords column */
        .keywords-cell, 
        .tabulator-cell[tabulator-field="keywords"] {
            white-space: normal !important;  /* Allow wrapping for keywords */
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
            max-width: 400px !important;
            min-width: 250px !important;
            user-select: none !important;  /* No text selection for keywords */
        }
        
        /* Allow clicking only for path links */
        .tabulator-cell[tabulator-field="path"] a {
            pointer-events: auto !important;
            cursor: pointer !important;
            user-select: none !important;
        }
        
        /* Ensure keywords are fully visible on hover */
        .tabulator-cell[tabulator-field="keywords"]:hover {
            overflow: visible !important;
            z-index: 10 !important;
            background-color: #f5f5f5 !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2) !important;
            position: relative !important;
        }
        
        /* Hover effects */
        .tabulator-cell:hover {
            background-color: #f5f5f5 !important;
        }
        
        .tabulator-row.tabulator-selectable:hover {
            background-color: #f0f0f0 !important;
        }
        
        /* Scrollbar styling */
        .tabulator-tableholder::-webkit-scrollbar {
            height: 10px;
            width: 10px;
        }
        
        .tabulator-tableholder::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        
        .tabulator-tableholder::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 5px;
        }
        
        .tabulator-tableholder::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
        """]
        
        # Update page size when selector changes
        def update_page_size(event):
            table.page_size = event.new
        
        row_selector.param.watch(update_page_size, 'value')
        
        return table, row_selector
    
    def create_sidebar(self):
        """Create sidebar with vault statistics"""
        stats = self.data["stats"]
        
        git_section = ""
        if stats.get('is_git_repo', False) and 'git_stats' in stats:
            git_stats = stats['git_stats']
            git_section = f"""
            <h3>Git Statistics</h3>
            <ul style="list-style-type: none; padding: 0;">
                <li>📊 <b>Files with history:</b> {git_stats.get('files_with_history', 0)}</li>
                <li>📈 <b>Avg commits/file:</b> {git_stats.get('average_commits', 0):.1f}</li>
                <li>🏆 <b>Max commits:</b> {git_stats.get('max_commits', 0)}</li>
            </ul>
            """
        
        stats_html = f"""
        <h3>Vault Statistics</h3>
        <ul style="list-style-type: none; padding: 0;">
            <li>📝 <b>Total Notes:</b> {stats['total_notes']}</li>
            <li>📄 <b>Markdown:</b> {stats['markdown_count']}</li>
            <li>🎨 <b>Excalidraw:</b> {stats['excalidraw_count']}</li>
            <li>🔗 <b>Connections:</b> {stats['graph_edges']}</li>
            <li>🏝️ <b>Orphaned:</b> {stats['orphaned_count']}</li>
        </ul>
        {git_section}
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
        display_df = recent_df[['path', 'modified', 'commit_count', 'type', 'importance_score']].copy()
        display_df['modified'] = display_df['modified'].dt.strftime('%Y-%m-%d %H:%M')
        
        # Use common table component
        recent_table, recent_row_selector = self.create_scrollable_table(
            display_df,
            page_size=25,
            height=800,
            selectable=False  # No selection needed for overview
        )
        
        # Apply specific formatters and titles
        recent_table.formatters = {
            'path': {'type': 'link', 'urlPrefix': 'obsidian://open?path='},
            'importance_score': {'type': 'progress', 'max': 50}
        }
        recent_table.sorters = [{'field': 'modified', 'dir': 'desc'}]
        recent_table.titles = {
            'importance_score': 'Importance Score',
            'commit_count': 'Commits'
        }
        
        return pn.Column(
            "# Vault Overview",
            metrics,
            pn.Row(
                pn.Column(
                    pn.pane.Plotly(pie_chart, height=350),
                    width=400,
                    sizing_mode='fixed'
                ),
                pn.Column(
                    pn.Row(
                        pn.pane.Markdown("### Recently Modified Notes"),
                        pn.Spacer(),
                        recent_row_selector
                    ),
                    recent_table,
                    sizing_mode='stretch_both'
                ),
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
            'path', 'importance_score', 'commit_count', 'in_degree', 'out_degree', 
            'word_count', 'modified', 'type'
        ]].copy()
        
        display_df['modified'] = pd.to_datetime(display_df['modified'], format='mixed').dt.strftime('%Y-%m-%d')
        display_df['importance_score'] = display_df['importance_score'].round(2)
        
        # Use common table component
        table, row_selector = self.create_scrollable_table(
            display_df,
            page_size=20,
            height=600
        )
        
        # Add custom formatting after table creation
        table.formatters = {
            'importance_score': {'type': 'progress', 'max': display_df['importance_score'].max()},
            'path': {'type': 'link', 'urlPrefix': 'obsidian://open?path='}
        }
        table.titles = {
            'importance_score': 'Importance Score',
            'commit_count': 'Commits',
            'in_degree': 'In Links',
            'out_degree': 'Out Links',
            'word_count': 'Words'
        }
        table.sorters = [{'field': 'importance_score', 'dir': 'desc'}]
        
        # Importance factors breakdown
        factors_fig = go.Figure()
        
        for _, note in important_df.head(10).iterrows():
            factors_fig.add_trace(go.Bar(
                name=note['path'].split('/')[-1][:20] + '...',
                x=['Git Activity', 'PageRank', 'In Links', 'Out Links', 'Content'],
                y=[
                    note.get('git_score', 0) * 10 * 0.30,  # Git activity score - MOST IMPORTANT
                    note['pagerank'] * 20,  # Scaled to match new importance calculation
                    note['in_degree'] * 0.15,
                    note['out_degree'] * 0.15,
                    min(note['word_count'] / 1000 + len(note.get('images', [])) * 0.5, 10) * 0.10
                ]
            ))
        
        factors_fig.update_layout(
            title="Importance Score Breakdown (Top 10 Notes)",
            barmode='group',
            height=400
        )
        
        # Create help icon with explanation
        help_text = pn.pane.HTML("""
            <div style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
                <b>ℹ️ Importance Score Formula:</b> 30% Git Commits + 20% PageRank + 15% Incoming Links + 15% Outgoing Links + 10% Content + 10% Base
                <details style="margin-top: 10px;">
                    <summary style="cursor: pointer; color: #1a73e8;"><b>Click to see what each factor means</b></summary>
                    <div style="margin-top: 10px; padding-left: 15px; font-size: 0.9em;">
                        <p><b>Git Commits (30%):</b> How often the note has been edited. More commits = more important.</p>
                        <p><b>PageRank (20%):</b> How "central" the note is. Notes linked by important notes score higher.</p>
                        <p><b>Incoming Links (15%):</b> Number of other notes that link TO this note.</p>
                        <p><b>Outgoing Links (15%):</b> Number of notes this note links TO (hub notes).</p>
                        <p><b>Content (10%):</b> Word count/1000 + images×0.5 + tags×0.2 (capped at 10).</p>
                        <p><b>Base (10%):</b> Every note gets 1.0 point minimum for existing.</p>
                    </div>
                </details>
            </div>
        """)
        
        return pn.Column(
            "# Important Notes",
            "Notes ranked by their importance score (links, content, and network position)",
            help_text,
            pn.Row(
                pn.pane.Markdown("### Top Important Notes"),
                pn.Spacer(),
                row_selector
            ),
            table,
            pn.pane.Plotly(factors_fig)
        )
    
    def create_orphaned_notes_tab(self):
        """Create tab for orphaned notes"""
        orphaned_df = pd.DataFrame(self.data['orphaned_notes'])
        
        if len(orphaned_df) > 0:
            # Prepare display
            display_df = orphaned_df[['path', 'commit_count', 'modified', 'word_count', 'type']].copy()
            display_df['modified'] = pd.to_datetime(display_df['modified'], format='mixed').dt.strftime('%Y-%m-%d')
            
            # Use common table component
            table, row_selector = self.create_scrollable_table(
                display_df,
                page_size=20,
                height=500
            )
            
            # Add custom formatting
            table.formatters = {
                'path': {'type': 'link', 'urlPrefix': 'obsidian://open?path='}
            }
            table.titles = {
                'commit_count': 'Commits',
                'word_count': 'Words'
            }
            
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
                pn.Row(
                    pn.pane.Markdown("### Orphaned Notes List"),
                    pn.Spacer(),
                    row_selector
                ),
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
        
        # Create notes table using common component
        notes_table, notes_row_selector = self.create_scrollable_table(
            pd.DataFrame(),
            page_size=10,
            height=400,
            selectable=True
        )
        
        # Apply specific formatters and titles for hashtag table
        notes_table.formatters = {'path': {'type': 'link', 'urlPrefix': 'obsidian://open?path='}}
        notes_table.titles = {
            'importance_score': 'Importance Score',
            'commit_count': 'Commits',
            'word_count': 'Words'
        }
        
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
                    # Use note_id as key since that's what matches the data structure
                    current_notes_metadata[note_id] = metadata
                    
                    filtered_notes.append({
                        'path': metadata.get('path', ''),
                        'type': metadata.get('type', ''),
                        'commit_count': metadata.get('commit_count', 0),
                        'importance_score': metadata.get('importance_score', 0),
                        'word_count': metadata.get('word_count', 0),
                        'modified': pd.to_datetime(metadata.get('modified', ''), format='mixed').strftime('%Y-%m-%d') if metadata.get('modified') else '',
                        'keywords': ', '.join(metadata.get('keywords', []))  # Show all keywords
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
                    # Convert path to note_id by removing .md extension
                    note_id = selected_path.rstrip('.md') if selected_path.endswith('.md') else selected_path
                    
                    # Look up the full metadata
                    if note_id in current_notes_metadata:
                        metadata = current_notes_metadata[note_id]
                        ai_summary = metadata.get('ai_summary', None)
                        linked_content = metadata.get('linked_content', {})
                        
                        # Build linked content HTML
                        linked_html = ""
                        if linked_content:
                            linked_sections = []
                            
                            # Linked notes - display all
                            if linked_content.get('notes'):
                                notes_list = "".join([f'<li>📄 <a href="obsidian://open?path={note["path"]}" style="color: #1a73e8;">{note["title"]}</a></li>' 
                                                     for note in linked_content['notes']])  # Show all notes
                                linked_sections.append(f'<div style="margin: 10px 0;"><b>Linked Notes ({len(linked_content["notes"])}):</b><ul style="margin: 5px 0; padding-left: 20px; list-style-type: none; max-height: 400px; overflow-y: auto;">{notes_list}</ul></div>')
                            
                            # Images - display all with scroll
                            if linked_content.get('images'):
                                img_list = "".join([f'<li>🖼️ {img["path"].split("/")[-1]}</li>' for img in linked_content['images']])
                                linked_sections.append(f'<div style="margin: 10px 0;"><b>Images ({len(linked_content["images"])}):</b><ul style="margin: 5px 0; padding-left: 20px; list-style-type: none; max-height: 200px; overflow-y: auto;">{img_list}</ul></div>')
                            
                            # PDFs - display all with scroll
                            if linked_content.get('pdfs'):
                                pdf_list = "".join([f'<li>📑 {pdf["text"]}</li>' for pdf in linked_content['pdfs']])
                                linked_sections.append(f'<div style="margin: 10px 0;"><b>PDFs ({len(linked_content["pdfs"])}):</b><ul style="margin: 5px 0; padding-left: 20px; list-style-type: none; max-height: 200px; overflow-y: auto;">{pdf_list}</ul></div>')
                            
                            # URLs - display all with scroll
                            if linked_content.get('urls'):
                                url_list = "".join([f'<li>🔗 <a href="{url["url"]}" target="_blank" style="color: #1a73e8;">{url["text"][:80]}{"..." if len(url["text"]) > 80 else ""}</a></li>' 
                                                   for url in linked_content['urls']])
                                linked_sections.append(f'<div style="margin: 10px 0;"><b>External URLs ({len(linked_content["urls"])}):</b><ul style="margin: 5px 0; padding-left: 20px; list-style-type: none; max-height: 200px; overflow-y: auto;">{url_list}</ul></div>')
                            
                            # Other files - display all with scroll
                            if linked_content.get('files'):
                                file_list = "".join([f'<li>📎 {file["text"]}</li>' for file in linked_content['files']])
                                linked_sections.append(f'<div style="margin: 10px 0;"><b>Other Files ({len(linked_content["files"])}):</b><ul style="margin: 5px 0; padding-left: 20px; list-style-type: none; max-height: 200px; overflow-y: auto;">{file_list}</ul></div>')
                            
                            if linked_sections:
                                linked_html = f"""
                                <div style='background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-top: 15px;'>
                                    <h4 style="margin-top: 0;">Linked Content</h4>
                                    {"".join(linked_sections)}
                                </div>
                                """
                        
                        if ai_summary:
                            # Get AI hashtags
                            ai_hashtags = metadata.get('ai_hashtags', [])
                            hashtags_display = ' '.join(ai_hashtags) if ai_hashtags else 'None'
                            
                            # Format the AI summary nicely
                            summary_html = f"""
                            <div style='background-color: #f9f9f9; padding: 20px; border-radius: 5px;'>
                                <h4>AI Summary for: {selected_path.split('/')[-1]}</h4>
                                <div style='margin-top: 15px; line-height: 1.6;'>
                                    {ai_summary}
                                </div>
                                <div style='margin-top: 15px; color: #444; font-size: 0.95em;'>
                                    <b>Hashtags:</b> <span style='color: #1a73e8;'>{hashtags_display}</span>
                                </div>
                                <div style='margin-top: 10px; color: #666; font-size: 0.9em;'>
                                    <b>Keywords:</b> {', '.join(metadata.get('keywords', [])[:10])}
                                </div>
                            </div>
                            {linked_html}
                            """
                        else:
                            # Get AI hashtags even if no summary
                            ai_hashtags = metadata.get('ai_hashtags', [])
                            hashtags_display = ' '.join(ai_hashtags) if ai_hashtags else 'None'
                            
                            summary_html = f"""
                            <div style='background-color: #f9f9f9; padding: 20px; border-radius: 5px;'>
                                <h4>AI Summary for: {selected_path.split('/')[-1]}</h4>
                                <p style='color: #999; font-style: italic;'>No AI summary available for this note</p>
                                <div style='margin-top: 15px; color: #444; font-size: 0.95em;'>
                                    <b>Hashtags:</b> <span style='color: #1a73e8;'>{hashtags_display}</span>
                                </div>
                            </div>
                            {linked_html}
                            """
                        
                        ai_summary_panel.object = summary_html
                    else:
                        # Note not found in metadata
                        ai_summary_panel.object = f"""
                        <div style='background-color: #f9f9f9; padding: 20px; border-radius: 5px;'>
                            <h4>AI Summary for: {selected_path.split('/')[-1]}</h4>
                            <p style='color: #999; font-style: italic;'>Note metadata not found</p>
                        </div>
                        """
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
        notes_row_selector.param.watch(on_row_count_change, 'value')
        
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
        
        # Create help text for importance score
        score_help = pn.pane.HTML("""
            <div style="background-color: #e8f4f8; padding: 10px; border-radius: 5px; margin-bottom: 10px; font-size: 0.9em;">
                <b>ℹ️ Importance Score:</b> 30% Git Commits + 20% PageRank + 15% Incoming Links + 15% Outgoing Links + 10% Content + 10% Base
                <details style="margin-top: 8px;">
                    <summary style="cursor: pointer; color: #1a73e8; font-size: 0.95em;"><b>What does each factor mean?</b></summary>
                    <div style="margin-top: 8px; padding-left: 12px; font-size: 0.85em;">
                        <b>• Git:</b> Edit frequency | <b>• PageRank:</b> Network centrality | <b>• In/Out Links:</b> Connections<br>
                        <b>• Content:</b> Words + images + tags | <b>• Base:</b> Minimum score for all notes
                    </div>
                </details>
            </div>
        """)
        
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
                notes_row_selector
            ),
            score_help,
            notes_table,
            "## AI Summary",
            ai_summary_panel
        )
    
    def create_images_tab(self):
        """Create images browser tab - showing only linked images"""
        # Get image usage data (only images that are actually used in notes)
        image_usage = self.data.get('image_usage', {})
        
        # Convert to list format for display - only include images with links
        image_data = []
        for img_path, notes in image_usage.items():
            if len(notes) > 0:  # Only include images that are actually used
                # Get format from extension
                ext = img_path.split('.')[-1].lower() if '.' in img_path else 'unknown'
                
                image_data.append({
                    'image': img_path,
                    'format': ext,
                    'link_count': len(notes),
                    'notes': notes,
                    'filename': img_path.split('/')[-1]
                })
        
        # Sort by link count (descending)
        image_data.sort(key=lambda x: x['link_count'], reverse=True)
        
        # Create DataFrame for display
        if image_data:
            display_df = pd.DataFrame([
                {
                    'Image': item['filename'],
                    'Format': item['format'].upper(),
                    'Links': item['link_count'],
                    'Path': item['image']
                }
                for item in image_data
            ])
            
            # Use common table component
            image_table, image_row_selector = self.create_scrollable_table(
                display_df,
                page_size=20,
                height=500,
                selectable=True
            )
            
            # Apply specific configuration
            image_table.sorters = [{'field': 'Links', 'dir': 'desc'}]
            
            # Panel to show notes using selected image
            notes_panel = pn.pane.HTML(
                "<div style='background-color: #f9f9f9; padding: 20px; border-radius: 5px; min-height: 200px;'>"
                "<h4>Notes Using This Image</h4>"
                "<p style='color: #666;'>Select an image to see which notes use it</p>"
                "</div>",
                sizing_mode='stretch_width'
            )
            
            # Store image data for lookup
            image_lookup = {item['image']: item['notes'] for item in image_data}
            
            def on_image_select(event):
                """Update notes panel when an image is selected"""
                if event.new and len(event.new) > 0:
                    selected_idx = event.new[0]
                    if selected_idx < len(image_table.value):
                        selected_path = image_table.value.iloc[selected_idx]['Path']
                        
                        if selected_path in image_lookup:
                            notes = image_lookup[selected_path]
                            
                            # Create HTML for notes list
                            notes_html = f"""
                            <div style='background-color: #f9f9f9; padding: 20px; border-radius: 5px;'>
                                <h4>Notes Using: {selected_path.split('/')[-1]}</h4>
                                <p style='color: #666; margin-bottom: 15px;'>Found in {len(notes)} note(s):</p>
                                <ul style='list-style-type: none; padding: 0;'>
                            """
                            
                            for note in notes:
                                note_path = note['path']
                                notes_html += f"""
                                    <li style='margin: 8px 0; padding: 8px; background-color: white; border-radius: 4px;'>
                                        <a href='obsidian://open?path={note_path}' style='color: #1a73e8; text-decoration: none;'>
                                            📄 {note['title']}
                                        </a>
                                        <span style='color: #999; font-size: 0.85em; display: block; margin-top: 2px;'>
                                            {note_path}
                                        </span>
                                    </li>
                                """
                            
                            notes_html += """
                                </ul>
                            </div>
                            """
                            
                            notes_panel.object = notes_html
                else:
                    # Reset to default
                    notes_panel.object = (
                        "<div style='background-color: #f9f9f9; padding: 20px; border-radius: 5px; min-height: 200px;'>"
                        "<h4>Notes Using This Image</h4>"
                        "<p style='color: #666;'>Select an image to see which notes use it</p>"
                        "</div>"
                    )
            
            # Bind selection handler
            image_table.param.watch(on_image_select, 'selection')
            
            # Calculate statistics
            total_images = len(image_data)
            total_usage = sum(item['link_count'] for item in image_data)
            avg_usage = total_usage / total_images if total_images > 0 else 0
            
            # Format distribution
            format_counts = {}
            for item in image_data:
                fmt = item['format']
                format_counts[fmt] = format_counts.get(fmt, 0) + 1
            
            stats_html = f"""
            <div style="background-color: #f0f0f0; padding: 20px; border-radius: 5px; margin-bottom: 20px;">
                <h3>Linked Images Statistics</h3>
                <p><b>Total Linked Images:</b> {total_images:,}</p>
                <p><b>Total Links:</b> {total_usage:,}</p>
                <p><b>Average Links per Image:</b> {avg_usage:.1f}</p>
                <p><b>Formats:</b> {', '.join(f'{fmt.upper()} ({count})' for fmt, count in sorted(format_counts.items()))}</p>
            </div>
            """
            
            return pn.Column(
                "# Linked Images",
                pn.pane.HTML(stats_html),
                pn.Row(
                    pn.pane.Markdown(f"## All Linked Images ({total_images:,} images)"),
                    pn.Spacer(),
                    image_row_selector
                ),
                image_table,
                "## Notes Using Selected Image",
                notes_panel
            )
        else:
            return pn.Column(
                "# Images in Vault",
                pn.pane.Alert(
                    "No images found in the vault.",
                    alert_type="info"
                )
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