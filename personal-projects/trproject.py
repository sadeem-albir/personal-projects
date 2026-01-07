import turtle as tr
import math
import threading

mypen = tr.Turtle()

mypen.speed(0)

# This whole building class is where the majority of the code goes
class Building:

#   initializers to create the seed of all the sprouting values,
#   they control the root of the important data and make this process doable
    def __init__(self, x, y, width, layer_height, rows, color1, color2, window_color):
        self.x = x
        self.y = y
        self.width = width
        self.layer_height = layer_height
        self.rows = rows
        self.color1 = color1
        self.color2 = color2
        self.tilt = 22.5
        self.perceived_length = self.width * (2 / 4)
        self.box_width = self.width / 12
        self.window_color = window_color
        self.elements = []
        self.color_thread = []
        self.move_thread = []
        self.delay_time = 50


#   The layers or starting rows of the buildings that haven't been yet filled
    def draw_layers(self):
        mypen.up()
        mypen.setheading(0)
        mypen.goto(self.x, self.y)
        mypen.down()

        for i in range(self.rows):
            for j in range(2):
                mypen.forward(self.width)
                mypen.left(90)
                mypen.forward(self.layer_height)
                mypen.left(90)
            mypen.left(90)
            mypen.forward(self.layer_height)
            mypen.right(90)

#   whatever function in this file has the prefix 'side' to it, is just the same drawing but on the other side of the 3D
    def draw_side_layers(self):
        mypen.up()
        mypen.goto(self.x + self.width, self.y)
        mypen.down()
        mypen.setheading(self.tilt)

        for i in range(self.rows):
            for j in range(2):
                mypen.forward(self.perceived_length)
                mypen.left(90 - self.tilt)
                mypen.forward(self.layer_height)
                mypen.left(90 + self.tilt)
            mypen.left(90 - self.tilt)
            mypen.forward(self.layer_height)
            mypen.right(90 - self.tilt)

#   unless you're comfortable looking at a sky from your bed :)
    def draw_roof(self):
        mypen.up()
        mypen.goto(self.x, self.y + (self.layer_height * 10))
        mypen.setheading(0)

        mypen.down()
        mypen.fillcolor(self.color1)
        mypen.begin_fill()

        for i in range(2):
            mypen.forward(self.width)
            mypen.left(self.tilt)
            mypen.forward(self.perceived_length)
            mypen.left(180 - self.tilt)
        mypen.end_fill()

#   this is to paint the building with the two color arguments in the initializer before the last self.window argument
    def fill_layers(self):
        x = 0
        mypen.fillcolor(self.color2)
        for i in range(2):
            mypen.up()
            mypen.goto(self.x + x, self.y)
            mypen.setheading(0)

            mypen.down()
            mypen.begin_fill()
            for j in range(2):
                mypen.forward(self.width / 6)
                mypen.left(90)
                mypen.forward(self.layer_height * 10)
                mypen.left(90)
            mypen.end_fill()
            x += (self.width * (5 / 6))

    def fill_center(self):
        mypen.up()
        mypen.fillcolor(self.color1)
        mypen.goto(self.x + (self.width / 6), self.y)
        mypen.setheading(0)
        mypen.down()

        mypen.begin_fill()
        for i in range(2):
            mypen.forward((self.width / 6) * 4)
            mypen.left(90)
            mypen.forward(self.layer_height * self.rows)
            mypen.left(90)
        mypen.end_fill()

    def fill_side_layers(self):
        offset = (self.perceived_length / 6) * 2
        mypen.fillcolor(self.color2)
        for i in range(2):
            mypen.up()
            mypen.goto(self.x + self.width, self.y)
            mypen.setheading(self.tilt)
            mypen.forward(offset)

            mypen.down()
            mypen.begin_fill()
            for j in range(2):
                mypen.forward(self.perceived_length / 6)
                mypen.left(90 - self.tilt)
                mypen.forward(self.layer_height * 10)
                mypen.left(90 + self.tilt)
            mypen.end_fill()
            offset += ((self.perceived_length / 6) * 2)

    def fill_side_center(self):
        mypen.up()
        mypen.fillcolor(self.color1)
        delta_offset = [3, 2]
        fill_width = [2, 1]
        offset, n = 0, 0

        for i in range(3):
            mypen.goto(self.x + self.width, self.y)
            mypen.setheading(self.tilt)
            mypen.forward(offset)

            mypen.down()
            mypen.begin_fill()
            for j in range(2):
                mypen.forward((self.perceived_length / 6) * fill_width[n])
                mypen.left(90 - self.tilt)
                mypen.forward(self.layer_height * self.rows)
                mypen.left(90 + self.tilt)
            mypen.end_fill()
            offset += ((delta_offset[n]) * self.perceived_length / 6)
            if n < 1:
                n += 1

