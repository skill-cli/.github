import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = 'skill-cli/.github'
WORKFLOW = (ROOT / '.github/workflows/presentation.yml').read_text()
CI = (ROOT / '.github/workflows/ci.yml').read_text()
FIXTURE = ROOT / 'Tests/Fixtures/Presentation'


def step(name, workflow=WORKFLOW):
    return workflow.split('      - name: ' + name + '\n', 1)[1].split('\n      - ', 1)[0]


def command(name):
    return textwrap.dedent(step(name).split('        run: |\n', 1)[1])


class PresentationContractTests(unittest.TestCase):
    def test_standard_checkout_is_bound_to_executing_workflow(self):
        checkout = step('Check out pinned standard')
        self.assertIn(f'repository: {REPOSITORY}\n', checkout)
        self.assertIn('ref: ${{ job.workflow_sha }}\n', checkout)
        self.assertIn('path: standard\n', checkout)
        self.assertIn('STANDARD_SHA: ${{ job.workflow_sha }}\n', step('Validate workflow revision'))
        self.assertIn('path: caller\n', step('Check out caller'))
        self.assertNotIn('ref:', step('Check out caller'))
        self.assertEqual(WORKFLOW.count('persist-credentials: false'), 2)
        self.assertEqual(re.findall(r'^\s+contents: (\w+)$', WORKFLOW, re.M), ['read', 'read'])
        self.assertNotRegex(WORKFLOW, r': write\b')
        self.assertIn('group: shared-presentation-${{ github.workflow }}-', WORKFLOW)
        self.assertIn('  presentation:\n    name: presentation\n', WORKFLOW)
        self.assertIn('runs-on: ${{ inputs.runner }}', WORKFLOW)

    def test_public_interface_and_action_pins(self):
        inputs = WORKFLOW.split('    inputs:\n', 1)[1].split('\npermissions:', 1)[0]
        self.assertEqual(re.findall(r'^      ([\w-]+):$', inputs, re.M),
                         ['runner', 'executable-artifact', 'executable-path', 'assets'])
        self.assertIn('default: ubuntu-24.04', inputs)
        self.assertIn('default: .github/assets', inputs)
        self.assertEqual(inputs.count('required: true'), 2)
        for action, version in re.findall(r'^\s+(?:- )?uses: (\S+)(?: # (\S+))?$', WORKFLOW, re.M):
            self.assertRegex(action, r'^[\w./-]+@[0-9a-f]{40}$')
            self.assertRegex(version, r'^v\d+\.\d+\.\d+$')

    def test_toolchain_uses_pinned_design_and_build_artifact(self):
        download = step('Download executable')
        self.assertIn('name: ${{ inputs.executable-artifact }}', download)
        self.assertIn('path: ${{ runner.temp }}/executable', download)
        terminal = step('Check terminal presentation')
        for setting in ('asset: terminal', 'command: check', 'design: standard/DESIGN.md',
                        'fonts: standard/Brand/Fonts', 'assets: caller/${{ inputs.assets }}/terminal',
                        'executable: ${{ runner.temp }}/executable/${{ inputs.executable-path }}',
                        'artifact-dir: ${{ runner.temp }}/presentation-terminal'):
            self.assertIn(setting, terminal)
        lint = step('Lint DESIGN.md', CI)
        toolchain = re.compile(r'uses: (showxu/skills/skills/github-readme-design/scripts@[0-9a-f]{40} # v\d+\.\d+\.\d+)')
        self.assertEqual(toolchain.search(terminal)[1], toolchain.search(lint)[1])
        for setting in ('asset: design', 'command: lint', 'design: DESIGN.md'):
            self.assertIn(setting, lint)
        archive = step('Archive regenerated terminal assets')
        self.assertIn('if: ${{ failure() }}', archive)
        upload = step('Upload regenerated terminal assets')
        for setting in ('if: ${{ failure() }}', 'name: presentation-terminal',
                        'path: ${{ runner.temp }}/presentation-terminal.tar', 'if-no-files-found: ignore'):
            self.assertIn(setting, upload)
        names = re.findall(r'^      - name: (.+)$', WORKFLOW, re.M)
        self.assertEqual(names, ['Validate workflow revision', 'Check out caller',
                                 'Check out pinned standard', 'Download executable',
                                 'Prepare executable', 'Check terminal presentation',
                                 'Archive regenerated terminal assets',
                                 'Upload regenerated terminal assets'])

    def test_self_call_downloads_the_uploaded_fixture(self):
        self.assertIn('  presentation:\n    needs: presentation-fixture\n'
                      '    uses: ./.github/workflows/presentation.yml\n', CI)
        for setting in ('runner: ubuntu-24.04', 'executable-artifact: presentation-fixture',
                        'executable-path: demo', 'assets: Tests/Fixtures/Presentation',
                        'name: presentation-fixture', 'path: Tests/Fixtures/Presentation/demo',
                        'if-no-files-found: error'):
            self.assertIn(setting, CI)
        self.assertEqual((FIXTURE / 'demo').stat().st_mode & 0o777, 0o755)
        recording = json.loads((FIXTURE / 'terminal/recording.json').read_text())
        self.assertEqual(recording, {'title': 'demo', 'steps': [
            {'command': 'demo hello', 'output': 'Hello from demo.'},
            {'command': 'demo read message.txt', 'output': 'Presentation fixture ready.'},
        ]})


