# utils/pr_reviewer.py
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.config import OPENAI_API_KEY
import re

# Initialize the LLM
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.3)

# Create a prompt template for PR review
review_template = """
You are an expert code reviewer. Analyze the following code changes in a pull request and provide constructive feedback.

Repository: {repo}
Pull Request: #{pr_number}
Title: {pr_title}
Description: {pr_description}

Files Changed:
{file_changes}

Review Guidelines:
1. Identify potential bugs or issues
2. Suggest performance improvements
3. Check for security vulnerabilities
4. Evaluate code readability and maintainability
5. Ensure consistency with the project's coding standards

Provide your review in the following format:
## Summary
[Brief summary of your overall assessment]

## Issues Found
[List any issues found, with file paths and line numbers if possible]

## Suggestions
[Provide specific suggestions for improvement]

## Positive Notes
[Mention any positive aspects of the changes]

Review:
"""

review_prompt = ChatPromptTemplate.from_template(review_template)

# Create the chain
review_chain = review_prompt | llm | StrOutputParser()

def format_file_changes(files):
    """Format file changes for the prompt."""
    formatted = ""
    for file in files:
        formatted += f"\n### File: {file['filename']}\n"
        formatted += f"Status: {file['status']}\n"
        formatted += f"Changes: {file['additions']} additions, {file['deletions']} deletions\n"
        
        # Include a snippet of the diff
        if 'patch' in file:
            # Limit the diff size to avoid token limits
            diff_lines = file['patch'].split('\n')
            if len(diff_lines) > 50:
                formatted += "```diff\n" + '\n'.join(diff_lines[:25]) + "\n...\n" + '\n'.join(diff_lines[-25:]) + "\n```\n"
            else:
                formatted += "```diff\n" + file['patch'] + "\n```\n"
        formatted += "\n"
    return formatted

def generate_pr_review(repo, pr_number, pr_title, pr_description, files):
    """Generate a review for a pull request."""
    file_changes = format_file_changes(files)
    
    review = review_chain.invoke({
        "repo": repo,
        "pr_number": pr_number,
        "pr_title": pr_title,
        "pr_description": pr_description,
        "file_changes": file_changes
    })
    
    return review

def extract_line_comments(review):
    """Extract line-specific comments from the review."""
    # This is a simple implementation that looks for patterns like "File: path, Line: number"
    line_comments = []
    
    # Pattern to match file and line references
    pattern = r"File:\s*([^\s,]+),\s*Line:\s*(\d+)"
    
    for match in re.finditer(pattern, review):
        file_path = match.group(1)
        line_number = int(match.group(2))
        
        # Extract the comment text (this is simplified)
        start_pos = match.end()
        end_pos = review.find("\n\n", start_pos)
        if end_pos == -1:
            end_pos = len(review)
        
        comment_text = review[start_pos:end_pos].strip()
        
        line_comments.append({
            "file": file_path,
            "line": line_number,
            "comment": comment_text
        })
    
    return line_comments