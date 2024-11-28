from recognize_service import recognize_service as rs


if __name__ == '__main__':
    test = rs()
    test.start()
    print(test.recognize(None))
