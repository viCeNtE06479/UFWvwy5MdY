# 代码生成时间: 2025-09-23 17:02:33
import json
def json_converter(json_data):    """
    Converts JSON data to Python objects.
    
    Parameters:
    json_data (str): JSON formatted string.
    
    Returns:
    dict or list: Python object representation of JSON data.
    Raises:
    json.JSONDecodeError: If the input is not valid JSON.
    """    try:        # Attempt to convert JSON string to Python object        python_object = json.loads(json_data)        return python_object    except json.JSONDecodeError as e:        # Handle JSON decoding errors        print(f"Error decoding JSON: {e}")        return None
def main():    # Example usage of json_converter    test_json_data = '''    {
        "name": "John",
        "age": 30,
        "city": "New York"
    }'''    result = json_converter(test_json_data)    if result is not None:        print("JSON data converted to Python object:",
              json.dumps(result, indent=4))    else:        print("Failed to convert JSON data to Python object.")
if __name__ == "__main__":    main()