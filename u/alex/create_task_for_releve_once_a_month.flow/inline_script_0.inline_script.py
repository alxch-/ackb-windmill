from typing import TypedDict, Optional
from todoist_api_python.api import TodoistAPI
from datetime import datetime, date

class todoist(TypedDict):
    token: str

def main(
    todoist_resource: todoist,
    task_name: str,
    description: str = "",
    due_date: Optional[str] = None,
    project_id: Optional[str] = None
):
    """
    Create a new task in Todoist
    
    Args:
        todoist_resource: Todoist API token resource
        task_name: Name of the task
        description: Task description (optional)
        due_date: Due date in YYYY-MM-DD format (optional, defaults to today)
        project_id: Project ID where to create the task (optional, uses inbox if not specified)
    
    Returns:
        dict: Created task information
    """
    
    # Initialize the Todoist API client
    api = TodoistAPI(todoist_resource["token"])
    
    try:
        # Prepare task data
        task_data = {
            "content": task_name,
        }
        
        # Add description if provided
        if description:
            task_data["description"] = description
        
        # Set due date - use today if not provided or empty
        if not due_date:  # This handles None, empty string, etc.
            due_date = date.today().strftime("%Y-%m-%d")
        
        # Validate and add due date
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
            task_data["due_string"] = due_date
        except ValueError:
            raise ValueError("Due date must be in YYYY-MM-DD format")
        
        # Add project if provided
        if project_id:
            task_data["project_id"] = project_id
        
        # Create the task
        task = api.add_task(**task_data)
        
        return {
            "success": True,
            "task_id": task.id,
            "task_name": task.content,
            "description": task.description,
            "due_date": task.due.string if task.due else None,
            "project_id": task.project_id,
            "url": task.url,
            "created_at": task.created_at
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
