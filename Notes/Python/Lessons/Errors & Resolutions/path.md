# PATH ERROR

- **DESCRIPTION** : Whenever we are fetching the details from the file which is not in the current folder, We will found this error like No module found.
- **REASON** : The reason why this happening is that whenever we are importing the module it will look into the current folder, which is sys.path. So with in that folder we will not be able to fetch those details, because those are in different folder.
- **RESOLUTION** : So we are going to add our path to the sys.path at the index 0. So the system will think that one is the main path and will fetch those details


```python
import sys
config_folder = Path(__file__).resolve().parents[1] / "logging"
sys.path.insert(0,str(config_folder))
```

- Path(__file__).resolve().parents[1] / "logging"
    - Path(__file__) : gives us the file path
    - resolve() : gives us the absolute path
    - parents[1] : take us one folder back.
        - Ex : c/git/testing/code results in c/git/testing
    - "/" will add logging to the existing path.
- sys.path.insert(0,str(config_folder))
    - Why ? because the system reads 0 index from the sys.path whenever looking for the modules.
    - sys.path : gives us sys.path
    - insert(0,str(config_folder)) : it inserts the path at the index 0.

- **NOTE** : sys.path control where python search for imported modules, it doesn't control ordinary file paths.
