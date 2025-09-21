# 代码生成时间: 2025-09-22 02:17:13
import bleach
from celery import Celery
from celery.signals import after_task_publish
from celery.signals import task_failure

# Celery app configuration
app = Celery('xss_protection', broker='pyamqp://guest@localhost//')

# Celery configuration to avoid duplicate tasks
app.conf.duplicate_job = 'ignore'

# Celery task to sanitize input to prevent XSS attacks
@app.task
def sanitize_input(input_data):
    """
    Sanitizes the input data to prevent XSS attacks by stripping out
    executable scripts and dangerous HTML tags.
    
    Parameters:
        input_data (str): The input data to be sanitized.
    
    Returns:
        str: The sanitized input data.
    
    Raises:
        Exception: If any error occurs during sanitization.
    """
    try:
        # Use bleach library to sanitize input data
        sanitized_data = bleach.clean(input_data)
        return sanitized_data
    except Exception as e:
        # Log the error and re-raise it
        raise Exception(f"Failed to sanitize input data: {str(e)}")

# Register signal handler for task failure
@task_failure.connect
def handle_task_failure(sender=None, task_id=None, exception=None, **kwargs):
    # Handle task failure and log the error
    print(f"Task {task_id} failed with error: {str(exception)}")

# Register signal handler for after task publish
@after_task_publish.connect
def handle_after_task_publish(sender=None, body=None, exchange=None, routing_key=None, **kwargs):
    # Log the task publish event
    print(f"Task published to {exchange} with routing key {routing_key}")

# Example usage of the sanitize_input task
if __name__ == '__main__':
    # Simulate some input data that could potentially contain XSS
    potentially_harmful_input = "<script>alert('XSS')</script>"
    
    # Call the sanitize_input task to clean the input data
    sanitized_data = sanitize_input.delay(potentially_harmful_input)
    
    # Wait for the task to complete and get the result
    sanitized_result = sanitized_data.get()
    
    # Print the sanitized result
    print(f"Sanitized Input: {sanitized_result}")
