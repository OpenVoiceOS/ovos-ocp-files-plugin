import pytest

from ovos_ocp_files_plugin import (
	WAVE,
	FormatError,
	RIFFTags,
	WAVEAudioFormat,
	WAVEStreamInfo,
)
from test.fixtures import (
	null,
	wave_riff_tags_data,
	wave_riff_tags_subchunk,
	wave_streaminfo_data,
	wave_streaminfo_subchunk,
)


def test_rifftags(
	null,
	wave_riff_tags_data,
):
	with pytest.raises(FormatError) as exc:
		RIFFTags.parse(null)
	assert str(exc.value) == "Valid RIFF INFO chunk not found."

	riff_tags_init = RIFFTags(
		album=['test-album'],
		artist=['test-artist'],
		comment=['test-comment'],
		date=['2000'],
		genre=['test-genre'],
		title=['test-title'],
		tracknumber=['1'],
	)
	riff_tags_parse = RIFFTags.parse(wave_riff_tags_data)

	assert riff_tags_init == riff_tags_parse


def test_wavestreaminfo(wave_streaminfo_data):

	wave_stream_info_init = WAVEStreamInfo(
		size=None,
		start=None,
		extension_data=None,
		audio_format=WAVEAudioFormat.PCM,
		bit_depth=16,
		bitrate=1411200,
		channels=2,
		duration=None,
		sample_rate=44100,
	)
	wave_stream_info_parse = WAVEStreamInfo.parse(wave_streaminfo_data)

	assert wave_stream_info_init == wave_stream_info_parse


def test_parse_riff_tags_subchunk(wave_riff_tags_subchunk):
	riff_tags = WAVE._parse_subchunk(wave_riff_tags_subchunk)

	assert riff_tags == RIFFTags(
		album=['test-album'],
		artist=['test-artist'],
		comment=['test-comment'],
		date=['2000'],
		genre=['test-genre'],
		title=['test-title'],
		tracknumber=['1'],
	)


def test_parse_wave_streaminfo_subchunk(wave_streaminfo_subchunk):
	wave_streaminfo = WAVE._parse_subchunk(wave_streaminfo_subchunk)

	assert wave_streaminfo == WAVEStreamInfo(
		size=None,
		start=None,
		extension_data=None,
		audio_format=WAVEAudioFormat.PCM,
		bit_depth=16,
		bitrate=1411200,
		channels=2,
		duration=None,
		sample_rate=44100,
	)


def test_invalid_header(null):
	with pytest.raises(FormatError) as exc:
		WAVE.parse(null)
	assert str(exc.value) == "Valid WAVE header not found."


def test_invalid_id3():
	with pytest.raises(FormatError) as exc:
		WAVE.parse(b'RIFF0000WAVEid3 1234')
	assert str(exc.value) == "Valid ID3v2 header not found."


def test_invalid_stream_info():
	with pytest.raises(FormatError) as exc:
		WAVE.parse(b'RIFF0000WAVE')
	assert str(exc.value) == "Valid WAVE stream info not found."
