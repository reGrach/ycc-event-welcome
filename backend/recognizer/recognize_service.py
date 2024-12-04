class recognize_service:    

    def __init__(self) -> None:
        self.name = 'тест'
        pass

    # Отвечает за инициализацию нейронки и загрузку имеющихся фотографий
    def start(self) -> None:
        print('recognize_service was started')
        
    
    # Принимает на вход изображение и возвращает строку с именем человека в случае успешного распознования
    def recognize(self, img) -> str:
        print('getting image')
        return self.name