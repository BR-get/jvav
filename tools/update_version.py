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

ROOT = os.path.dirname(os.path.dirname(__file__))
VERSION_FILE = os.path.join(ROOT, 'version.json')

DEFAULT_TARGETS = [
    os.path.join(ROOT, 'index.html'),
    os.path.join(ROOT, 'help.html'),
    os.path.join(ROOT, 'tx.html'),
    os.path.join(ROOT, 'downloads', 'index.html'),
]


def load_version():
    with open(VERSION_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def make_banner(version_obj):
    v = version_obj.get('version', 'UNKNOWN')
    d = version_obj.get('release_date', '')
    return f'<div class="jvav-version-banner" style="background:#fffbeb;border:1px solid #ffd86b;padding:8px;text-align:center;font-weight:600">{v} — 发布日期: {d}</div>\n'


def inject_banner_into_html(path, banner_html):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # If banner already present, replace it
    if 'jvav-version-banner' in content:
        content = _replace_existing_banner(content, banner_html)
    else:
        # insert right after opening <body ...> tag
        idx = content.lower().find('<body')
        if idx != -1:
            # find end of opening body tag
            end = content.find('>', idx)
            if end != -1:
                content = content[:end+1] + '\n' + banner_html + content[end+1:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def _replace_existing_banner(content, banner_html):
    # naive: remove any div with jvav-version-banner class
    start = content.find('jvav-version-banner')
    if start == -1:
        return content
    # find the nearest opening '<' before the class
    open_tag = content.rfind('<', 0, start)
    close_tag = content.find('</div>', start)
    if open_tag != -1 and close_tag != -1:
        return content[:open_tag] + banner_html + content[close_tag+6:]
    return content


def main(paths):
    ver = load_version()
    banner = make_banner(ver)
    for p in paths:
        if not os.path.isabs(p):
            p = os.path.join(ROOT, p)
        if os.path.exists(p) and p.lower().endswith('.html'):
            print('Updating', p)
            inject_banner_into_html(p, banner)
        else:
            print('Skipping (not found or not html):', p)


if __name__ == '__main__':
    targets = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_TARGETS
    main(targets)
