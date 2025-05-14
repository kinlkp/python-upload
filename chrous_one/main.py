import math
import csv


"""
You will be supplied with two data files in CSV format .
The first file contains statistics about various dinosaurs. The second file contains additional data.
Given the following formula, speed = ((STRIDE_LENGTH / LEG_LENGTH) - 1) * SQRT(LEG_LENGTH * g)
Where g = 9.8 m/s^2 (gravitational constant)

Write a program to read in the data files from disk, it must then print the names of only the bipedal dinosaurs from fastest to slowest.
Do not print any other information.

$ cat dataset1.csv
NAME,LEG_LENGTH,DIET
Hadrosaurus,1.4,herbivore
Struthiomimus,0.72,omnivore
Velociraptor,1.8,carnivore
Triceratops,0.47,herbivore
Euoplocephalus,2.6,herbivore
Stegosaurus,1.50,herbivore
Tyrannosaurus Rex,6.5,carnivore
Hadrosaurus,1.6,herbivore

$ cat dataset2.csv
NAME,STRIDE_LENGTH,STANCE
Euoplocephalus,1.97,quadrupedal
Stegosaurus,1.70,quadrupedal
Tyrannosaurus Rex,4.76,bipedal
Hadrosaurus,1.3,bipedal
Deinonychus,1.11,bipedal
Struthiomimus,1.24,bipedal
Velociraptor,2.62,bipedal
"""

# speed = ((STRIDE_LENGTH / LEG_LENGTH) - 1) * SQRT(LEG_LENGTH * g)
res = []
with open("dataset2.csv", mode='r')  as f:
    csvFile = csv.reader(f)
    for x in csvFile:
        if x[2] == 'bipedal':
            with open("dataset1.csv", mode='r')  as f1:
                csvFile2 = csv.reader(f1)
                for y in csvFile2:
                    if x[0] in y:
                        speed = ((float(x[1])/float(y[1])) - 1) * math.sqrt(float(y[1]) * 9.8**2)
                        res.append([x[0], speed])

x=sorted(res, key=lambda x: x[1], reverse=True)
for i in x:
    print(i[0])
