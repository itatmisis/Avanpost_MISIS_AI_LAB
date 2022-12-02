import warnings
import torchvision
import zipfile

import torch
import torch.nn as nn
from tqdm import tqdm
from torch.utils.data import DataLoader


def device_to():
    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    return device


device = device_to()


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

weights = torchvision.models.ResNet50_Weights.IMAGENET1K_V2
preprocess = weights.transforms()

train_set = torchvision.datasets.ImageFolder('train', transform=preprocess)
val_set = torchvision.datasets.ImageFolder('valid', transform=preprocess)

train_dataset = DataLoader(train_set, batch_size=16, num_workers=1, shuffle=True)
val_dataset = DataLoader(val_set, batch_size=16, num_workers=1, shuffle=False)


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


model_backbone = torch.load('resnet_model.pt') # подгружаем нашу предобученную модель

num_classes = 10 # количество классов
model = ResNet(model_backbone, 10)


def train(model, epoches, train_data, val_data, device):
    for i in tqdm(range(epoches)):
        train_loss, train_accuracy = train_epoch(model, train_data, device)
        test_loss, test_accuracy = evaluation_epoch(model, val_data, device)
        print(f'\n Epoch #{i + 1}\nTrain loss = {train_loss}, Train accuracy = {train_accuracy}')
        print(f'Test loss = {test_loss}, Test accuracy = {test_accuracy}')
    torch.save(model, 'new_model.pt')


if __name__ == '__main__':
    train(model=model, epoches=5, train_data=train_dataset, val_data=val_dataset, device=device)




