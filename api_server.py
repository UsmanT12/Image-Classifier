import os
import shutil
import tempfile
from typing import Dict, List, Tuple

# Patch Starlette's multipart limits BEFORE importing FastAPI, so Request uses our class.
import starlette.formparsers as _formparsers

class _LenientMultiPartParser(_formparsers.MultiPartParser):
    """Raise Starlette's 1000-file limit so large image datasets work."""
    def __init__(self, *args, **kwargs):
        kwargs["max_files"] = 200_000
        kwargs["max_fields"] = 200_000
        super().__init__(*args, **kwargs)

_formparsers.MultiPartParser = _LenientMultiPartParser  # type: ignore[assignment]

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from ImageClass_helper import predict_class
from supportFuncs import precompute_classes


app = FastAPI(title="Image Classifier API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _safe_relpath(name: str) -> str:
    """
    Convert an arbitrary upload filename into a safe relative path.
    Supports browser folder uploads where `filename` includes subpaths.
    """
    name = (name or "file").replace("\\", "/")
    # Drop leading slashes
    name = name.lstrip("/")

    parts: List[str] = []
    for part in name.split("/"):
        if part in ("", ".", ".."):
            continue
        # Very defensive: avoid weird drive-letter segments (Windows)
        if part.endswith(":"):
            continue
        parts.append(part)

    if not parts:
        return "file"
    return os.path.join(*parts)


def _pick_dataset_root(base_dir: str) -> str:
    """
    If the upload contains a single top-level folder, use it as the dataset root.
    Otherwise treat `base_dir` as the dataset root.
    """
    try:
        entries = [
            d
            for d in os.listdir(base_dir)
            if os.path.isdir(os.path.join(base_dir, d)) and not d.startswith(".")
        ]
    except FileNotFoundError:
        return base_dir

    if len(entries) == 1:
        return os.path.join(base_dir, entries[0])
    return base_dir


def _infer_class_from_filename(filename: str) -> str:
    """
    Derive a class label from a flat filename when no subfolders are present.
    - For names like 'cat.1.jpg' -> 'cat'
    - For digit-style names like '7_001.jpg' -> '7'
    """
    base = os.path.splitext(os.path.basename(filename))[0]
    if not base:
        return "class"
    # If it starts with a digit, treat that digit as the class (e.g. MNIST-like)
    if base[0].isdigit():
        return base[0]
    # Otherwise, take the part before the first dot (e.g. 'cat.1' -> 'cat')
    return base.split(".")[0]


def _reorganize_flat_images_into_class_dirs(root: str) -> None:
    """
    If there are no subdirectories under `root`, but there are images directly in it,
    group them into subfolders by inferred class name.
    """
    entries = os.listdir(root)
    has_dirs = any(os.path.isdir(os.path.join(root, d)) for d in entries)
    if has_dirs:
        return

    moved_any = False
    for name in entries:
        full = os.path.join(root, name)
        if not os.path.isfile(full):
            continue
        lower = name.lower()
        if not (lower.endswith(".jpg") or lower.endswith(".jpeg")):
            continue

        cls = _infer_class_from_filename(name)
        target_dir = os.path.join(root, cls)
        os.makedirs(target_dir, exist_ok=True)
        shutil.move(full, os.path.join(target_dir, name))
        moved_any = True

    # If nothing was moved, leave the structure as-is; the later check will still error out.


def _evaluate(trained_arr, test_arr) -> Dict:
    correct = 0
    total = 0

    class_accuracy: Dict[str, Dict[str, int]] = {str(m.name): {"correct": 0, "total": 0} for m in trained_arr}
    trained_images: Dict[str, int] = {str(m.name): int(getattr(m, "trained_images", 0)) for m in trained_arr}

    misclassified: List[Dict[str, str]] = []

    for test_matrix in test_arr:
        for image_name, image_vector in test_matrix.img_dict.items():
            predicted = predict_class(trained_arr, image_vector)
            actual = str(test_matrix.name)

            total += 1
            class_accuracy.setdefault(actual, {"correct": 0, "total": 0})
            class_accuracy[actual]["total"] += 1

            if predicted == actual:
                correct += 1
                class_accuracy[actual]["correct"] += 1
            else:
                misclassified.append(
                    {"predicted": str(predicted), "actual": actual, "image": str(image_name), "class": actual}
                )

    wrong = total - correct
    accuracy = (correct / total) if total > 0 else 0.0

    per_class = {}
    for cls, stats in sorted(class_accuracy.items(), key=lambda kv: kv[0]):
        denom = stats["total"]
        per_class[cls] = {
            "accuracy": (stats["correct"] / denom) if denom > 0 else 0.0,
            "correct": stats["correct"],
            "total": stats["total"],
            "trained_images": trained_images.get(cls, 0),
        }

    return {
        "correct": correct,
        "wrong": wrong,
        "total": total,
        "accuracy": accuracy,
        "per_class": per_class,
        "misclassified": misclassified[:200],  # keep responses bounded
    }


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/train-test")
async def train_test(
    training_files: List[UploadFile] = File(...),
    test_files: List[UploadFile] = File(...),
    threshold: float = Form(0.015),
    img_width: int = Form(28),
    img_height: int = Form(28),
    num_classes: int = Form(2),
):
    if num_classes < 2 or num_classes > 10:
        raise HTTPException(status_code=400, detail="num_classes must be between 2 and 10")
    if threshold < 0 or threshold > 1.0:
        raise HTTPException(status_code=400, detail="threshold must be between 0 and 1.0")
    if img_width < 1 or img_height < 1 or img_width > 128 or img_height > 128:
        raise HTTPException(status_code=400, detail="img_width/img_height must be between 1 and 128")

    with tempfile.TemporaryDirectory(prefix="image-classifier-") as tmp:
        train_base = os.path.join(tmp, "train")
        test_base = os.path.join(tmp, "test")
        os.makedirs(train_base, exist_ok=True)
        os.makedirs(test_base, exist_ok=True)

        async def _save_all(files: List[UploadFile], base: str) -> None:
            for f in files:
                rel = _safe_relpath(f.filename)
                out_path = os.path.join(base, rel)
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                with open(out_path, "wb") as w:
                    shutil.copyfileobj(f.file, w)

        await _save_all(training_files, train_base)
        await _save_all(test_files, test_base)

        training_set_path = _pick_dataset_root(train_base)
        testing_set_path = _pick_dataset_root(test_base)

        # If the user could only select flat files (no explicit subfolders),
        # reorganize them into class directories by inferring labels from filenames.
        _reorganize_flat_images_into_class_dirs(training_set_path)
        _reorganize_flat_images_into_class_dirs(testing_set_path)

        # The classifier expects: dataset_root/<class_name>/*.jpg
        train_dirs = [
            d
            for d in os.listdir(training_set_path)
            if os.path.isdir(os.path.join(training_set_path, d)) and not d.startswith(".")
        ]
        test_dirs = [
            d
            for d in os.listdir(testing_set_path)
            if os.path.isdir(os.path.join(testing_set_path, d)) and not d.startswith(".")
        ]
        if not train_dirs:
            raise HTTPException(
                status_code=400,
                detail="No training classes were found. Ensure you selected at least some .jpg/.jpeg files.",
            )
        if not test_dirs:
            raise HTTPException(
                status_code=400,
                detail="No test classes were found. Ensure you selected at least some .jpg/.jpeg files.",
            )

        trained_arr, test_arr = precompute_classes(
            training_set_path, testing_set_path, (img_width, img_height), num_classes, threshold
        )

        if not trained_arr or not test_arr:
            raise HTTPException(
                status_code=400,
                detail="No classes were initialized. Check folder structure and ensure images are .jpg/.jpeg.",
            )

        return _evaluate(trained_arr, test_arr)

