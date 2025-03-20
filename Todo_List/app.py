import streamlit as st 
# Ye Ui banane ke liye use hota hai
import pandas as pd 
# Ye Dataframe banane ke liye use hota hai
from datetime import datetime, timedelta 
# Ye Date and Time banane ke liye use hota hai
import json 
# Ye JSON file banane ke liye use hota hai
import os 
# Ye File path banane ke liye use hota hai
import plotly.express as px 
# Ye Plot banane ke liye use hota hai
import uuid 
# Ye Unique ID banane ke liye use hota hai
import random 
# Ye Random number banane ke liye use hota hai
from PIL import Image 
# Ye Image banane ke liye use hota hai
import io
# Ye Input/Output banane ke liye use hota hai


# Ye Page ki Configuration ko modify karne ke liye use hota hai
st.set_page_config(
    page_title="TaskMaster - Advanced Todo List",
    page_icon="✅",
    layout="wide"
)

st.markdown(
    """
    <style>
    .stSidebar {
        width: 500px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Apply custom styling to the TaskMaster application
st.markdown("""
    <style>
        /* Theme variables */
        :root {
            --background-primary: #ffffff;
            --background-secondary: #f8f9fa;
            --text-primary: #1a1a2e;
            --text-secondary: #666666;
            --accent-color: #4ecca3;
            --quote-bg: #ffffff;
            --quote-border: #4ecca3;
            --header-color: #4ecca3;
            --divider-color: rgba(0,0,0,0.1);
            --tag-bg-color: #4ecca3;
            --tag-text-color: white;
            --due-overdue-color: #f44336;
            --due-today-color: #ff9800;
            --due-soon-color: #ffc107;
            --due-future-color: #4caf50;
            --input-bg-color: #ffffff;  /* Changed to white for light theme */
            --input-text-color: #1a1a2e; /* Changed to dark text for light theme */
        }
        /* Dark theme overrides */
        @media (prefers-color-scheme: dark) {
            :root {
                --background-primary: #1B1B2F;
                --background-secondary: #1F1F3A;
                --text-primary: #ffffff;
                --text-secondary: rgba(255, 255, 255, 0.7);
                --quote-bg: rgba(31, 31, 58, 0.95);
                --divider-color: rgba(255,255,255,0.1);
                --tag-bg-color: #4ecca3;
                --tag-text-color: #1B1B2F;
                --input-bg-color: #121212; /* Dark background for dark theme */
                --input-text-color: white; /* White text for dark theme */
            }
        }
        header{
            background-color: var(--background-primary) !important;
        }
        .stApp {
            background: linear-gradient(180deg, var(--background-primary) 0%, var(--background-secondary) 100%);
            color: var(--text-primary);
        }
        .st-an{
            background-color: var(--background-primary) !important;
        }

        .header-title {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            margin-bottom: 0.5rem;
            color: var(--accent-color);
            font-size: 2.5em !important;
        }
        .st-emotion-cache-1cvow4s{
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .quote-text {
            font-size: 28px;
            font-family: 'Georgia', serif;
            line-height: 1.6;
            margin: 20px 0;
            padding: 30px;
            border-left: 5px solid var(--quote-border);
            background: var(--quote-bg);
            border-radius: 10px;
            color: var(--text-primary);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }

        .author {
            font-size: 20px;
            color: var(--text-secondary);
            font-style: italic;
            margin: 20px 0;
            padding-left: 30px;
        }

        .category {
            font-size: 14px;
            color: var(--accent-color);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-top: 10px;
            padding-left: 30px;
        }

        .stButton button {
            width: 100%;
            border-radius: 8px !important;
            height: 3em;
            font-weight: 600;
            background-color: var(--accent-color) !important;
            color: var(--background-primary) !important;
            border: none !important;
            transition: all 0.3s ease;
        }

        .stButton button:hover {
            opacity: 0.9;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        /* Style the expander */
        .streamlit-expanderHeader {
            background: var(--quote-bg) !important;
            border-radius: 8px !important;
            border: 1px solid var(--accent-color) !important;
            color: var(--text-primary) !important;
        }

        .streamlit-expanderContent {
            background: var(--quote-bg) !important;
            border-radius: 0 0 8px 8px !important;
        }
        /* Footer styling */
        footer {
            color: var(--text-secondary);
        }

        /* Task-specific styling */
        .section-header {
            font-size: 1.2em;
            font-weight: 600;
            margin: 20px 0 10px 0;
            padding-bottom: 5px;
            border-bottom: 2px solid var(--accent-color);
            color: var(--accent-color);
        }

        .task-card {
            background-color: var(--quote-bg);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
            border-left: 4px solid var(--accent-color);
            transition: all 0.2s ease;
        }

        .task-card:hover {
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
        }

        .priority-high {
            border-left-color: var(--due-overdue-color);
        }

        .priority-medium {
            border-left-color: var(--due-today-color);
        }

        .priority-low {
            border-left-color: var(--due-future-color);
        }

        .tag {
            display: inline-block;
            background-color: var(--tag-bg-color);
            color: var(--tag-text-color);
            padding: 3px 8px;
            margin: 2px;
            border-radius: 12px;
            font-size: 0.8em;
        }

        .due-overdue {
            color: var(--due-overdue-color);
            font-weight: bold;
        }

        .due-today {
            color: var(--due-today-color);
            font-weight: bold;
        }

        .due-soon {
            color: var(--due-soon-color);
        }

        .due-future {
            color: var(--due-future-color);
        }

        /* Sidebar styling */
        .stSidebar {
            background-color: var(--background-primary);
        }

        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: var(--background-secondary);
            border-radius: 4px 4px 0 0;
            padding: 8px 16px;
            border: none;
        }

        .stTabs [aria-selected="true"] {
            background-color: var(--accent-color) !important;
            color: white !important;
        }

        /* Metric styling */
        [data-testid="stMetricValue"] {
            font-size: 1.8rem;
            font-weight: bold;
            color: var(--accent-color);
        }

        [data-testid="stMetricLabel"] {
            color: var(--text-secondary);
        }

        /* Chart styling */
        .js-plotly-plot .plotly {
            background-color: transparent !important;
        }

        /* Form styling */
        input, textarea, select, .stSlider, [data-baseweb="select"] {
            border-radius: 6px !important;
        }

        [data-baseweb="select"] {
            background-color: var(--background-secondary);
        }

        /* Fix for textarea and input colors */
        textarea, input[type="text"], input[type="date"], .stTextInput>div>div>input, .stDateInput>div>div>input {
            background-color: var(--input-bg-color) !important;
            color: var(--input-text-color) !important;
            border: 1px solid var(--divider-color) !important;
        }

        /* Ensure textarea has the same styling as input fields */
        .stTextArea>div>div>textarea {
            background-color: var(--input-bg-color) !important;
            color: var(--input-text-color) !important;
            border: 1px solid var(--divider-color) !important;
            min-height: 100px;
        }

        /* Select dropdown styling */
        [data-baseweb="select"] input {
            background-color: var(--input-bg-color) !important;
            color: var(--input-text-color) !important;
        }

        [data-baseweb="select"] [data-baseweb="popover"] {
            background-color: var(--background-secondary) !important;
        }

        /* Checkbox styling */
        [data-testid="stCheckbox"] > div {
            background-color: var(--background-secondary);
            border-radius: 4px;
        }
    </style>
    """, unsafe_allow_html=True)

# You can call this function at the beginning of your TaskMaster app
def apply_custom_styling():
    st.markdown("""
    <style>
    .stSidebar {
        width: 500px;
    }
    </style>
    """, unsafe_allow_html=True)

# You can call this function at the beginning of your TaskMaster app
def apply_custom_styling():
    st.markdown("""
    <style>
    .stSidebar {
        width: 500px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'todos' not in st.session_state:
     # Ye if ki statement check karegi ke 'todos.json' file computer par exist karti hai ya nahi agar karti hai toh to open karega or todos ko load karega 
    if os.path.exists('todos.json'):
        with open('todos.json', 'r') as f:
            st.session_state.todos = json.load(f)
    else:
        # or agar file exist nahi karti hai to ek empty list create karega
        st.session_state.todos = []

if 'view' not in st.session_state:
    st.session_state.view = "All"

if 'filter_priority' not in st.session_state:
    st.session_state.filter_priority = "All"

if 'sort_by' not in st.session_state:
    st.session_state.sort_by = "Due Date"

if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = None

# Functions for Todo operations
def save_todos():
    with open('todos.json', 'w') as f:
        json.dump(st.session_state.todos, f)

def add_todo(title, description, category, priority, due_date, tags):
    if not title:
        st.error("Task title cannot be empty!")
        return
    
    # Create a unique ID for the todo
    todo_id = str(uuid.uuid4())
    
    # Parse tags
    tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
    
    new_todo = {
        "id": todo_id,
        "title": title,
        "description": description,
        "category": category,
        "priority": priority,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "due_date": due_date,
        "completed": False,
        "completed_at": None,
        "tags": tag_list
    }
    
    st.session_state.todos.append(new_todo)
    save_todos()
    st.success(f"Task '{title}' added successfully!")

def toggle_todo_status(todo_id):
    for todo in st.session_state.todos:
        if todo["id"] == todo_id:
            todo["completed"] = not todo["completed"]
            todo["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if todo["completed"] else None
            save_todos()
            break

def delete_todo(todo_id):
    st.session_state.todos = [todo for todo in st.session_state.todos if todo["id"] != todo_id]
    save_todos()
    st.success("Task deleted successfully!")

def edit_todo(todo_id, title, description, category, priority, due_date, tags):
    for todo in st.session_state.todos:
        if todo["id"] == todo_id:
            tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
            
            todo["title"] = title
            todo["description"] = description
            todo["category"] = category
            todo["priority"] = priority
            todo["due_date"] = due_date
            todo["tags"] = tag_list
            save_todos()
            st.success(f"Task '{title}' updated successfully!")
            break

def get_filtered_todos():
    filtered_todos = st.session_state.todos.copy()
    
    # Filter by status
    if st.session_state.view == "Active":
        filtered_todos = [todo for todo in filtered_todos if not todo["completed"]]
    elif st.session_state.view == "Completed":
        filtered_todos = [todo for todo in filtered_todos if todo["completed"]]
    
    # Filter by priority
    if st.session_state.filter_priority != "All":
        filtered_todos = [todo for todo in filtered_todos if todo["priority"] == st.session_state.filter_priority]
    
    # Filter by search query
    if st.session_state.search_query:
        query = st.session_state.search_query.lower()
        filtered_todos = [
            todo for todo in filtered_todos if 
            query in todo["title"].lower() or 
            query in todo["description"].lower() or
            query in todo["category"].lower() or
            any(query in tag.lower() for tag in todo["tags"])
        ]
    
    # Sort todos
    if st.session_state.sort_by == "Due Date":
        filtered_todos.sort(key=lambda x: x["due_date"] if x["due_date"] else "9999-12-31")
    elif st.session_state.sort_by == "Priority":
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        filtered_todos.sort(key=lambda x: priority_order.get(x["priority"], 3))
    elif st.session_state.sort_by == "Creation Date":
        filtered_todos.sort(key=lambda x: x["created_at"])
    elif st.session_state.sort_by == "Category":
        filtered_todos.sort(key=lambda x: x["category"].lower())
    
    return filtered_todos

# Get statistics functions
def get_category_stats():
    categories = {}
    for todo in st.session_state.todos:
        if todo["category"] in categories:
            categories[todo["category"]] += 1
        else:
            categories[todo["category"]] = 1
    return categories

def get_tag_stats():
    tags = {}
    for todo in st.session_state.todos:
        for tag in todo["tags"]:
            if tag in tags:
                tags[tag] += 1
            else:
                tags[tag] = 1
    return tags

def get_priority_stats():
    priorities = {"High": 0, "Medium": 0, "Low": 0}
    for todo in st.session_state.todos:
        if todo["priority"] in priorities:
            priorities[todo["priority"]] += 1
    return priorities

def get_completion_stats():
    total = len(st.session_state.todos)
    completed = len([todo for todo in st.session_state.todos if todo["completed"]])
    active = total - completed
    return {"Completed": completed, "Active": active}

def export_todos_csv():
    df = pd.DataFrame(st.session_state.todos)
    return df.to_csv(index=False).encode('utf-8')

# Helper function to render priority indicator
def render_priority_indicator(priority):
    if priority == "High":
        return "🔴 High"
    elif priority == "Medium":
        return "🟡 Medium"
    else:
        return "🟢 Low"

# Helper function to render due date status
def render_due_date_status(due_date_str, completed):
    if completed or not due_date_str:
        return ""
    
    due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
    days_left = (due_date - datetime.now()).days
    
    if days_left < 0:
        return f"<span class='due-overdue'>⚠️ {abs(days_left)}d late</span>"
    elif days_left == 0:
        return "<span class='due-today'>Due today</span>"
    elif days_left <= 2:
        return f"<span class='due-soon'>{days_left}d left</span>"
    else:
        return f"<span class='due-future'>{days_left}d left</span>"

# Main App UI with enhanced styling
st.title("✅ TaskMaster - Advanced Todo List")

# Sidebar for app controls
with st.sidebar:
    st.header("Task Management")
    
    # Add new todo form
    with st.expander("➕ Add New Task", expanded=True):
        with st.form("add_todo_form", clear_on_submit=True):
            title = st.text_input("Title")
            description = st.text_area("Description")
            col1, col2 = st.columns(2)
            with col1:
                category = st.selectbox(
                    "Category", 
                    options=["Work", "Personal", "Shopping", "Health", "Finance", "Other"]
                )
                priority = st.select_slider(
                    "Priority", 
                    options=["Low", "Medium", "High"], 
                    value="Medium"
                )
            with col2:
                due_date = st.date_input(
                    "Due Date", 
                    value=datetime.now() + timedelta(days=1)
                )
                tags = st.text_input("Tags (comma-separated)")
            
            submit_button = st.form_submit_button("Add Task")
            if submit_button:
                add_todo(title, description, category, priority, due_date.strftime("%Y-%m-%d"), tags)
    
    # Filter options
    st.markdown("<div class='section-header'>Filters & Sorting</div>", unsafe_allow_html=True)
    st.session_state.view = st.radio("Show", ["All", "Active", "Completed"])
    st.session_state.filter_priority = st.selectbox("Priority", ["All", "High", "Medium", "Low"])
    st.session_state.sort_by = st.selectbox("Sort By", ["Due Date", "Priority", "Creation Date", "Category"])
    st.session_state.search_query = st.text_input("🔍 Search tasks")
    
    # Data export
    st.markdown("<div class='section-header'>Export Data</div>", unsafe_allow_html=True)
    csv = export_todos_csv()
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name="todo_list.csv",
        mime="text/csv",
    )
    
    # App info
    st.markdown("<div class='section-header'>About</div>", unsafe_allow_html=True)
    st.info("TaskMaster v1.0 - Built with Streamlit")

# Main content area
tab1, tab2 = st.tabs(["📋 Tasks", "📊 Statistics"])

with tab1:
    filtered_todos = get_filtered_todos()
    
    if not filtered_todos:
        st.markdown("""
            <div style="text-align: center; padding: 50px; color: var(--text-color);">
                <h3>No tasks found matching your filters</h3>
                <p>Try adjusting your filters or add a new task</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.write(f"Showing {len(filtered_todos)} tasks")
        
        for todo in filtered_todos:
            # Create a task card with theme-compatible styling
            with st.container():
                # Determine card styling based on completion status
                card_style = "task-card"
                title_style = "text-decoration: line-through;" if todo["completed"] else ""
                
                # Determine priority class
                priority_class = ""
                if todo["priority"] == "High":
                    priority_class = "priority-high"
                elif todo["priority"] == "Medium":
                    priority_class = "priority-medium"
                else:
                    priority_class = "priority-low"
                
                # Render the task card header
                col1, col2, col3 = st.columns([0.05, 0.85, 0.1])
                
                with col1:
                    completed = st.checkbox("", value=todo["completed"], key=f"check_{todo['id']}")
                    if completed != todo["completed"]:
                        toggle_todo_status(todo["id"])
                
                with col2:
                    expander_label = f"{todo['title']} "
                    if todo["priority"] == "High":
                        expander_label += "🔴"
                    elif todo["priority"] == "Medium":
                        expander_label += "🟡"
                    else:
                        expander_label += "🟢"
                        
                    if todo["completed"]:
                        expander_label = f"~~{expander_label}~~"
                    
                    with st.expander(expander_label):
                        with st.form(key=f"edit_form_{todo['id']}"):
                            new_title = st.text_input("Title", value=todo["title"])
                            new_description = st.text_area("Description", value=todo["description"])
                            col1, col2 = st.columns(2)
                            with col1:
                                new_category = st.selectbox(
                                    "Category", 
                                    options=["Work", "Personal", "Shopping", "Health", "Finance", "Other"],
                                    index=["Work", "Personal", "Shopping", "Health", "Finance", "Other"].index(todo["category"]) if todo["category"] in ["Work", "Personal", "Shopping", "Health", "Finance", "Other"] else 0
                                )
                                new_priority = st.select_slider(
                                    "Priority", 
                                    options=["Low", "Medium", "High"], 
                                    value=todo["priority"]
                                )
                            with col2:
                                new_due_date = st.date_input(
                                    "Due Date", 
                                    value=datetime.strptime(todo["due_date"], "%Y-%m-%d") if todo["due_date"] else datetime.now()
                                )
                                new_tags = st.text_input("Tags (comma-separated)", value=", ".join(todo["tags"]))
                            
                            col1, col2 = st.columns([1, 1])
                            with col1:
                                update_button = st.form_submit_button("Update Task")
                            with col2:
                                delete_button = st.form_submit_button("Delete Task", type="primary")
                            
                            if update_button:
                                edit_todo(
                                    todo["id"],
                                    new_title,
                                    new_description,
                                    new_category,
                                    new_priority,
                                    new_due_date.strftime("%Y-%m-%d"),
                                    new_tags
                                )
                            
                            if delete_button:
                                delete_todo(todo["id"])
                                st.rerun()
                        
                        # Display task details with improved styling
                        st.markdown(f"**Description:** {todo['description']}")
                        st.markdown(f"**Category:** {todo['category']}")
                        st.markdown(f"**Created:** {todo['created_at']}")
                        st.markdown(f"**Due:** {todo['due_date']}")
                        
                        if todo["completed"] and todo["completed_at"]:
                            st.markdown(f"**Completed:** {todo['completed_at']}")
                        
                        if todo["tags"]:
                            st.markdown("**Tags:**")
                            tags_html = ""
                            for tag in todo["tags"]:
                                tags_html += f'<span class="tag">{tag}</span> '
                            st.markdown(tags_html, unsafe_allow_html=True)
                
                with col3:
                    # Render due date status with theme-compatible styling
                    if not todo["completed"] and todo["due_date"]:
                        due_date_html = render_due_date_status(todo["due_date"], todo["completed"])
                        st.markdown(due_date_html, unsafe_allow_html=True)
            
            st.markdown("<hr style='margin: 10px 0; border-color: var(--divider-color);'>", unsafe_allow_html=True)

with tab2:
    if not st.session_state.todos:
        st.markdown("""
            <div style="text-align: center; padding: 50px; color: var(--text-color);">
                <h3>No tasks to display statistics for</h3>
                <p>Add some tasks to see your productivity stats</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Create theme-compatible Plotly charts
        plotly_config = {
            "template": "plotly_dark" if "prefers-color-scheme: dark" in st.markdown.__doc__ else "plotly_white"
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Completion status chart
            completion_stats = get_completion_stats()
            fig1 = px.pie(
                values=list(completion_stats.values()),
                names=list(completion_stats.keys()),
                title="Task Completion Status",
                color_discrete_sequence=px.colors.qualitative.Set3,
                **plotly_config
            )
            # Make the chart theme-compatible
            fig1.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"color": "var(--text-color)"}
            )
            st.plotly_chart(fig1, use_container_width=True)
            
            # Priority distribution chart
            priority_stats = get_priority_stats()
            fig2 = px.bar(
                x=list(priority_stats.keys()),
                y=list(priority_stats.values()),
                title="Tasks by Priority",
                color=list(priority_stats.keys()),
                color_discrete_map={"High": "#f44336", "Medium": "#ff9800", "Low": "#4caf50"},
                **plotly_config
            )
            # Make the chart theme-compatible
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"color": "var(--text-color)"}
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            # Category distribution chart
            category_stats = get_category_stats()
            fig3 = px.bar(
                x=list(category_stats.keys()),
                y=list(category_stats.values()),
                title="Tasks by Category",
                color=list(category_stats.keys()),
                color_discrete_sequence=px.colors.qualitative.Bold,
                **plotly_config
            )
            # Make the chart theme-compatible
            fig3.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"color": "var(--text-color)"}
            )
            st.plotly_chart(fig3, use_container_width=True)
            
            # Tag cloud with theme-compatible styling
            tag_stats = get_tag_stats()
            if tag_stats:
                st.subheader("Popular Tags")
                
                # Sort tags by frequency
                sorted_tags = sorted(tag_stats.items(), key=lambda x: x[1], reverse=True)
                
                # Display tags with theme-compatible styling
                tags_html = ""
                for tag, count in sorted_tags[:10]:
                    # Scale font size based on frequency
                    font_size = min(16 + count * 2, 28)
                    tags_html += f"""
                    <span style='
                        background-color: var(--tag-bg-color);
                        color: var(--tag-text-color);
                        padding: 6px 12px;
                        margin: 4px;
                        border-radius: 15px;
                        font-size: {font_size}px;
                        display: inline-block;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    '>{tag}</span>
                    """
                if tags_html:
                    st.write(f"<span>{tags_html}</span>", unsafe_allow_html=True)
                else:
                    st.markdown("No tags found")
            else:
                st.markdown("No tags found")
        
        # Task completion over time (if completed tasks exist)
        completed_todos = [todo for todo in st.session_state.todos if todo["completed"] and todo["completed_at"]]
        if completed_todos:
            st.subheader("Recent Task Completion")
            
            # Process completion dates
            completion_dates = {}
            for todo in completed_todos:
                date_str = todo["completed_at"].split(" ")[0]  # Extract just the date part
                if date_str in completion_dates:
                    completion_dates[date_str] += 1
                else:
                    completion_dates[date_str] = 1
            
            # Sort by date
            sorted_dates = sorted(completion_dates.items(), key=lambda x: x[0])
            
            # Convert to dataframe for plotting
            date_df = pd.DataFrame(sorted_dates, columns=["date", "count"])
            
            # Plot completion trend with theme-compatible styling
            fig4 = px.line(
                date_df, 
                x="date", 
                y="count",
                markers=True,
                title="Tasks Completed by Date",
                line_shape="linear",
                **plotly_config
            )
            # Make the chart theme-compatible
            fig4.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"color": "var(--text-color)"}
            )
            st.plotly_chart(fig4, use_container_width=True)
        
        # Task stats summary with improved styling
        st.markdown("<div class='section-header'>Task Summary</div>", unsafe_allow_html=True)
        total = len(st.session_state.todos)
        completed = len([todo for todo in st.session_state.todos if todo["completed"]])
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        # Create a more visually appealing metrics display
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Tasks", total)
        col2.metric("Completed", completed)
        col3.metric("Active", total - completed)
        col4.metric("Completion Rate", f"{completion_rate:.1f}%")
        
        # Check for overdue tasks with theme-compatible styling
        now = datetime.now()
        overdue = 0
        due_soon = 0
        
        for todo in st.session_state.todos:
            if not todo["completed"] and todo["due_date"]:
                due_date = datetime.strptime(todo["due_date"], "%Y-%m-%d")
                days_left = (due_date - now).days
                
                if days_left < 0:
                    overdue += 1
                elif days_left <= 2:
                    due_soon += 1
        
        if overdue > 0 or due_soon > 0:
            st.markdown(f"""
                <div style="
                    padding: 10px 15px;
                    border-radius: 5px;
                    margin: 10px 0;
                    background-color: rgba(255, 152, 0, 0.1);
                    border-left: 4px solid var(--due-today-color);
                ">
                    <h4 style="margin: 0; color: var(--due-today-color);">⚠️ Task Alert</h4>
                    <p style="margin: 5px 0 0 0;">You have {overdue} overdue tasks and {due_soon} tasks due in the next 2 days.</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Productivity tips with theme-compatible styling
        st.markdown("<div class='section-header'>Productivity Tips</div>", unsafe_allow_html=True)
        productivity_tips = [
            "Break large tasks into smaller, manageable subtasks.",
            "Use the 'Pomodoro Technique': work for 25 minutes, then take a 5-minute break.",
            "Complete high-priority tasks first thing in the morning.",
            "Set specific, measurable goals for each task.",
            "Minimize distractions by silencing notifications when focusing on important tasks.",
            "Review your task list at the end of each day and plan for tomorrow.",
            "Celebrate your accomplishments when you complete tasks.",
            "Try time-blocking your calendar for focused work on specific categories.",
            "If a task takes less than 2 minutes, do it immediately instead of adding it to your list."
        ]
        
        tip = random.choice(productivity_tips)
        st.markdown(f"""
            <div style="
                padding: 15px;
                border-radius: 5px;
                margin: 10px 0;
                background-color: rgba(33, 150, 243, 0.1);
                border-left: 4px solid var(--header-color);
            ">
                <h4 style="margin: 0; color: var(--header-color);">💡 Tip of the Day</h4>
                <p style="margin: 5px 0 0 0;">{tip}</p>
            </div>
        """, unsafe_allow_html=True)