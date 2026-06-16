import pytest

from ovos_ocp_files_plugin import (
	FLAC,
	FLACApplication,
	FLACCueSheet,
	FLACCueSheetIndex,
	FLACCueSheetTrack,
	FLACMetadataBlock,
	FLACPadding,
	FLACPicture,
	FLACSeekPoint,
	FLACSeekTable,
	FLACStreamInfo,
	FLACVorbisComments,
	FormatError,
	ID3PictureType,
)
from test.fixtures import (
	flac_0_duration,
	flac_0_size_block,
	flac_application_block,
	flac_application_data,
	flac_cuesheet_block,
	flac_cuesheet_data,
	flac_cuesheet_index_1,
	flac_cuesheet_index_2,
	flac_cuesheet_track_1,
	flac_cuesheet_track_2,
	flac_id3v2,
	flac_invalid_block,
	flac_padding_block,
	flac_padding_data,
	flac_picture_block,
	flac_picture_data,
	flac_reserved_block,
	flac_seektable_block,
	flac_seektable_data,
	flac_streaminfo_block,
	flac_streaminfo_data,
	flac_vorbis_comment_block,
	flac_vorbis_comment_data,
	null,
)


def test_flacapplication(flac_application_data):
	application_init = FLACApplication(
		id='aiff',
		data=b'FORM\x02\xe0\x9b\x08AIFF'
	)
	application_parse = FLACApplication.parse(flac_application_data)

	assert application_init == application_parse
	assert application_init.id == application_parse.id == 'aiff'
	assert application_init.data == application_parse.data == b'FORM\x02\xe0\x9b\x08AIFF'
	assert repr(application_init) == repr(application_parse) == '<FLACApplication (aiff)>'


def test_flaccuesheetindex(flac_cuesheet_index_1, flac_cuesheet_index_2):
	cuesheet_index_init = FLACCueSheetIndex(
		number=1,
		offset=0,
	)
	cuesheet_index_parse = FLACCueSheetIndex.parse(flac_cuesheet_index_1)

	assert cuesheet_index_init == cuesheet_index_parse
	assert cuesheet_index_init.number == cuesheet_index_parse.number == 1
	assert cuesheet_index_init.offset == cuesheet_index_parse.offset == 0
	assert repr(cuesheet_index_init) == repr(cuesheet_index_parse) == "<FLACCueSheetIndex({'number': 1, 'offset': 0})>"

	cuesheet_index_init = FLACCueSheetIndex(
		number=2,
		offset=588,
	)
	cuesheet_index_parse = FLACCueSheetIndex.parse(flac_cuesheet_index_2)

	assert cuesheet_index_init == cuesheet_index_parse
	assert cuesheet_index_init.number == cuesheet_index_parse.number == 2
	assert cuesheet_index_init.offset == cuesheet_index_parse.offset == 588
	assert repr(cuesheet_index_init) == repr(cuesheet_index_parse) == "<FLACCueSheetIndex({'number': 2, 'offset': 588})>"


def test_flaccuesheettrack(flac_cuesheet_track_1, flac_cuesheet_track_2):
	cuesheet_track_init = FLACCueSheetTrack(
		track_number=1,
		offset=0,
		isrc='123456789012',
		type=0,
		pre_emphasis=False,
		indexes=[
			FLACCueSheetIndex(
				number=1,
				offset=0,
			)
		]
	)
	cuesheet_track_parse = FLACCueSheetTrack.parse(flac_cuesheet_track_1)

	assert cuesheet_track_init == cuesheet_track_parse
	assert cuesheet_track_init.track_number == cuesheet_track_parse.track_number == 1
	assert cuesheet_track_init.offset == cuesheet_track_parse.offset == 0
	assert cuesheet_track_init.isrc == cuesheet_track_parse.isrc == '123456789012'
	assert cuesheet_track_init.type == cuesheet_track_parse.type == 0
	assert cuesheet_track_init.pre_emphasis is False
	assert cuesheet_track_parse.pre_emphasis is False

	cuesheet_track_init = FLACCueSheetTrack(
		track_number=2,
		offset=44100,
		isrc='',
		type=1,
		pre_emphasis=True,
		indexes=[
			FLACCueSheetIndex(
				number=1,
				offset=0,
			),
			FLACCueSheetIndex(
				number=2,
				offset=588,
			),
		],
	)
	cuesheet_track_parse = FLACCueSheetTrack.parse(flac_cuesheet_track_2)

	assert cuesheet_track_init == cuesheet_track_parse
	assert cuesheet_track_init.track_number == cuesheet_track_parse.track_number == 2
	assert cuesheet_track_init.offset == cuesheet_track_parse.offset == 44100
	assert cuesheet_track_init.isrc == cuesheet_track_parse.isrc == ''
	assert cuesheet_track_init.type == cuesheet_track_parse.type == 1
	assert cuesheet_track_init.pre_emphasis is True
	assert cuesheet_track_parse.pre_emphasis is True


