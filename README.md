# ovos-ocp-files-plugin

This plugin lets [OVOS Common Play (OCP)](https://github.com/OpenVoiceOS/ovos-plugin-manager) read local audio and video files. It reads file metadata, such as title, and reports the playback type so OCP can play the file.

It bundles a fork of [audio-metadata](https://github.com/thebigmunch/audio-metadata), adds MP4 support, and publishes it to PyPI as an updated dependency. There is no active development in this repository beyond packaging.

## Install

```bash
pip install ovos-ocp-files-plugin
```

## Usage

OCP loads this plugin through its extractor entry point. It handles a stream URI in the form `file//<path>` or a local file path, and returns metadata such as title and playback type:

```python
from ovos_ocp_files_plugin.plugin import OCPFilesMetadataExtractor

extractor = OCPFilesMetadataExtractor()
extractor.validate_uri("/home/user/music/song.mp3")  # True
meta = extractor.extract_metadata("/home/user/music/song.mp3")
```

## Related projects

- [OpenVoiceOS/ovos-plugin-manager](https://github.com/OpenVoiceOS/ovos-plugin-manager) defines the `OCPStreamExtractor` base class this plugin implements.
- [OpenVoiceOS/ovos-ocp-audio-plugin](https://github.com/OpenVoiceOS/ovos-ocp-audio-plugin) is a sibling OCP stream extractor.
- [thebigmunch/audio-metadata](https://github.com/thebigmunch/audio-metadata) is the upstream metadata library this plugin packages and extends.

## License

MIT
