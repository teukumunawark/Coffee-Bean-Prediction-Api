from typing import List
import base64
from io import BytesIO
import torch
from PIL import Image
import torch.nn.functional as F
from utils.round_decimals import round_decimals_up

import utils.constants as constants


def imageclassification(image_path, transform, model):
    try:
        test_image = Image.open(image_path)
    except Exception as e:
        return {"error": str(e)}

    test_image_tensor = transform(test_image)
    if torch.cuda.is_available():
        test_image_tensor = test_image_tensor.view(1, 3, 256, 256).cuda()
    else:
        test_image_tensor = test_image_tensor.view(1, 3, 256, 256)

    with torch.no_grad():
        out = model(test_image_tensor)
        ps = F.softmax(out.data, dim=1)
        topk, topclass = ps.topk(4, dim=1)

    classifications = [{
        "name": constants.idx_to_class[topclass.cpu().numpy()[0][i]],
        "score": round_decimals_up(topk.cpu().numpy()[0][i] * 100, 1)
    } for i in range(4)]

    buffered = BytesIO()
    test_image.save(buffered, format="JPEG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return {
        "result": classifications,
        "image": image_base64
    }


def multiclassification(image_paths: List[str]) -> List[dict]:
    classifications = []
    for image_path in image_paths:
        c = imageclassification(
            image_path, constants.image_transforms, constants.model)
        classification = {
            "result": [c] if "error" in c else c["result"],
            "image": c["image"] if "image" in c else None
        }
        classifications.append(classification)

    with torch.no_grad():
        classifications.sort(
            key=lambda x: x["result"][0]["score"], reverse=True)

    return classifications