def test_flaccuesheet(flac_cuesheet_data):
	cuesheet_init = FLACCueSheet(
		[
			FLACCueSheetTrack(
				track_number=1,
				offset=0,
				isrc='123456789012',
				type=0,
				pre_emphasis=False,
				indexes=[
					FLACCueSheetIndex(
						number=1,
						offset=0,
					)
				]
			),
			FLACCueSheetTrack(
				track_number=2,
				offset=44100,
				isrc='',
				type=1,
				pre_emphasis=True,
				indexes=[
					FLACCueSheetIndex(
						number=1,
						offset=0,
					),
					FLACCueSheetIndex(
						number=2,
						offset=588,
					),
				],
			),
			FLACCueSheetTrack(
				track_number=3,
				offset=88200,
				isrc='',
				type=0,
				pre_emphasis=False,
				indexes=[
					FLACCueSheetIndex(
						number=1,
						offset=0,
					)
				],
			),
			FLACCueSheetTrack(
				track_number=170,
				offset=162496,
				isrc='',
				type=0,
				pre_emphasis=False,
				indexes=[]
			)
		],
		catalog_number='1234567890123',
		lead_in_samples=88200,
		compact_disc=True,
	)
	cuesheet_parse = FLACCueSheet.parse(flac_cuesheet_data)

	assert cuesheet_init == cuesheet_parse
	assert repr(cuesheet_init) == repr(cuesheet_parse) == '<FLACCueSheet (4 tracks)>'


def test_flacmetadatablock():
	metadata_block = FLACMetadataBlock(
		type=100,
		data=b'\x00' * 10
	)

	assert metadata_block.type == 100
	assert metadata_block.data == b'\x00' * 10
	assert repr(metadata_block) == '<FLACMetadataBlock [100] (10 bytes)>'


def test_flacpadding(flac_padding_data):
	padding_init = FLACPadding(size=10)
	padding_parse = FLACPadding.parse(flac_padding_data)

	assert padding_init == padding_parse
	assert repr(padding_init) == repr(padding_parse) == '<FLACPadding (10 bytes)>'


def test_flacpicture(flac_picture_data):
	flac_picture_init = FLACPicture(
		type=ID3PictureType.COVER_FRONT,
		mime_type='image/png',
		description='',
		width=16,
		height=16,
		bit_depth=32,
		colors=0,
		data=flac_picture_data[41:],
	)
	flac_picture_parse = FLACPicture.parse(flac_picture_data)

	assert flac_picture_init == flac_picture_parse


def test_flacseektable(flac_seektable_data):
	seekpoints = [
		FLACSeekPoint(
			first_sample=first_sample,
			offset=offset,
			num_samples=num_samples)
		for first_sample, offset, num_samples in [
			(0, 0, 4096),
			(40960, 140, 4096),
			(86016, 294, 4096),
			(131072, 448, 4096),
			(176128, 602, 4096)
		]
	]

	seektable_init = FLACSeekTable(seekpoints)
	seektable_parse = FLACSeekTable.parse(flac_seektable_data)

	assert seektable_init == seektable_parse
	assert seektable_init.data == seektable_parse.data == seekpoints


