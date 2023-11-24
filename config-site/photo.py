from PIL import Image, ImageDraw
from io import BytesIO
import math
import base64

# Resize the traffic camera photo as it is a bit too big
def processPhoto(response):
    # Turn response into base64 encoded string
    base64photo = str(base64.b64encode(response.content).decode("utf-8"))
    # Open base64 string as Image 
    image = Image.open(BytesIO(base64.b64decode(base64photo)))
    # Create new image that is 3/8 of the original size 
    # new_image = image.resize((640, 360)) # half size
    new_image = image.resize((480, 270)) # 3/8 size
    # Set up IO buffer
    buffer = BytesIO()
    # Save the created smaller image  as jpeg into buffer
    new_image.save(buffer, format="JPEG")
    # Create working base64 encoded jpeg
    b64string = "data:" + response.headers['Content-Type'] + ";base64, " + str(base64.b64encode(buffer.getvalue()).decode("utf-8"))
    # Return base64 photo
    return b64string

# Calculate the coordinate point of line when origo, angle and length is known
def coordinate(a, l):    
    # Set origo when picture size is 480x270
    origo_x = 240
    origo_y = 135
    # Set the length    
    length = l
    # Turn the angle so the arrow points in the right direction
    # Wind directional degree is always pointing from where the wind is blowing
    # So 0 degree wind blows from north towards south, so the arrow needs to 
    # point towards south
    angle = 180 - a  
    # Initialize the math functions with corrected angle
    radians = math.radians(angle) 
    cosine = math.cos(radians)
    sine = math.sin(radians)
    # Calculate coordinates x and y point
    endpoint_x = origo_x + length * sine
    endpoint_y = origo_y + length * cosine
    # Create coordinate as tuple and return it
    value = (endpoint_x, endpoint_y)    
    return value

# Draw the comically sketched arrow over compass image
def drawArrow(a):
    # Load the background image, courtesy of AI artist
    # Might some day draw the compass base with these tools to replace this   
    image = Image.open("static/images/template.jpg")  # (size: 480 x 270) 
    # get the starting angle
    angle = a
    # Set the length of first point
    length = 75
    # Initialize list variable points, that will hold coordinate tuples
    points = []
    # Get starting point for the first line
    points.append(coordinate(angle,length))
    # Turn angle 180 degrees and keep the length same so the arrow will go nicely
    # over origo
    angle += 180
    # Get ending point for the first line, keep the ending point as it really is
    # true ending point
    endpoint = coordinate(angle,length)
    points.append(endpoint)
    # Turn angle 25 degrees and change the length in order to start drawing the 
    # arrow head
    angle += 25
    length = 25    
    points.append(coordinate(angle,length))
    # Turn angle by -60 degrees and adjust length to get a bit skewed angle for 
    # the arrow head
    angle -= 60
    length = 20
    points.append(coordinate(angle,length))
    # Now return to true endpoint
    points.append(endpoint)
    
    # Initialize the drawing canvas
    draw = ImageDraw.Draw(image)
    # Draw green thick lines by connecting the coordinates to act as background of arrow
    draw.line(points, width= 15, fill="green", joint="curve")
    # Use the same points to draw thinner black lines to act as foreground of arrow
    draw.line(points, width= 5, fill="black", joint="curve")
    # Save the created image
    image.save("static/images/compass.jpg")
    
    


