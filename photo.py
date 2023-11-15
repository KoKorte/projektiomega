from PIL import Image
from io import BytesIO
import base64

def processPhoto(response):
    # Turn response into base64 encoded string
    base64photo = str(base64.b64encode(response.content).decode("utf-8"))
    # Open base64 string as Image 
    image = Image.open(BytesIO(base64.b64decode(base64photo)))
    # Create new image that is half the size of original
    new_image = image.resize((640, 360))
    # Set up IO buffer
    buffer = BytesIO()
    # Save the created smaller image  as jpeg into buffer
    new_image.save(buffer, format="JPEG")
    # Create working base64 encoded jpeg
    b64string = "data:" + response.headers['Content-Type'] + ";base64, " + str(base64.b64encode(buffer.getvalue()).decode("utf-8"))
    # Return base64 photo
    return b64string
