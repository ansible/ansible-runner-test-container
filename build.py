#!/usr/bin/env python3

import subprocess
import urllib.request

from pathlib import Path


def download_files():
    reqs_path = Path('requirements')
    if reqs_path.exists():
        for file in reqs_path.glob('*.txt'):
            file.unlink()
        # reqs_path.rmdir()

    reqs_path.mkdir(exist_ok=True)

    files = {
        'requirements.txt': [
            'https://raw.githubusercontent.com/ansible/ansible-runner/bd39582b0db418238c4f7023f431076131a92ee7/requirements.txt',
            'https://raw.githubusercontent.com/ansible/ansible-runner/ace172e5b34ad8a24b8703a4551dc83b816da852/test/requirements.txt',
        ],
        'constraints.txt': [
            'https://raw.githubusercontent.com/ansible/ansible-runner/bd39582b0db418238c4f7023f431076131a92ee7/test/constraints.txt',
        ]
    }

    for filename, urls in files.items():
        for url in urls:
            with urllib.request.urlopen(url) as resp:
                with open(reqs_path / filename, 'ab') as f:
                    f.write(resp.read())


def build_image(tag, path, containerfile='Containerfile'):
    cmd = [
        'docker',
        'build',
        '--tag', tag,
        '--file', containerfile,
        path,
    ]
    subprocess.run(cmd)


def main():
    download_files()
    build_image('quay.io/ansible/ansible-runner-test-container', Path('.').absolute())


if __name__ == '__main__':
    main()
