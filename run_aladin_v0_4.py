from pathlib import Path
import json
from openai import OpenAI

ROOT = Path(__file__).resolve().parent
BRAIN_DIR = ROOT / "brain"

brain = (BRAIN_DIR / "ALADIN_BRAIN_V0_4.md").read_text()
examples = (BRAIN_DIR / "examples.md").read_text()
context = (BRAIN_DIR / "context.md").read_text()
decision_spec = json.loads((BRAIN_DIR / "decision_spec_v0_2.json").read_text())

client = OpenAI()

print("ALADIN v0.4")
print("Paste the NEW business/creator information you want diagnosed.")
print("Aladin already has the persistent context in context.md.")
print("Default mode is Ultra-Concise Decision Mode.")
print("If you want the full reasoning layer, include: AUDIT MODE")
print("When finished, type END on its own line.")
print()

lines = []
while True:
    line = input()
    if line.strip() == "END":
        break
    lines.append(line)

case_input = "\n".join(lines).strip()

instructions = f"""
You are ALADIN, a business constraint-diagnosis system.

Use these four layers:

1. MASTER BRAIN
{brain}

2. WORKED EXAMPLES
{examples}

3. PERSISTENT CONTEXT
{context}

4. CURRENT INPUT
The user's new case is provided separately.

Rules:
- Persistent context is background knowledge, not automatically current evidence.
- If current input conflicts with older context, current input wins.
- Separate facts, interpretations, and hypotheses.
- Do not invent information.
- Diagnose one primary constraint.
- Preserve what is already working.
- Recommend one main change now.
- Think deeply, but default to Ultra-Concise Decision Mode unless the user explicitly requests AUDIT MODE.
- The default user-facing answer should be approximately 75–150 words and should prioritize:
  1. Bottleneck
  2. Fix Now
  3. Proof
  4. Watch For
- Use the decision specification below as the output contract.

DECISION SPEC:
{json.dumps(decision_spec, indent=2)}
"""

response = client.responses.create(
    model="gpt-5.6-terra",
    instructions=instructions,
    input=case_input
)

print()
print(response.output_text)
