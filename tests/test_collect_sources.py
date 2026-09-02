from pathlib import Path

import pytest

from scripts.collect_sources import (
    SourceCollectionError,
    count_images_by_parent_directory,
    find_images,
    get_data_directory,
    select_sources,
)


def test_select_sources_returns_all_sources():
    sources = [
        {"id": "source_a"},
        {"id": "source_b"},
    ]

    selected = select_sources(sources, "all")

    assert selected == sources


def test_select_sources_returns_one_requested_source():
    sources = [
        {"id": "source_a"},
        {"id": "source_b"},
    ]

    selected = select_sources(sources, "source_b")

    assert selected == [{"id": "source_b"}]


def test_select_sources_rejects_unknown_source():
    with pytest.raises(SourceCollectionError):
        select_sources([{"id": "source_a"}], "unknown")


def test_find_images_ignores_non_image_files(tmp_path):
    images_directory = tmp_path / "cardboard"
    images_directory.mkdir()

    image_path = images_directory / "sample.JPG"
    text_path = images_directory / "notes.txt"

    image_path.touch()
    text_path.touch()

    images = find_images(tmp_path)

    assert images == [image_path]


def test_count_images_by_parent_directory():
    image_paths = [
        Path("cardboard/image_1.jpg"),
        Path("cardboard/image_2.jpg"),
        Path("glass/image_1.jpg"),
    ]

    assert count_images_by_parent_directory(image_paths) == {
        "cardboard": 2,
        "glass": 1,
    }


def test_get_data_directory_uses_original_subdirectory(tmp_path):
    original_directory = (
        tmp_path / "data/raw/garbage_dataset_v2/original"
    )
    original_directory.mkdir(parents=True)

    source = {
        "local_directory": "data/raw/garbage_dataset_v2",
        "source_subdirectory_used": "original",
    }

    assert get_data_directory(tmp_path, source) == original_directory