#   this chunk of code is extremely important for the patterns, as I am primarily using an array
#   of turtle objects to be able to implement the animation more efficiently
    def create_window_array(self):
        real_size = self.box_width / 2
        x_offset = 0
        y_offset = 0
        tr.register_shape("window", ((-real_size, -real_size), (real_size, -real_size), (real_size, real_size), (-real_size, real_size)))
        for i in range(self.rows * 2):
            self.elements.append(tr.Turtle())
            self.elements[i].shape("window")
            self.elements[i].color(self.window_color)
            self.elements[i].up()
            first_pane_x = self.elements[0].xcor()
            first_pane_y = self.elements[0].ycor()
            self.elements[i].goto(first_pane_x + x_offset, first_pane_y - y_offset)
            x_offset += self.box_width * 2
            if (i + 1) % 4 == 0:
                y_offset += self.box_width * 2
                x_offset = 0

#   extra features, press 1 to show glass panes (for some reason I decided to prefer using the term pane instead of window)
    def show_panes(self):
        for i in range(2 * self.rows - 1, -1, -1):
            self.elements[i].showturtle()
#   press 0 to hide glass panes
    def hide_panes(self):
        for i in range(2 * self.rows):
            self.elements[i].hideturtle()

#   the cool, but not coolest pattern
    def pattern_1(self, c1, c2):
        delta_color = 0

        for i in range(10):
            for j in range(delta_color, self.rows * 2 + delta_color):
                if j % 2 == 0:
                    self.elements[j - delta_color].color(c1)
                else:
                    self.elements[j - delta_color].color(c2)
            delta_color += 1

        for i in range(2 * self.rows):
            self.elements[i].color(self.window_color)

#   the one cooler than pattern 1
    def pattern_2(self, c1, c2):
        offset = 5
        for i in range(5):
            for j in range(self.rows * 2 + offset):
                limit = False
                offset = 5
                tr.delay(self.delay_time)

                if j == 0 and self.elements[-1].color()[0] == c1 and self.elements[-2].color()[0] == c2:
                    self.elements[-1].color(c2)
                if j < self.rows / 2:
                    self.elements[j].color(c1)
                else:
                    if j < self.rows * 2:
                        self.elements[j].color(c1)
                    if offset > 0 and not limit:
                        self.elements[j - int(self.rows / 2)].color(c2)
                        offset -= 1
                    else:
                        limit = True
                        self.elements[offset].color(self.window_color)
                        offset += 1

        for i in range(self.rows * 2):
            self.elements[i].color(self.window_color)

