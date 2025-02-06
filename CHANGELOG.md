# Changelog

All notable changes to this project will be documented in this file based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/). This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

- See upcoming changes in [News directory](https://github.com/makukha/docsub/tree/main/NEWS.d)

<!-- towncrier release notes start -->

## [v0.8.3](https://github.com/makukha/docsub/releases/tag/v0.8.3) — 2025-02-06

***Added 🌿***

- Support indented substitution blocks in markdown ([#64](https://github.com/makukha/docsub/issues/64))


## [v0.8.2](https://github.com/makukha/docsub/releases/tag/v0.8.2) — 2025-02-05

***Changed***

- Updated importloc to 0.3+ ([#71](https://github.com/makukha/docsub/issues/71))


## [v0.8.1](https://github.com/makukha/docsub/releases/tag/v0.8.1) — 2025-02-05

***Fixed***

- Typing errors ([#65](https://github.com/makukha/docsub/issues/65))

***Misc***

- Started using [Just](https://just.systems) ([#65](https://github.com/makukha/docsub/issues/65))
- Added pre-commit hook ([#65](https://github.com/makukha/docsub/issues/65))
- Added tox testing matrix ([#65](https://github.com/makukha/docsub/issues/65))
- Added py.typed marker ([#67](https://github.com/makukha/docsub/issues/67))


## [v0.8.0](https://github.com/makukha/docsub/releases/tag/v0.8.0) — 2025-01-18

***Breaking 🔥***

- Changed default config file name to `docsub.toml` ([#58](https://github.com/makukha/docsub/issues/58))
- Renamed `ExecConfig.workdir` and `IncludeConfig.basedir` to `work_dir` and `base_dir` ([#58](https://github.com/makukha/docsub/issues/58))
- Switch back to `click` ([#58](https://github.com/makukha/docsub/issues/58))

***Added 🌿***

- Provide temporary directory to author of project-local commands ([#58](https://github.com/makukha/docsub/issues/58))
- Developers of project-local commands can use `Environment` object to get temporary directory etc. ([#58](https://github.com/makukha/docsub/issues/58))
- Command line options to override config values and config file location ([#58](https://github.com/makukha/docsub/issues/58))
- Project-local commands can be executed directly with `docsub x cmd-name [args]` ([#58](https://github.com/makukha/docsub/issues/58))

***Misc:***

- Major internal refactoring ([#60](https://github.com/makukha/docsub/issues/60))


## [v0.7.1](https://github.com/makukha/docsub/releases/tag/v0.7.1) — 2025-01-14

***Fixed***

- Duplicate newlines bug in `docsub x` cli command ([#54](https://github.com/makukha/docsub/issues/54))


## [v0.7.0](https://github.com/makukha/docsub/releases/tag/v0.7.0) — 2025-01-14

***Breaking 🔥***

- Changed the way `docsub` is invoked: `docsub apply` instead of invocation without commands ([#50](https://github.com/makukha/docsub/issues/50))

***Added 🌿***

- New command line command `docsub x` ([#50](https://github.com/makukha/docsub/issues/50))


## [v0.6.0](https://github.com/makukha/docsub/releases/tag/v0.6.0) — 2025-01-13

***Added 🌿***

- New *producing* command `docsub: x` to run commands from project-local `docsubfile.py` ([#46](https://github.com/makukha/docsub/issues/46))

***Docs***

- Updated docs ([#42](https://github.com/makukha/docsub/issues/42))

***Misc***

- Changed [click](https://click.palletsprojects.com) to [cyclopts](https://cyclopts.readthedocs.io) ([#46](https://github.com/makukha/docsub/issues/46))


## [v0.5.0](https://github.com/makukha/docsub/releases/tag/v0.5.0) — 2025-01-10

***Breaking 🔥***

- Completely changed syntax and command available ([#36](https://github.com/makukha/docsub/issues/36))

***Added 🌿***

- Logging with [loguru](https://loguru.readthedocs.io) ([#11](https://github.com/makukha/docsub/issues/11))

***Docs***

- Updated project metadata ([#29](https://github.com/makukha/docsub/issues/29))

***Misc***

- Started using docsub for self README management ([#36](https://github.com/makukha/docsub/issues/36))
- Started using [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings) for settings management ([#37](https://github.com/makukha/docsub/issues/37))


## [v0.4.0](https://github.com/makukha/docsub/releases/tag/v0.4.0) — 2024-12-30

***Added 🌿***

- `docsub: sh` command to substitute results of shell script execution ([#7](https://github.com/makukha/docsub/issues/7))

***Misc***

- Updated changelog icons ([#7](https://github.com/makukha/docsub/issues/7))


## [v0.3.0](https://github.com/makukha/docsub/releases/tag/v0.3.0) — 2024-12-30

***Added 🌿***

- Option `docsub after line N:` to keep N first lines of replaced block content ([#13](https://github.com/makukha/docsub/issues/13))

***Misc***

- Fixed changelog URLs and release name ([#25](https://github.com/makukha/docsub/issues/25))


## [v0.2.0](https://github.com/makukha/docsub/releases/tag/v0.2.0) — 2024-12-29

***Breaking 🔥***

- In Markdown files, `docsub` header is now used in one-line comment before content block, other than part of fenced code syntax ([#19](https://github.com/makukha/docsub/issues/19))

***Added 🌿***

- Changelog, managed by [Towncrier](https://towncrier.readthedocs.io) ([#12](https://github.com/makukha/docsub/issues/12))

***Changed***

- Multiple heavy refactoring of logic, structure, and dev tasks; introduced multi-format modular architecture ([#6](https://github.com/makukha/docsub/issues/6))

***Fixed***

- Made config file `.docsub.toml` optional, using default command config values if missing ([#3](https://github.com/makukha/docsub/issues/3))
- Fixed regular expression bug ([#5](https://github.com/makukha/docsub/issues/5))

***Docs***

- Appended old Changelog entries ([#17](https://github.com/makukha/docsub/issues/17))

***Misc***

- Fixed dev task release bug when `uv.lock` file was not updated after version bump ([#9](https://github.com/makukha/docsub/issues/9))
- Minor changes related to changelog management ([#17](https://github.com/makukha/docsub/issues/17))
- Added new changelog section "Breaking" ([#19](https://github.com/makukha/docsub/issues/19))
- Add informative icons to changelog sections ([#22](https://github.com/makukha/docsub/issues/22))


## [v0.1.0](https://github.com/makukha/docsub/releases/tag/v0.1.0) — 2024-12-28

***Added 🌿***

- Initial release ([#2](https://github.com/makukha/docsub/issues/2))
