import os
import time
import pandas as pd
from typing import List, Dict, Any
from scipy.stats import spearmanr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

from shared.llm_client import LLMClient
from m1_parser.resume_parser import ResumeParser
from m2_tree.tree_builder import ResumeTreeBuilder
from m3_jd.jd_parser import JDParser
from m4_eval.eval_agent import EvaluationAgent

class ExperimentRunner:
    def __init__(self):
        self.llm = LLMClient()
        self.sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.resume_parser = ResumeParser()
        self.tree_builder = ResumeTreeBuilder()
        self.jd_parser = JDParser()
        self.eval_agent = EvaluationAgent()

    def _precision_at_k(self, true_ranks: List[str], pred_ranks: List[str], k: int) -> float:
        pred_top_k = set(pred_ranks[:k])
        true_top_k = set(true_ranks[:k])
        if not pred_top_k:
            return 0.0
        return len(pred_top_k.intersection(true_top_k)) / float(k)

    def _get_ranks(self, filename_score_dict: Dict[str, float]) -> List[str]:
        # Sort desc by score, return list of filenames
        sorted_items = sorted(filename_score_dict.items(), key=lambda x: x[1], reverse=True)
        return [k for k, v in sorted_items]

    def _extract_text(self, filepath: str) -> str:
        text, _ = self.resume_parser._extract_text(filepath)
        return text

    def run_tfidf_baseline(self, jd_text: str, resume_texts: Dict[str, str]) -> Dict[str, float]:
        filenames = list(resume_texts.keys())
        texts = [resume_texts[name] for name in filenames]
        vectorizer = TfidfVectorizer().fit([jd_text] + texts)
        jd_vec = vectorizer.transform([jd_text])
        res_vecs = vectorizer.transform(texts)
        scores = cosine_similarity(jd_vec, res_vecs)[0]
        return {filenames[i]: float(scores[i]) for i in range(len(filenames))}

    def run_sbert_baseline(self, jd_text: str, resume_texts: Dict[str, str]) -> Dict[str, float]:
        filenames = list(resume_texts.keys())
        texts = [resume_texts[name] for name in filenames]
        jd_emb = self.sbert_model.encode([jd_text])
        res_embs = self.sbert_model.encode(texts)
        scores = cosine_similarity(jd_emb, res_embs)[0]
        return {filenames[i]: float(scores[i]) for i in range(len(filenames))}

    def run_flat_llm_baseline(self, jd_text: str, resume_texts: Dict[str, str]) -> Dict[str, float]:
        scores = {}
        prompt_sys = "You are a recruiter. Output ONLY a valid JSON object like {\"score\": 85}. Score candidate fit out of 100 based on the JD."
        for filename, text in resume_texts.items():
            prompt_user = f"JD:\n{jd_text}\n\nResume:\n{text}"
            try:
                res = self.llm.call_json(prompt_user, prompt_sys, 0.2)
                scores[filename] = float(res.get("score", 0))
            except Exception:
                scores[filename] = 0.0
        return scores

    def run_resumetree(self, jd_filepath: str, list_of_resumes: List[str]) -> Dict[str, float]:
        jd_tree = self.jd_parser.parse(jd_filepath)
        scores = {}
        for resume_filepath in list_of_resumes:
            filename = os.path.basename(resume_filepath)
            try:
                resume_json = self.resume_parser.parse(resume_filepath)
                resume_tree = self.tree_builder.build_tree(resume_json)
                eval_res = self.eval_agent.evaluate(resume_tree, jd_tree)
                scores[filename] = float(eval_res.get("overall_score", 0))
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                scores[filename] = 0.0
        return scores

    def run_experiment(self, dataset_folder: str, jd_filepath: str, output_csv: str):
        print("Starting experiment...")
        # Get absolute path for jd to avoid issues in jd_parser
        abs_jd_filepath = os.path.abspath(jd_filepath)
        try:
            with open(abs_jd_filepath, "r", encoding="utf-8") as f:
                jd_text = f.read()
        except UnicodeDecodeError:
            with open(abs_jd_filepath, "r", encoding="latin-1") as f:
                jd_text = f.read()

        jd_text = jd_text.replace('\r\n', '\n').strip()

        # Load resumes
        resume_texts = {}
        resume_filepaths = []
        for filename in os.listdir(dataset_folder):
            if filename.endswith(".pdf") or filename.endswith(".docx") or filename.endswith(".txt"):
                if "jd" not in filename.lower():  # ensure we don't treat JDs as resumes
                    filepath = os.path.join(dataset_folder, filename)
                    resume_texts[filename] = self._extract_text(filepath)
                    resume_filepaths.append(filepath)

        dataset_size = len(resume_texts)
        if dataset_size == 0:
            print("No resumes found in dataset folder.")
            return

        # Load ground truth if exists
        ground_truth_path = os.path.join(dataset_folder, "ground_truth.csv")
        true_scores = {}
        if os.path.exists(ground_truth_path):
            df_gt = pd.read_csv(ground_truth_path)
            for idx, row in df_gt.iterrows():
                true_scores[row['filename']] = float(row['score'])

        if not true_scores:
            print("No ground_truth.csv found, generating surrogate ground truth using TF-IDF baseline...")
            true_scores = self.run_tfidf_baseline(jd_text, resume_texts)
            # Save ground truth generator
            gt_records = [{"filename": k, "score": v} for k, v in true_scores.items()]
            pd.DataFrame(gt_records).to_csv(ground_truth_path, index=False)
            print(f"Generated ground_truth.csv at {ground_truth_path}")
            
        true_ranks = self._get_ranks(true_scores)

        results = []

        methods = [
            ("TF-IDF", self.run_tfidf_baseline),
            ("SBERT", self.run_sbert_baseline),
            ("Flat-LLM", self.run_flat_llm_baseline),
            ("ResumeTree", lambda jd, res: self.run_resumetree(abs_jd_filepath, resume_filepaths))
        ]

        for method_name, method_func in methods:
            print(f"Running {method_name}...")
            start_time = time.time()
            pred_scores = method_func(jd_text, resume_texts)
            # calculate average latency per resume in milliseconds
            latency = (time.time() - start_time) / (dataset_size if dataset_size > 0 else 1) * 1000

            pred_ranks = self._get_ranks(pred_scores)
            
            p5 = self._precision_at_k(true_ranks, pred_ranks, min(5, dataset_size))
            p10 = self._precision_at_k(true_ranks, pred_ranks, min(10, dataset_size))
            
            # Handle spearman correlation calculation gracefully
            ordered_true = [true_scores.get(fname, 0.0) for fname in resume_texts.keys()]
            ordered_pred = [pred_scores.get(fname, 0.0) for fname in resume_texts.keys()]
            
            # Spearman correlation needs at least 2 distinct data points to be meaningful and not throw warning/nan
            if dataset_size < 2 or len(set(ordered_true)) < 2 or len(set(ordered_pred)) < 2:
                rho = 1.0 if ordered_true == ordered_pred else 0.0
            else:
                rho, _ = spearmanr(ordered_true, ordered_pred)
            
            results.append({
                "method": method_name,
                "dataset_size": dataset_size,
                "precision_at_5": float(p5),
                "precision_at_10": float(p10),
                "spearman_rho": float(rho if pd.notna(rho) else 0.0),
                "avg_latency_ms": float(latency)
            })

        df_results = pd.DataFrame(results)
        df_results.to_csv(output_csv, index=False)
        print(f"\nExperiment finished. Results saved to {output_csv}\n")
        
        # Print a clean results table
        print(f"{'METHOD':<15} {'P@5':<6} {'P@10':<6} {'SPEARMAN':<10} {'LATENCY'}")
        for r in results:
            m = r['method']
            p5 = f"{r['precision_at_5']:.2f}"
            p10 = f"{r['precision_at_10']:.2f}"
            rho = f"{r['spearman_rho']:.2f}"
            lat = f"{int(r['avg_latency_ms'])}ms"
            print(f"{m:<15} {p5:<6} {p10:<6} {rho:<10} {lat}")
