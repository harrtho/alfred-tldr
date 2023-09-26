# tldr Alfred Workflow

[![GitHub Version][shield-version]][gh-releases]
[![GitHub All Releases][shield-downloads]][gh-releases]
[![GitHub][shield-license]][license-mit]

Display cheatsheets for console commands from [tldr][tldr] in [Alfred][alfred]

![][preview]

## Download & Installation

Download the [latest workflow release][gh-latest-release] from GitHub. Open the workflow file to
install in Alfred.

## Usage

- `tldr [<query>]` — List/filter available console commands
  - `↩` or `⌘ + C` — Copy one command cheatsheet entry to clipboard

The cheatsheets from [tldr][tldr] are updated automatically every seven days, or you can simply type `tldr -u` to update the command list manually.

The default platform is `osx`. You can type `tldr -o`(eg: `tldr apt-get -o linux`) to specify a platform.

## Bug Reports and Feature Requests

Please use [GitHub issues][gh-issues] to report bugs or request features.

## Contributors

This Alfred Workflow comes from the [abandoned Workflow][abandoned-workflow] of
[Hodor][cs1707]

## License

tldr Alfred Workflow is licensed under the [MIT License][license-mit]

The workflow uses the following libraries:

- [Alfred-PyWorkflow][alfred-pyworkflow] ([MIT License][license-mit])

The cheatsheets from [tldr][tldr] are licensed under
[Creative Commons Attribution 4.0 International License][license-cc]

[abandoned-workflow]: https://github.com/cs1707/tldr-alfred
[alfred-pyworkflow]: https://github.com/harrtho/alfred-pyworkflow
[alfred]: https://www.alfredapp.com
[cs1707]: https://github.com/cs1707
[gh-issues]: https://github.com/harrtho/alfred-tldr/issues
[gh-latest-release]: https://github.com/harrtho/alfred-tldr/releases/latest
[gh-releases]: https://github.com/harrtho/alfred-tldr/releases
[license-mit]: http://opensource.org/licenses/MIT
[license-cc]: https://creativecommons.org/licenses/by/4.0/
[preview]: img/preview.png
[shield-downloads]: https://img.shields.io/github/downloads/harrtho/alfred-tldr/total.svg
[shield-license]: https://img.shields.io/github/license/harrtho/alfred-tldr.svg
[shield-version]: https://img.shields.io/github/release/harrtho/alfred-tldr.svg
[tldr]: https://github.com/tldr-pages/tldr
