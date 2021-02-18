import sys
import json
import math
import argparse
input_filename = sys.argv[1]

parser=argparse.ArgumentParser()
parser.add_argument("-m", action="store_true")
parser.add_argument("input_file")
parser.add_argument("output_file", nargs='?',default="stdout")
args = parser.parse_args()
args=parser.parse_args() 

with open(args.input_file) as json_file:
    dictionary = json.load(json_file)

def rotate(pivot, point, angle):
    radians_angle = angle * math.pi / 180
    s = math.sin(radians_angle)
    c = math.cos(radians_angle)
    r_point = [*point]
    r_point[0] -= pivot[0]
    r_point[1] -= pivot[1]
    x_new = r_point[0] * c - r_point[1] * s
    y_new = r_point[0] * s + r_point[1] * c
    r_point[0] = x_new + pivot[0]
    r_point[1] = y_new + pivot[1]
    return r_point

def makeTheString(dictionary):
    diction={}
    diction.update({0:[]})
    for h in list(dictionary["axiom"]):
        diction.setdefault(0,[]).append(h)
    i=1
    while i<=dictionary["order"]:
        diction.update({i:[]})
        lista=diction.get(i-1)
        for element in lista:
            if element=="F":
                for h in list(dictionary["rules"]["F"]):
                    diction.setdefault(i,[]).append(h)
            elif element=="G":
                for h in list(dictionary["rules"]["G"]):
                    diction.setdefault(i,[]).append(h)
            elif element=="+":
                diction.setdefault(i,[]).append("+")
            elif element=="-":
                diction.setdefault(i,[]).append("-")
            elif element=="[":
                diction.setdefault(i,[]).append("[")
            elif element=="]":
                diction.setdefault(i,[]).append("]")
            elif element=="X":
                for h in list(dictionary["rules"]["X"]):
                    diction.setdefault(i,[]).append(h)
            elif element=="Y":
                for h in list(dictionary["rules"]["Y"]):
                    diction.setdefault(i,[]).append(h)
            elif element=="W":
                for h in list(dictionary["rules"]["W"]):
                    diction.setdefault(i,[]).append(h)
            elif element=="Z":
                for h in list(dictionary["rules"]["Z"]):
                    diction.setdefault(i,[]).append(h)
        i=i+1
    return diction
  
          
diction=makeTheString(dictionary)
coordinates=[]
angle=dictionary["start_angle"]-dictionary["left_angle"]
lista=diction[dictionary["order"]]
x1=0
y1=0
i=0
brackets=[]
counter=0
firstTime="true"
for element in lista:
    if firstTime=="true":
        x2=round(dictionary["step_length"]*math.cos(math.radians(dictionary["start_angle"]))+x1,2)
        y2=round(dictionary["step_length"]*math.sin(math.radians(dictionary["start_angle"]))+y1,2)
        coordinates.append(((x1,y1),(x2,y2)))
        x1=x2
        y1=y2
        firstTime="false"
    else:
        if element=="F":
            if lista[i-1]!="+" and lista[i-1]!="-":
                x2=round(dictionary["step_length"]*math.cos(math.radians(dictionary["start_angle"]))+x1,2)
                y2=round(dictionary["step_length"]*math.sin(math.radians(dictionary["start_angle"]))+y1,2)
                coordinates.append(((x1,y1),(x2,y2)))
                x1=x2
                y1=y2
            else:
                x2=round(dictionary["step_length"]*math.cos(math.radians(dictionary["left_angle"]))+x1,2)
                y2=round(dictionary["step_length"]*math.sin(math.radians(dictionary["left_angle"]))+y1,2)
                pivot=(x1,y1)
                point=(x2,y2)
                newpoint=rotate(pivot,point,angle)
                x2=round(newpoint[0],2)
                y2=round(newpoint[1],2)
                coordinates.append(((x1,y1),(x2,y2)))
                x1=x2
                y1=y2
        elif element=="G":
            x2=round(dictionary["step_length"]*math.cos(math.radians(dictionary["left_angle"]))+x1,2)
            y2=round(dictionary["step_length"]*math.sin(math.radians(dictionary["left_angle"]))+y1,2)
            pivot=(x1,y1)
            point=(x2,y2)
            newpoint=rotate(pivot,point,angle)
            x2=round(newpoint[0],2)
            y2=round(newpoint[1],2)
            coordinates.append(((x1,y1),(x2,y2)))
            x1=x2
            y1=y2
        elif element=="[":
            storedx=x2
            storedy=y2
            brackets.append((storedx,storedy))
            counter=counter+1
        elif element=="]":
            x1=brackets[counter-1][0]
            y1=brackets[counter-1][1]
            brackets.pop(counter-1)
            counter=counter-1
        elif element=="+":
            angle=angle+dictionary["left_angle"]
        elif element=="-":
            angle=angle-dictionary["right_angle"]
        if angle>360:
            angle=angle-360
        elif angle<0:
            angle=360-abs(angle)
        else:
            angle=angle
    i=i+1
str1=''.join(diction[dictionary["order"]])

with open(args.output_file, 'w') as output_file:
    h=0
    while h<len(coordinates):
        output_file.write("(%.2f, %.2f) (%.2f, %.2f)\n" % (coordinates[h][0][0],coordinates[h][0][1], coordinates[h][1][0], coordinates[h][1][1]))
        h=h+1

if args.m:
    print(str1)




            
    



