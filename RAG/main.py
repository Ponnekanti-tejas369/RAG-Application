#!/usr/bin/env python3
"""
RAG Pipeline CLI

A command-line interface for the Retrieval-Augmented Generation pipeline.
Supports document ingestion, question answering, and evaluation.

Usage:
    python main.py ingest [--docs PATH]
    python main.py ask "Your question here" [--prompt-version 1|2]
    python main.py evaluate [--prompt-version 1|2]
"""

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from config import DATA_DIR
from src.document_loader import load_and_chunk
from src.vector_store import create_vector_store, load_vector_store
from src.llm_chain import ask_question
from src.evaluator import run_evaluation, save_results, print_summary


def cmd_ingest(args):
    """Ingest documents into the vector store."""
    docs_path = Path(args.docs) if args.docs else DATA_DIR
    
    print(f"\n📂 Loading documents from: {docs_path}")
    
    try:
        chunks = load_and_chunk(docs_path)
        create_vector_store(chunks)
        print("\n✅ Ingestion complete!")
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


def cmd_ask(args):
    """Answer a question using the RAG pipeline."""
    vector_store = load_vector_store()
    
    if vector_store is None:
        print("\n❌ Error: No vector store found. Run 'python main.py ingest' first.")
        sys.exit(1)
    
    print(f"\n🔍 Question: {args.question}")
    print(f"📝 Using prompt version: v{args.prompt_version}")
    print("-" * 50)
    
    answer, has_context, context = ask_question(
        args.question,
        vector_store,
        prompt_version=args.prompt_version,
    )
    
    if args.show_context:
        print("\n📚 Retrieved Context:")
        print("-" * 50)
        print(context if context else "[No relevant context found]")
        print("-" * 50)
    
    print(f"\n💬 Answer:\n{answer}")
    
    if not has_context:
        print("\n⚠️  Note: No highly relevant documents were found for this query.")


def cmd_evaluate(args):
    """Run the evaluation suite."""
    vector_store = load_vector_store()
    
    if vector_store is None:
        print("\n❌ Error: No vector store found. Run 'python main.py ingest' first.")
        sys.exit(1)
    
    print(f"\n📊 Running evaluation with prompt version: v{args.prompt_version}")
    
    results = run_evaluation(vector_store, prompt_version=args.prompt_version)
    print_summary(results)
    save_results(results)


def main():
    parser = argparse.ArgumentParser(
        description="RAG Pipeline CLI - Question answering over policy documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Ingest command
    ingest_parser = subparsers.add_parser(
        "ingest",
        help="Load and embed documents into the vector store",
    )
    ingest_parser.add_argument(
        "--docs",
        type=str,
        help=f"Path to documents directory (default: {DATA_DIR})",
    )
    
    # Ask command
    ask_parser = subparsers.add_parser(
        "ask",
        help="Ask a question about the policy documents",
    )
    ask_parser.add_argument(
        "question",
        type=str,
        help="The question to ask",
    )
    ask_parser.add_argument(
        "--prompt-version",
        type=int,
        choices=[1, 2],
        default=2,
        help="Prompt template version (default: 2)",
    )
    ask_parser.add_argument(
        "--show-context",
        action="store_true",
        help="Show retrieved context chunks",
    )
    
    # Evaluate command
    eval_parser = subparsers.add_parser(
        "evaluate",
        help="Run the evaluation suite",
    )
    eval_parser.add_argument(
        "--prompt-version",
        type=int,
        choices=[1, 2],
        default=2,
        help="Prompt template version (default: 2)",
    )
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(0)
    
    commands = {
        "ingest": cmd_ingest,
        "ask": cmd_ask,
        "evaluate": cmd_evaluate,
    }
    
    commands[args.command](args)


if __name__ == "__main__":
    main()
