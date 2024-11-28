class recognize_service:    

    def __init__(self) -> None:
        self.name = 'тест'
        pass

    def start(self) -> None:
        print('recognize_service was started')
        
    def recognize(self, img) -> str:
        print('getting image')
        return self.name