class PresentationShellTests(unittest.TestCase):
    def setUp(self):
        self.root = ROOT / '.build/test-presentation'
        self.root.mkdir(parents=True)
        self.addCleanup(shutil.rmtree, self.root)

    def run_step(self, name, **environment):
        shell = command(name)
        self.assertNotIn('${{', shell)
        return subprocess.run(
            ['bash', '-eo', 'pipefail', '-c', shell], cwd=self.root,
            env={**os.environ, 'RUNNER_TEMP': str(self.root), **environment},
            capture_output=True, text=True,
        )

    def test_missing_or_mutable_workflow_revision_fails(self):
        for revision, valid in [('a' * 40, True), ('', False), ('master', False),
                                ('a' * 39, False), ('a' * 40 + '\n', False)]:
            with self.subTest(revision=revision):
                result = self.run_step('Validate workflow revision', STANDARD_SHA=revision)
                self.assertEqual(result.returncode == 0, valid, result.stdout + result.stderr)

    def test_downloaded_executable_regains_execute_permission(self):
        for relative in ('demo', 'directory with spaces/demo', '$(touch injected)'):
            with self.subTest(path=relative):
                executable = self.root / 'executable' / relative
                executable.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(FIXTURE / 'demo', executable)
                executable.chmod(0o644)
                result = self.run_step('Prepare executable', EXECUTABLE_PATH=relative)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertTrue(os.access(executable, os.X_OK))
                self.assertFalse((self.root / 'injected').exists())

    def test_failure_archive_preserves_modes_and_hidden_files(self):
        regenerated = self.root / 'presentation-terminal'
        (regenerated / 'fixture').mkdir(parents=True)
        (regenerated / 'script.yml').write_text('title: demo\n')
        (regenerated / 'fixture/.config').write_text('hidden\n')
        helper = regenerated / 'fixture/helper'
        helper.write_text('#!/bin/sh\n')
        helper.chmod(0o755)
        result = self.run_step('Archive regenerated terminal assets')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        with tarfile.open(self.root / 'presentation-terminal.tar') as archive:
            members = {member.name.removeprefix('./'): member for member in archive.getmembers()}
        self.assertIn('script.yml', members)
        self.assertIn('fixture/.config', members)
        self.assertEqual(members['fixture/helper'].mode & 0o777, 0o755)

    def test_failure_archive_is_skipped_without_regenerated_files(self):
        result = self.run_step('Archive regenerated terminal assets')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse((self.root / 'presentation-terminal.tar').exists())

    def test_invalid_executable_paths_fail_before_chmod(self):
        outside = self.root / 'outside'
        outside.write_text('unchanged\n')
        outside.chmod(0o644)
        for relative in ('', str(outside), '../outside', 'nested/../../outside',
                         'nested/../demo', 'demo..bak', 'missing'):
            with self.subTest(path=relative):
                result = self.run_step('Prepare executable', EXECUTABLE_PATH=relative)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('executable-path', result.stdout)
                self.assertEqual(outside.stat().st_mode & 0o777, 0o644)


if __name__ == '__main__':
    unittest.main()
