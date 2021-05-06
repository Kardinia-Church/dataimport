# Convert the exported elvanto notes into the correct format for import
# Please save the elvanto output to .csv MS-DOS named toConvert.csv in the files directory

import csv
import os
import time
import datetime

# The map for definitions
definitions = {
    "Administrative Note (visible to all Leaders and Administrators)": "note",
    "Highly Confidential (visible to Pastoral staff only)": "highlyconfidentialnote",
    "Pastoral Notes (visible to Connect Group leaders & Pastoral staff)": "pastoralNote",
    "": "note"
}

errorsAt = []

def copyRow(resultRow, readRow, outputKeys, inputKeys, outputSearch, inputSearch):
    try:
        resultRow[outputKeys.index(outputSearch)] = readRow[inputKeys.index(inputSearch)]
    except:
        print("Warning: Failed to read key " + outputSearch)

input("To begin the conversion please rename the file to toConvert.csv in the files directory\n Press enter to begin");
if(not os.path.isfile("./files/toConvert.csv")):
    print("Error: Could not find the file!")
else:
    with open("./files/toConvert.csv", "r") as file:
        with open("./files/converted.csv", "w", newline="") as output:
            reader = csv.reader(file)
            writer = csv.writer(output)
            inputRow = []
            outputRow = ["Member ID", "First Name", "Last Name", "Gender", "Phone Number", "Email Address", "Created On", "Createdby_FirstName", "Createdby_LastName", "Notes", "Categories"]

            rowNumber = 0
            for row in reader:
                print("Converting (" + str(rowNumber) + ") ", end='')
                print(row)

                if(rowNumber == 0):
                    #If the row number is 0 write our first row number
                    inputRow = row
                    writer.writerow(outputRow)
                else:
                    # Lets write our data!!
                    tempRow = [""] * len(outputRow)

                    # Write the stuff we don't need to alter
                    copyRow(tempRow, row, outputRow, inputRow, "Member ID", "Member ID")

                    # Date
                    year = row[inputRow.index("Note Date")].split('/')[2]
                    month = row[inputRow.index("Note Date")].split('/')[1]
                    date = row[inputRow.index("Note Date")].split('/')[0]
                    tempRow[outputRow.index("Created On")] = year + "-" + month + "-" + date + "T00:00:00Z"

                    copyRow(tempRow, row, outputRow, inputRow, "Notes", "Notes")
                    copyRow(tempRow, row, outputRow, inputRow, "Gender", "Gender")
                    copyRow(tempRow, row, outputRow, inputRow, "Phone Number", "Phone Number")
                    copyRow(tempRow, row, outputRow, inputRow, "Email Address", "Email Address")

                    # Person name
                    if(row[inputRow.index("Person")] == ""):
                        errorsAt.append(rowNumber)
                        tempRow[outputRow.index("First Name")] = "Unknown"
                        tempRow[outputRow.index("Last Name")] = "Unknown"
                        print(row)
                        if(input("Warning: Person name is empty! Inport as Unknown, Unknown? (y/n): ") != "y"):
                            print("Exiting script. Please delete or change item at " + str(rowNumber))
                            exit()
                    elif(row[inputRow.index("Person")].find(',') != -1):
                        tempRow[outputRow.index("First Name")] = row[inputRow.index("Person")].split(', ')[1]
                        tempRow[outputRow.index("Last Name")] = row[inputRow.index("Person")].split(', ')[0]
                    else:
                        errorsAt.append(rowNumber)
                        tempRow[outputRow.index("First Name")] = row[inputRow.index("Person")]
                        tempRow[outputRow.index("Last Name")] = "Unknown"
                        print(row)
                        if(input("Warning: Person name is in a weird format should the first name be " + tempRow[outputRow.index("First Name")] + " and last name be Unknown? (y/n): ") != "y"):
                            print("Exiting script. Please delete or change item at " + str(rowNumber))
                            exit()

                    # Author name
                    if(row[inputRow.index("Created By")] == ""):
                        errorsAt.append(rowNumber)
                        tempRow[outputRow.index("Createdby_FirstName")] = "Unknown"
                        tempRow[outputRow.index("Createdby_LastName")] = "Unknown"
                        print(row)
                        if(input("Warning: Author name is empty! Inport as Unknown, Unknown? (y/n): ") != "y"):
                            print("Exiting script. Please delete or change item at " + str(rowNumber))
                            exit()
                    elif(row[inputRow.index("Created By")].find(',') != -1):
                        tempRow[outputRow.index("Createdby_FirstName")] = row[inputRow.index("Created By")].split(', ')[1]
                        tempRow[outputRow.index("Createdby_LastName")] = row[inputRow.index("Created By")].split(', ')[0]
                    else:
                        errorsAt.append(rowNumber)
                        tempRow[outputRow.index("Createdby_FirstName")] = row[inputRow.index("Created By")]
                        tempRow[outputRow.index("Createdby_LastName")] = "Unknown"
                        print(row)
                        if(input("Warning: Author name is in a weird format should the first name be " + tempRow[outputRow.index("Createdby_FirstName")] + " and last name be Unknown? (y/n): ") != "y"):
                            print("Exiting script. Please delete or change item at " + str(rowNumber))
                            exit()

                    # Category
                    categories = row[inputRow.index("Categories")]

                    if(categories.find(',') != -1):
                        # Found a comma we need to deal with this!
                        errorsAt.append(rowNumber)
                        print("Error: There are multiple categories found. Please select a single category this item should be apart of")
                        print(row)
                        i = 1
                        for item in categories.split(','):
                            print(str(i) + " - " + item)
                            i += 1
                        categories = categories.split(',')[int(input("Please select a category (number) to use for this item: ")) - 1]
                        print("OK - " + categories)
                        time.sleep(3)

                    # There is a singular category try to find it and replace it with it's new name
                    if(not categories in definitions):
                        print("ERROR: Key not found! " + categories + " Please resolve this missing key and re-run the script")
                        exit()
                    else:
                        tempRow[outputRow.index("Categories")] = definitions[categories]
                        if(tempRow[outputRow.index("Categories")] == "NOTSET"):
                            print("Error: Category " + categories + " is not set (Currently NOTSET) in the definitions at the top of this script!")
                            exit()

                    writer.writerow(tempRow)
                rowNumber += 1

# Print the error lines if there were any
print("Done!")
if(len(errorsAt) > 0):
    print("Errors were found at lines: ")
    for line in errorsAt:
        print(str(line + 1))