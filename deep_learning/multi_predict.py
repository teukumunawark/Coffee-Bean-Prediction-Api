import os
import torch
from PIL import Image
from flask import jsonify
from datetime import datetime
import torch.nn.functional as F
from utils.round_decimals import round_decimals_up

import utils.constants as constants


def predict_image(image_path, transform, model):
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

    predictions = []
    for i in range(4):
        cls_idx = int(topclass.cpu().numpy()[0][i])
        cls_name = constants.idx_to_class[topclass.cpu().numpy()[0][i]]
        score = round_decimals_up(topk.cpu().numpy()[0][i] * 100, 1)
        probability = round_decimals_up(ps.cpu().numpy()[0][cls_idx] * 100, 1)

        prediction = {
            "class_name": cls_name,
            "score": score,
            "probability": probability
        }
        predictions.append(prediction)

    return {"prediction": predictions}


def multiprediction(image_names):
    responses = []
    for image_name in image_names:
        response = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        image_path = os.path.join(os.getcwd(), image_name)
        image_prediction = predict_image(
            image_path, constants.image_transforms, constants.model)

        if "error" in image_prediction:
            response["prediction"] = [image_prediction]
        else:
            response["prediction"] = image_prediction["prediction"]

        responses.append(response)

    return jsonify(responses)
