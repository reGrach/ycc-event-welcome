from PIL import Image;
import torch
from facenet_pytorch import InceptionResnetV1, MTCNN
from types import MethodType
import cv2
import os
import time
from datetime import datetime
from config import Config


class recognize_service:
    all_people_faces = {}
    mtcnn = {}
    resnet = {}

    def __init__(self, cnf: Config) -> None:
        self.__threshold = float(cnf.THRESHOLD_REC)
        self.__photo_dir = cnf.PHOTO_DIR
        self.__photo_save_img = cnf.SAVE_IMG_FOLDER

    def __detect_box(self, self_mtcnn: MTCNN, img: Image, save_path=None):
        batch_box, batch_probs = self_mtcnn.detect(img) 
        face = self_mtcnn.extract(img, batch_box, save_path)
        return face
    
    ### load images
    def __loadDataset(self):
        self.__createFolderIfNotExists(self.__photo_dir)
        for filename in os.listdir(self.__photo_dir):
            person_face, extension = filename.split(".")
            img = cv2.imread(f'{self.__photo_dir}/{person_face}.{extension}')
            cropped = self.mtcnn(img)
            if cropped is not None:
                self.all_people_faces[person_face] = self.__encode(cropped)[0, :]
    
    def __encode(self, img):
        tensor_img = torch.Tensor(img)
        tensor_img = tensor_img.unsqueeze(0)
        res = self.resnet(tensor_img)
        return res
    
    def __savePhoto(self, img: Image, name: str):
        try:
            self.__createFolderIfNotExists(self.__photo_save_img)                
            img.save(self.__photo_save_img + '/' + name + '.jpg')
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)

    def __createFolderIfNotExists(self, name: str):
        if not os.path.isdir(name):
            try:
                os.mkdir(name)
                print(f"Directory '{name}' created successfully.")
            except PermissionError:
                print(f"Permission denied: Unable to create '{name}'.")
            except Exception as e:
                print(f"An error occurred: {e}")

    def __writeInfo(self, msg: str):
        with open('recognize_service.log', "a+") as file:
            file.write(msg + "\n")

    # Отвечает за инициализацию нейронки и загрузку имеющихся фотографий
    def start(self) -> None:
        self.resnet = InceptionResnetV1(pretrained='vggface2').eval()
        self.mtcnn = MTCNN(min_face_size=80)
        self.mtcnn.detect_box = MethodType(self.__detect_box, self.mtcnn)
        self.__loadDataset()

    # Принимает на вход изображение и возвращает строку с именем человека в случае успешного распознования
    def recognize(self, img: Image) -> str:
        session_id = str(time.time_ns())
        self.__savePhoto(img, session_id)

        cropped_img = self.mtcnn.detect_box(img)
        result_name = None
        if cropped_img is not None:
            img_embedding = self.__encode(cropped_img)
            detect_dict = {}
            for k, v in self.all_people_faces.items():
                detect_dict[k] = (v - img_embedding).norm().item()

            result_name = min(detect_dict, key=detect_dict.get)

            if detect_dict[result_name] >= self.__threshold:
                result_name = None
        if result_name is None:
            self.__writeInfo(str(datetime.now()) + '|FAIL|' + session_id)
        else:
            self.__writeInfo(str(datetime.now()) + '|SUCCESS|' + session_id + '|' + result_name)

        return result_name