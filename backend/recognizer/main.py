import torch #импорт пакета торч, который отвечает за
from facenet_pytorch import InceptionResnetV1, MTCNN
from types import MethodType
import cv2
import os

### get encoded features for all saved images
saved_pictures = "./known_img/" 
all_people_faces = {}
mtcnn= {}

### encoding image
def encode(img):
    res = resnet(torch.Tensor(img))
    return res

def detect_box(self, img, save_path=None):
    # Detect faces
    batch_boxes, batch_probs, batch_points = self.detect(img, landmarks=True)
    # Select faces
    if not self.keep_all:
        batch_boxes, batch_probs, batch_points = self.select_boxes(
            batch_boxes, batch_probs, batch_points, img, method=self.selection_method
        )
    # Extract faces
    faces = self.extract(img, batch_boxes, save_path)
    return batch_boxes, faces

### load images
def loadDataset():
    for filename in os.listdir(saved_pictures):
        person_face, extension = filename.split(".")
        img = cv2.imread(f'{saved_pictures}/{person_face}.{extension}')
        cropped = mtcnn(img)
        if cropped is not None:
            all_people_faces[person_face] = encode(cropped)[0, :]

def main():
    cam=0
    thres=0.7
    vdo = cv2.VideoCapture(cam)
    while vdo.grab():
        _, img0 = vdo.retrieve()
        batch_boxes, cropped_images = mtcnn.detect_box(img0)

        if cropped_images is not None:
            # начало цикла, который проходится по двум массивам одновременно:
            # batch_boxes -
            # cropped_images - 
            for box, cropped in zip(batch_boxes, cropped_images):
                x, y, x2, y2 = [int(x) for x in box]
                img_embedding = encode(cropped.unsqueeze(0))
                detect_dict = {}
                for k, v in all_people_faces.items():
                    detect_dict[k] = (v - img_embedding).norm().item()

                min_key = min(detect_dict, key=detect_dict.get)

                if detect_dict[min_key] >= thres:
                    min_key = 'Undetected'
                
                cv2.rectangle(img0, (x, y), (x2, y2), (0, 0, 255), 2)
                cv2.putText(
                  img0, min_key, (x + 5, y + 10), 
                   cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
                
        ### display
        cv2.imshow("output", img0)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__": # это условие нужно
    ### load model
    resnet = InceptionResnetV1(pretrained='vggface2').eval()
    mtcnn = MTCNN(image_size=224, keep_all=True, thresholds=[0.4, 0.5, 0.5], min_face_size=60)
    mtcnn.detect_box = MethodType(detect_box, mtcnn)
    print ("start")
    loadDataset() # вызов метода loadDataset
    main()  # вызов метода loadDataset
    print ("finish")