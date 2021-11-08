import matplotlib.pyplot as plt

class Circle(object):
    # This is the constructor. It sets the basic properties of what a circle is.
    # "Init" sounds like something a bloke from Liverpool would say, but it's actually a way of telling Python you're
    # trying to initialise a new object.
    # "Self" refers to the instance of the object. When using the object, in its place you'd use the name of the object,
    # eg "red_circle.colour = 'red'".
    def __init__(self,radius=3,colour="blue"):
        self.radius = radius;
        self.colour = colour;
    # This method lets you increase the size of the circle. A method actually changes the properties of the object.
    def add_radius(self,r):
        self.radius = self.radius+r
        return(self.radius)
    # This one draws a picture of the circle using some Python wizadry called matplotlib.pyplot.
    # This too is a method.
    def drawCircle(self):
        plt.gca().add_patch(plt.Circle((0, 0), radius=self.radius, fc=self.colour))
        plt.axis('scaled')
        plt.show()

Red_Circle = Circle(10,"red")
Red_Circle.drawCircle()