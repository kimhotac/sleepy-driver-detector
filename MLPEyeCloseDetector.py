import torch
import torch.nn as nn
import torchvision.transforms as transforms
from EyeCloseDetection import EyeCloseDetector

class MLPEyeCloseDetector(EyeCloseDetector):
    def __init__ (self, model_path):
        super().__init__()  # 부모 클래스 초기화 (필요한 경우)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self.model = EyeCNN().to(self.device)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()
    
        self.transform = transforms.Compose([
            transforms.ToPILImage(),      # OpenCV 이미지 (numpy) → PIL 이미지
            transforms.Grayscale(),
            transforms.Resize((90, 90)),
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,))
        ])
    def predict(self, eye_img):
        if eye_img.size == 0:
            return None

        input_tensor = self.transform(eye_img).unsqueeze(0).to(self.device)
    
        with torch.no_grad():
            output = self.model(input_tensor)
            pred = torch.argmax(output, dim=1).item()  # 0: closed, 1: open
        return pred

class EyeCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )

        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 5 * 5, 128),  # 입력 이미지가 90x90일 때
            nn.ReLU(),
            nn.Linear(128, 2)
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x
