# Dictionaries

- Dictioanaries are used to store the data in key value pairs
- Dictionaries are unordered, changeable and do not allow duplicates.
- Does not allow duplicates refers to that it will overwrite the existing values
- we can use dictionary constructor to actually build the dictionaries.

## Accessing items
- ```python
    thisdict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
    }
    ```
- Accessing a single variable :
- ```python
    x = thisdict["brand"]
    print(x)
    ```
- we can use get method to retrive the variables.
- ```python
    x = thisdict.get("brand")
    ```
- use keys() to get all the key items
- ```python
    x = thisdict.keys()
    print(x)
    ```
- use values() to get all the value items
-   ```python
    x = thisdict.values()
    print(x)
    ```
- use items() to all the items
- ```python
    x = thisdict.items()
    print(x)
    ```

- If Exists or not:
- ```python
    if "brand" in thisdict:
        print("yes")
    ```

## Changing the elements

### Method 1 : Direct Key assignment

- ```python

    thisdict = {"brand" : "Ford" , "year" : 1965}
    thisdict["brand"] : "Mustang" #updates existing one.
    thisdict["Color"] : "Red" # adds new row

    ```

### Method 2 : .update() Method

- ```python

    thisdict = {"brand" : "Ford" , "year" : 2000}
    thisdict.update(year = 1965) #updates existing one.
    thisdict.update({"color" = "Red"}) # Adds new row
    thisdict.udpate(year= 1965, brand = "mustang") #updating multiple rows at a time.
    thisdict.update([("year", 2021)]) # using iterable pairs
    ```

### Method 3 : Dictionary comprehension

- ```python
    {k : v * 2 for k,v in thisdict.items()}
    ```

### Method 4 : Merging  |=

- ```python
    thisdict = {"brand": "Ford", "year": 1964}
    thisdict |= {"year": 2020, "color": "red"}
    ```


## Remove Items :

### Method 1 : using pop

- ```python

    thisdict.pop("brand")
    print(thisdict)

    ```

### Method 2 : Removing Last inserted item

- ```python

    thisdict.popitem()
    print(thisdict)

    ```

### Method 3 : deleting the dict & deleting the item using del

- ```python

    del thisdict #Deleting entire dictionary

    del thisdict["model"] #deleting a single value.

    ```

### Method 4 : clear the data in dictionary

- ```python

    thisdict.clear()
    print(thisdict) # Returns empty dictionary.

    ```


## Looping through Dictionaries

- ```python

    for i in thisdict:
        print(thisdict[i])

    ```

- ```python

    for i in thisdict.keys():
        print(i)

    for i in thisdict.values():
        print(i)

    for i,j in thisdict.items():
        print(i,j)

    ```
