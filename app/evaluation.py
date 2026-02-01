def evaluate_answer(question, context, answer):
    results = {}

    # 1️⃣ Did retrieval return something?
    results["has_context"] = bool(context.strip())

    # 2️⃣ Did model refuse appropriately?
    results["answered"] = answer.strip().lower() != "i don't know"

    # 3️⃣ Is answer grounded in context (simple heuristic)
    overlap = any(word.lower() in context.lower() for word in answer.split())
    results["grounded"] = overlap

    return results
