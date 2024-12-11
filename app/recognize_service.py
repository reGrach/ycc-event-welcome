from PIL import Image;
import torch
from facenet_pytorch import InceptionResnetV1, MTCNN
from types import MethodType
import cv2
import os
from config import Config


class recognize_service:
    all_people_faces = {}
    mtcnn = {}
    resnet = {}

    def __init__(self, cnf: Config) -> None:
        self.__threshold = float(cnf.THRESHOLD_REC)
        self.__photo_dir = cnf.PHOTO_DIR

    def __detect_box(self, self_mtcnn: MTCNN, img: Image, save_path=None):
        batch_boxes, batch_probs, batch_points = self_mtcnn.detect(img, landmarks=True) 
        if not self_mtcnn.keep_all:
            batch_boxes, batch_probs, batch_points = self_mtcnn.select_boxes(
                    batch_boxes,
                    batch_probs,
                    batch_points,
                    img,
                    method=self_mtcnn.selection_method)

        faces = self_mtcnn.extract(img, batch_boxes, save_path)
        return batch_boxes, faces
    
    ### load images
    def __loadDataset(self):
        for filename in os.listdir(self.__photo_dir):
            person_face, extension = filename.split(".")
            img = cv2.imread(f'{self.__photo_dir}/{person_face}.{extension}')
            cropped = self.mtcnn(img)
            if cropped is not None:
                self.all_people_faces[person_face] = self.__encode(cropped)[0, :]
    
    def __encode(self, img):
        res = self.resnet(torch.Tensor(img))
        return res

    # Отвечает за инициализацию нейронки и загрузку имеющихся фотографий
    def start(self) -> None:
        self.resnet = InceptionResnetV1(pretrained='vggface2').eval()
        self.mtcnn = MTCNN(image_size=224, keep_all=True, thresholds=[0.4, 0.5, 0.5], min_face_size=60)
        self.mtcnn.detect_box = MethodType(self.__detect_box, self.mtcnn)
        self.__loadDataset()

    # Принимает на вход изображение и возвращает строку с именем человека в случае успешного распознования
    def recognize(self, img: Image) -> str:
        batch_boxes, cropped_images = self.mtcnn.detect_box(img)
        result_name = None
        if cropped_images is not None:
            for box, cropped in zip(batch_boxes, cropped_images):
                x, y, x2, y2 = [int(x) for x in box]
                img_embedding = self.__encode(cropped.unsqueeze(0))
                detect_dict = {}
                for k, v in self.all_people_faces.items():
                    detect_dict[k] = (v - img_embedding).norm().item()

                result_name = min(detect_dict, key=detect_dict.get)

                if detect_dict[result_name] >= self.__threshold:
                    result_name = None
                
        return result_name