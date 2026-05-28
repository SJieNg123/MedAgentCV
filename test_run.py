import os
import sys
from PIL import Image
from langchain_core.messages import AIMessage

# Monkey-patch ChatOpenAI before importing app/workflow to mock LLM calls
def mock_invoke(self, messages, *args, **kwargs):
    print(f"\n[Mock LLM] Invoked with prompt:\n---")
    for msg in messages:
        role = getattr(msg, "type", "message")
        print(f"{role.capitalize()}: {getattr(msg, 'content', str(msg))}")
    print("---\n")
    
    full_text = "\n".join([getattr(msg, "content", str(msg)) for msg in messages])
    
    if "consistency" in full_text.lower() or "reviewer" in full_text.lower():
        # This is the verify agent
        response_content = "CONSISTENT: The draft analysis supports the findings and is consistent with the description."
        print(f"[Mock LLM] Response (Verify Agent): {response_content}\n")
        return AIMessage(content=response_content)
    else:
        # This is the analytic agent
        response_content = "Draft Analysis: The chest X-ray was processed. No abnormalities were detected by the CV model, which is consistent with the patient showing no signs of acute disease."
        print(f"[Mock LLM] Response (Analytic Agent): {response_content}\n")
        return AIMessage(content=response_content)

# Apply monkey patch to ChatOpenAI
from langchain_openai import ChatOpenAI
ChatOpenAI.invoke = mock_invoke

# Ensure the app folder is in the python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.workflow.graph import compile_graph

def main():
    # 1. Create a dummy image
    dummy_image_path = "dummy_xray.png"
    img = Image.new("RGB", (640, 640), color="black")
    img.save(dummy_image_path)
    print(f"Created dummy image at {dummy_image_path}")

    try:
        # 2. Compile the graph
        print("Compiling LangGraph workflow...")
        graph = compile_graph()

        # 3. Define initial state
        initial_state = {
            "image_path": dummy_image_path,
            "disease_description": "The patient has aortic enlargement and pleural effusion.",
            "cv_tool_raw_output": "",
            "draft_analysis": "",
            "verification_feedback": "",
            "is_consistent": False,
            "iterations": 0,
            "messages": [],
        }

        # 4. Invoke the graph
        print("Invoking graph (this will trace to LangSmith)...")
        final_state = graph.invoke(initial_state)

        print("\n--- TEST RUN SUCCESSFUL ---")
        print("Final State Keys:", list(final_state.keys()))
        print("Is Consistent:", final_state.get("is_consistent"))
        print("Iterations:", final_state.get("iterations"))
        print("\nCV Tool Raw Output:\n", final_state.get("cv_tool_raw_output"))
        print("\nDraft Analysis:\n", final_state.get("draft_analysis"))
        print("\nVerification Feedback:\n", final_state.get("verification_feedback"))
    
    except Exception as e:
        print("\n--- TEST RUN FAILED ---")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        if os.path.exists(dummy_image_path):
            os.remove(dummy_image_path)
            print(f"Cleaned up {dummy_image_path}")

if __name__ == "__main__":
    main()
