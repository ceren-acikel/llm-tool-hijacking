import time
import json
import os
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from toolbench.utils import standardize, standardize_category, change_name, process_retrieval_ducoment


class ToolRetriever:
    def __init__(self, corpus_tsv_path="", model_path="", log_path="retrieval_topk.jsonl"):
        self.corpus_tsv_path = corpus_tsv_path
        self.model_path = model_path
        self.log_path = log_path

        self.corpus, self.corpus2tool = self.build_retrieval_corpus()
        self.embedder = self.build_retrieval_embedder()
        self.corpus_embeddings = self.build_corpus_embeddings()

        # fresh log
        if self.log_path and os.path.exists(self.log_path):
            os.remove(self.log_path)

    def build_retrieval_corpus(self):
        print("Building corpus...")
        documents_df = pd.read_csv(self.corpus_tsv_path, sep="\t")
        corpus_dict, corpus2tool = process_retrieval_ducoment(documents_df)

        corpus_ids = list(corpus_dict.keys())
        corpus_texts = [corpus_dict[cid] for cid in corpus_ids]

        # IMPORTANT: corpus2tool uses retrieval_text as key, same as corpus_texts elements
        return corpus_texts, corpus2tool

    def build_retrieval_embedder(self):
        print("Building embedder...")
        return SentenceTransformer(self.model_path)

    def build_corpus_embeddings(self):
        print("Building corpus embeddings with embedder...")
        return self.embedder.encode(self.corpus, convert_to_tensor=True, show_progress_bar=True)

    def _append_log(self, obj: dict):
        if not self.log_path:
            return
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    def retrieving(self, query, top_k=5, excluded_tools=None, oversample_factor=10):
        """
        Returns a list of tool dicts: [{category, tool_name, api_name}, ...] length == top_k (unless corpus too small)
        Also logs the raw top-k candidates with scores/ranks.
        """
        if excluded_tools is None:
            excluded_tools = {}

        start = time.time()

        query_embedding = self.embedder.encode(query, convert_to_tensor=True)

        # oversample to survive exclusions, but keep it bounded
        raw_k = min(len(self.corpus), max(top_k, oversample_factor * top_k))

        hits = util.semantic_search(
            query_embedding,
            self.corpus_embeddings,
            top_k=raw_k,
            score_function=util.cos_sim
        )

        retrieved_tools = []
        raw_top = []

        for rank, hit in enumerate(hits[0], start=1):
            corpus_id = hit["corpus_id"]
            score = float(hit["score"])

            retrieval_text = self.corpus[corpus_id]
            # map back to (category, tool_name, api_name)
            category, tool_name, api_name = self.corpus2tool[retrieval_text].split("\t")

            # standardize
            std_category = standardize_category(category)
            std_tool = standardize(tool_name)
            std_api = change_name(standardize(api_name))

            raw_top.append({
                "rank": rank,
                "score": score,
                "category": std_category,
                "tool_name": std_tool,
                "api_name": std_api
            })

            # apply exclusion filter
            if std_category in excluded_tools and std_tool in excluded_tools[std_category]:
                continue

            retrieved_tools.append({
                "category": std_category,
                "tool_name": std_tool,
                "api_name": std_api
            })

            if len(retrieved_tools) >= top_k:
                break

        elapsed_ms = int((time.time() - start) * 1000)

        # LOG: top-k raw candidates + final list
        self._append_log({
            "query": query,
            "top_k": top_k,
            "raw_k": raw_k,
            "elapsed_ms": elapsed_ms,
            "raw_candidates": raw_top[:min(len(raw_top), raw_k)],
            "final_tools": retrieved_tools
        })

        return retrieved_tools