from fastmcp import FastMCP
import ngrok
from dotenv import load_dotenv
import os
import requests
from enum import Enum

load_dotenv()

mcp = FastMCP(
    name="pax-vulnerabilities-server",
    instructions="""
        This server scans local servers for security vulnerabilities.

        Available scan levels:
        - low: Quick reconnaissance (~2-5 seconds) - headers + basic endpoint discovery
        - medium: Standard scan (~10-30 seconds) - adds SQL injection + XSS testing
        - high: Full audit (~30-60+ seconds) - adds fuzzing + AI analysis

        Choose the appropriate level based on time constraints and thoroughness needed.
    """,
)


class ScanLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@mcp.tool()
async def scan(port_num: int, level: str = "medium") -> dict:
    """
    Scan a local port for security vulnerabilities.

    Args:
        port_num: The local port number where the server is running
        level: Scan intensity - "low" (fast), "medium" (standard), or "high" (comprehensive)

    Returns:
        Vulnerability scan results with findings categorized by severity
    """
    # Validate scan level
    valid_levels = ["low", "medium", "high"]
    if level not in valid_levels:
        return {
            "error": f"Invalid scan level '{level}'. Must be one of: {valid_levels}",
            "valid_levels": {
                "low": "Quick reconnaissance (~2-5 seconds)",
                "medium": "Standard vulnerability scan (~10-30 seconds)",
                "high": "Comprehensive audit with AI analysis (~30-60+ seconds)"
            }
        }

    listener = None
    try:
        # Create ngrok tunnel to expose local port
        listener = await ngrok.forward(port_num, authtoken_from_env=True)
        tunnel_url = listener.url()

        # Call the scanner API with the appropriate level
        scanner_url = f"https://vulnerability-scanner-three.vercel.app/scan/{level}/{tunnel_url}"
        response = requests.get(scanner_url, timeout=120)

        result = response.json()
        result["tunnel_url"] = tunnel_url
        result["local_port"] = port_num

        return result

    except requests.exceptions.Timeout:
        return {
            "error": "Scan timed out. Try a lower intensity scan level.",
            "port": port_num,
            "level": level
        }
    except Exception as e:
        return {
            "error": f"Error scanning for vulnerabilities: {str(e)}",
            "port": port_num,
            "level": level
        }
    finally:
        # Always close the ngrok tunnel after scanning
        if listener is not None:
            await listener.close()


@mcp.tool()
async def get_scan_options() -> dict:
    """
    Get available scan levels and their descriptions.

    Returns:
        Dictionary describing each scan level, what tests it includes, and estimated time.
    """
    return {
        "scan_levels": {
            "low": {
                "description": "Quick reconnaissance scan",
                "tests": ["security_headers", "quick_endpoint_discovery"],
                "estimated_time": "2-5 seconds",
                "use_case": "Fast initial assessment, time-constrained situations"
            },
            "medium": {
                "description": "Standard vulnerability testing",
                "tests": ["security_headers", "endpoint_discovery", "sql_injection", "xss"],
                "estimated_time": "10-30 seconds",
                "use_case": "Regular security checks, balanced thoroughness"
            },
            "high": {
                "description": "Comprehensive security audit",
                "tests": ["security_headers", "endpoint_discovery", "sql_injection", "xss", "fuzzing", "ai_analysis"],
                "estimated_time": "30-60+ seconds",
                "use_case": "Full security audit, production deployments"
            }
        },
        "recommendation": "Start with 'medium' for most cases. Use 'low' for quick checks, 'high' for thorough audits."
    }


def main():
    """Entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
