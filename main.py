import os
import argparse
import json
import sys

from m1_parser.resume_parser import ResumeParser
from m2_tree.tree_builder import ResumeTreeBuilder
from m3_jd.jd_parser import JDParser
from m4_eval.eval_agent import EvaluationAgent
from m5_feedback.feedback_module import FeedbackModule

def setup_data_dirs():
    dirs = [
        "./data",
        "./data/parsed",
        "./data/trees",
        "./data/experiments",
        "./data/evals",
        "./data/api_cache"
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def cmd_evaluate(args):
    print("Parsing Resume...")
    resume_parser = ResumeParser()
    resume_json = resume_parser.parse(args.resume)
    
    with open(f"./data/parsed/{resume_json['file_hash']}.json", "w", encoding="utf-8") as f:
        json.dump(resume_json, f, indent=2)

    print("Building Resume Tree...")
    tree_builder = ResumeTreeBuilder()
    resume_tree = tree_builder.build_tree(resume_json)
    
    with open(f"./data/trees/{resume_tree['node_id']}_{resume_json['file_hash']}.json", "w", encoding="utf-8") as f:
        json.dump(resume_tree, f, indent=2)

    print("Parsing JD...")
    jd_parser = JDParser()
    jd_tree = jd_parser.parse(args.jd)
    
    print("Evaluating fit (this may take a minute)...")
    eval_agent = EvaluationAgent()
    eval_result = eval_agent.evaluate(resume_tree, jd_tree)
    
    eval_id = eval_result['eval_id']
    with open(f"./data/evals/{eval_id}.json", "w", encoding="utf-8") as f:
        json.dump(eval_result, f, indent=2)
        
    print(f"\nEvaluation Complete! (Eval ID: {eval_id})\n")
    print(f"OVERALL SCORE: {eval_result['overall_score']}/100")
    print("DIMENSION SCORES:")
    for dim, score in eval_result['dimension_scores'].items():
        print(f"  - {dim.replace('_', ' ').title()}: {score}/100")
        
    print("\nMATCHED REQUIREMENTS:")
    for match in eval_result.get('matched_requirements', []):
        node = match.get('resume_node_id', 'N/A')
        print(f"  [{match['match_type'].upper()}] Req: {match['req_id']} -> Node: {node}")
        print(f"    Reason: {match['reasoning']}")
        
    print("\nSTRENGTHS:")
    for s in eval_result.get('strengths', []):
        print(f"  + {s}")
        
    print("\nGAPS:")
    for g in eval_result.get('gaps', []):
        print(f"  - {g}")
        

def cmd_feedback(args):
    eval_path = f"./data/evals/{args.eval_id}.json"
    if not os.path.exists(eval_path):
        print(f"Error: Evaluation ID {args.eval_id} not found in ./data/evals/")
        sys.exit(1)
        
    with open(eval_path, "r", encoding="utf-8") as f:
        eval_result = json.load(f)
        
    print("Generating actionable feedback...")
    feedback_module = FeedbackModule()
    feedback = feedback_module.generate_feedback(eval_result)
    
    print("\nFEEDBACK GENERATED:")
    print("OVERALL ADVICE:")
    print(feedback.get('overall_advice', ''))
    
    print("\nIMPROVEMENT TIPS (Ranked by Impact):")
    for tip in feedback.get('improvement_tips', []):
        print(f"[{tip.get('impact', 'N/A').upper()}] Gap: {tip.get('gap', '')}")
        print(f"  Tip: {tip.get('tip', '')} (Node: {tip.get('node_id', 'N/A')})")
        
    print("\nRESUME REWRITES:")
    for rw in feedback.get('resume_rewrites', []):
        print(f"  Node [{rw.get('node_id', '')}]")
        print(f"  Old: {rw.get('original_summary', '')}")
        print(f"  New: {rw.get('improved_summary', '')}")
        print(f"  Reason: {rw.get('reason', '')}\n")

def cmd_experiment(args):
    from m6_experiment.experiment_runner import ExperimentRunner
    runner = ExperimentRunner()
    runner.run_experiment(args.dataset, args.jd, args.output)

def main():
    setup_data_dirs()
    
    parser = argparse.ArgumentParser(description="ResumeTree Evaluator")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    p_eval = subparsers.add_parser("evaluate", help="Evaluate a resume against a JD")
    p_eval.add_argument("--resume", required=True, help="Path to resume")
    p_eval.add_argument("--jd", required=True, help="Path to jd.txt")
    
    p_feed = subparsers.add_parser("feedback", help="Generate feedback from evaluation")
    p_feed.add_argument("--eval-id", required=True, help="Evaluation UUID")
    
    p_exp = subparsers.add_parser("experiment", help="Run baseline benchmarks")
    p_exp.add_argument("--dataset", required=True, help="Path to resumes folder")
    p_exp.add_argument("--jd", required=True, help="Path to JD txt")
    p_exp.add_argument("--output", required=True, help="Output CSV path")
    
    args = parser.parse_args()
    
    if args.command == "evaluate":
        cmd_evaluate(args)
    elif args.command == "feedback":
        cmd_feedback(args)
    elif args.command == "experiment":
        cmd_experiment(args)

if __name__ == "__main__":
    main()
