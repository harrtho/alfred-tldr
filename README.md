# Alfred tldr

[![GitHub Version][version-shield]][releases]
[![GitHub All Releases][downloads-shield]][releases]
[![GitHub][licence-shield]][mit-licence]

Alfred workflow for [tldr][tldr]

![][demo]

## Usage

Type `tldr {command}`(eg: `tldr rm`) to search your command.

It automatically updates every seven days. Or you can just type `tldr -u` to manually update the command list.

The default platform is `osx`. You can type `tldr -o`(eg: `tldr apt-get -o linux`) to specify a platform.

## License

The workflow code and the bundled [Alfred-PyWorkflow][alfred-pyworkflow] library are
under the [MIT Licence][mit-licence].

[demo]: screenshot.gif
[downloads-shield]: https://img.shields.io/github/downloads/harrtho/alfred-tldr/total.svg
[licence-shield]: https://img.shields.io/github/license/harrtho/alfred-tldr.svg
[mit-licence]: http://opensource.org/licenses/MIT
[releases]: https://github.com/harrtho/alfred-tldr/releases
[tldr]: https://github.com/tldr-pages/tldr
[version-shield]: https://img.shields.io/github/release/harrtho/alfred-tldr.svg
