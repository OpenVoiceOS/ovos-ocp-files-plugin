from pathlib import Path

import pytest

import ovos_ocp_files_plugin
from ovos_ocp_files_plugin import UnsupportedFormat
from test.fixtures import id3v2_header

AUDIO_FILEPATHS = list((Path(__file__).parent / 'audio').iterdir())


def test_id3v2_only_is_none(id3v2_header):
	assert ovos_ocp_files_plugin.determine_format(id3v2_header) is None


def test_invalid_file_is_none():
	assert ovos_ocp_files_plugin.determine_format([__file__]) is None


def test_non_audio_file_is_none():
	assert ovos_ocp_files_plugin.determine_format(__file__) is None


@pytest.mark.parametrize("fp", AUDIO_FILEPATHS)
def test_bytes_determine_format(fp):
	assert issubclass(
		ovos_ocp_files_plugin.determine_format(fp.read_bytes()),
		ovos_ocp_files_plugin.Format
	)


@pytest.mark.parametrize("fp", AUDIO_FILEPATHS)
def test_filepath_determine_format(fp):
	assert issubclass(
		ovos_ocp_files_plugin.determine_format(str(fp)),
		ovos_ocp_files_plugin.Format
	)


@pytest.mark.parametrize("fp", AUDIO_FILEPATHS)
def test_file_like_object_determine_format(fp):
	assert issubclass(
		ovos_ocp_files_plugin.determine_format(fp.open('rb')),
		ovos_ocp_files_plugin.Format
	)


@pytest.mark.parametrize("fp", AUDIO_FILEPATHS)
def test_path_object_determine_format(fp):
	assert issubclass(
		ovos_ocp_files_plugin.determine_format(fp),
		ovos_ocp_files_plugin.Format
	)


def test_non_audio_file_raises_unsupportedformat():
	with pytest.raises(UnsupportedFormat) as exc:
		ovos_ocp_files_plugin.load(__file__)
	assert str(exc.value) == "Supported format signature not found."


def test_non_file_raises_valueerror():
	with pytest.raises(ValueError) as exc:
		ovos_ocp_files_plugin.load(b'test')
	assert str(exc.value) == "Not a valid filepath or file-like object."


@pytest.mark.parametrize("fp", AUDIO_FILEPATHS)
def test_filepath_load(fp):
	ovos_ocp_files_plugin.load(str(fp))


@pytest.mark.parametrize("fp", AUDIO_FILEPATHS)
def test_file_like_object_load(fp):
	with open(fp, 'rb') as f:
		ovos_ocp_files_plugin.load(f)


@pytest.mark.parametrize("fp", AUDIO_FILEPATHS)
def test_path_object_load(fp):
	ovos_ocp_files_plugin.load(fp)


def test_non_audio_raises_unsupportedformat():
	with pytest.raises(UnsupportedFormat) as exc:
		with open(__file__, 'rb') as f:
			ovos_ocp_files_plugin.loads(f.read())
	assert str(exc.value) == "Supported format signature not found."


def test_non_bytes_like_object_raises_valueerror():
	with pytest.raises(ValueError) as exc:
		ovos_ocp_files_plugin.loads(__file__)
	assert str(exc.value) == "Not a valid bytes-like object."


@pytest.mark.parametrize("fp", AUDIO_FILEPATHS)
def test_bytes_loads(fp):
	ovos_ocp_files_plugin.loads(fp.read_bytes())


@pytest.mark.parametrize("fp", AUDIO_FILEPATHS)
def test_bytearray_loads(fp):
	ovos_ocp_files_plugin.loads(bytearray(fp.read_bytes()))


@pytest.mark.parametrize("fp", AUDIO_FILEPATHS)
def test_memory_view_loads(fp):
	ovos_ocp_files_plugin.loads(memoryview(fp.read_bytes()))
