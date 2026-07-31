from pathlib import Path

import pytest

from ovos_ocp_files_plugin.utils import (
	apply_unsynchronization,
	decode_bytestring,
	decode_synchsafe_int,
	determine_encoding,
	encode_synchsafe_int,
	get_image_size,
	humanize_bitrate,
	humanize_duration,
	humanize_sample_rate,
	remove_unsynchronization,
	split_encoded
)

images = (Path(__file__).parent / 'image').glob('*.*')


@pytest.mark.parametrize(
	"b,expected",
	list(zip(
		[
			b'TEST',
			b'\xFF',
			b'\x00',
			b'\xFF\xFE',
			b'\xFF\x00',
			b'\xFF\x00\xFF',
			b'\xFF\x00\x00',
			b'\xFF\x00\xFF\xFE',
		],
		[
			b'TEST',
			b'\xFF',
			b'\x00',
			b'\xFF\x00\xFE',
			b'\xFF\x00\x00',
			b'\xFF\x00\x00\xFF',
			b'\xFF\x00\x00\x00',
			b'\xFF\x00\x00\xFF\x00\xFE',
		],
	))
)
def test_apply_unsynchronization(b, expected):
	assert apply_unsynchronization(b) == expected


@pytest.mark.parametrize(
	"b,expected",
	list(zip(
		[
			b'TEST',
			b'\xFF',
			b'\x00',
			b'\xFF\x00\xFE',
			b'\xFF\x00\x00',
			b'\xFF\x00\x00\xFF',
			b'\xFF\x00\x00\x00',
			b'\xFF\x00\x00\xFF\x00\xFE',
		],
		[
			b'TEST',
			b'\xFF',
			b'\x00',
			b'\xFF\xFE',
			b'\xFF\x00',
			b'\xFF\x00\xFF',
			b'\xFF\x00\x00',
			b'\xFF\x00\xFF\xFE',
		],
	))
)
def test_remove_unsynchronization(b, expected):
	assert remove_unsynchronization(b) == expected


@pytest.mark.parametrize(
	"args,expected",
	list(zip(
		[
			(b'\x00\x00\x01\x7f', 7),
			(b'\x00\x00\x02\x7f', 6),
			(b'\x00\x00\x01\x7f', 6),
		],
		[
			255,
			255,
			191,
		],
	))
)
def test_decode_synchsafe_int(args, expected):
	assert decode_synchsafe_int(*args) == expected


@pytest.mark.parametrize(
	"args",
	[
		(b'\x80\x00\x00\x00', 7),
		(b'@\x00\x00\x00', 6),
	]
)
def test_decoding_too_large_synchsafe_int_raises_valueerror(args):
	with pytest.raises(ValueError):
		decode_synchsafe_int(*args)


@pytest.mark.parametrize(
	"args,expected",
	list(zip(
		[
			(255, 7),
			(255, 6),
		],
		[
			b'\x00\x00\x01\x7f',
			b'\x00\x00\x02\x7f',
		],
	))
)
def test_encode_synchsafe_int(args, expected):
	assert encode_synchsafe_int(*args) == expected


@pytest.mark.parametrize(
	"args",
	[
		(268435456, 7),
		(16777216, 6),
	]
)
def test_encoding_too_large_synchsafe_int_raises_valueerror(args):
	with pytest.raises(ValueError):
		encode_synchsafe_int(*args)


@pytest.mark.parametrize(
	"b,encoding,expected",
	list(zip(
		[
			b'test\x00',
			b'\xff\xfet\x00e\x00s\x00t\x00',
			b'\xff\xfet\x00e\x00s\x00t\x00\x00',
			b'\xfe\xff\x00t\x00e\x00s\x00t',
			b'\xfe\xff\x00t\x00e\x00s\x00t\x00',
			b'test\x00',
			b'test\x00',
			b''
		],
		[
			'iso-8859-1',
			'utf-16-le',
			'utf-16-le',
			'utf-16-be',
			'utf-16-be',
			'utf-8',
			None,
			None,
		],
		[
			'test',
			'test',
			'test',
			'test',
			'test',
			'test',
			'test',
			'',
		],
	))
)
def test_decode_bytestring(b, encoding, expected):
	if encoding is None:
		assert decode_bytestring(b) == expected
	else:
		assert decode_bytestring(b, encoding=encoding) == expected


@pytest.mark.parametrize(
	"b,encoding",
	list(zip(
		[
			b'\x00',
			b'\x01\xff\xfe',
			b'\x01\xfe\xff',
			b'\x02',
			b'\x03',
			b'\x04',
			b'',
		],
		[
			'iso-8859-1',
			'utf-16-le',
			'utf-16-be',
			'utf-16-be',
			'utf-8',
			'iso-8859-1',
			'iso-8859-1',
		],
	))
)
def test_determine_encoding(b, encoding):
	assert determine_encoding(b) == encoding


def test_get_image_size():
	for image in images:
		with image.open('rb') as f:
			assert get_image_size(f) == (16, 16)

	with pytest.raises(ValueError):
		get_image_size(b'')


@pytest.mark.parametrize(
	"bitrate,humanized",
	list(zip(
		[
			None,
			0,
			1,
			100,
			1000,
		],
		[
			None,
			'0 bps',
			'1 bps',
			'100 bps',
			'1 Kbps',
		],
	))
)
def test_humanize_bitrate(bitrate, humanized):
	assert humanize_bitrate(bitrate) == humanized


@pytest.mark.parametrize(
	"duration,humanized",
	list(zip(
		[
			None,
			0,
			1,
			60,
			3600,
		],
		[
			None,
			'00:00',
			'00:01',
			'01:00',
			'01:00:00',
		],
	))
)
def test_humanize_duration(duration, humanized):
	assert humanize_duration(duration) == humanized


@pytest.mark.parametrize(
	"sample_rate,humanized",
	list(zip(
		[
			None,
			0,
			1,
			1000,
			44100,
		],
		[
			None,
			'0.0 Hz',
			'1.0 Hz',
			'1.0 KHz',
			'44.1 KHz',
		],
	))
)
def test_humanize_sample_rate(sample_rate, humanized):
	assert humanize_sample_rate(sample_rate) == humanized


@pytest.mark.parametrize(
	"b,encoding,expected",
	list(zip(
		[
			b'test\x00',
			b'\xff\xfe\x00\x00\xff\xfet\x00e\x00s\x00t\x00\x00\x00',
			b'\xff\xfe\x00\x00\xff\xfet\x00e\x00s\x00t\x00\x00',
			b'\xff\xfet\x00e\x00s\x00t\x00\x00\x00',
			b'\xfe\xff\x00t\x00e\x00s\x00t\x00\x00',
			b'\xfe\xff\x00t\x00e\x00s\x00t\x00',
			b'test\x00',
			b'test',
		],
		[
			'iso-8859-1',
			'utf-16-le',
			'utf-16-le',
			'utf-16-le',
			'utf-16-be',
			'utf-16-be',
			'utf-8',
			'iso-9959-1',
		],
		[
			[b'test'],
			[b'\xff\xfe', b'\xff\xfet\x00e\x00s\x00t\x00'],
			[b'\xff\xfe', b'\xff\xfet\x00e\x00s\x00t\x00'],
			[b'\xff\xfet\x00e\x00s\x00t\x00'],
			[b'\xfe\xff\x00t\x00e\x00s\x00t'],
			[b'\xfe\xff\x00t\x00e\x00s\x00t'],
			[b'test'],
			[b'test'],
		],
	))
)
def test_split_encoded(b, encoding, expected):
	assert split_encoded(b, encoding) == expected
