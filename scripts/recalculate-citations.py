#!/usr/bin/env python3
"""
Recalculate citation statistics from LaTeX chapter files
while preserving the "done" markers from the existing statistics file.
"""

import re
from pathlib import Path
from collections import Counter, defaultdict

def extract_citations(tex_content):
    """Extract all citations from LaTeX content."""
    # Match \vglfootcite, \footcite, \cite, \parencite, etc.
    pattern = r'\\(?:vgl)?(?:foot)?(?:paren)?cite(?:\[.*?\])?\{([^}]+)\}'
    matches = re.findall(pattern, tex_content)
    
    # Split multiple citations in one command
    citations = []
    for match in matches:
        citations.extend([c.strip() for c in match.split(',')])
    
    return citations

def load_done_markers(stats_file):
    """Load existing 'done' markers from the statistics file."""
    done_keys = set()
    
    if not stats_file.exists():
        return done_keys
    
    content = stats_file.read_text(encoding='utf-8')
    
    # Find the "ALL CITATION KEYS" section
    lines = content.split('\n')
    in_keys_section = False
    
    for line in lines:
        if 'ALL CITATION KEYS' in line:
            in_keys_section = True
            continue
        
        if in_keys_section and ':' in line and 'time(s)' in line:
            # Extract key and check for 'done'
            parts = line.split(':')
            if len(parts) >= 2:
                key = parts[0].strip()
                if 'done' in parts[1]:
                    done_keys.add(key)
    
    return done_keys

def main():
    # Paths
    base_path = Path(r'c:\development\PrivProjects\BachlorsThesis')
    chapters_path = base_path / 'Paper' / 'chapters'
    stats_file = base_path / 'citations_statistics.txt'
    
    # Chapter files
    chapter_files = [
        '01_einleitung.tex',
        '02_grundlagen.tex',
        '03_monitoring_systeme.tex',
        '04_implikationen.tex',
        '05_kritische_betrachtung.tex',
        '06_fazit.tex'
    ]
    
    # Load existing done markers
    done_keys = load_done_markers(stats_file)
    
    # Process each chapter
    citations_per_file = {}
    all_citations = []
    
    for chapter_file in chapter_files:
        file_path = chapters_path / chapter_file
        if not file_path.exists():
            continue
        
        content = file_path.read_text(encoding='utf-8')
        citations = extract_citations(content)
        
        # Store per-file statistics
        rel_path = f'Paper\\chapters\\{chapter_file}'
        citations_per_file[rel_path] = len(citations)
        all_citations.extend(citations)
    
    # Calculate statistics
    total_citations = len(all_citations)
    citation_counts = Counter(all_citations)
    unique_keys = len(citation_counts)
    
    # Sort files by citation count (descending)
    sorted_files = sorted(citations_per_file.items(), key=lambda x: x[1], reverse=True)
    
    # Sort citations by count (descending) and then alphabetically by key
    sorted_citations = sorted(citation_counts.items(), key=lambda x: (-x[1], x[0]))
    
    # Get top 20
    top_20 = sorted_citations[:20]
    
    # Sort all keys alphabetically
    all_keys_sorted = sorted(citation_counts.items(), key=lambda x: x[0])
    
    # Generate output
    output = []
    output.append('=' * 60)
    output.append('CITATION STATISTICS')
    output.append('=' * 60)
    output.append('')
    output.append(f'Total citations: {total_citations}')
    output.append(f'Unique citation keys: {unique_keys}')
    output.append('')
    output.append('-' * 60)
    output.append('CITATIONS PER FILE')
    output.append('-' * 60)
    
    for file_path, count in sorted_files:
        output.append(f'{file_path}: {count} citations')
    
    output.append('')
    output.append('-' * 60)
    output.append('MOST CITED SOURCES (Top 20)')
    output.append('-' * 60)
    
    for i, (key, count) in enumerate(top_20, 1):
        output.append(f'{i:2d}. {key}: {count} times')
    
    output.append('')
    output.append('-' * 60)
    output.append('ALL CITATION KEYS (Alphabetical)')
    output.append('-' * 60)
    
    for key, count in all_keys_sorted:
        done_marker = ' done' if key in done_keys else ''
        output.append(f'{key}: {count} time(s){done_marker}')
    
    # Write to file
    stats_file.write_text('\n'.join(output), encoding='utf-8')
    
    print(f'✓ Citation statistics recalculated')
    print(f'  Total citations: {total_citations}')
    print(f'  Unique keys: {unique_keys}')
    print(f'  Done markers preserved: {len(done_keys)}')
    print(f'  Output written to: {stats_file}')

if __name__ == '__main__':
    main()
