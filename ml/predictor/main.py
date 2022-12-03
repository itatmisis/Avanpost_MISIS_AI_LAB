import warnings
import torchvision
import zipfile

import torch
import torch.nn as nn
from tqdm import tqdm
from torch.utils.data import DataLoader
from predictor.config import device, preprocess, pretrained_model

def train_epoch(model, train, device):
    model.train(True)
    model.to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = torch.nn.CrossEntropyLoss()
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=1, gamma=0.7)

    optimizer.zero_grad()
    total = len(train.dataset)
    epoch_loss, epoch_acc = 0, 0
    for inp, target in train:
        inp, target = inp.to(device), target.to(device)
        pred = model(inp)

        loss = criterion(pred, target)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        epoch_loss += loss.item()
        epoch_acc += torch.sum(torch.argmax(pred, 1) == target).item()

    scheduler.step()

    epoch_acc = epoch_acc / total
    epoch_loss = epoch_loss / total
    return epoch_loss, epoch_acc


def evaluation_epoch(model, val, device):
    model.train(False)
    model.to(device)

    total = len(val.dataset)
    epoch_loss, epoch_acc = 0, 0
    criterion = torch.nn.CrossEntropyLoss()

    with torch.no_grad():
        for inp, target in val:
            inp, target = inp.to(device), target.to(device)
            pred = model(inp)
            loss = criterion(pred, target)
            epoch_loss += loss.item()
            epoch_acc += torch.sum(torch.argmax(pred, 1) == target).item()

    epoch_acc = epoch_acc / total
    epoch_loss = epoch_loss / total
    return epoch_loss, epoch_acc


'''
with open('classes.txt', "r") as file:
    json_str = file.read().splitlines()

labels = list(map(lambda x: x.split("\'")[1], json_str))

with zipfile.ZipFile('validation.zip', 'r') as zip_ref:
    zip_ref.extractall()'''

#new_path = 'train'




class ResNet(nn.Module):
    def __init__(self, backbone, output_dim):
        super().__init__()
        self.backbone = backbone
        del backbone.fc
        self.backbone.dropout = torch.nn.Dropout(p=0.05)
        self.backbone.fc = torch.nn.Linear(in_features=2048, out_features=output_dim, bias=True)
        for name, param in self.backbone.named_parameters():
            if not (name.startswith("layer4")) and not name.startswith("fc"):
                param.requires_grad = False

    def forward(self, image):
        out = self.backbone(image)
        return out

def train(model, epoches, train_data, device, val_data = None):
    for i in tqdm(range(epoches)):
        train_loss, train_accuracy = train_epoch(model, train_data, device)
        print(f'\n Epoch #{i + 1}\nTrain loss = {train_loss}, Train accuracy = {train_accuracy}')
        if val_data is not None:
            test_loss, test_accuracy = evaluation_epoch(model, val_data, device)
            print(f'Test loss = {test_loss}, Test accuracy = {test_accuracy}')
    # torch.save(model, 'new_model.pt')

def train_model(model_path:str, dataset_path:str):
    train_set = torchvision.datasets.ImageFolder(dataset_path, transform=preprocess)
    train_dataset = DataLoader(train_set, batch_size=16, num_workers=1, shuffle=True)
    # подгружаем нашу предобученную модель
    model_backbone = pretrained_model
    # создаем новую модель с нашим количеством классов
    model = ResNet(model_backbone, 10) 
    train(model=model, epoches=5, train_data=train_dataset, device=device)
    model_path += ".pth"
    torch.save(model, model_path)

# if __name__ == '__main__':
#     val_set = torchvision.datasets.ImageFolder('valid', transform=preprocess)
#     val_dataset = DataLoader(val_set, batch_size=16, num_workers=1, shuffle=False)