def test_flacstreaminfo(flac_streaminfo_data):
	flac_streaminfo_init = FLACStreamInfo(
		start=None,
		size=None,
		min_block_size=4096,
		max_block_size=4096,
		min_frame_size=14,
		max_frame_size=16,
		bit_depth=16,
		bitrate=None,
		channels=2,
		duration=5,
		md5='9b1be87c6b579fde2341515f4d82c008',
		sample_rate=44100,
	)
	flac_streaminfo_parse = FLACStreamInfo.parse(flac_streaminfo_data)

	assert flac_streaminfo_init == flac_streaminfo_parse


def test_flacvorbiscomments(flac_vorbis_comment_data):
	vorbis_comments = FLACVorbisComments.parse(flac_vorbis_comment_data)

	assert vorbis_comments == FLACVorbisComments(
		_vendor='reference libFLAC 1.3.2 20170101',
		album=['test-album'],
		artist=['test-artist'],
		comment=['test-comment'],
		date=['2000'],
		discnumber=['1'],
		disctotal=['99'],
		genre=['test-genre'],
		title=['test-title'],
		tracknumber=['1'],
		tracktotal=['99'],
	)


def test_parse_flac_application_block(flac_application_block):
	application_block, _ = FLAC._parse_metadata_block(flac_application_block)

	assert application_block == FLACApplication(
		id='aiff',
		data=b'FORM\x02\xe0\x9b\x08AIFF'
	)


def test_parse_flac_cuesheet_block(flac_cuesheet_block):
	cuesheet_block, _ = FLAC._parse_metadata_block(flac_cuesheet_block)

	assert cuesheet_block == FLACCueSheet(
		[
			FLACCueSheetTrack(
				track_number=1,
				offset=0,
				isrc='123456789012',
				type=0,
				pre_emphasis=False,
				indexes=[
					FLACCueSheetIndex(
						number=1,
						offset=0,
					)
				]
			),
			FLACCueSheetTrack(
				track_number=2,
				offset=44100,
				isrc='',
				type=1,
				pre_emphasis=True,
				indexes=[
					FLACCueSheetIndex(
						number=1,
						offset=0,
					),
					FLACCueSheetIndex(
						number=2,
						offset=588,
					),
				],
			),
			FLACCueSheetTrack(
				track_number=3,
				offset=88200,
				isrc='',
				type=0,
				pre_emphasis=False,
				indexes=[
					FLACCueSheetIndex(
						number=1,
						offset=0,
					)
				],
			),
			FLACCueSheetTrack(
				track_number=170,
				offset=162496,
				isrc='',
				type=0,
				pre_emphasis=False,
				indexes=[]
			)
		],
		catalog_number='1234567890123',
		lead_in_samples=88200,
		compact_disc=True,
	)


def test_parse_flac_padding_block(flac_padding_block):
	padding_block, _ = FLAC._parse_metadata_block(flac_padding_block)

	assert padding_block == FLACPadding(size=10)


def test_parse_flac_picture_block(flac_picture_block):
	picture_block, _ = FLAC._parse_metadata_block(flac_picture_block)

	assert picture_block == FLACPicture(
		type=ID3PictureType.COVER_FRONT,
		mime_type='image/png',
		description='',
		width=16,
		height=16,
		bit_depth=32,
		colors=0,
		data=flac_picture_block[45:],
	)


def test_parse_flac_seektable_block(flac_seektable_block):
	seektable_block, _ = FLAC._parse_metadata_block(flac_seektable_block)

	assert seektable_block == FLACSeekTable(
		[
			FLACSeekPoint(
				first_sample=first_sample,
				offset=offset,
				num_samples=num_samples)
			for first_sample, offset, num_samples in [
				(0, 0, 4096),
				(40960, 140, 4096),
				(86016, 294, 4096),
				(131072, 448, 4096),
				(176128, 602, 4096)
			]
		]
	)


def test_parse_flac_streaminfo_block(flac_streaminfo_block):
	streaminfo_block, _ = FLAC._parse_metadata_block(flac_streaminfo_block)

	assert streaminfo_block == FLACStreamInfo(
		start=None,
		size=None,
		min_block_size=4096,
		max_block_size=4096,
		min_frame_size=14,
		max_frame_size=16,
		bit_depth=16,
		bitrate=None,
		channels=2,
		duration=5,
		md5='9b1be87c6b579fde2341515f4d82c008',
		sample_rate=44100,
	)


