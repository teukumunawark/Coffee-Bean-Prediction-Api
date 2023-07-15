# import torch
# from PIL import Image
# import torch.nn.functional as F
# from flask import jsonify
# from utils.round_decimals import round_decimals_up

# import utils.constants as constants


# def singleclassification(image_name):

#     with Image.open(image_name) as img:
#         tensor_img = constants.image_transforms(img).unsqueeze(0)
#         if torch.cuda.is_available():
#             tensor_img = tensor_img.cuda()

#         with torch.no_grad():
#             output = F.softmax(constants.model(tensor_img), dim=1)
#             top_k_prob, top_k_index = output.topk(4, dim=1)

#         predictions = []
#         for i in range(4):
#             class_idx = top_k_index[0][i].item()
#             class_name = constants.idx_to_class[class_idx]
#             score = round_decimals_up(top_k_prob[0][i].item() * 100, 1)

#             prediction = {
#                 "name": class_name,
#                 "score": score,
#             }
#             predictions.append(prediction)

#         response = {
#             "result": predictions
#         }
#         return jsonify(response)


# def highestscore(image_name):
#     with Image.open(image_name) as img:
#         tensor_img = constants.image_transforms(img).unsqueeze(0)
#         tensor_img = tensor_img.to(device)

#         with torch.no_grad():
#             output = F.softmax(constants.model(tensor_img), dim=1)
#             top_k_prob, top_k_index = output.topk(1, dim=1)

#         class_idx = top_k_index[0][0].item()
#         class_name = constants.idx_to_class[class_idx]
#         score = round_decimals_up(top_k_prob[0][0].item() * 100, 1)

#         prediction = {
#             "name": class_name,
#             "score": score,
#         }
#         return prediction

# if torch.cuda.is_available():
#     device = torch.device("cuda")
# else:
#     device = torch.device("cpu")