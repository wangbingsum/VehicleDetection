import re

def test_split():
    image_path = r'D:\Image\20210723\358\LSGUL8AL3MA247727\4UM167G27OS1\p_9.jpg'

    position = re.findall(r'_(.+?).jpg', image_path)[0]
    assert position == "9"
    
    position = image_path.split(".")[0].split("_")[-1]
    assert position == "9"

    package = '4UM167G27OS1'
    assert package[:9] == "4UM167G27"

    date = re.findall(r'[0-9]{8}', image_path)[0]
    assert date == "20210723"