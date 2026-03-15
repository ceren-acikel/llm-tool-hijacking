from sentence_transformers import SentenceTransformer, util
import json
import pandas as pd
from collections import defaultdict
import torch
from tqdm import tqdm
import argparse
import os
from datetime import datetime


def build_retrieval_text(doc: dict, desc_max_chars: int = 300, schema_max_chars: int = 800) -> str:

    def _s(x):
        return x if isinstance(x, str) else ("" if x is None else str(x))

    def _trunc(s: str, n: int) -> str:
        s = _s(s)
        return s if len(s) <= n else s[:n]

    category = _s(doc.get("category_name", "") or "")
    tool_name = _s(doc.get("tool_name", "") or "")
    api_name = _s(doc.get("api_name", "") or "")

    api_desc = _trunc(_s(doc.get("api_description", "") or ""), desc_max_chars)
    tool_desc = _trunc(_s(doc.get("tool_description", "") or doc.get("tool_desc", "") or doc.get("description", "") or ""), desc_max_chars)

    required_params = _trunc(json.dumps(doc.get("required_parameters", ""), ensure_ascii=False), schema_max_chars)
    optional_params = _trunc(json.dumps(doc.get("optional_parameters", ""), ensure_ascii=False), schema_max_chars)
    return_schema = _trunc(json.dumps(doc.get("template_response", ""), ensure_ascii=False), schema_max_chars)

    return (
        f"{category}, {tool_name}, {api_name}, "
        f"tool_description: {tool_desc}, "
        f"api_description: {api_desc}, "
        f"required_params: {required_params}, "
        f"optional_params: {optional_params}, "
        f"return_schema: {return_schema}"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("model_path", type=str, help="Your trained model path")
    parser.add_argument("dataset_path", type=str, help="The processed dataset files path")
    parser.add_argument("--top_k", type=int, default=5, help="Top-k retrieval depth")
    parser.add_argument("--log_jsonl", type=str, default="retrieval_topk.jsonl", help="Where to write per-query top-k logs (JSONL)")
    parser.add_argument("--out_json", type=str, default="topk_results_with_matches.json", help="Where to write aggregated results (JSON)")
    parser.add_argument("--use_full_retrieval_text", action="store_true",
                        help="If set, embed the same retrieval_text used in process_retrieval_ducoment (includes descriptions/params).")
    args = parser.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = SentenceTransformer(args.model_path, device=device)

    documents_df = pd.read_csv(os.path.join(args.dataset_path, "corpus.tsv"), sep="\t")
    test_queries_df = pd.read_csv(
        os.path.join(args.dataset_path, "test.query.txt"),
        sep="\t",
        names=["qid", "query_text"],
    )
    test_labels_df = pd.read_csv(
        os.path.join(args.dataset_path, "qrels.test.tsv"),
        sep="\t",
        names=["qid", "useless", "docid", "label"],
    )

    # Build corpus maps
    
    corpus_docs = {}
    for _, row in documents_df.iterrows():
        corpus_docs[str(row.docid)] = json.loads(row.document_content)

    ir_test_queries = {str(row.qid): row.query_text for _, row in test_queries_df.iterrows()}

    ir_relevant_docs = defaultdict(list)
    for _, row in test_labels_df.iterrows():
        ir_relevant_docs[str(row.qid)].append(str(row.docid))

    # Prepare corpus texts for embedding
    corpus_ids = list(corpus_docs.keys())

    corpus_texts = [build_retrieval_text(corpus_docs[cid]) for cid in corpus_ids]
    
    query_ids = list(ir_test_queries.keys())
    query_texts = [ir_test_queries[qid] for qid in query_ids]

    # Encode
    test_query_embeddings = model.encode(
        query_texts,
        convert_to_tensor=True,
        show_progress_bar=True,
    )
    corpus_embeddings = model.encode(
        corpus_texts,
        convert_to_tensor=True,
        show_progress_bar=True,
    )

    # Cosine similarity
    cos_scores = util.pytorch_cos_sim(test_query_embeddings, corpus_embeddings)

    # Prepare output containers
    top_results = {
        "_meta": {
            "created_at": datetime.now().isoformat(),
            "device": device,
            "top_k": args.top_k,
            "use_full_retrieval_text": bool(args.use_full_retrieval_text),
            "model_path": args.model_path,
            "dataset_path": args.dataset_path,
        },
        "results": {}
    }

    # Ensure log file is fresh
    if args.log_jsonl and os.path.exists(args.log_jsonl):
        os.remove(args.log_jsonl)

    for q_idx, qid in enumerate(tqdm(query_ids, desc="Queries")):
        query = ir_test_queries[qid]

        top = cos_scores[q_idx].topk(args.top_k)
        indices = top.indices.tolist()
        scores = top.values.tolist()

        topk_list = []
        for rank, (idx, sc) in enumerate(zip(indices, scores), start=1):
            doc_id = corpus_ids[idx]
            d = corpus_docs[doc_id]
            topk_list.append({
                "rank": rank,
                "docid": doc_id,
                "tool_name": d.get("tool_name", ""),
                "api_name": d.get("api_name", ""),
                "score": float(sc),
            })

        # Compute matches w.r.t. qrels
        gold = set(ir_relevant_docs.get(qid, []))
        retrieved_docids = [x["docid"] for x in topk_list]
        matches = len(set(retrieved_docids) & gold)

        # Log JSONL per query (best for later parsing)
        if args.log_jsonl:
            with open(args.log_jsonl, "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "qid": qid,
                    "query": query,
                    "top_k": args.top_k,
                    "topk": topk_list,
                    "gold_docids": list(gold),
                    "successful_matches": matches
                }, ensure_ascii=False) + "\n")

        # Aggregated JSON (qid-indexed to avoid overwriting)
        top_results["results"][qid] = {
            "query": query,
            "original_docs": [corpus_texts[corpus_ids.index(docid)] for docid in ir_relevant_docs.get(qid, []) if docid in corpus_docs],
            "topk": topk_list,
            "successful_matches": matches,
        }

    with open(args.out_json, "w", encoding="utf-8") as f:
        json.dump(top_results, f, indent=2, ensure_ascii=False)

    print(f"[OK] Wrote per-query logs to: {args.log_jsonl}")
    print(f"[OK] Wrote aggregated results to: {args.out_json}")


if __name__ == "__main__":
    main()