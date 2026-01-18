from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langgraph.prebuilt import ToolNode
from typing import List, Dict, Any, TypedDict
from config import AppConfig
from constants import GROQ_API_KEY
from logger import setup_logger
from enhanced_tools import (
    book_appointment,
    get_next_available_appointment,
    get_optimal_appointment_slots,
    suggest_alternative_slots,
    get_wait_time_prediction,
    get_busiest_times,
    get_least_busy_times,
    cancel_appointment,
    view_all_appointments
)

logger = setup_logger(__name__)

load_dotenv()

config = AppConfig()

llm = ChatGroq(model=config.LLM_MODEL, api_key=GROQ_API_KEY)
logger.info(f"LLM initialized with model: {llm}")

# Define tools list early for LLM binding
caller_tools = [
    book_appointment,
    get_next_available_appointment,
    get_optimal_appointment_slots,
    get_wait_time_prediction,
    get_busiest_times,
    get_least_busy_times,
    cancel_appointment
]

# Bind tools to LLM
llm_with_tools = llm.bind_tools(caller_tools)
logger.info(f"LLM bound with {len(caller_tools)} tools")

class AgentState(TypedDict):
    messages: List[Any]
    current_time: str

CONVERSATION: List[Any] = []

def receive_message_from_caller(message: str) -> None:
    logger.info(f"Received message: {message}")
    CONVERSATION.append(HumanMessage(content=message))
    state: AgentState = {
        "messages": CONVERSATION,
        "current_time": config.get_current_time()
    }
    logger.debug(f"State before invoke: {state}")
    try:
        new_state = caller_app.invoke(state)
        logger.debug(f"New state after invoke: {new_state}")
        CONVERSATION.extend(new_state["messages"][len(CONVERSATION):])
    except Exception as e:
        logger.exception(f"Error in receive_message_from_caller: {str(e)}")
        raise

def should_continue_caller(state: AgentState) -> str:
    logger.debug(f"Entering should_continue_caller with state: {state}")
    messages = state["messages"]
    if not messages:
        logger.warning("No messages in state")
        return "end"
    last_message = messages[-1]
    logger.debug(f"Last message type: {type(last_message)}, content: {last_message.content if hasattr(last_message, 'content') else 'N/A'}")
    
    # Check if message has tool_calls (indicates tools should be invoked)
    if isinstance(last_message, AIMessage) and hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        logger.info(f"Tool calls detected: {last_message.tool_calls}, continuing to action node")
        return "continue"
    # If message only has content (no tool calls), end the conversation
    elif isinstance(last_message, AIMessage) and last_message.content.strip() and not isinstance(last_message, ToolMessage):
        logger.info("AI message with content (no tool calls), ending conversation")
        return "end"
    # If last message is a ToolMessage, we need to go back to agent for synthesis
    elif hasattr(last_message, 'name') and last_message.name:  # ToolMessage has 'name' attribute
        logger.info("Tool message detected, returning to agent for synthesis")
        return "continue"
    else:
        logger.info("Other message type, continuing conversation")
        return "continue"

def call_caller_model(state: AgentState) -> AgentState:
    logger.debug(f"Entering call_caller_model with state: {state}")
    messages = state["messages"]
    current_time = state["current_time"]

    try:
        system_message = config.CALLER_PA_PROMPT.format(current_time=current_time)
        logger.debug(f"Formatted system message: {system_message}")

        formatted_messages = [
            SystemMessage(content=system_message)
        ]

        # Check if we have tool messages (results from tool execution)
        # If so, this is a synthesis step - don't bind tools to prevent new tool calls
        has_tool_messages = any(isinstance(m, ToolMessage) for m in messages)
        
        # Include all messages for context
        for m in messages:
            if isinstance(m, HumanMessage):
                formatted_messages.append(m)
            elif isinstance(m, AIMessage):
                # For synthesis step, include only content messages (not tool calls)
                # For initial request step, include everything
                if has_tool_messages:
                    if not (hasattr(m, 'tool_calls') and m.tool_calls):
                        formatted_messages.append(m)
                else:
                    formatted_messages.append(m)
            elif isinstance(m, ToolMessage):
                # Include tool messages as simple text
                formatted_messages.append(
                    HumanMessage(content=f"Tool results for {m.name}:\n{m.content}")
                )

        logger.debug(f"Formatted messages count: {len(formatted_messages)}")

        # For synthesis (when we have tool results), use LLM without tools
        # For initial request, use LLM with tools
        if has_tool_messages:
            logger.debug("Synthesis step - using LLM without tools")
            llm_response = llm.invoke(formatted_messages)  # Use base llm, not llm_with_tools
        else:
            logger.debug("Initial request step - using LLM with tools")
            llm_response = llm_with_tools.invoke(formatted_messages)

        logger.info(f"LLM response: {llm_response}")

        new_state = {"messages": messages + [llm_response], "current_time": current_time}
        logger.debug(f"New state after LLM response: {new_state}")
        return new_state

    except Exception as e:
        logger.exception(f"Error in call_caller_model: {str(e)}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return {
            "messages": messages + [
                AIMessage(content="I'm sorry, I encountered an error. Could you please try again?")
            ],
            "current_time": current_time
        }

def preprocess_llm_output(state: AgentState) -> AgentState:
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and last_message.content:
        content = last_message.content
        if "<tool_call>" in content:
            tool_call = content.split("<tool_call>")[1].split("</tool_call>")[0].strip()
            try:
                result = eval(tool_call)
                content = result
            except Exception as e:
                content = f"Error processing request: {str(e)}"
        state["messages"][-1] = AIMessage(content=content)
    return state

tool_node = ToolNode(caller_tools)
logger.info(f"Tools initialized: {len(caller_tools)} ML-enhanced tools")

# Graph
caller_workflow = StateGraph(AgentState)

# Add Nodes
caller_workflow.add_node("agent", call_caller_model)
caller_workflow.add_node("action", tool_node)

# Add Edges - from agent, decide if we have tool calls or end
caller_workflow.add_conditional_edges(
    "agent",
    should_continue_caller,
    {
        "continue": "action",  # Continue to action node if tool calls present
        "end": END,            # End if no tool calls
    },
)
# After tools are executed, go back to agent
caller_workflow.add_edge("action", "agent")

# Set Entry Point and build the graph
caller_workflow.set_entry_point("agent")

caller_app = caller_workflow.compile()
logger.info("Caller workflow compiled successfully")