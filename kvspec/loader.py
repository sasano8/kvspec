from typing import Iterator, Tuple
from itertools import islice


class MediaStream:
    def __init__(self, path, encode: str = ".jpg"):
        self.path = path
        self.encode = encode

    def __getitem__(self, key):
        if isinstance(key, int):
            key = slice(key, key + 1)

        if isinstance(key, slice):
            source = islice(self._iterate(), key.start, key.stop, key.step)
            return self._encode(source)
        else:
            raise Exception()

    def _get_capture(self):
        import cv2

        return cv2.VideoCapture(self.path)

    def _iterate(self):
        import cv2

        cap = self._get_capture()
        try:
            encode = self.encode
            current_frame = 0

            while cap.isOpened():
                success, frame = cap.read()
                if not success:
                    # raise StopIteration()  # 必ずStopIterationなのか、それ以外の例外が含まれるのか理解していない
                    return

                current_frame += 1
                frame_name = str(current_frame) + encode
                yield frame_name, frame

        finally:
            cap.release()
            cv2.destroyAllWindows()

    def _encode(self, source):
        import cv2

        for key, frame in source:
            success, encoded_image = cv2.imencode(self.encode, frame)
            if not success:
                # raise StopIteration()  # 必ずStopIterationなのか、それ以外の例外が含まれるのか理解していない
                return
            yield key, encoded_image.tobytes()

    def __iter__(self) -> Iterator[Tuple[str, bytes]]:
        return self._encode(self._iterate())


def extract_frames_from_mp4(path, encode: str = ".jpg") -> MediaStream:
    return MediaStream(path, encode)


def save_sound():
    """wav, mp3, aac
    cv2は画像のみ取り扱う
    """
