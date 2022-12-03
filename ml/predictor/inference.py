import torch
import torchvision
from PIL import Image
from predictor.config import device, preprocess

def predict(model_name:str, dataset_path:str, img_root:str):
    model_name += ".pth"
    train_set = torchvision.datasets.ImageFolder(dataset_path, transform=preprocess)
    model = torch.load(model_name)
    model.eval()
    model.to(device)
    image = Image.open(img_root)
    image = preprocess(image)
    with torch.no_grad():
        ans = model(image.unsqueeze(dim=0)).argmax(dim=1).detach().cpu().item()
        ans = train_set.classes[ans]
    return ans

if __name__ == '__main__':
    pred = predict(model_name='new_model.pt', img_root="test_data/shutterstock_81020101.jpg")
    print(pred)
