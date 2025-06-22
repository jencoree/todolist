import streamlit as st
from datetime import date
import base64
from collections import Counter
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(layout="wide")

def get_base64_of_file(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Backgrounds
main_bg = get_base64_of_file(r"C:\Users\jeniy\Downloads\sanrio.jpeg")
left_bg = get_base64_of_file(r"C:\Users\jeniy\Downloads\note.jpeg")
login_bg = main_bg

# ---------------- SESSION INIT ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# ---------------- LOGIN STYLING ----------------
def login_styles():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{login_bg}");
            background-size: cover;
            background-position: center;
        }}
        [data-testid="stHeader"]{{background-color: rgba(0, 0, 0, 0);}}
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(255, 255, 255, 0.85);
            z-index: -1;
        }}
        .stApp, .stApp * {{
            color: #9F2B68;
            font-family: 'Segoe UI', sans-serif;
        }}
        input[type="text"], input[type="password"], .stTextInput > div > div > input {{
            background-color: #F2D2BD !important;
            color: #9F2B68 !important;
            border-radius: 6px;
            border: 1.5px solid #9F2B68;
        }}
        button {{
            background-color: #F2D2BD !important;
            color: #9F2B68 !important;
            border-radius: 6px;
            font-weight: 600;
            border: 1.5px solid #9F2B68;
        }}
        button:hover {{
            background-color: #9F2B68 !important;
            color: white !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------- LOGIN PAGE ----------------
def login():
    login_styles()
    st.title("Login 𐙚⋆°.")


    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")

        if login_btn:
            if username == "jeni" and password == "sanrio123":
                st.session_state.logged_in = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password.")

if not st.session_state.logged_in:
    login()
    st.stop()

# ---------------- MAIN APP STYLING ----------------
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{main_bg}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}
    [data-testid="stHeader"]{{background-color: rgba(0, 0, 0, 0);}}
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left:  0;
        width: 100%;
        height: 100%;
        background-color: rgba(255,255,255,0.88);
        z-index: -1;
    }}
    .stApp, .stApp * {{
        color: #9F2B68;
        font-family: 'Segoe UI', sans-serif;
    }}
    input[type="text"], .stTextInput > div > div > input {{
        background-color: #F2D2BD !important;
        color: #9F2B68 !important;
        border-radius: 6px;
        border: 1.5px solid #9F2B68 ;
    }}
    div[data-baseweb="select"] > div > div {{
        background-color: #F2D2BD !important;
        color: #9F2B68 !important;
        border-radius: 6px;
        border: 1.5px solid #9F2B68 ;
    }}
    div[data-baseweb="select"] svg {{
        fill: #9F2B68 !important;
    }}
    button {{
        background-color: #F2D2BD !important;
        color: #9F2B68 !important;
        border-radius: 6px;
        font-weight: 600;
    }}
    button:hover {{
        background-color: #9F2B68 !important;
        color: white !important;
    }}
    .left-background {{
        background-image: url("data:image/jpeg;base64,{left_bg}");
        background-size: cover;
        background-position: center;
        border-radius: 15px;
        padding: 30px;
        min-height: 650px;
        overflow: auto;
        position: relative;
    }}
    .tasks-overlay {{
        background-color: rgba(255, 255, 255, 0.85);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        max-height: 620px;
        overflow-y: auto;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- TASK MANAGER ----------------
PRIORITY_LEVELS = ["High", "Medium", "Low"]
STATUS_OPTIONS = ["To Do", "Doing", "Almost Done", "Completed"]
CATEGORIES = ["Work", "School", "Personal", "Other"]
PRIORITY_ORDER = {level: i for i, level in enumerate(PRIORITY_LEVELS)}

left_col, right_col = st.columns([5, 5])

# PIE CHARTS IN LEFT PANEL
with left_col:
    if st.session_state.tasks:
        st.subheader("Task Summary 𐙚⋆°")

        priority_counts = Counter(task["priority"] for task in st.session_state.tasks)
        status_counts = Counter(task["status"] for task in st.session_state.tasks)

        st.markdown("**By Priority**")
        fig1, ax1 = plt.subplots(figsize=(1.2, 1.2), facecolor='none')
        ax1.set_facecolor('none')

        wedges1, _, _ = ax1.pie(
            priority_counts.values(),
            autopct='%1.1f%%',
            startangle=140,
            colors=["#9F2B68", "#B9558A", "#C973A1"],
            textprops={'fontsize': 5}
        )
        ax1.axis('equal')
        ax1.legend(
            wedges1,
            priority_counts.keys(),
            title="Priority",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),
            fontsize=5,
            title_fontsize=6,
            frameon=True
        )
        st.pyplot(fig1, clear_figure=True)

        st.markdown("**By Status**")
        fig2, ax2 = plt.subplots(figsize=(1.2, 1.2), facecolor='none')
        ax2.set_facecolor('none')

        wedges2, _, _ = ax2.pie(
            status_counts.values(),
            autopct='%1.1f%%',
            startangle=140,
            colors=["#9F2B68", "#B9558A", "#C973A1", "#E19DC1"],
            textprops={'fontsize': 5}
        )
        ax2.axis('equal')
        ax2.legend(
            wedges2,
            status_counts.keys(),
            title="Status",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),
            fontsize=5,
            title_fontsize=6,
            frameon=True
        )
        st.pyplot(fig2, clear_figure=True)

