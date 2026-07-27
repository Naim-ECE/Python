status = int(input("Enter status code: "))

if status == 200:
    print("Success")
elif status == 404:
    print("Not Found")
else:
    print("Error")