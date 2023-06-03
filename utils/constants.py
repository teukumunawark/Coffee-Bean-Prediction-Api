import torch
from torchvision import datasets, transforms

batch_size = 4
train_dir = './data/classes'

mean = [0.7980, 0.7820, 0.7562]
std = [0.1441, 0.1729, 0.2341]

# Load the model from file
model = torch.load('./models/model.pth')
model.eval()

if torch.cuda.is_available():
    model.cuda()

idx_to_class = {v: k for k, v in datasets.ImageFolder(
    root=train_dir).class_to_idx.items()}

image_transforms = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean, std)
])
