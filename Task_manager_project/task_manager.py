import flet as ft
from datetime import datetime
import json
import os

class TaskManager:
    def __init__(self, page: ft.Page):
        self.page = page
        self.tasks = []
        self.data_file = "tasks.json"
        self.load_tasks()
        
        # Configure page for accessibility
        self.page.title = "Task Manager"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = "#1e1e1e"
        self.page.padding = 20
        
        # Priority colors (high contrast for visibility)
        self.priority_colors = {
            "High": "#ff4444",      # Bright red
            "Medium": "#ffaa00",    # Bright orange
            "Low": "#44ff44",       # Bright green
            "None": "#888888"       # Gray
        }
        
        self.build_ui()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.tasks = json.load(f)
            except:
                self.tasks = []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)
    
    def build_ui(self):
        """Build the user interface"""
        # Header
        header = ft.Container(
            content=ft.Text(
                "Task Manager",
                size=32,
                weight=ft.FontWeight.BOLD,
                color="#ffffff"
            ),
            padding=ft.padding.only(bottom=20)
        )
        
        # Task input section
        self.task_input = ft.TextField(
            label="New Task",
            hint_text="Enter a new task...",
            expand=True,
            color="#ffffff",
            bgcolor="#2d2d2d",
            border_color="#555555",
            focused_border_color="#0078d4",
            text_size=16,
            autofocus=True
        )
        
        # Priority dropdown
        self.priority_dropdown = ft.Dropdown(
            label="Priority",
            options=[
                ft.dropdown.Option("None"),
                ft.dropdown.Option("Low"),
                ft.dropdown.Option("Medium"),
                ft.dropdown.Option("High"),
            ],
            value="None",
            width=200,
            color="#ffffff",
            bgcolor="#2d2d2d",
            border_color="#555555",
            focused_border_color="#0078d4",
            text_size=14
        )
        
        # Add button
        add_button = ft.ElevatedButton(
            "Add Task",
            icon="add",
            on_click=self.add_task,
            bgcolor="#0078d4",
            height=50,
            style=ft.ButtonStyle(
                color="#ffffff",
                shape=ft.RoundedRectangleBorder(radius=5)
            )
        )
        
        # Input row
        input_row = ft.Row(
            controls=[
                self.task_input,
                self.priority_dropdown,
                add_button
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START
        )
        
        # Filter section
        self.status_filter = ft.Dropdown(
            label="Status",
            options=[
                ft.dropdown.Option("All"),
                ft.dropdown.Option("Active"),
                ft.dropdown.Option("Completed"),
            ],
            value="All",
            width=150,
            color="#ffffff",
            bgcolor="#2d2d2d",
            border_color="#555555",
            focused_border_color="#0078d4",
            text_size=14,
            on_change=self.refresh_tasks
        )
        
        self.priority_filter = ft.Dropdown(
            label="Priority Filter",
            options=[
                ft.dropdown.Option("All"),
                ft.dropdown.Option("High"),
                ft.dropdown.Option("Medium"),
                ft.dropdown.Option("Low"),
                ft.dropdown.Option("None"),
            ],
            value="All",
            width=150,
            color="#ffffff",
            bgcolor="#2d2d2d",
            border_color="#555555",
            focused_border_color="#0078d4",
            text_size=14,
            on_change=self.refresh_tasks
        )
        
        # Filter row
        filter_row = ft.Row(
            controls=[
                self.status_filter,
                self.priority_filter,
            ],
            spacing=15,
            alignment=ft.MainAxisAlignment.START
        )
        
        # Tasks list
        self.tasks_column = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
        
        # Statistics
        self.stats_text = ft.Text(
            "",
            size=16,
            color="#aaaaaa",
            weight=ft.FontWeight.W_500
        )
        
        # Clear completed button
        clear_button = ft.OutlinedButton(
            "Clear Completed",
            icon="clear_all",
            on_click=self.clear_completed,
            style=ft.ButtonStyle(
                color="#ffffff",
                side=ft.BorderSide(1, "#555555")
            )
        )
        
        # Main layout
        self.page.add(
            header,
            input_row,
            ft.Divider(height=20, color="#444444"),
            filter_row,
            ft.Divider(height=10, color="#444444"),
            ft.Container(
                content=self.tasks_column,
                expand=True,
                padding=ft.padding.only(bottom=10)
            ),
            ft.Divider(height=20, color="#444444"),
            ft.Row(
                controls=[self.stats_text, clear_button],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )
        
        self.refresh_tasks()
    
    def add_task(self, e):
        """Add a new task"""
        task_text = self.task_input.value.strip()
        if task_text:
            priority = self.priority_dropdown.value or "None"
            task = {
                "id": len(self.tasks),
                "text": task_text,
                "completed": False,
                "priority": priority,
                "created": datetime.now().isoformat()
            }
            self.tasks.append(task)
            self.task_input.value = ""
            self.priority_dropdown.value = "None"
            self.save_tasks()
            self.refresh_tasks()
            self.page.update()
    
    def toggle_task(self, task_id):
        """Toggle task completion status"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = not task["completed"]
                break
        self.save_tasks()
        self.refresh_tasks()
        self.page.update()
    
    def delete_task(self, task_id):
        """Delete a task"""
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        # Reassign IDs
        for i, task in enumerate(self.tasks):
            task["id"] = i
        self.save_tasks()
        self.refresh_tasks()
        self.page.update()
    
    def clear_completed(self, e):
        """Remove all completed tasks"""
        self.tasks = [t for t in self.tasks if not t["completed"]]
        # Reassign IDs
        for i, task in enumerate(self.tasks):
            task["id"] = i
        self.save_tasks()
        self.refresh_tasks()
        self.page.update()
    
    def refresh_tasks(self, e=None):
        """Refresh the tasks display with filtering"""
        self.tasks_column.controls.clear()
        
        # Get filter values
        status_filter = self.status_filter.value or "All"
        priority_filter = self.priority_filter.value or "All"
        
        # Apply filters
        filtered_tasks = self.tasks.copy()
        
        # Apply status filter
        if status_filter == "Active":
            filtered_tasks = [t for t in filtered_tasks if not t["completed"]]
        elif status_filter == "Completed":
            filtered_tasks = [t for t in filtered_tasks if t["completed"]]
        
        # Apply priority filter
        if priority_filter != "All":
            filtered_tasks = [t for t in filtered_tasks if t["priority"] == priority_filter]
        
        # Sort tasks: incomplete first, then by priority
        def sort_key(task):
            priority_order = {"High": 0, "Medium": 1, "Low": 2, "None": 3}
            return (task["completed"], priority_order.get(task["priority"], 3))
        
        sorted_tasks = sorted(filtered_tasks, key=sort_key)
        
        for task in sorted_tasks:
            task_card = self.create_task_card(task)
            self.tasks_column.controls.append(task_card)
        
        # Update statistics
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t["completed"])
        remaining = total - completed
        filtered_count = len(filtered_tasks)
        
        if status_filter != "All" or priority_filter != "All":
            self.stats_text.value = f"Showing: {filtered_count} of {total} | Completed: {completed} | Remaining: {remaining}"
        else:
            self.stats_text.value = f"Total: {total} | Completed: {completed} | Remaining: {remaining}"
        
        if not filtered_tasks:
            empty_message = "No tasks match your filters."
            if status_filter == "All" and priority_filter == "All":
                empty_message = "No tasks yet. Add one above!"
            
            empty_state = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon("filter_list", size=64, color="#555555"),
                        ft.Text(
                            empty_message,
                            size=18,
                            color="#888888",
                            text_align=ft.TextAlign.CENTER
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10
                ),
                padding=40,
                alignment=ft.alignment.center
            )
            self.tasks_column.controls.append(empty_state)
        
        self.page.update()
    
    def create_task_card(self, task):
        """Create a task card UI element"""
        priority = task["priority"]
        priority_color = self.priority_colors.get(priority, "#888888")
        
        # Task text with strikethrough if completed
        task_text = ft.Text(
            task["text"],
            size=16,
            color="#ffffff" if not task["completed"] else "#888888",
            weight=ft.FontWeight.W_500 if not task["completed"] else ft.FontWeight.NORMAL,
            expand=True,
            selectable=True
        )
        
        if task["completed"]:
            task_text.style = ft.TextThemeStyle.BODY_MEDIUM
            # Add strikethrough effect
            task_text.value = f"✓ {task['text']}"
        
        # Priority badge
        priority_badge = ft.Container(
            content=ft.Text(
                priority,
                size=12,
                color="#ffffff",
                weight=ft.FontWeight.BOLD
            ),
            bgcolor=priority_color,
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
            border_radius=10,
            width=80,
            alignment=ft.alignment.center
        )
        
        # Checkbox
        checkbox = ft.Checkbox(
            value=task["completed"],
            on_change=lambda e, tid=task["id"]: self.toggle_task(tid),
            check_color="#ffffff",
            fill_color="#0078d4"
        )
        
        # Delete button
        delete_button = ft.IconButton(
            icon="delete",
            icon_color="#ff4444",
            tooltip="Delete task",
            on_click=lambda e, tid=task["id"]: self.delete_task(tid),
            icon_size=20
        )
        
        # Task card container
        card = ft.Container(
            content=ft.Row(
                controls=[
                    checkbox,
                    task_text,
                    priority_badge,
                    delete_button
                ],
                spacing=15,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            bgcolor="#2d2d2d",
            padding=15,
            border_radius=8,
            border=ft.border.all(1, "#444444"),
            margin=ft.margin.only(bottom=5)
        )
        
        return card


def main(page: ft.Page):
    """Main entry point"""
    # Set window properties
    page.window.width = 900
    page.window.height = 700
    page.window.min_width = 600
    page.window.min_height = 500
    page.window.title = "Task Manager"
    
    # Initialize task manager
    TaskManager(page)


if __name__ == "__main__":
    ft.app(target=main)

