import time
import csv
import os

from langchain_core.messages import BaseMessage

from backend.prompts.system_prompt import build_user_message
from backend.rag.embeddings import get_embedding_model
from backend.rag.retriever import Retriever
from backend.llm.ollama import LLMService
from backend.exceptions import DocumentNotFoundError


def check_message_type():
    """
    Sanity check: LLMService.invoke() requires a list[BaseMessage].
    Fail loudly here instead of deep inside a 30-question benchmark run.
    """
    sample = build_user_message(context="sample context", question="sample question")
    if not isinstance(sample, BaseMessage):
        raise TypeError(
            f"build_user_message() returned {type(sample)}, not a BaseMessage "
            f"(e.g. HumanMessage). LLMService.invoke() expects list[BaseMessage] — "
            f"wrap the return value accordingly before running the benchmark."
        )
    print(f"build_user_message() returns {type(sample).__name__} — OK")


def warm_up_model(llm_service: LLMService, model_name: str):
    """
    Trigger ChatOllama client initialization (and first-call overhead)
    outside the timed benchmark loop, so client-caching cost doesn't
    leak into the first question's generation_s.
    """
    print(f"Warming up model: {model_name} ...")
    t0 = time.time()
    llm_service.get_client(model_name)  # initializes + caches the client
    print(f"Warm-up client init took {time.time() - t0:.3f}s (excluded from results)")


def warm_up_embedding_model():
    """
    First call to the embedding model pays a one-time weight-loading cost
    (seen as ~2s vs ~0.01s on subsequent calls). Absorb that here so it
    doesn't distort the first benchmarked question's embedding_s.
    """
    print("Warming up embedding model ...")
    t0 = time.time()
    get_embedding_model().embed_query("warm up query")
    print(f"Warm-up embedding load took {time.time() - t0:.3f}s (excluded from results)")


def query_rag(question: str, retriever: Retriever, llm_service: LLMService,
              collection_name: str, model_name: str, k: int = 4):
    t0 = time.time()

    # Isolated embedding timing (note: Retriever.retrieve() re-embeds internally,
    # so this measures embedding cost in isolation, not as an extra pipeline step)
    _ = get_embedding_model().embed_query(question)
    t1 = time.time()

    try:
        documents = retriever.retrieve(
            collection_name=collection_name,
            query=question,
            k=k,
        )
    except DocumentNotFoundError:
        print(f"No documents found for question: {question!r} — skipping")
        return None, None
    t2 = time.time()

    context = "\n\n".join(doc.page_content for doc in documents)
    response = llm_service.invoke(
        messages=[build_user_message(context=context, question=question)],
        model_name=model_name,
    )
    t3 = time.time()

    timings = {
        "question": question,
        "embedding_s": round(t1 - t0, 3),
        "retrieval_s": round(t2 - t1, 3),
        "generation_s": round(t3 - t2, 3),
        "total_s": round(t3 - t0, 3),
        "num_chunks_retrieved": len(documents),
    }
    print(
        f"Embedding: {timings['embedding_s']}s | Retrieval: {timings['retrieval_s']}s | "
        f"Generation: {timings['generation_s']}s | Total: {timings['total_s']}s | "
        f"Chunks: {timings['num_chunks_retrieved']}"
    )
    return response, timings


if __name__ == "__main__":
    check_message_type()  # fail fast if build_user_message() has the wrong return type

    retriever = Retriever()
    llm_service = LLMService()
    collection_name = "a2_b3_33_dp_pract01"
    model_name = "llama3.2"

    warm_up_embedding_model()
    warm_up_model(llm_service, model_name)  # exclude client-init cost from results

    test_questions = [
        # --- Broad / overview questions (known working, hit the needs_broad_context() path) ---
        "tell me about what is in this file",
        "summarize the contents of this file",
        "what is this document about",
        "what does this file contain",
        "give me an overview of this document",
        "list the main points in this document",
        "what are the key requirements mentioned",

        # --- Narrow / specific questions ---
        # TODO: replace each placeholder below with a real question about actual
        # content in a2_b3_33_dp_pract01 (a heading, term, section number, etc.)
        # so retrieval has something specific to match against.
        "What does section 1 of this document cover?",
        "What does section 2 of this document cover?",
        "Explain the term mentioned in the first paragraph.",
        "What is defined in the introduction?",
        "What steps are described in this document?",
        "What examples are given in this document?",
        "What conclusion does this document reach?",
        "What tools or technologies are mentioned in this document?",
        "What definitions are provided in this document?",
        "What is the purpose stated in this document?",
        "What data or figures are referenced in this document?",
        "What recommendations are made in this document?",
        "What limitations are discussed in this document?",
    ]

    all_timings = []
    for q in test_questions:
        _, timings = query_rag(q, retriever, llm_service, collection_name, model_name)
        if timings:
            all_timings.append(timings)

    if not all_timings:
        print("No successful queries to report on.")
    else:
        os.makedirs("results", exist_ok=True)  # ensuring output directory exists before writing
        with open("results/benchmark_results.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=all_timings[0].keys())
            writer.writeheader()
            writer.writerows(all_timings)

        avg_total = sum(t["total_s"] for t in all_timings) / len(all_timings)
        avg_retrieval = sum(t["retrieval_s"] for t in all_timings) / len(all_timings)
        avg_generation = sum(t["generation_s"] for t in all_timings) / len(all_timings)
        print(f"\nAcross {len(all_timings)} queries:")
        print(f"  Average total:      {avg_total:.3f}s")
        print(f"  Average retrieval:  {avg_retrieval:.3f}s")
        print(f"  Average generation: {avg_generation:.3f}s")