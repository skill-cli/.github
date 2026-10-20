# Presentation fixture

`demo` is an executable POSIX shell fixture. `terminal/script.yml` runs one
hidden setup command that writes `message.txt`, then shows `demo hello` and
`demo read message.txt`. Its expectation checks the complete file content.

CI uploads `demo` as `presentation-fixture` and calls this repository's
reusable presentation workflow on `ubuntu-24.04`. The workflow downloads the
executable, restores its execute bit, re-records the script and compares
`terminal/recording.json`, `terminal/terminal-light.svg` and
`terminal/terminal-dark.svg` byte for byte. On drift, the regenerated directory is archived
as `presentation-terminal.tar` and uploaded as artifact `presentation-terminal`. This self-test exercises the workflow;
member adoption requires a real CLI build and re-recording on its build OS.

Generate from the repository root with Node 24.22.0 and the toolchain at
`ca4eee1bf838cfa81fa6de3912270c74e47c3e76` (`v0.1.0`), obtained in
`.build/presentation-toolchain` using its [local regeneration instructions](https://github.com/showxu/skills/blob/ca4eee1bf838cfa81fa6de3912270c74e47c3e76/skills/github-readme-design/references/renderers.md#local-regeneration):

```sh
toolchain_dir="$PWD/.build/presentation-toolchain"
node "$toolchain_dir/src/cli.ts" terminal record \
  --script Tests/Fixtures/Presentation/terminal/script.yml \
  --executable Tests/Fixtures/Presentation/demo \
  --out Tests/Fixtures/Presentation/terminal/recording.json
node "$toolchain_dir/src/cli.ts" terminal render \
  --recording Tests/Fixtures/Presentation/terminal/recording.json \
  --design DESIGN.md --fonts Brand/Fonts \
  --out-dir Tests/Fixtures/Presentation/terminal
node "$toolchain_dir/src/cli.ts" terminal check \
  --assets Tests/Fixtures/Presentation/terminal --design DESIGN.md \
  --fonts Brand/Fonts --executable Tests/Fixtures/Presentation/demo
```

Each repository supplies its own `DESIGN.md` and `Brand/Fonts`.
Commit the script, executable, recording and both SVGs together.
