import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = (ROOT / '.github/workflows/profile.yml').read_text()
REPOSITORY = json.loads((ROOT / 'profile/catalog.json').read_text())['organization']['login'] + '/.github'


def step(name):
    return WORKFLOW.split('      - name: ' + name + '\n', 1)[1].split('\n      - ', 1)[0]


class ProfileContractTests(unittest.TestCase):
    def test_profile_inputs_and_validation_order(self):
        inputs = WORKFLOW.split('    inputs:\n', 1)[1].split('\npermissions:', 1)[0]
        self.assertEqual(re.findall(r'^      ([\w-]+):$', inputs, re.M), ['mode', 'member', 'output'])
        for value in ('default: public', 'default: profile/member.json', 'default: profile/README.md'):
            self.assertIn(value, inputs)
        names = re.findall(r'^      - name: (.+)$', WORKFLOW, re.M)
        self.assertEqual(names[:4], ['Validate workflow revision', 'Validate profile inputs',
                                    'Check out caller', 'Check out pinned standard'])
        self.assertIn('  profile:\n    name: profile\n', WORKFLOW)
        self.assertIn('group: shared-profile-${{ github.workflow }}-', WORKFLOW)

    def test_standard_revision_and_read_only_checkouts(self):
        self.assertIn('STANDARD_SHA: ${{ job.workflow_sha }}', step('Validate workflow revision'))
        checkout = step('Check out pinned standard')
        for value in (f'repository: {REPOSITORY}', 'ref: ${{ job.workflow_sha }}', 'path: standard'):
            self.assertIn(value, checkout)
        self.assertIn('path: caller', step('Check out caller'))
        self.assertNotIn('ref:', step('Check out caller'))
        self.assertEqual(WORKFLOW.count('persist-credentials: false'), 2)
        self.assertEqual(re.findall(r'^\s+contents: (\w+)$', WORKFLOW, re.M), ['read', 'read'])
        self.assertNotRegex(WORKFLOW, r': write\b')
        for action, version in re.findall(r'^\s+(?:- )?uses: (\S+)(?: # (\S+))?$', WORKFLOW, re.M):
            self.assertRegex(action, r'^[\w./-]+@[0-9a-f]{40}$')
            self.assertRegex(version, r'^v\d+\.\d+\.\d+$')

    def test_member_binding_is_supplied_only_in_member_mode(self):
        action = step('Check profile')
        for value in ('asset: profile', 'command: check', 'design: standard/DESIGN.md',
                      'catalog: standard/profile/catalog.json', 'mode: ${{ inputs.mode }}',
                      "member: ${{ inputs.mode == 'member' && format('caller/{0}', inputs.member) || '' }}",
                      "catalog-revision: ${{ inputs.mode == 'member' && job.workflow_sha || '' }}",
                      'output: caller/${{ inputs.output }}', 'artifact-dir: ${{ runner.temp }}/profile'):
            self.assertIn(value, action)

    def test_failure_upload_uses_the_profile_directory(self):
        upload = step('Upload regenerated profile')
        for value in ('if: ${{ failure() }}', 'name: profile', 'path: ${{ runner.temp }}/profile',
                      'if-no-files-found: ignore'):
            self.assertIn(value, upload)


class ProfileShellTests(unittest.TestCase):
    def setUp(self):
        self.root = ROOT / '.build/test-profile'
        (self.root / 'caller/profile').mkdir(parents=True)
        self.addCleanup(shutil.rmtree, self.root)

    def run_step(self, name, **environment):
        shell = textwrap.dedent(step(name).split('        run: |\n', 1)[1])
        self.assertNotIn('${{', shell)
        env = {**os.environ, 'PROFILE_MODE': 'public', 'PROFILE_MEMBER': 'profile/member.json',
               'PROFILE_OUTPUT': 'profile/README.md', **environment}
        return subprocess.run(['bash', '-eo', 'pipefail', '-c', shell], cwd=self.root,
                              env=env, capture_output=True, text=True)

    def test_invalid_workflow_revisions_fail(self):
        for revision, valid in [('a' * 40, True), ('', False), ('master', False), ('a' * 39, False),
                                ('a' * 40 + '\n', False)]:
            with self.subTest(revision=revision):
                result = self.run_step('Validate workflow revision', STANDARD_SHA=revision)
                self.assertEqual(result.returncode == 0, valid, result.stdout + result.stderr)

    def test_modes_are_validated_before_checkout(self):
        for mode, valid in [('public', True), ('member', True), ('', False), ('PUBLIC', False),
                           ('private', False), ('$(touch injected)', False)]:
            with self.subTest(mode=mode):
                result = self.run_step('Validate profile inputs', PROFILE_MODE=mode)
                self.assertEqual(result.returncode == 0, valid, result.stdout + result.stderr)
                self.assertFalse((self.root / 'injected').exists())

    def test_member_and_output_paths_are_relative_without_parent_segments(self):
        for name in ('PROFILE_MEMBER', 'PROFILE_OUTPUT'):
            for path, valid in [('profile/README.md', True), ('folder with spaces/file', True),
                                ('./profile/name..json', True), ('', False), ('/tmp/file', False),
                                ('../standard/file', False), ('profile/../file', False),
                                ('profile/../../file', False), ('profile\\file', False), ('a\nb', False)]:
                with self.subTest(name=name, path=path):
                    result = self.run_step('Validate profile inputs', **{name: path})
                    self.assertEqual(result.returncode == 0, valid, result.stdout + result.stderr)

    def test_symlinks_cannot_cross_checkouts(self):
        standard = self.root / 'standard'
        standard.mkdir()
        (self.root / 'caller/link').symlink_to(standard, target_is_directory=True)
        for name in ('PROFILE_MEMBER', 'PROFILE_OUTPUT'):
            with self.subTest(name=name):
                result = self.run_step('Validate profile paths', PROFILE_MODE='member', **{name: 'link/file'})
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('must stay inside the caller checkout', result.stderr)
        result = self.run_step('Validate profile paths', PROFILE_MODE='public', PROFILE_MEMBER='link/file')
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