#   this is primarily where I place the turtle objects mentioned previously into each window fit
    def draw_windows(self):
        self.create_window_array()
        x = (self.width / 6) * 2
        y = 0
        elem_index = 0
        elem_x_cor = []
        elem_y_cor = []
        window_align = self.width / 36
        # mypen.fillcolor(self.window_color)
        for i in range(2):

            for j in range(self.rows):
                mypen.up()
                mypen.goto(self.x + x, self.y + y)
                mypen.setheading(0)

                mypen.left(45)
                mypen.forward(window_align)
                mypen.right(45)
                mypen.down()

                # self.elements[elem_index].goto(mypen.xcor() + self.box_width / 2, mypen.ycor() + self.box_width / 2)
                # mypen.begin_fill()
                elem_x_cor.append(mypen.xcor() + self.box_width / 2)
                elem_y_cor.append(mypen.ycor() + self.box_width / 2)
                for k in range(4):
                    mypen.forward(self.box_width)
                    mypen.left(90)
                # mypen.end_fill()
                if (i == 0):
                    y += self.layer_height
                else:
                    y -= self.layer_height

            x += (self.width / 6)
            y -= self.layer_height

        for i in range(2 * self.rows):
            self.elements[i].goto(elem_x_cor[i], elem_y_cor[i])

#   the windows on the other side of the 3D
    def draw_side_windows(self):
        offset = (self.perceived_length / 6) * 2
        y = 0
        mypen.fillcolor("cyan")

        for i in range(2):

            for j in range(self.rows):
                mypen.up()
                mypen.goto(self.x + self.width, self.y + y)
                mypen.setheading(self.tilt)
                mypen.forward(offset)

                mypen.left(45 - self.tilt)
                mypen.forward((self.perceived_length / 6) / 6)
                mypen.right(45 - self.tilt)
                mypen.down()

                mypen.begin_fill()
                for k in range(2):
                    mypen.forward((self.perceived_length / 6) / 2)
                    mypen.left(90 - self.tilt)
                    mypen.forward((self.width / 6) / 2)
                    mypen.left(90 + self.tilt)
                mypen.end_fill()
                y += self.layer_height
            offset += (self.perceived_length / 6) * 2
            y = 0

    def draw_side_balconies(self):
        mypen.fillcolor(self.color1)

        layer_offset = 0
#       the balcony 'arm' is just the two sides of the balcony, it creates a 3D effect but needs to go into deeper detail and focus
        def draw_balcony_arm():
            mypen.setheading(-self.tilt)
            mypen.begin_fill()
            for i in range(2):
                mypen.forward(self.perceived_length / 12)
                mypen.left(90 + self.tilt)
                mypen.forward(self.layer_height / 2)
                mypen.left(90 - self.tilt)
            mypen.end_fill()

        def draw_balcony_window():
            mypen.up()
            mypen.goto(self.x + self.width, self.y + layer_offset + (self.layer_height / 2))
            mypen.setheading(self.tilt)
            mypen.down()
            mypen.fillcolor("cyan")

            mypen.begin_fill()
            for i in range(2):
                mypen.forward(self.perceived_length * (2 / 6))
                mypen.left(90 - self.tilt)
                mypen.forward(self.layer_height / 2)
                mypen.left(90 + self.tilt)
            mypen.end_fill()
            mypen.fillcolor(self.color1)

#       the outmost part of the balcony
        def draw_balcony_center():
            mypen.up()
            mypen.goto(self.x + self.width, self.y + layer_offset)
            mypen.setheading(-self.tilt)
            mypen.forward(self.perceived_length / 12)
            mypen.left(self.tilt * 2)
            mypen.down()

            mypen.begin_fill()
            for i in range(2):
                mypen.forward(self.perceived_length * (2 / 6))
                mypen.left(90 - self.tilt)
                mypen.forward(self.layer_height / 2)
                mypen.left(90 + self.tilt)
            mypen.end_fill()


        for i in range(1):
            for j in range(self.rows):
                mypen.up()
                mypen.goto(self.x + self.width, self.y + layer_offset)

                mypen.down()
                draw_balcony_arm()
                mypen.up()

                mypen.setheading(self.tilt)
                mypen.forward(self.perceived_length * (2 / 6))

                mypen.down()
                draw_balcony_arm()

                draw_balcony_window()
                draw_balcony_center()
                layer_offset += self.layer_height
                
