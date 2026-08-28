from langchain_core.tools import tool


@tool
def get_telecom_help(topic: str) -> str:
    """Provide basic telecom troubleshooting guidance."""

    knowledge = {
        "internet": "For slow mobile internet, check signal strength, mobile data settings, package status, and restart the device.",
        "sim": "For SIM problems, check whether the SIM is properly inserted and whether the network is available.",
        "call": "For call problems, check signal strength, airplane mode, SIM status, and network availability.",
    }

    topic = topic.lower()

    for key, answer in knowledge.items():
        if key in topic:
            return answer

    return "No specific telecom troubleshooting information was found."


@tool
def create_support_ticket(issue: str) -> str:
    """Create a simulated customer support ticket."""

    return (
        "Support ticket created successfully.\n\n"
        f"Issue: {issue}\n"
        "Status: Pending\n"
        "Priority: Normal"
    )