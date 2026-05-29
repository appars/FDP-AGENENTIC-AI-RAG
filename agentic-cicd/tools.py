from langchain.tools import tool

@tool
def read_logs(log_path: str) -> str:
    """Read Jenkins test logs"""
    with open(log_path, "r") as f:
        return f.read()

@tool
def retry_recommendation(error_text: str) -> str:
    """Check whether retry is useful"""
    flaky_keywords = [
        "timeout",
        "connection",
        "network"
    ]

    for word in flaky_keywords:
        if word in error_text.lower():
            return "RETRY"

    return "STOP"
