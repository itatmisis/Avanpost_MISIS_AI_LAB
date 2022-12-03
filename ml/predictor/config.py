import torch
import torchvision
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
pretrained_model = torchvision.models.resnet50(weights=torchvision.models.ResNet50_Weights.IMAGENET1K_V2)
weights = torchvision.models.ResNet50_Weights.IMAGENET1K_V2
preprocess = weights.transforms()
