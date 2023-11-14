from kvspec import loader


def test_load_mp4():
    source = loader.extract_frames_from_mp4("data/movie.mp4", ".jpg")

    it = iter(source)
    key, value = next(it)
    assert key == "1.jpg"
    assert isinstance(value, bytes)

    key, value = next(it)
    assert key == "2.jpg"
    assert isinstance(value, bytes)

    result = [k for k, v in source._iterate()]
    assert len(result) == 406
