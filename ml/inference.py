import os
import torch
import tqdm
from PIL import Image
from main import train_set, device, preprocess


def predict(model_name, device, img_root, transform):
    model = torch.load(model_name)
    model.eval()
    model.to(device)
    image = Image.open(img_root)
    image = transform(image)
    with torch.no_grad():
        ans = model(image.cuda().unsqueeze(dim=0)).argmax(dim=1).detach().cpu().item()
        print(ans)
        ans = train_set.classes[ans]

    return ans


pred = predict(model_name='new_model.pt', device=device, img_root="test_data/shutterstock_81020101.jpg", transform=preprocess)

print(pred)
