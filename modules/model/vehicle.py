import re

class Vehicle(dict):
    def __init__(self, vin, package, images):
        super().__init__()
        self.vin = vin
        self.package = package[:9]
        self.vehicle_package = package
        self.images = images
        self._update(images)
    
    def _update(self, images):
        '''
        image: D:\Image\20210723\358\LSGUL8AL3MA247727\4UM167G27OS1\p_9.jpg
        '''
        for image in images:
            position = int(re.findall(r'_(.+?).jpg', image)[0])
            self.__setitem__(position, image)

    def __len__(self):
        return len(self.images)

if __name__ == '__main__':
    
    image = r'D:\Image\20210723\358\LSGUL8AL3MA247727\4UM167G27OS1\p_9.jpg'

    position = re.findall(r'_(.+?).jpg', image)[0]
    print(position)

    package = '4UM167G27OS1'
    print(package[:9])