# RIGHT PANEL
with right_col:
    st.title("To-Do List 𐙚⋆°.")
    st.subheader("✚ Add New Task")

    with st.form("add_task_form", clear_on_submit=True):
        new_task = st.text_input("Task Description")
        new_priority = st.selectbox("Priority", PRIORITY_LEVELS)
        due_date = st.date_input("Due Date", value=date.today())
        status = st.selectbox("Status", STATUS_OPTIONS)
        category = st.selectbox("Category", CATEGORIES)
        add_btn = st.form_submit_button("Add Task")

        if add_btn:
            if new_task.strip():
                st.session_state.tasks.append({
                    "task": new_task.strip(),
                    "priority": new_priority,
                    "due_date": due_date,
                    "status": status,
                    "category": category
                })
                st.success("Task added successfully!")
            else:
                st.warning("Please enter a task description.")

    if st.button("⇕ Sort by Priority"):
        st.session_state.tasks.sort(key=lambda x: PRIORITY_ORDER[x["priority"]])
        st.success("Tasks sorted by priority.")
        st.rerun()

    st.subheader("🗒 Your Tasks")
    if not st.session_state.tasks:
        st.info("No tasks added yet.")
    else:
        updated_tasks = st.session_state.tasks.copy()
        task_to_update = None
        task_to_delete = None

        for idx, task in enumerate(st.session_state.tasks):
            col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 2, 0.8, 0.8])
            with col1:
                updated_task = st.text_input(f"Task {idx}", value=task["task"], key=f"text_{idx}")
            with col2:
                updated_priority = st.selectbox(f"Priority {idx}", PRIORITY_LEVELS, index=PRIORITY_LEVELS.index(task["priority"]), key=f"priority_{idx}")
            with col3:
                updated_date = st.date_input(f"Due {idx}", value=task["due_date"], key=f"date_{idx}")
            with col4:
                updated_status = st.selectbox(f"Status {idx}", STATUS_OPTIONS, index=STATUS_OPTIONS.index(task.get("status", "To Do")), key=f"status_{idx}")
            with col5:
                if st.button("✓", key=f"update_{idx}"):
                    task_to_update = idx
            with col6:
                if st.button("✗", key=f"delete_{idx}"):
                    task_to_delete = idx

            updated_tasks[idx] = {
                "task": updated_task.strip(),
                "priority": updated_priority,
                "due_date": updated_date,
                "status": updated_status,
                "category": task.get("category", "Other")
            }

        if task_to_update is not None:
            st.session_state.tasks[task_to_update] = updated_tasks[task_to_update]
            st.success(f"Task {task_to_update + 1} updated.")
            st.rerun()

        if task_to_delete is not None:
            st.session_state.tasks.pop(task_to_delete)
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
