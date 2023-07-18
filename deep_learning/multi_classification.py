from typing import List
import base64
import torch
from PIL import Image
from io import BytesIO
import torch.nn.functional as F
import utils.constants as constants


def classify_image(image_path: str, transform: torch.Tensor, model: torch.nn.Module) -> dict:
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
        model.eval()
        out = model(test_image_tensor)
        ps = F.softmax(out.data, dim=1)
        topk, topclass = ps.topk(4, dim=1)
        
    for i in range(4):
        print(constants.idx_to_class[topclass.cpu().numpy()[0][i]])
    
    classifications = [{
        "name": f"{constants.idx_to_class[topclass.cpu().numpy()[0][i]]}",
        "score": round(topk.cpu().numpy()[0][i] * 100, 1),
    } for i in range(4)]

    buffered = BytesIO()
    test_image.save(buffered, format="JPEG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return {
        "result": classifications,
        "image": image_base64
    }


def classify_multiple_images(image_paths: List[str]) -> List[dict]:
    classifications = []
    for image_path in image_paths:
        c = classify_image(
            image_path,
            constants.image_transforms,
            constants.model,
        )
        classification = {
            "result": [c] if "error" in c else c["result"],
            "image": c["image"] if "image" in c else None
        }
        classifications.append(classification)

    with torch.no_grad():
        classifications = sorted(
            classifications, key=lambda x: x["result"][0]["score"], reverse=True)

    return classifications
