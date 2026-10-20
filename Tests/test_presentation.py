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
REPOSITORY = json.loads((ROOT / 'profile/catalog.json').read_text())['organization']['login'] + '/.github'
WORKFLOW = (ROOT / '.github/workflows/presentation.yml').read_text()
CI = (ROOT / '.github/workflows/ci.yml').read_text()


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
        self.assertEqual(inputs.count("default: ''"), 2)
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
                        'artifact-dir: ${{ runner.temp }}/presentation/terminal'):
            self.assertIn(setting, terminal)
        lint = step('Lint DESIGN.md', CI)
        toolchain = re.compile(r'uses: (showxu/skills/skills/github-readme-design/scripts@[0-9a-f]{40} # v\d+\.\d+\.\d+)')
        self.assertEqual(toolchain.search(terminal)[1], toolchain.search(lint)[1])
        for setting in ('asset: design', 'command: lint', 'design: DESIGN.md'):
            self.assertIn(setting, lint)
        archive = step('Archive regenerated presentation assets')
        self.assertIn('if: ${{ failure() }}', archive)
        upload = step('Upload regenerated presentation assets')
        for setting in ('if: ${{ failure() }}', 'name: presentation',
                        'path: ${{ runner.temp }}/presentation.tar', 'if-no-files-found: ignore'):
            self.assertIn(setting, upload)
        names = re.findall(r'^      - name: (.+)$', WORKFLOW, re.M)
        self.assertEqual(names, ['Validate workflow revision', 'Check out caller',
                                 'Check out pinned standard', 'Resolve inputs', 'Download executable',
                                 'Prepare executable', 'Check terminal presentation', 'Check social preview',
                                 'Archive regenerated presentation assets',
                                 'Upload regenerated presentation assets'])

    def test_self_calls_use_default_organization_inputs(self):
        jobs = CI.split('jobs:\n', 1)[1].split('  check:\n', 1)[0]
        self.assertEqual(jobs, '  presentation:\n    uses: ./.github/workflows/presentation.yml\n'
                         '  profile:\n    uses: ./.github/workflows/profile.yml\n')

    def test_resolver_and_kind_conditions(self):
        resolver = step('Resolve inputs')
        for value in ('id: inputs', 'working-directory: standard',
                      'CALLER_REPOSITORY: ${{ github.repository }}',
                      'ASSETS: ${{ inputs.assets }}',
                      'EXECUTABLE_ARTIFACT: ${{ inputs.executable-artifact }}',
                      'EXECUTABLE_PATH: ${{ inputs.executable-path }}',
                      'python3 Scripts/presentation-inputs.py --repository "$CALLER_REPOSITORY"'):
            self.assertIn(value, resolver)
        for name in ('Download executable', 'Prepare executable', 'Check terminal presentation'):
            self.assertIn("if: ${{ steps.inputs.outputs.kind == 'tool' }}", step(name))
        social = step('Check social preview')
        self.assertIn("if: ${{ !cancelled() && steps.inputs.outcome == 'success' }}", social)
        for value in ('asset: social-preview', 'command: check', 'design: standard/DESIGN.md',
                      'fonts: standard/Brand/Fonts', 'catalog: standard/profile/catalog.json',
                      'repository: ${{ steps.inputs.outputs.repository }}',
                      'icon: ${{ steps.inputs.outputs.icon }}',
                      'assets: caller/${{ inputs.assets }}/social-preview',
                      'artifact-dir: ${{ runner.temp }}/presentation/social-preview'):
            self.assertIn(value, social)

    def test_every_toolchain_reference_uses_one_release_pin(self):
        workflows = WORKFLOW + CI + (ROOT / '.github/workflows/profile.yml').read_text()
        pins = re.findall(r'uses: (showxu/skills/skills/github-readme-design/scripts@.*)', workflows)
        self.assertEqual(len(pins), 4)
        self.assertEqual(set(pins), {
            'showxu/skills/skills/github-readme-design/scripts@e5a50c34bf66264a436288f96e44db9caa305912 # v0.2.0'
        })


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
                executable.write_text('#!/bin/sh\nprintf hello\n')
                executable.chmod(0o644)
                result = self.run_step('Prepare executable', EXECUTABLE_PATH=relative)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertTrue(os.access(executable, os.X_OK))
                self.assertFalse((self.root / 'injected').exists())

    def test_failure_archive_preserves_modes_and_hidden_files(self):
        regenerated = self.root / 'presentation/terminal'
        (regenerated / 'fixture').mkdir(parents=True)
        (regenerated / 'script.yml').write_text('title: demo\n')
        (regenerated / 'fixture/.config').write_text('hidden\n')
        helper = regenerated / 'fixture/helper'
        helper.write_text('#!/bin/sh\n')
        helper.chmod(0o755)
        social = self.root / 'presentation/social-preview'
        social.mkdir()
        (social / 'social-preview.png').write_bytes(b'png')
        result = self.run_step('Archive regenerated presentation assets')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        with tarfile.open(self.root / 'presentation.tar') as archive:
            members = {member.name.removeprefix('./'): member for member in archive.getmembers()}
        self.assertIn('social-preview/social-preview.png', members)
        self.assertIn('terminal/script.yml', members)
        self.assertIn('terminal/fixture/.config', members)
        self.assertEqual(members['terminal/fixture/helper'].mode & 0o777, 0o755)

    def test_failure_archive_is_skipped_without_regenerated_files(self):
        result = self.run_step('Archive regenerated presentation assets')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse((self.root / 'presentation.tar').exists())

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
