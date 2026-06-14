
```python
import anthropic
import math


def calculate_circle_area(radius: float) -> float:
    """
    Calculate the area of a circle given its radius.
    
    Args:
        radius: The radius of the circle
        
    Returns:
        The area of the circle
        
    Raises:
        ValueError: If radius is negative
    """
    # Validate input using Claude
    client = anthropic.Anthropic()
    
    # Use Claude to validate the input
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": f"Is {radius} a valid radius value (must be non-negative)? Reply with only 'yes' or '