#   now, we compile all the previous draw functions into this seed function
    def draw(self):
        self.draw_layers()
        self.draw_side_layers()
        self.draw_roof()
        self.fill_layers()
        self.fill_center()
        self.fill_side_layers()
        self.fill_side_center()
        self.draw_windows()
        self.draw_side_windows()
        self.draw_side_balconies()

# background image
def draw_background():
    mypen.up()
    mypen.goto(tr.window_width() * -1, tr.window_height() * (1 / 4))
    mypen.fillcolor("chartreuse4")
    mypen.setheading(0)
    mypen.down()

    mypen.begin_fill()
    for i in range(2):
        mypen.forward(tr.window_width() * 2)
        mypen.right(90)
        mypen.forward(tr.window_height())
        mypen.right(90)
    mypen.end_fill()

    mypen.up()
    mypen.fillcolor("blue4")

    mypen.goto(tr.window_width() * -1, tr.window_height() / 4)
    mypen.setheading(0)
    mypen.down()

    mypen.begin_fill()
    for i in range(2):
        mypen.forward(tr.window_width() * 2)
        mypen.left(90)
        mypen.forward(tr.window_height() / 2)
        mypen.left(90)
    mypen.end_fill()

# this displays a kind and supportive message after you press 'q' for quitting
def write_rainbow_text(text, position, color):
    mypen.up()
    mypen.goto(position[0], position[1])
    mypen.setheading(0)
    mypen.down()

    n = 0

    for i in text:
        if (not i.isalpha()) and ( i != '!'):
            mypen.color("white")
        else:
            mypen.color(color[n])
        mypen.write(i, font=('Arial', 30, 'normal'))
        mypen.up()
        if i == 'i':
            mypen.forward(12)
        else:
            mypen.forward(33)
        mypen.down()
        if n < len(color) - 1:
            n += 1
        else:
            n = 0

    mypen.color("black")

# this is where all the main implementation goes, and thanks to the building class above,
# all the complicated details can be undercover and you can use the building with ease
# by simply instantiating a class and adding the right arguments to the initializer's parameters
def main():
    root = tr.Screen()
    root.setup(width=1000, height=800)
    root.bgcolor("black")

    color_palette = ["red", "SpringGreen", "firebrick1", "yellow", "cyan", "DarkOrchid", "DeepPink1", "goldenrod1", "magenta"]
    building_x, building_y = -300, 0
    building_width = 250
    building_layer_height = 30
    building_rows = 10
    building_color1, building_color2 = (220, 220, 220), (83, 104, 120)

    tr.colormode(255)
    my_building = Building(building_x, building_y, building_width, building_layer_height, building_rows, building_color1, building_color2, "cyan")


    draw_background()
    my_building.draw()

#   command-line part of the program (input/output)
    print("q --> quit\n0 --> hide panes\n1 --> show panes\np1 --> pattern1\np2 --> pattern2")
    print("For pattern 2, cyan as color 1 and white or yellow as color 2 are highly recommended\n")
    while (c := input()):
        if c == '0':
            print("hiding panes...")
            my_building.hide_panes()
        elif c == '1':
            print("showing panes...")
            my_building.show_panes()
        elif c == 'p1':
            color1 = input("Enter color 1: ")
            color2 = input("Enter color2: ")
            my_building.pattern_1(color1, color2)
            print("showing pattern 1...\n")
        elif c == 'p2':
            color1 = input("Enter color 1: ")
            color2 = input("Enter color2: ")
            my_building.pattern_2(color1, color2)
            print("showing pattern 1...\n")
        elif c.lower() == 'q':
            write_rainbow_text("Happy Coding! :)", [building_x + (building_width * 1.6), building_y + (building_layer_height * building_rows) + 35], color_palette)
            break

    tr.bye()


if __name__ == '__main__':
    main()
