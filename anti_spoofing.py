import sys
import types

try:
    import imp
except ImportError:
    import importlib.machinery
    import importlib.util
    from types import ModuleType

    class MockImp:

        def find_module(self, name, path=None):
            # Divert module finding to modern importlib
            spec = importlib.machinery.PathFinder.find_spec(name, path)
            if spec is None:
                raise ImportError(f"No module named '{name}'")
            return (
                None,
                spec.origin,
                (
                    "",
                    "",
                    importlib.machinery.BYTECODE_SUFFIXES,
                ),
            )

        def load_module(self, name, file, filename, details):
            spec = importlib.util.spec_from_file_location(name, filename)
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)
            return module

        def new_module(self, name):
            return ModuleType(name)

    sys.modules["imp"] = MockImp()

import cv2
from deepface import DeepFace


class AntiSpoofingDetector:

    def __init__(self):
        pass

    def process_frame(self, frame):
        try:
            results = DeepFace.extract_faces(
                img_path=frame,
                detector_backend="yunet",
                anti_spoofing=True,
                enforce_detection=False,
            )

            # Pastikan results tidak kosong
            if results and isinstance(results, list):
                for res in results:
                    # Ambil area wajah
                    facial_area = res.get("facial_area", {})

                    x = int(
                        facial_area.get("x")
                        if facial_area.get("x") is not None
                        else facial_area.get("left", 0)
                    )
                    y = int(
                        facial_area.get("y")
                        if facial_area.get("y") is not None
                        else facial_area.get("top", 0)
                    )
                    w = int(
                        facial_area.get("w")
                        if facial_area.get("w") is not None
                        else facial_area.get("width", 0)
                    )
                    h = int(
                        facial_area.get("h")
                        if facial_area.get("h") is not None
                        else facial_area.get("height", 0)
                    )

                    if w <= 10 or h <= 10:
                        continue

                    is_real = res.get("is_real", False)

                    if is_real:
                        color = (0, 255, 0)
                        label = "ASLI (REAL)"
                    else:
                        color = (0, 0, 255)
                        label = "PALSU (FAKE)"

                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)

                    cv2.putText(
                        frame,
                        label,
                        (
                            x,
                            max(y - 12, 20),
                        ),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        color,
                        2,
                    )
            else:
                # Opsi debug: print jika DeepFace mengembalikan data kosong
                # print("Tidak ada wajah terdeteksi di frame ini")
                pass

        except Exception as e:
            print(f"[DEBUG ERROR] Gagal memproses frame: {e}")

        return frame


if __name__ == "__main__":
    detector = AntiSpoofingDetector()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[ERROR] Kamera tidak dapat diakses!")
        exit()

    print("[INFO] Program Berjalan dengan Anti-Spoofing Akurat.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        processed_frame = detector.process_frame(frame)

        cv2.imshow("Anti-Spoofing Detection", processed_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
