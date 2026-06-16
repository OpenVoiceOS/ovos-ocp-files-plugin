import pytest

from ovos_ocp_files_plugin import (
	FormatError,
	ID3v1,
	ID3v1Fields,
)
from test.fixtures import (
	id3v1,
	null,
)


def test_valid(id3v1):
	id3v1 = ID3v1.parse(id3v1)
	expected_fields = ID3v1Fields(
		title=['test-title'],
		artist=['test-artist'],
		album=['test-album'],
		year=['2000'],
		comment=['test-comment'],
		tracknumber=['1'],
		genre=['Jazz']
	)

	assert id3v1.tags == expected_fields


def test_missing_tag_raises_formaterror(null):
	with pytest.raises(FormatError) as exc:
		ID3v1.parse(null)
	assert str(exc.value) == "Valid ID3v1 header not found."


def test_no_title(id3v1):
	no_title = ID3v1.parse(id3v1.replace(b'test-title', b'\x00' * 10))
	assert 'title' not in no_title.tags


def test_no_artist(id3v1):
	no_artist = ID3v1.parse(id3v1.replace(b'test-artist', b'\x00' * 11))
	assert 'artist' not in no_artist.tags


def test_no_album(id3v1):
	no_album = ID3v1.parse(id3v1.replace(b'test-album', b'\x00' * 10))
	assert 'album' not in no_album.tags


def test_no_year(id3v1):
	no_year = ID3v1.parse(id3v1.replace(b'2000', b'\x00' * 4))
	assert 'year' not in no_year.tags


def test_no_comment(id3v1):
	no_comment = ID3v1.parse(id3v1.replace(b'test-comment', b'\x00' * 12))
	assert 'comment' not in no_comment.tags


def test_no_tracknumber(id3v1):
	no_tracknumber = ID3v1.parse(id3v1.replace(b'\x01', b'\x00'))
	assert 'tracknumber' not in no_tracknumber.tags


def test_invalid_genre(id3v1):
	invalid_genre = ID3v1.parse(id3v1.replace(b'\x01\x08', b'\x01\xEF'))
	assert 'genre' not in invalid_genre.tags
