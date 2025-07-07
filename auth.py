import streamlit as st
import bcrypt
import json
import os

class AuthSystem:
    def __init__(self):
        self.users_file = "users.json"
        self.init_default_users()
    
    def init_default_users(self):
        """Initialize default users if users file doesn't exist"""
        if not os.path.exists(self.users_file):
            default_users = {
                "admin": {
                    "password": self.hash_password("admin123"),
                    "role": "admin",
                    "name": "Administrator"
                },
                "teacher1": {
                    "password": self.hash_password("teacher123"),
                    "role": "teacher", 
                    "name": "Demo Teacher"
                },
                "student1": {
                    "password": self.hash_password("student123"),
                    "role": "student",
                    "name": "Demo Student",
                    "class": 10
                }
            }
            self.save_users(default_users)
    
    def hash_password(self, password):
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password, hashed):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def load_users(self):
        """Load users from JSON file"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_users(self, users):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def authenticate(self, username, password):
        """Authenticate user"""
        users = self.load_users()
        if username in users:
            if self.verify_password(password, users[username]["password"]):
                return users[username]
        return None
    
    def register_user(self, username, password, role, name, class_num=None):
        """Register new user"""
        users = self.load_users()
        if username in users:
            return False, "Username already exists"
        
        users[username] = {
            "password": self.hash_password(password),
            "role": role,
            "name": name
        }
        
        if role == "student" and class_num:
            users[username]["class"] = class_num
        
        self.save_users(users)
        return True, "User registered successfully"
    
    def get_all_users(self):
        """Get all users (admin only)"""
        return self.load_users()
    
    def delete_user(self, username):
        """Delete user (admin only)"""
        users = self.load_users()
        if username in users and username != "admin":
            del users[username]
            self.save_users(users)
            return True
        return False

    def update_user(self, username, name=None, password=None, role=None, class_num=None):
        """Update user details (admin only)"""
        users = self.load_users()
        if username not in users:
            return False, "User not found"
        if name:
            users[username]["name"] = name
        if password:
            users[username]["password"] = self.hash_password(password)
        if role and username != "admin":
            users[username]["role"] = role
        if role == "student" and class_num is not None:
            users[username]["class"] = class_num
        elif "class" in users[username] and (role != "student" or class_num is None):
            users[username].pop("class", None)
        self.save_users(users)
        return True, "User updated successfully"

def show_login():
    """Show login interface"""
    st.markdown("### 🔐 Login to Vidya Sakhi")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            auth = AuthSystem()
            user = auth.authenticate(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.user_role = user["role"]
                st.session_state.user_name = user["name"]
                st.session_state.name = user["name"]
                st.session_state.username = username
                if "class" in user:
                    st.session_state.selected_class = user["class"]
                st.success(f"Welcome {user['name']}!")
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    st.markdown("---")
    with st.expander("Register New Account"):
        show_register()

def show_register():
    """Show registration interface"""
    with st.form("register_form"):
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        name = st.text_input("Full Name")
        role = st.selectbox("Role", ["student", "teacher"])
        
        class_num = None
        if role == "student":
            class_num = st.selectbox("Class", list(range(3, 13)))
        
        register_submitted = st.form_submit_button("Register")
        
        if register_submitted:
            if new_password != confirm_password:
                st.error("Passwords don't match")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters")
            elif not new_username or not name:
                st.error("Please fill all fields")
            else:
                auth = AuthSystem()
                success, message = auth.register_user(new_username, new_password, role, name, class_num)
                if success:
                    st.success(message)
                else:
                    st.error(message)

def show_admin_panel():
    """Show admin panel"""
    st.markdown("### 👑 Admin Panel")
    
    auth = AuthSystem()
    users = auth.get_all_users()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Users Management")
        for username, user_data in users.items():
            with st.expander(f"{user_data['name']} ({username})"):
                st.write(f"**Role:** {user_data['role']}")
                if "class" in user_data:
                    st.write(f"**Class:** {user_data['class']}")
                # Edit form
                with st.form(f"edit_{username}"):
                    new_name = st.text_input("Full Name", value=user_data["name"], key=f"name_{username}")
                    new_password = st.text_input("New Password (leave blank to keep current)", type="password", key=f"pwd_{username}")
                    new_role = st.selectbox("Role", ["admin", "teacher", "student"], index=["admin", "teacher", "student"].index(user_data["role"]), key=f"role_{username}", disabled=(username=="admin"))
                    new_class = None
                    if new_role == "student":
                        new_class = st.number_input("Class", min_value=3, max_value=12, value=user_data.get("class", 10), key=f"class_{username}")
                    submitted = st.form_submit_button("Save Changes")
                    if submitted:
                        pw = new_password if new_password else None
                        result, msg = auth.update_user(username, name=new_name, password=pw, role=new_role, class_num=new_class)
                        if result:
                            st.success("User updated successfully!")
                            st.rerun()
                        else:
                            st.error(msg)
                if username != "admin" and st.button(f"Delete {username}", key=f"del_{username}"):
                    if auth.delete_user(username):
                        st.success(f"User {username} deleted")
                        st.rerun()
    
    with col2:
        st.markdown("#### System Statistics")
        total_users = len(users)
        students = sum(1 for u in users.values() if u['role'] == 'student')
        teachers = sum(1 for u in users.values() if u['role'] == 'teacher')
        admins = sum(1 for u in users.values() if u['role'] == 'admin')
        
        st.metric("Total Users", total_users)
        st.metric("Students", students)
        st.metric("Teachers", teachers)
        st.metric("Admins", admins)

def logout():
    """Logout user"""
    keys_to_remove = ['logged_in', 'username', 'user_role', 'user_name']
    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()