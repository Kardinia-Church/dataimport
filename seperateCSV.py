# Separate a CSV into individual files
import os
import csv

input("To begin the conversion please rename the file to converted.csv in the files directory\n Press enter to begin");
if(not os.path.isfile("./files/converted.csv")):
    print("Error: Could not find the file!")
else:
    with open("./files/converted.csv", "r") as file:
        reader = csv.reader(file)
        rows = list(reader)
        fileNumber = 0
        rowNumber = 1
        header = rows[0]

        while True:
            with open("./files/converted_" + str(fileNumber) + ".csv", "w", newline="") as output:
                writer = csv.writer(output)
                writer.writerow(header)
                for i in range(rowNumber, rowNumber + 30):
                    if(i >= len(rows)):
                        print("Done " + str(i) + " rows read and saved " + str(fileNumber) + " files")
                        exit()
                    print(str(i))
                    writer.writerow(rows[i])
                    rowNumber = i;
                fileNumber += 1
                rowNumber += 1