import os
from typing import Dict

def get_markdown_content(topic: str) -> str:
    path = f"../data/knowledge/{topic}.md"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return None

def format_structured_answer(content: str) -> str:
    # A simple formatter that can be expanded to return structured JSON
    # For now, it returns the raw markdown from the file
    return content

# Template placeholders
def get_service_template(data: Dict) -> str:
    return f"""
# {data.get('title')}

## Overview
{data.get('overview')}

## Eligibility
{data.get('eligibility')}

## Benefits
{data.get('benefits')}

## Required Documents
{data.get('documents')}

## Application Steps
{data.get('steps')}

## Official Portal
{data.get('portal')}
"""
