"""Setup for editorjs_html XBlock."""

import os
from setuptools import setup


def package_data(pkg, root_list):
    """Generic function to find package_data for `pkg` under `root`."""
    data = []
    for root in root_list:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='editorjs-html',
    version='0.0.1',
    description='Course component (Open edX XBlock) that provides an easy way to embed a HTML',
    packages=[
        'editorjs_html',
    ],
    install_requires=[
        'XBlock',
        'xblock-utils',
    ],
    entry_points={
        'xblock.v1': [
            'editorjs_html = editorjs_html.html:HtmlBlock',
        ]
    },
    package_data=package_data('editorjs_html', ['static', 'templates', 'translations']),
)
