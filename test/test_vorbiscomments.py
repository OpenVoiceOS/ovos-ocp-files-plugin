import pytest

from ovos_ocp_files_plugin import (
	FormatError,
	TagError,
	VorbisComment,
	VorbisComments,
)
from test.fixtures import vorbis_comments


@pytest.mark.parametrize(
	"data,expected",
	list(zip(
		[
			b'\x10\x00\x00\x00album=test-album',
			b'\x14\x00\x00\x00COMMENT=test-comment',
			b'\t\x00\x00\x00date=2000',
			b'\x0c\x00\x00\x00discnumber=1',
			b'\x10\x00\x00\x00genre=test-genre',
			b'\x0c\x00\x00\x00DISCTOTAL=99',
			b'\r\x00\x00\x00TRACKTOTAL=99',
			b'\r\x00\x00\x00tracknumber=1',
		],
		[
			VorbisComment(
				name='album',
				value='test-album',
			),
			VorbisComment(
				name='comment',
				value='test-comment',
			),
			VorbisComment(
				name='date',
				value='2000',
			),
			VorbisComment(
				name='discnumber',
				value='1',
			),
			VorbisComment(
				name='genre',
				value='test-genre',
			),
			VorbisComment(
				name='disctotal',
				value='99',
			),
			VorbisComment(
				name='tracktotal',
				value='99',
			),
			VorbisComment(
				name='tracknumber',
				value='1',
			),
		],
	))
)
def test_vorbiscomment(data, expected):
	assert VorbisComment.parse(data) == expected


def test_invalid_equals_in_vorbis_comment_raises_formaterror():
	with pytest.raises(FormatError) as exc:
		VorbisComment.parse(b'\x09\x00\x00\x00albumtest-album')
	assert str(exc.value) == "Vorbis comment must contain an ``=``."


def test_invalid_character_in_vorbis_comment_name_raises_tagerror():
	with pytest.raises(TagError) as exc:
		VorbisComment.parse(b'\x10\x00\x00\x00albu~=test-album')
	assert str(exc.value) == "Invalid character in Vorbis comment name: ``albu~``."


def test_vorbiscomments(vorbis_comments):
	data = vorbis_comments
	vorbis_comments_init = VorbisComments(
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
	vorbis_comments_parse = VorbisComments.parse(data)

	assert vorbis_comments_init == vorbis_comments_parse


def test_invalid_character_in_vorbis_comment_name_raises_tagerror_in_vorbiscomments():
	with pytest.raises(TagError) as exc:
		VorbisComments({'albu~': 'test-album'})
	assert str(exc.value) == "Invalid character in Vorbis comment name: ``albu~``."
