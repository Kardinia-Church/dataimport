import csv
import os
import string
import random

print("WARNING THERE MAY BE A BUG WHERE SERVICE IDS ARE NOT IMPORTED CORRECTLY! EXITING! (Bug should not exist in this but will need to test!)")
exit()


errorsAt = []
outputRow = ["ElvantoEventID", "Date", "Title", "Total", "People In Group"]

def copyRow(resultRow, readRow, outputKeys, inputKeys, outputSearch, inputSearch):
    try:
        resultRow[outputKeys.index(outputSearch)] = readRow[inputKeys.index(inputSearch)]
    except:
        print("Warning: Failed to read key " + outputSearch)

input("To begin the conversion please rename the file to toConvert.csv in the files directory\n Press enter to begin");
if(not os.path.isfile("./files/toConvert.csv")):
    print("Error: Could not find the file!")
else:
    # If the services file does not exist create it
    if(not os.path.isfile("./files/services.csv")):
        print("Service file did not exist, created it")
        with open("./files/services.csv", "a", newline="") as serviceOutput:
            csv.writer(serviceOutput).writerow(["id", "name", "date"])

    # If the converted file does not exist create it
    if(not os.path.isfile("./files/converted.csv")):
        print("Conversion file did not exist, created it")
        with open("./files/converted.csv", "a", newline="") as serviceOutput:
            csv.writer(serviceOutput).writerow(outputRow)

    with open("./files/toConvert.csv", "r") as file:
        with open("./files/converted.csv", "a", newline="") as output:
            with open("./files/services.csv", "r") as serviceFile:
                with open("./files/services.csv", "a", newline="") as serviceOutput:
                    reader = csv.reader(file)
                    writer = csv.writer(output)
                    inputRow = []
                    events = {}
                    readEvents = []

                    # First read in our stored events from the csv file
                    serviceReader = csv.reader(serviceFile)
                    serviceWriter = csv.writer(serviceOutput)
                    for row in serviceReader:
                        events[row[1] + " " + row[2]] = {
                            "date": row[2],
                            "randomId": row[0],
                            "name": row[1]
                        }

                    rowNumber = 0
                    for row in reader:
                        if(rowNumber == 0):
                            inputRow = row
                            pass
                        else:
                            # Lets write our data!!
                            tempRow = [""] * len(outputRow)

                            # Validate the row
                            if row[0] == "" or row[1] == "" or row[2] == "" or row[3] == ""or row[4] == "":
                                pass
                            else:
                                # Check if our event exists, if not add it
                                try:
                                    events[row[0] + " " + row[1] + " 00:00"]
                                except:
                                    print("New service = " + row[0] + " " + row[1] + " 00:00")
                                    randId = ''.join(random.choices(string.digits + string.digits, k = 6)) + "-" + ''.join(random.choices(string.digits + string.digits, k = 6))
                                    events[row[0] + " " + row[1] + " 00:00"] = {
                                        "date": row[1] + " 00:00",
                                        "randomId": randId,
                                        "name": row[0]
                                    };
                                    with open('./files/services.csv','a', newline="") as fd:
                                        servicesRow = [randId, row[0], row[1] + " 00:00"]
                                        serviceWriter.writerow(servicesRow)
                                    pass
                                
                                # Add our row
                                copyRow(tempRow, row, outputRow, inputRow, "Total", "Members Attended")
                                copyRow(tempRow, row, outputRow, inputRow, "People In Group", "People In Group")
                                
                                tempRow[outputRow.index("ElvantoEventID")] = events[row[0] + " " + row[1] + " 00:00"]["randomId"]
                                tempRow[outputRow.index("Date")] = events[row[0] + " " + row[1] + " 00:00"]["date"]
                                tempRow[outputRow.index("Title")] = events[row[0] + " " + row[1] + " 00:00"]["name"]
                                writer.writerow(tempRow)
                        rowNumber += 1

# Print the error lines if there were any
print("Done!")
if(len(errorsAt) > 0):
    print("Errors were found at lines: ")
    for line in errorsAt:
        print(str(line + 1))