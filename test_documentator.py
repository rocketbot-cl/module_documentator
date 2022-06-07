from . import documentator
import os
import pytest


# Test if the Exception if correctly raised
def test_package_json_not_found_exception():
    with pytest.raises(Exception, match="File package.json not found!"):
        assert documentator.Documentator(r"no_json_testing_folder")


@pytest.fixture
def arrange_documentator():
    test_instance = documentator.Documentator(r"json_testing_folder")
    test_instance.to_manual()
    yield test_instance
    # cleanup
    os.remove("json_testing_folder/CHANGES.txt")
    os.remove("json_testing_folder/docs/Manual_gmail_.md")
    os.rmdir("json_testing_folder/docs")


def test_documentator_changes(arrange_documentator):
    assert os.path.isfile("json_testing_folder/CHANGES.txt")
    with open("json_testing_folder/CHANGES.txt", "r") as file:
        contents = file.read()
        assert contents == "Sat Nov 13 19:41:50 2021  v1.2 test 2"


def test_documentator_docs_dir(arrange_documentator):
    # check if docs folder exists
    assert os.path.isdir("json_testing_folder/docs")
    # check if contents have a .pdf file
    assert os.path.isfile("json_testing_folder/docs/Manual_gmail_.md")
