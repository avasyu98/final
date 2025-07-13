def write_prompt(topic):
    """Create a prompt for AI image generation from the topic."""
    return (f"Create a vibrant, eye-catching image about: '{topic['title']}'. "
            f"Category: {topic['category']}. Description: {topic.get('description', '')}. "
            "Style: modern, social-media ready, with clear visual storytelling.")