# Changelog

All notable changes to this project will be documented in this file. Changes for the *upcoming release* can be found in [News directory](https://github.com/makukha/docsub/tree/main/src/docsub/news.d).

> [!NOTE]
> * The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
> * This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- towncrier release notes start -->

## [v0.3.0](https://github.com/makukha/docsub/releases/tag/v0.3.0) — 2024-12-30

### Added 🌱

- Option `docsub after line N:` to keep N first lines of replaced block content ([#13](https://github.com/makukha/docsub/issues/13))

### Misc

- Fixed changelog URLs and release name ([#25](https://github.com/makukha/docsub/issues/25))


## [v0.2.0](https://github.com/makukha/docsub/releases/tag/v0.2.0) — 2024-12-29

### Breaking 🔥

- In Markdown files, `docsub` header is now used in one-line comment before content block, other than part of fenced code syntax ([#19](https://github.com/makukha/docsub/issues/19))

### Added 🌱

- Changelog, managed by [Towncrier](https://towncrier.readthedocs.io) ([#12](https://github.com/makukha/docsub/issues/12))

### Changed

- Multiple heavy refactoring of logic, structure, and dev tasks; introduced multi-format modular architecture. ([#6](https://github.com/makukha/docsub/issues/6))

### Fixed

- Made config file `.docsub.toml` optional, using default command config values if missing. ([#3](https://github.com/makukha/docsub/issues/3))
- Fixed regular expression bug. ([#5](https://github.com/makukha/docsub/issues/5))

### Docs

- Appended old Changelog entries ([#17](https://github.com/makukha/docsub/issues/17))

### Misc

- Fixed dev task release bug when `uv.lock` file was not updated after version bump. ([#9](https://github.com/makukha/docsub/issues/9))
- Minor changes related to changelog management. ([#17](https://github.com/makukha/docsub/issues/17))
- Added new changelog section "Breaking" ([#19](https://github.com/makukha/docsub/issues/19))
- Add informative icons to changelog sections ([#22](https://github.com/makukha/docsub/issues/22))


## [v0.1.0](https://github.com/makukha/docsub/releases/tag/v0.1.0) — 2024-12-28

### Added 🌱

- Initial release ([#2](https://github.com/makukha/docsub/issues/2))
