from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List, Dict, Any
from langgraph.graph.message import add_messages
import streamlit as st
from rag_assistants import (
    EmployeeAssistant, 
    EngineeringAssistant, 
    FinanceAssistant, 
    HRAssistant, 
    MarketingAssistant,
    CLevelAssistant
)
from conversation_memory import get_conversation_memory

class ConversationState(TypedDict):
    """Enhanced state with conversation memory"""
    messages: Annotated[List, add_messages]
    user_role: str
    user_id: int
    user_name: str
    query: str
    response: str
    conversation_context: str
    enhanced_query: str
    memory_stats: Dict[str, Any]
    session_id: str

class RoleBasedRAGWorkflow:
    """Enhanced RAG workflow with advanced conversation memory"""
    
    def __init__(self):
        self.workflow = StateGraph(ConversationState)
        self.assistants = {
            'Employee': EmployeeAssistant(),
            'Engineering': EngineeringAssistant(),
            'Finance': FinanceAssistant(),
            'HR': HRAssistant(),
            'Marketing': MarketingAssistant(),
            'C-Level': CLevelAssistant()
        }
        self._build_workflow()

    def _build_workflow(self):
        """Build the enhanced LangGraph workflow with memory"""
        # Add nodes
        self.workflow.add_node("memory_initialization", self.initialize_memory)
        self.workflow.add_node("query_enhancement", self.enhance_query_with_memory)
        self.workflow.add_node("role_routing", self.determine_role_route)
        self.workflow.add_node("employee_assistant", self.employee_assistant)
        self.workflow.add_node("engineering_assistant", self.engineering_assistant)
        self.workflow.add_node("finance_assistant", self.finance_assistant)
        self.workflow.add_node("hr_assistant", self.hr_assistant)
        self.workflow.add_node("marketing_assistant", self.marketing_assistant)
        self.workflow.add_node("clevel_assistant", self.clevel_assistant)
        self.workflow.add_node("memory_update", self.update_conversation_memory)

        # Set entry point
        self.workflow.set_entry_point("memory_initialization")

        # Linear flow for memory management
        self.workflow.add_edge("memory_initialization", "query_enhancement")
        self.workflow.add_edge("query_enhancement", "role_routing")

        # Conditional routing from role_routing to specific assistants
        self.workflow.add_conditional_edges(
            "role_routing",
            self.route_to_assistant,
            {
                "Employee": "employee_assistant",
                "Engineering": "engineering_assistant",
                "Finance": "finance_assistant",
                "HR": "hr_assistant",
                "Marketing": "marketing_assistant",
                "C-Level": "clevel_assistant"
            }
        )

        # All assistants flow to memory update
        self.workflow.add_edge("employee_assistant", "memory_update")
        self.workflow.add_edge("engineering_assistant", "memory_update")
        self.workflow.add_edge("finance_assistant", "memory_update")
        self.workflow.add_edge("hr_assistant", "memory_update")
        self.workflow.add_edge("marketing_assistant", "memory_update")
        self.workflow.add_edge("clevel_assistant", "memory_update")

        # Memory update ends the workflow
        self.workflow.add_edge("memory_update", END)

        # Compile the workflow
        self.app = self.workflow.compile()

    def initialize_memory(self, state: ConversationState) -> ConversationState:
        """Initialize conversation memory for the user session"""
        print(f"Initializing memory for user {state['user_id']}, session {state.get('session_id', 'default')}")
        
        # Get or create conversation memory
        memory = get_conversation_memory(
            state['user_id'], 
            state.get('session_id', 'default')
        )
        
        # Get current conversation context
        state['conversation_context'] = memory.get_conversation_context()
        state['memory_stats'] = memory.get_memory_stats()
        
        print(f"Memory initialized: {len(state['conversation_context'])} chars of context")
        return state

    def enhance_query_with_memory(self, state: ConversationState) -> ConversationState:
        """Enhance user query with conversation memory"""
        memory = get_conversation_memory(
            state['user_id'], 
            state.get('session_id', 'default')
        )
        
        # Enhance query with conversation context
        state['enhanced_query'] = memory.enhance_query_with_context(state['query'])
        
        print(f"Query enhanced: {len(state['enhanced_query'])} chars total")
        return state

    def determine_role_route(self, state: ConversationState) -> ConversationState:
        """Prepare for role-based routing"""
        print(f"Routing query for role: {state['user_role']}")
        return state

    def route_to_assistant(self, state: ConversationState) -> str:
        """Route to appropriate assistant based on user role"""
        return state['user_role']

    def employee_assistant(self, state: ConversationState) -> ConversationState:
        """Handle Employee queries with enhanced context"""
        try:
            print("Processing Employee query with enhanced context...")
            enhanced_query = state.get('enhanced_query', state['query'])
            response = self.assistants['Employee'].get_response(enhanced_query)
            state['response'] = response
        except Exception as e:
            print(f"Employee assistant error: {e}")
            state['response'] = f"📋 **Employee Assistant Error:** An error occurred while processing your request: {str(e)}"
        return state

    def engineering_assistant(self, state: ConversationState) -> ConversationState:
        """Handle Engineering queries with enhanced context"""
        try:
            print("Processing Engineering query with enhanced context...")
            enhanced_query = state.get('enhanced_query', state['query'])
            response = self.assistants['Engineering'].get_response(enhanced_query)
            state['response'] = response
        except Exception as e:
            print(f"Engineering assistant error: {e}")
            state['response'] = f"🔧 **Engineering Assistant Error:** An error occurred while processing your request: {str(e)}"
        return state

    def finance_assistant(self, state: ConversationState) -> ConversationState:
        """Handle Finance queries with enhanced context"""
        try:
            print("Processing Finance query with enhanced context...")
            enhanced_query = state.get('enhanced_query', state['query'])
            response = self.assistants['Finance'].get_response(enhanced_query)
            state['response'] = response
        except Exception as e:
            print(f"Finance assistant error: {e}")
            state['response'] = f"💰 **Finance Assistant Error:** An error occurred while processing your request: {str(e)}"
        return state

    def hr_assistant(self, state: ConversationState) -> ConversationState:
        """Handle HR queries with enhanced context"""
        try:
            print("Processing HR query with enhanced context...")
            enhanced_query = state.get('enhanced_query', state['query'])
            response = self.assistants['HR'].get_response(enhanced_query)
            state['response'] = response
        except Exception as e:
            print(f"HR assistant error: {e}")
            state['response'] = f"👥 **HR Assistant Error:** An error occurred while processing your request: {str(e)}"
        return state

    def marketing_assistant(self, state: ConversationState) -> ConversationState:
        """Handle Marketing queries with enhanced context"""
        try:
            print("Processing Marketing query with enhanced context...")
            enhanced_query = state.get('enhanced_query', state['query'])
            response = self.assistants['Marketing'].get_response(enhanced_query)
            state['response'] = response
        except Exception as e:
            print(f"Marketing assistant error: {e}")
            state['response'] = f"📈 **Marketing Assistant Error:** An error occurred while processing your request: {str(e)}"
        return state

    def clevel_assistant(self, state: ConversationState) -> ConversationState:
        """Handle C-Level Executive queries with enhanced context"""
        try:
            print("Processing C-Level query with enhanced context...")
            enhanced_query = state.get('enhanced_query', state['query'])
            response = self.assistants['C-Level'].get_response(enhanced_query)
            state['response'] = response
        except Exception as e:
            print(f"C-Level assistant error: {e}")
            state['response'] = f"🏢 **C-Level Assistant Error:** An error occurred while processing your request: {str(e)}"
        return state

    def update_conversation_memory(self, state: ConversationState) -> ConversationState:
        """Update conversation memory with the new turn"""
        try:
            print("Updating conversation memory...")
            memory = get_conversation_memory(
                state['user_id'], 
                state.get('session_id', 'default')
            )
            
            # Add the conversation turn to memory
            memory.add_turn(state['query'], state['response'])
            
            # Update memory stats
            state['memory_stats'] = memory.get_memory_stats()
            print(f"Memory updated: {state['memory_stats']}")
            
        except Exception as e:
            print(f"Error updating conversation memory: {e}")
        
        return state

    def process_query(self, user_role: str, user_id: int, user_name: str, query: str, session_id: str = "default") -> Dict[str, Any]:
        """Process a user query through the enhanced workflow"""
        initial_state = {
            'messages': [],
            'user_role': user_role,
            'user_id': user_id,
            'user_name': user_name,
            'query': query,
            'response': '',
            'conversation_context': '',
            'enhanced_query': '',
            'memory_stats': {},
            'session_id': session_id
        }
        
        print(f"Processing query for {user_name} ({user_role}): {query[:100]}...")
        result = self.app.invoke(initial_state)
        
        return {
            'response': result['response'],
            'memory_stats': result.get('memory_stats', {}),
            'conversation_context': result.get('conversation_context', ''),
            'session_id': session_id
        }

# Global workflow instance
workflow_instance = None

def get_workflow():
    """Get or create workflow instance"""
    global workflow_instance
    if workflow_instance is None:
        print("Creating new RAG workflow instance...")
        workflow_instance = RoleBasedRAGWorkflow()
        print("RAG workflow initialized successfully")
    return workflow_instance

def clear_conversation_session(user_id: int, session_id: str = "default"):
    """Clear conversation memory for a user session"""
    from conversation_memory import clear_conversation_memory
    clear_conversation_memory(user_id, session_id)
    print(f"Cleared conversation session for user {user_id}, session {session_id}")
