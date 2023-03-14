import os
import torch
from PIL import Image
import torch.nn.functional as F
from torchvision import datasets, transforms
from flask import jsonify
from round_decimals import round_decimals_up
from datetime import datetime

batch_size = 4
train_dir = './data/train'

mean = [0.7980, 0.7820, 0.7562]
std = [0.1441, 0.1729, 0.2341]

# Load the model from file
model = torch.load('./models/model.pth')
model.eval()

if torch.cuda.is_available():
    model.cuda()
image_transforms = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean, std)
])

idx_to_class = {v: k for k, v in datasets.ImageFolder(
    root=train_dir).class_to_idx.items()}

def single_prediction(image_name):
    transform = image_transforms
    test_image = Image.open(image_name)
    test_image_tensor = transform(test_image)

    if torch.cuda.is_available():
        test_image_tensor = test_image_tensor.view(1, 3, 256, 256).cuda()
    else:
        test_image_tensor = test_image_tensor.view(1, 3, 256, 256)
        
    with torch.no_grad():
        # Model outputs log probabilities
        out = model(test_image_tensor)
        ps = F.softmax(out.data, dim=1)
        topk, topclass = ps.topk(4, dim=1)

        # Create dictionary of predictions
        predictions = []
        for i in range(4):
            cls_idx = int(topclass.cpu().numpy()[0][i])
            cls_name = idx_to_class[topclass.cpu().numpy()[0][i]]
            score = round_decimals_up(topk.cpu().numpy()[0][i] * 100, 1)
            probability = round_decimals_up(
                ps.cpu().numpy()[0][cls_idx] * 100, 1)

            prediction = {
                "class_name": cls_name,
                "score": score,
                "probability": probability
            }

            predictions.append(prediction)

        # Create dictionary of response
        response = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "predictions": predictions
        }

        # Return JSON response
        return jsonify(response)


def multiprediction(image_names):
    transform = image_transforms
    responses = []
    for image_name in image_names:
        try:
            test_image = Image.open(image_name)
        except Exception as e:
            response = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "predictions": [{"error": str(e)}]
            }
            responses.append(response)
            continue
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
            cls_name = idx_to_class[topclass.cpu().numpy()[0][i]]
            score = round_decimals_up(topk.cpu().numpy()[0][i] * 100, 1)
            probability = round_decimals_up(
                ps.cpu().numpy()[0][cls_idx] * 100, 1)

            prediction = {
                "class_name": cls_name,
                "score": score,
                "probability": probability
            }
            predictions.append(prediction)
        response = {
            "prediction": predictions
        }
        responses.append(response)
        
    return jsonify(responses)
