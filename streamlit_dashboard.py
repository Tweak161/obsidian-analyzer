#!/usr/bin/env python3
"""
Streamlit Dashboard for Obsidian Vault Analysis
"""

import json
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import networkx as nx
from pyvis.network import Network
import tempfile
import os

# Page config
st.set_page_config(
    page_title="Obsidian Vault Analyzer",
    page_icon="📝",
    layout="wide"
)

@st.cache_data
def load_data():
    """Load analysis data"""
    with open("vault_analysis.json", 'r') as f:
        return json.load(f)

def main():
    st.title("📝 Obsidian Vault Analyzer")
    
    # Load data
    data = load_data()
    
    # Sidebar with statistics
    with st.sidebar:
        st.header("Vault Statistics")
        stats = data["stats"]
        
        st.metric("Total Notes", f"{stats['total_notes']:,}")
        st.metric("Markdown Files", f"{stats['markdown_count']:,}")
        st.metric("Excalidraw Files", f"{stats['excalidraw_count']:,}")
        st.metric("Connections", f"{stats['graph_edges']:,}")
        st.metric("Orphaned Notes", f"{stats['orphaned_count']:,}")
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📅 Timeline", "⭐ Important Notes", "🏝️ Orphaned Notes", "🕸️ Network"])
    
    with tab1:
        st.header("Vault Overview")
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Notes", stats['total_notes'])
        with col2:
            st.metric("Total Connections", stats['graph_edges'])
        with col3:
            st.metric("Orphaned Notes", stats['orphaned_count'])
        with col4:
            orphan_percent = (stats['orphaned_count'] / stats['total_notes'] * 100) if stats['total_notes'] > 0 else 0
            st.metric("Orphan Rate", f"{orphan_percent:.1f}%")
        
        # File type distribution
        col1, col2 = st.columns(2)
        
        with col1:
            file_types = pd.DataFrame([
                {'Type': 'Markdown', 'Count': stats['markdown_count']},
                {'Type': 'Excalidraw', 'Count': stats['excalidraw_count']}
            ])
            
            fig = px.pie(file_types, values='Count', names='Type', title='File Type Distribution')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Recent activity
            st.subheader("Recently Modified Notes")
            recent_df = pd.DataFrame(data['timeline']['modified'][-10:])
            recent_df['modified'] = pd.to_datetime(recent_df['modified'], format='mixed')
            recent_df = recent_df[['path', 'modified', 'type']].sort_values('modified', ascending=False)
            st.dataframe(recent_df, use_container_width=True)
    
    with tab2:
        st.header("Timeline Analysis")
        
        # Prepare data
        created_df = pd.DataFrame(data['timeline']['created'])
        created_df['created'] = pd.to_datetime(created_df['created'], format='mixed')
        
        modified_df = pd.DataFrame(data['timeline']['modified'])
        modified_df['modified'] = pd.to_datetime(modified_df['modified'], format='mixed')
        
        # Creation timeline
        fig1 = px.scatter(
            created_df,
            x='created',
            y='importance_score',
            hover_data=['path', 'type'],
            color='type',
            title='Note Creation Timeline',
            labels={'created': 'Creation Date', 'importance_score': 'Importance Score'}
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # Modification histogram
        fig2 = px.histogram(
            modified_df,
            x='modified',
            nbins=50,
            title='Modification Activity Over Time'
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # Activity heatmap
        modified_df['hour'] = modified_df['modified'].dt.hour
        modified_df['day_of_week'] = modified_df['modified'].dt.day_name()
        
        activity_pivot = modified_df.pivot_table(
            index='hour',
            columns='day_of_week',
            values='path',
            aggfunc='count',
            fill_value=0
        )
        
        # Reorder days
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        activity_pivot = activity_pivot.reindex(columns=[d for d in days_order if d in activity_pivot.columns])
        
        fig3 = px.imshow(
            activity_pivot,
            labels=dict(x="Day of Week", y="Hour of Day", color="Notes Modified"),
            title="Activity Heatmap",
            aspect="auto"
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab3:
        st.header("Important Notes")
        st.markdown("Notes ranked by their importance score (based on links, content, and network position)")
        
        important_df = pd.DataFrame(data['important_notes'])
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            avg_importance = important_df['importance_score'].mean()
            st.metric("Average Importance", f"{avg_importance:.2f}")
        with col2:
            max_links = important_df['in_degree'].max()
            st.metric("Max Incoming Links", max_links)
        with col3:
            avg_words = important_df['word_count'].mean()
            st.metric("Avg Word Count", f"{avg_words:.0f}")
        
        # Table
        display_df = important_df[[
            'path', 'importance_score', 'in_degree', 'out_degree', 
            'word_count', 'modified', 'type'
        ]].copy()
        
        display_df['modified'] = pd.to_datetime(display_df['modified'], format='mixed').dt.strftime('%Y-%m-%d')
        display_df['importance_score'] = display_df['importance_score'].round(2)
        
        st.dataframe(
            display_df,
            use_container_width=True,
            column_config={
                "path": st.column_config.TextColumn("Note Path", width="large"),
                "importance_score": st.column_config.ProgressColumn(
                    "Importance",
                    min_value=0,
                    max_value=display_df['importance_score'].max(),
                ),
                "in_degree": st.column_config.NumberColumn("In Links"),
                "out_degree": st.column_config.NumberColumn("Out Links"),
                "word_count": st.column_config.NumberColumn("Words"),
                "modified": st.column_config.TextColumn("Modified"),
                "type": st.column_config.TextColumn("Type"),
            }
        )
        
        # Importance breakdown
        st.subheader("Importance Score Breakdown (Top 10)")
        
        fig = go.Figure()
        for _, note in important_df.head(10).iterrows():
            fig.add_trace(go.Bar(
                name=note['path'].split('/')[-1][:30] + '...' if len(note['path'].split('/')[-1]) > 30 else note['path'].split('/')[-1],
                x=['PageRank', 'In Links', 'Out Links', 'Content'],
                y=[
                    note['pagerank'] * 30,
                    note['in_degree'] * 0.25,
                    note['out_degree'] * 0.25,
                    min(note['word_count'] / 1000 + len(note.get('images', [])) * 0.5, 10) * 0.15
                ]
            ))
        
        fig.update_layout(barmode='group', height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.header("Orphaned Notes")
        st.markdown("Notes without any incoming or outgoing links")
        
        orphaned_df = pd.DataFrame(data['orphaned_notes'])
        
        if len(orphaned_df) > 0:
            # Statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Orphaned", len(orphaned_df))
            with col2:
                orphan_percent = len(orphaned_df) / stats['total_notes'] * 100
                st.metric("Percentage of Vault", f"{orphan_percent:.1f}%")
            with col3:
                total_words = orphaned_df['word_count'].sum()
                st.metric("Total Word Count", f"{total_words:,}")
            
            # Table
            display_df = orphaned_df[['path', 'modified', 'word_count', 'type']].copy()
            display_df['modified'] = pd.to_datetime(display_df['modified'], format='mixed').dt.strftime('%Y-%m-%d')
            
            st.dataframe(display_df, use_container_width=True)
        else:
            st.success("No orphaned notes found! All notes are connected.")
    
    with tab5:
        st.header("Network Graph")
        st.markdown("Interactive visualization of note connections")
        
        # Create network
        net = Network(height="600px", width="100%", notebook=False, cdn_resources='in_line')
        
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
        
        # Add nodes (limit for performance)
        node_count = len(data['graph']['nodes'])
        if node_count > 500:
            st.warning(f"Graph has {node_count} nodes. Showing top 500 by importance for performance.")
            # Sort by importance and take top 500
            nodes = sorted(data['graph']['nodes'], key=lambda x: x.get('value', 0), reverse=True)[:500]
            # Get edges for these nodes
            node_ids = {n['id'] for n in nodes}
            edges = [e for e in data['graph']['edges'] if e['from'] in node_ids and e['to'] in node_ids]
        else:
            nodes = data['graph']['nodes']
            edges = data['graph']['edges']
        
        for node in nodes:
            net.add_node(
                node['id'],
                label=node['label'],
                title=node['title'],
                value=node['value'],
                group=node['group']
            )
        
        for edge in edges:
            net.add_edge(edge['from'], edge['to'])
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            net.save_graph(f.name)
            temp_path = f.name
        
        # Read and display
        with open(temp_path, 'r') as f:
            html = f.read()
        
        os.unlink(temp_path)
        
        st.components.v1.html(html, height=600)

if __name__ == "__main__":
    main()