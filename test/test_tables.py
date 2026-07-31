from ovos_ocp_files_plugin.formats.tables import (
	_BaseEnum,
	_BaseIntEnum,
)


class TestEnum(_BaseEnum):
	__test__ = False
	MEMBER = 0


class TestIntEnum(_BaseIntEnum):
	__test__ = False
	MEMBER = 0


def test_table_enum_reprs():
	assert repr(TestEnum.MEMBER) == '<TestEnum.MEMBER>'
	assert repr(TestIntEnum.MEMBER) == '<TestIntEnum.MEMBER>'
