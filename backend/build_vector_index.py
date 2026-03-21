"""
Script to chunk knowledge base and build FAISS vector index
Processes yafi_knowledge_context.json into searchable chunks
"""

import json
import os
import sys
from typing import List, Dict

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from embedding_service import EmbeddingService


def chunk_qa_entry(qa: Dict, max_chunk_size: int = 500) -> List[Dict]:
    """
    Split a Q&A entry into manageable chunks
    
    Args:
        qa: Q&A dictionary with 'q', 'full_answer', 'category'
        max_chunk_size: Maximum characters per chunk
        
    Returns:
        List of chunk dictionaries
    """
    chunks = []
    question = qa['q']
    answer = qa['full_answer']
    category = qa.get('category', 'Général')
    
    # Chunk 1: Question + first part of answer (overview)
    first_chunk_text = f"Question: {question}\n\nRéponse: {answer[:max_chunk_size]}"
    chunks.append({
        'text': first_chunk_text,
        'metadata': {
            'question': question,
            'category': category,
            'chunk_type': 'overview',
            'source': 'yafi_knowledge_context.json'
        }
    })
    
    # If answer is long, create additional chunks
    if len(answer) > max_chunk_size:
        remaining = answer[max_chunk_size:]
        chunk_num = 2
        
        while remaining:
            chunk_text = f"Question: {question}\n\n(Suite) {remaining[:max_chunk_size]}"
            chunks.append({
                'text': chunk_text,
                'metadata': {
                    'question': question,
                    'category': category,
                    'chunk_type': f'detail_{chunk_num}',
                    'source': 'yafi_knowledge_context.json'
                }
            })
            remaining = remaining[max_chunk_size:]
            chunk_num += 1
    
    return chunks


def process_knowledge_base(input_file: str, output_file: str, max_chunk_size: int = 400):
    """
    Process the knowledge base JSON and create chunks
    
    Args:
        input_file: Path to yafi_knowledge_context.json
        output_file: Path to save knowledge_chunks.json
        max_chunk_size: Maximum characters per chunk
    """
    print(f"📖 Loading knowledge base from: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    qa_database = data.get('qa_database', [])
    print(f"✅ Loaded {len(qa_database)} Q&A entries")
    
    all_chunks = []
    
    for idx, qa in enumerate(qa_database, 1):
        chunks = chunk_qa_entry(qa, max_chunk_size)
        all_chunks.extend(chunks)
        print(f"  [{idx}/{len(qa_database)}] Processed: {qa['q'][:50]}... → {len(chunks)} chunks")
    
    # Save chunks
    output_data = {
        'total_chunks': len(all_chunks),
        'source_file': input_file,
        'chunk_size': max_chunk_size,
        'chunks': all_chunks
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Saved {len(all_chunks)} chunks to: {output_file}")
    return all_chunks


def build_vector_index(chunks_file: str, index_file: str):
    """
    Build FAISS index from chunks
    
    Args:
        chunks_file: Path to knowledge_chunks.json
        index_file: Path to save FAISS index
    """
    print(f"\n🔨 Building vector index...")
    
    # Initialize embedding service
    service = EmbeddingService()
    
    # Load chunks
    with open(chunks_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    chunks = data['chunks']
    
    # Build index
    service.build_index(chunks, save_path=index_file)
    
    print(f"\n✅ Vector index built successfully!")
    print(f"   Total vectors: {service.index.ntotal}")
    print(f"   Dimension: {service.dimension}")
    
    # Test search
    print(f"\n🧪 Testing search...")
    test_query = "C'est quoi l'ENSA ?"
    results = service.search(test_query, top_k=3, threshold=0.5)
    
    if results:
        print(f"\n   Query: '{test_query}'")
        print(f"   Found {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"\n   [{i}] Score: {result['score']:.3f}")
            print(f"       Category: {result['metadata']['category']}")
            print(f"       Text: {result['text'][:100]}...")
    else:
        print("   ⚠️ No results found (threshold too high?)")


def main():
    """Main execution"""
    # Paths
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(backend_dir, 'yafi_knowledge_context.json')
    chunks_file = os.path.join(backend_dir, 'knowledge_chunks.json')
    index_file = os.path.join(backend_dir, 'yafi_vector_index.faiss')
    
    print("=" * 60)
    print("🚀 YAFI Knowledge Base Vectorization")
    print("=" * 60)
    
    # Step 1: Chunk the knowledge base
    chunks = process_knowledge_base(input_file, chunks_file, max_chunk_size=400)
    
    # Step 2: Build vector index
    build_vector_index(chunks_file, index_file)
    
    print("\n" + "=" * 60)
    print("✅ DONE! Vector search system ready.")
    print("=" * 60)
    print(f"\n📁 Files created:")
    print(f"   - {chunks_file}")
    print(f"   - {index_file}")
    print(f"\n💡 Next: Integrate into server.py")


if __name__ == "__main__":
    main()
