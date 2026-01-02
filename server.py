from fastmcp import FastMCP
from dotenv import load_dotenv
import os
import requests
from enum import Enum
from typing import Optional

load_dotenv()

PAX_API_KEY = os.getenv("PAX_API_KEY")
REPORT_API_URL = "https://pax-report.vercel.app"

mcp = FastMCP(
    name="pax-report",
    instructions="""
        This server tracks development activity and generates personalized learning reports.

        Use the report_update tool every time you make a substantive update to the codebase.
        This includes:
        - Writing new code or features
        - Fixing bugs
        - Reviewing or refactoring code
        - Learning new concepts

        The updates are used to generate personalized tutorials tailored to the user's
        skill level and the concepts they've been working with.

        Examples of when to call report_update:
        - After implementing a new function or component
        - After fixing a bug or issue
        - After completing a code review
        - After refactoring existing code
        - After explaining or learning a new concept
    """,
)


class UpdateType(str, Enum):
    CODE_WRITTEN = "code_written"
    BUG_FIX = "bug_fix"
    CODE_REVIEW = "code_review"
    LEARNING = "learning"
    REFACTORING = "refactoring"


@mcp.tool()
async def report_update(
    update_type: str,
    description: str,
    files_changed: Optional[list[str]] = None,
    concepts: Optional[list[str]] = None,
    code_snippet: Optional[str] = None,
) -> dict:
    """
    Report a substantive development update for learning tracking.

    Call this tool every time you make a meaningful change to the codebase.
    Updates are used to generate personalized tutorials based on the user's
    skill level and demonstrated concepts.

    Args:
        update_type: Type of update - one of:
            - "code_written": New code, features, or components
            - "bug_fix": Bug fixes or issue resolutions
            - "code_review": Code review or analysis
            - "learning": New concept learned or explained
            - "refactoring": Code restructuring or improvements
        description: Brief description of what was done (1-3 sentences)
        files_changed: List of file paths that were modified (optional)
        concepts: List of programming concepts involved, e.g. ["async/await", "error handling"] (optional)
        code_snippet: Relevant code snippet if applicable (optional, max 500 chars)

    Returns:
        Confirmation of the update being recorded

    Examples:
        # After implementing a new feature
        report_update(
            update_type="code_written",
            description="Implemented user authentication with JWT tokens",
            files_changed=["src/auth/login.py", "src/auth/tokens.py"],
            concepts=["JWT", "authentication", "middleware"]
        )

        # After fixing a bug
        report_update(
            update_type="bug_fix",
            description="Fixed race condition in database connection pool",
            files_changed=["src/db/pool.py"],
            concepts=["concurrency", "connection pooling", "async"]
        )

        # After a code review
        report_update(
            update_type="code_review",
            description="Reviewed error handling patterns and suggested improvements",
            concepts=["error handling", "try/except", "logging"]
        )

        # After learning something new
        report_update(
            update_type="learning",
            description="Explained how React hooks work and when to use useEffect vs useMemo",
            concepts=["React hooks", "useEffect", "useMemo", "memoization"]
        )

        # After refactoring
        report_update(
            update_type="refactoring",
            description="Extracted common validation logic into reusable utility functions",
            files_changed=["src/utils/validation.py", "src/api/handlers.py"],
            concepts=["DRY principle", "utility functions", "code organization"]
        )
    """
    # Validate update type
    valid_types = ["code_written", "bug_fix", "code_review", "learning", "refactoring"]
    if update_type not in valid_types:
        return {
            "error": f"Invalid update_type '{update_type}'. Must be one of: {valid_types}",
            "valid_types": {
                "code_written": "New code, features, or components",
                "bug_fix": "Bug fixes or issue resolutions",
                "code_review": "Code review or analysis",
                "learning": "New concept learned or explained",
                "refactoring": "Code restructuring or improvements"
            }
        }

    # Build the payload
    payload = {
        "type": update_type,
        "description": description,
    }

    if files_changed:
        payload["files_changed"] = files_changed

    if concepts:
        payload["concepts"] = concepts

    if code_snippet:
        # Truncate code snippet if too long
        payload["code_snippet"] = code_snippet[:500] if len(code_snippet) > 500 else code_snippet

    try:
        # Call the report API
        response = requests.post(
            f"{REPORT_API_URL}/ingest/updates",
            json={
                "source": "claude-code",
                "payload": payload
            },
            headers={"Authorization": f"Bearer {PAX_API_KEY}"},
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            return {
                "success": True,
                "message": "Update recorded successfully",
                "update_id": result.get("update_id"),
                "update_type": update_type,
                "description": description
            }
        elif response.status_code == 401:
            return {
                "error": "Authentication failed. Check your PAX_API_KEY.",
                "status_code": response.status_code
            }
        else:
            return {
                "error": f"Failed to record update: {response.text}",
                "status_code": response.status_code
            }

    except requests.exceptions.Timeout:
        return {
            "error": "Request timed out while recording update.",
            "update_type": update_type
        }
    except Exception as e:
        return {
            "error": f"Error recording update: {str(e)}",
            "update_type": update_type
        }


@mcp.tool()
async def get_update_types() -> dict:
    """
    Get available update types and their descriptions.

    Returns:
        Dictionary describing each update type and when to use it.
    """
    return {
        "update_types": {
            "code_written": {
                "description": "New code, features, or components",
                "when_to_use": "After implementing new functionality, adding features, or creating new files",
                "example": "Implemented user registration form with validation"
            },
            "bug_fix": {
                "description": "Bug fixes or issue resolutions",
                "when_to_use": "After identifying and fixing a bug or resolving an issue",
                "example": "Fixed null pointer exception in user profile loader"
            },
            "code_review": {
                "description": "Code review or analysis",
                "when_to_use": "After reviewing code quality, patterns, or suggesting improvements",
                "example": "Reviewed authentication flow and identified security improvements"
            },
            "learning": {
                "description": "New concept learned or explained",
                "when_to_use": "After explaining a concept, answering questions, or teaching new skills",
                "example": "Explained async/await patterns and common pitfalls"
            },
            "refactoring": {
                "description": "Code restructuring or improvements",
                "when_to_use": "After reorganizing code, improving structure, or cleaning up",
                "example": "Extracted common API logic into shared utilities"
            }
        },
        "recommendation": "Call report_update after every substantive change to track learning progress."
    }


def main():
    """Entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
