"""LLM provider adapter TODO.

Keep provider-specific code behind this interface so the deployment can
switch between a local model and an approved enterprise provider.
"""

def generate_answer(question: str, context: list[dict]) -> str:
    # TODO: call a local/approved LLM. Treat retrieved text as untrusted data.
    raise NotImplementedError("Implement the LLM provider adapter")