def test_parse_flac_vorbis_comment_block(flac_vorbis_comment_block):
	vorbis_comment_block, _ = FLAC._parse_metadata_block(flac_vorbis_comment_block)

	assert vorbis_comment_block == FLACVorbisComments(
		_vendor='reference libFLAC 1.3.2 20170101',
		album=['test-album'],
		artist=['test-artist'],
		comment=['test-comment'],
		date=['2000'],
		discnumber=['1'],
		disctotal=['99'],
		genre=['test-genre'],
		title=['test-title'],
		tracknumber=['1'],
		tracktotal=['99'],
	)


def test_0_sized_flac_block_type_raises_formaterror(flac_0_size_block):
	with pytest.raises(FormatError) as ctx:
		FLAC._parse_metadata_block(flac_0_size_block)
	assert str(ctx.value) == "FLAC metadata block size must be greater than 0."


def test_invalid_flac_block_type_raises_formaterror(flac_invalid_block):
	with pytest.raises(FormatError) as ctx:
		FLAC._parse_metadata_block(flac_invalid_block)
	assert str(ctx.value) == "127 is not a valid FLAC metadata block type."


def test_flac_reserved_block_type_is_a_flacmetadatablock(flac_reserved_block):
	reserved_block, _ = FLAC._parse_metadata_block(flac_reserved_block)

	assert reserved_block == FLACMetadataBlock(
		type=10,
		data=b'\x00\x00\x00\x00',
	)


def test_ignore_id3v2_in_flac(flac_id3v2):
	FLAC.parse(flac_id3v2)


def test_0_duration_flac(flac_0_duration):
	FLAC.parse(flac_0_duration)


def test_reserved_flac_metadata_block_type(
	flac_reserved_block,
	flac_streaminfo_block,
):
	FLAC.parse(b'fLaC' + flac_streaminfo_block + b'\x8a' + flac_reserved_block[1:])


def test_no_flac_header_raises_formaterror(null):
	with pytest.raises(FormatError) as ctx:
		FLAC.parse(null)
	assert str(ctx.value) == "Valid FLAC header not found."


def test_flac_streaminfo_block_not_first_raises_formaterror(flac_padding_block):
	with pytest.raises(FormatError) as ctx:
		FLAC.parse(b'fLaC' + flac_padding_block)
	assert str(ctx.value) == "FLAC streaminfo block must be first."


def test_multiple_flac_cuesheet_blocks_raises_formaterror(
	flac_cuesheet_block,
	flac_streaminfo_block,
):
	with pytest.raises(FormatError) as ctx:
		FLAC.parse(b'fLaC' + flac_streaminfo_block + flac_cuesheet_block + flac_cuesheet_block)
	assert str(ctx.value) == "Multiple FLAC cuesheet blocks found."


def test_multiple_flac_seektable_blocks_raises_formaterror(
	flac_seektable_block,
	flac_streaminfo_block,
):
	with pytest.raises(FormatError) as ctx:
		FLAC.parse(b'fLaC' + flac_streaminfo_block + flac_seektable_block + flac_seektable_block)
	assert str(ctx.value) == "Multiple FLAC seektable blocks found."


def test_multiple_flac_streaminfo_blocks_raises_formaterror(flac_streaminfo_block):
	with pytest.raises(FormatError) as ctx:
		FLAC.parse(b'fLaC' + flac_streaminfo_block + flac_streaminfo_block)
	assert str(ctx.value) == "Multiple FLAC streaminfo blocks found."


def test_multiple_flac_vorbis_comment_blocks_raises_formaterror(
	flac_vorbis_comment_block,
	flac_streaminfo_block,
):
	with pytest.raises(FormatError) as ctx:
		FLAC.parse(b'fLaC' + flac_streaminfo_block + flac_vorbis_comment_block + flac_vorbis_comment_block)
	assert str(ctx.value) == "Multiple FLAC Vorbis comment blocks found."
