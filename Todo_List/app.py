import streamlit as st # Ye Ui banane ke liye use hota hai
import pandas as pd # Ye Dataframe banane ke liye use hota hai
from datetime import datetime, timedelta # Ye Date and Time banane ke liye use hota hai
import json # Ye JSON file banane ke liye use hota hai
import os # Ye File path banane ke liye use hota hai
import plotly.express as px # Ye Plot banane ke liye use hota hai
import uuid # Ye Unique ID banane ke liye use hota hai
import random # Ye Random number banane ke liye use hota hai
from PIL import Image # Ye Image banane ke liye use hota hai
import io # Ye Input/Output banane ke liye use hota hai

# Ye Page ki Configuration ko modify karne ke liye use hota hai
st.set_page_config(
    page_title="TaskMaster - Advanced Todo List",
    page_icon="✅",
    layout="wide"
)

st.markdown("""
<style>
    .stSidebar {
        width: 35% !important;
    }
</style>
""", unsafe_allow_html=True)

# Ye Check karega ke 'todos' ke name ka variable st.session_state me exist karti hai ya nahi
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

# Get category and tag statistics
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

# Main App UI
st.title("✅ TaskMaster - Advanced Todo List")

# Sidebar for app controls
with st.sidebar:
    st.header("Controls")
    
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
    st.subheader("Filters")
    st.session_state.view = st.radio("Show", ["All", "Active", "Completed"])
    st.session_state.filter_priority = st.selectbox("Priority", ["All", "High", "Medium", "Low"])
    st.session_state.sort_by = st.selectbox("Sort By", ["Due Date", "Priority", "Creation Date", "Category"])
    st.session_state.search_query = st.text_input("Search tasks")
    
    # Data export
    st.subheader("Export")
    csv = export_todos_csv()
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name="todo_list.csv",
        mime="text/csv",
    )
    
    # App info
    st.info("TaskMaster v1.0 - Built with Streamlit")

# Main content area
tab1, tab2 = st.tabs(["📋 Tasks", "📊 Statistics"])

with tab1:
    filtered_todos = get_filtered_todos()
    
    if not filtered_todos:
        st.write("No tasks found matching your filters.")
    else:
        st.write(f"Showing {len(filtered_todos)} tasks")
        
        for todo in filtered_todos:
            with st.container():
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
                        
                        # Display task details
                        st.write(f"**Category:** {todo['category']}")
                        st.write(f"**Created:** {todo['created_at']}")
                        st.write(f"**Due:** {todo['due_date']}")
                        
                        if todo["completed"] and todo["completed_at"]:
                            st.write(f"**Completed:** {todo['completed_at']}")
                        
                        if todo["tags"]:
                            st.write("**Tags:**")
                            for tag in todo["tags"]:
                                st.markdown(f"`{tag}`", unsafe_allow_html=True)
                
                with col3:
                    # Calculate days left or overdue
                    if not todo["completed"] and todo["due_date"]:
                        due_date = datetime.strptime(todo["due_date"], "%Y-%m-%d")
                        days_left = (due_date - datetime.now()).days
                        
                        if days_left < 0:
                            st.markdown(f"<span style='color:red'>⚠️ {abs(days_left)}d late</span>", unsafe_allow_html=True)
                        elif days_left == 0:
                            st.markdown("<span style='color:orange'>Due today</span>", unsafe_allow_html=True)
                        elif days_left <= 2:
                            st.markdown(f"<span style='color:orange'>{days_left}d left</span>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<span style='color:green'>{days_left}d left</span>", unsafe_allow_html=True)
            
            st.divider()

with tab2:
    if not st.session_state.todos:
        st.write("No tasks to display statistics for.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            # Completion status chart
            completion_stats = get_completion_stats()
            fig1 = px.pie(
                values=list(completion_stats.values()),
                names=list(completion_stats.keys()),
                title="Task Completion Status",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig1, use_container_width=True)
            
            # Priority distribution chart
            priority_stats = get_priority_stats()
            fig2 = px.bar(
                x=list(priority_stats.keys()),
                y=list(priority_stats.values()),
                title="Tasks by Priority",
                color=list(priority_stats.keys()),
                color_discrete_map={"High": "red", "Medium": "yellow", "Low": "green"}
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
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            st.plotly_chart(fig3, use_container_width=True)
            
            # Tag cloud (simplified representation)
            tag_stats = get_tag_stats()
            if tag_stats:
                st.subheader("Popular Tags")
                    
                # Sort tags by frequency
                sorted_tags = sorted(tag_stats.items(), key=lambda x: x[1], reverse=True)
                    
                # Display up to top 10 tags with improved visibility
                for tag, count in sorted_tags[:10]:
                    if count >= 5:
                        bg_color = "#1e3d59"  # Dark blue for high frequency
                        text_color = "white"
                    elif count >= 3:
                        bg_color = "#2b6777"  # Medium blue for medium frequency
                        text_color = "white"
                    else:
                        bg_color = "#52ab98"  # Light blue for low frequency
                        text_color = "white"
                        
                    st.markdown(
                        f"""<span style='
                            background-color:{bg_color}; 
                            color:{text_color}; 
                            padding:6px 12px; 
                            margin:4px; 
                            border-radius:15px; 
                            font-size:{min(16 + count * 2, 28)}px;
                            display:inline-block;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                            border: 1px solid rgba(255,255,255,0.2);
                        '>{tag} ({count})</span>""", 
                        unsafe_allow_html=True
                    ) 
        
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
            
            # Plot completion trend
            fig4 = px.line(
                date_df, 
                x="date", 
                y="count",
                markers=True,
                title="Tasks Completed by Date",
                line_shape="linear"
            )
            st.plotly_chart(fig4, use_container_width=True)
        
        # Task stats summary
        st.subheader("Task Summary")
        total = len(st.session_state.todos)
        completed = len([todo for todo in st.session_state.todos if todo["completed"]])
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Tasks", total)
        col2.metric("Completed", completed)
        col3.metric("Active", total - completed)
        col4.metric("Completion Rate", f"{completion_rate:.1f}%")
        
        # Check for overdue tasks
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
        
        st.warning(f"⚠️ You have {overdue} overdue tasks and {due_soon} tasks due in the next 2 days.")
        
        # Productivity tips
        st.subheader("Productivity Tips")
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
        
        st.info(random.choice(productivity_tips))