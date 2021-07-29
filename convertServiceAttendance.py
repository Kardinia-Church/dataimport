# Converts the output from Elvanto's service attendance to the correct format to be imported to Fluro

import csv
import os
import string
import random
import datetime

errorsAt = []
outputRow = ["Event_ID", "Meeting", "Attendance_Date", "ElvantoMemberID", "Full_Name", "First_Name", "Last_Name", "Date_of_Birth", "Gender"]

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
                    firstEventColIndex = 0
                    for row in reader:
                        if(rowNumber == 0):
                            inputRow = row

                            # We need to store our events here
                            colPosition = 0
                            for col in row:
                                colSplit = col.split(" ")
                                timePeriod = colSplit[len(colSplit) - 1]

                                # If the last split is AM or PM we know that this is an event
                                if (timePeriod == "AM" or timePeriod == "PM"):

                                    # Date needs to be in the format YYYY-MM-DD HH:MM
                                    dateSplit = colSplit[len(colSplit) - 3].split("/")
                                    time = datetime.datetime.strptime(colSplit[len(colSplit) - 2] + " " + timePeriod, '%I:%M %p')
                                    date = dateSplit[2] + "-" + dateSplit[1] + "-" + dateSplit[0] + " " + str(time.hour).zfill(2) + ":" + str(time.minute).zfill(2)
                                    eventName = col.split(" " + dateSplit[0] + "/" + dateSplit[1] + "/" + dateSplit[2] + " " + colSplit[len(colSplit) - 2] + " " + timePeriod)[0]

                                    randId = ''.join(random.choices(string.digits + string.digits, k = 6)) + "-" + ''.join(random.choices(string.digits + string.digits, k = 6))
                                    readEvents.append(eventName + " " + date)
                                    if(firstEventColIndex == 0):
                                        firstEventColIndex = colPosition
                                    try:
                                        events[eventName + " " + date]
                                    except:
                                        print("New service = " + eventName + " " + date)
                                        events[eventName + " " + date] = {
                                            "date": date,
                                            "randomId": randId,
                                            "name": eventName
                                        };
                                        with open('./files/services.csv','a', newline="") as fd:
                                            servicesRow = [randId, eventName, date]
                                            serviceWriter.writerow(servicesRow)
                                        pass
                                colPosition += 1
                        else:
                            # Lets write our data!!
                            tempRow = [""] * len(outputRow)
                            colPosition = 0
                            for col in row:
                                if colPosition >= firstEventColIndex:
                                    copyRow(tempRow, row, outputRow, inputRow, "ElvantoMemberID", "Member ID")
                                    copyRow(tempRow, row, outputRow, inputRow, "First_Name", "First Name")
                                    copyRow(tempRow, row, outputRow, inputRow, "Last_Name", "Last Name")
                                    copyRow(tempRow, row, outputRow, inputRow, "Full_Name", "Full Name")
                                    copyRow(tempRow, row, outputRow, inputRow, "Date_of_Birth", "Date of Birth")
                                    copyRow(tempRow, row, outputRow, inputRow, "Gender", "Gender")
                                    
                                    #If the person has this event ticked with a Y then add the row
                                    if col == "Y":
                                        tempRow[outputRow.index("Event_ID")] = events[readEvents[colPosition - firstEventColIndex]]["randomId"]
                                        tempRow[outputRow.index("Meeting")] = events[readEvents[colPosition - firstEventColIndex]]["name"]
                                        tempRow[outputRow.index("Attendance_Date")] = events[readEvents[colPosition - firstEventColIndex]]["date"]
                                        writer.writerow(tempRow)
                                colPosition += 1
                        rowNumber += 1

# Print the error lines if there were any
print("Done!")
if(len(errorsAt) > 0):
    print("Errors were found at lines: ")
    for line in errorsAt:
        print(str(line + 1))