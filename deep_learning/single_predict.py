import torch
from PIL import Image
import torch.nn.functional as F
from flask import jsonify
from round_decimals import round_decimals_up
from datetime import datetime

import constants

def singleprediction(image_name):
    with Image.open(image_name) as img:
        tensor_img = constants.image_transforms(img).unsqueeze(0)
        if torch.cuda.is_available():
            tensor_img = tensor_img.cuda()
        
        with torch.no_grad():
            output = F.softmax(constants.model(tensor_img), dim=1)
            top_k_prob, top_k_index = output.topk(4, dim=1)

        predictions = []
        for i in range(4):
            class_idx = top_k_index[0][i].item()
            class_name = constants.idx_to_class[class_idx]
            score = round_decimals_up(top_k_prob[0][i].item() * 100, 1)
            probability = round_decimals_up(output[0][class_idx].item() * 100, 1)

            prediction = {
                "class_name": class_name,
                "score": score,
                "probability": probability
            }
            predictions.append(prediction)

        response = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "predictions": predictions
        }
        return jsonify(response)
