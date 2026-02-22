#!/usr/bin/env python3
"""
Small utility to inject a version banner into HTML files.

Usage: python tools/update_version.py [path1 path2 ...]
If no paths are provided it updates a default set of files under the repo.
It reads `version.json` at repository root to get version and date.
"""
import json
import os
import sys
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION_FILE = os.path.join(ROOT, 'version.json')


def find_all_html_files():
    html_files = []
    for root, dirs, files in os.walk(ROOT):
        # Skip some dirs if needed
        if 'archive' in dirs: # Example of skipping or including
            pass 
        for file in files:
            if file.lower().endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files


def load_version():
    with open(VERSION_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def make_banner(version_obj):
    v = version_obj.get('version', 'UNKNOWN')
    d = version_obj.get('release_date', '')
    # Cleaner banner structure matching the new CSS
    return f'<div class="jvav-version-banner">{v} — 发布日期: {d}</div>'


def inject_banner_into_html(path, banner_html):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # If banner already present, replace it using regex for robustness
    pattern = r'<div class="jvav-version-banner">.*?</div>'
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, banner_html, content, flags=re.DOTALL)
    else:
        # insert right after opening <body ...> tag
        idx = content.lower().find('<body')
        if idx != -1:
            end = content.find('>', idx)
            if end != -1:
                content = content[:end+1] + '\n    ' + banner_html + content[end+1:]
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    ver = load_version()
    banner = make_banner(ver)
    html_files = find_all_html_files()
    
    print(f"Updating version information: {ver.get('version')}")
    for p in html_files:
        rel_path = os.path.relpath(p, ROOT)
        print(f'  -> Processing {rel_path}')
        inject_banner_into_html(p, banner)


if __name__ == '__main__':
    main()
