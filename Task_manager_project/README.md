# Task Manager - Desktop Application

A user-friendly desktop task manager application with priority levels, designed with accessibility in mind. Features a dark theme with high-contrast white text for optimal visibility.

## Features

- ✅ Add, complete, and delete tasks
- 🎯 Priority levels: High, Medium, Low, and None
- 🌙 Dark theme with high-contrast white text
- 💾 Automatic task persistence (saves to `tasks.json`)
- 📊 Task statistics (total, completed, remaining)
- 🧹 Clear all completed tasks at once
- ♿ Accessible design with large, clear text and high contrast

## Installation

1. Make sure you have Python 3.8 or higher installed on your system.

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Simply run:
```bash
python task_manager.py
```

The application will open in a new window.

## Usage

### Adding a Task
1. Type your task in the "New Task" field
2. (Optional) Select a priority level from the dropdown
3. Click "Add Task" or press Enter

### Managing Tasks
- **Complete a task**: Check the checkbox next to the task
- **Delete a task**: Click the red delete icon
- **Clear completed**: Click the "Clear Completed" button to remove all completed tasks

### Priority Levels
- **High**: Red badge - for urgent tasks
- **Medium**: Orange badge - for important tasks
- **Low**: Green badge - for less urgent tasks
- **None**: Gray badge - no priority

Tasks are automatically sorted with incomplete tasks first, then by priority level.

## Accessibility Features

- Dark background (#1e1e1e) with white text for high contrast
- Large, readable fonts (16px for task text, 32px for header)
- Clear visual indicators for priority levels
- Keyboard-friendly interface
- Selectable text for screen readers

## Data Storage

Tasks are automatically saved to `tasks.json` in the same directory as the application. This file is created automatically when you add your first task.

## Requirements

- Python 3.8+
- flet library (installed via requirements.txt)

## Troubleshooting

If you encounter any issues:
1. Make sure Python 3.8+ is installed
2. Verify all dependencies are installed: `pip install -r requirements.txt`
3. Check that you have write permissions in the application directory (for saving tasks)

