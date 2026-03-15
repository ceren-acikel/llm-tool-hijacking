import os
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

tool_root_dir = f"{BASE_DIR}/data_example/toolenv/tool_jsons"
input_query_file = f"{BASE_DIR}/data_example/instruction/G2_query.json"
output_dir = f"{BASE_DIR}/toolbench/tooleval/results/q2_gpt-4o-mini_CoT"



os.makedirs(output_dir, exist_ok=True)


os.environ["RAPIDAPI_KEY"] = os.getenv("RAPIDAPI_KEY", "")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

if not os.environ["OPENAI_API_KEY"]:
    raise RuntimeError("OPENAI_API_KEY is missing. export OPENAI_API_KEY=...")

cmd = [
    "python3", "-m", "toolbench.inference.qa_pipeline",
    "--backbone_model", "chatgpt_function",
    "--openai_key", os.environ["OPENAI_API_KEY"],
    "--tool_root_dir", tool_root_dir,
    "--input_query_file", input_query_file,
    "--output_answer_file", output_dir,
    "--method", "CoT@1",
    "--use_rapidapi_key",
    "--rapidapi_key", os.environ["RAPIDAPI_KEY"],
]
env = os.environ.copy()
env["MALICIOUS_BEACON_FILE"] = str(BASE_DIR / "malicious_beacon_q2.jsonl")
print("Running ToolGPT pipeline...")
subprocess.run(cmd, check=True, env=env)