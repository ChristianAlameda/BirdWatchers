# Open the file and read the lines
# with open('C:\\Users\\Christian Alameda\\OneDrive\\Documents\\csuImportant\\CSUClasses\\CS4280NoSQL\\group\\project\\country_list.txt', 'r') as file:
#     countries_list = file.read().splitlines()
# Open the text file in read mode
with open('common_name.txt', 'r', encoding='cp1252', errors='replace') as file:
    lines = file.readlines()

lines = [line.strip() for line in lines]
print(lines)
