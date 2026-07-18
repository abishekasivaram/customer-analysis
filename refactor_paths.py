import os
import glob
import re
from pathlib import Path

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    needs_change = False
    if '"outputs/' in content or "'outputs/" in content or '"datasets/' in content or "'datasets/" in content:
        needs_change = True
        
    if not needs_change:
        return

    print(f"Refactoring {filepath}")

    import_stmt = "from backend.core.config import OUTPUTS_DIR, DATASETS_DIR"
    if import_stmt not in content:
        # Inject right after the first import
        lines = content.split('\n')
        injected = False
        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                lines.insert(i, import_stmt)
                injected = True
                break
        if not injected:
            lines.insert(0, import_stmt)
        content = '\n'.join(lines)

    content = re.sub(r'\"outputs/(.*?)\"', r'str(OUTPUTS_DIR / "\1")', content)
    content = re.sub(r'\'outputs/(.*?)\'', r"str(OUTPUTS_DIR / '\1')", content)
    content = re.sub(r'\"outputs\"', r'str(OUTPUTS_DIR)', content)
    content = re.sub(r'\'outputs\'', r'str(OUTPUTS_DIR)', content)

    content = re.sub(r'\"datasets/(.*?)\"', r'str(DATASETS_DIR / "\1")', content)
    content = re.sub(r'\'datasets/(.*?)\'', r"str(DATASETS_DIR / '\1')", content)
    content = re.sub(r'\"datasets\"', r'str(DATASETS_DIR)', content)
    content = re.sub(r'\'datasets\'', r'str(DATASETS_DIR)', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, _, files in os.walk('backend'):
    for file in files:
        if file.endswith('.py') and file != 'config.py':
            process_file(os.path.join(root, file))
