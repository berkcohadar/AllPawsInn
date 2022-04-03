# customers.xlsx
from numpy import full
import pandas as pd

xls = pd.ExcelFile(r'.\customers.xlsx')
df = xls.parse(xls.sheet_names[0])
length = len(df)
data = df.to_dict()

customers = []
for i in range(0,length):
    customer = {}
    if (str(data["Name"][i]) != "nan"):
        for key in data:
            if key == "Name":
                print(data[key][i])
                fullName = data[key][i].split()

                if len(fullName) > 1:
                    lastName = fullName[-1]
                    fullName.pop()
                    firstName = " ".join(fullName)
                    customer["first_name"] = firstName
                    customer["last_name"] = lastName
                    
                else:
                    customer["first_name"] = fullName

            elif key == "Type":
                customer["TypeID"] = 1
                if data[key][i] == "Dog":
                    customer["TypeID"] = 2

            elif key == "Deceased":
                customer["Deceased"] = 0
                if data[key][i] == "Yes":
                    customer["Deceased"] = 1
                    
            elif key == "NeuteredSpayed":
                customer["NeuteredSpayed"] = 0
                if data[key][i] == "Yes":
                    customer["NeuteredSpayed"] = 1

            elif key == "Vaccinated":
                customer["Vaccinated"] = 0
                if data[key][i] == "Yes":
                    customer["Vaccinated"] = 1
                    
            else:
                customer[key] = str(data[key][i])

        customers.append(customer)

for customer in customers:
    print("\n\nNext Customer:")
    for key in customer:
        if(customer[key] != "nan"):
            print(key, customer[key])

# Some rows does not contain a customer name. They only contain animal information 

# We do not know what "Opted-in to marketing" and "Daycare Credits" columns do.
#    So, we don't save these two fields



