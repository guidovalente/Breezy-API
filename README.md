Python class for consuming Breezy's API.

Breezy's API documentation can be found at https://https://developer.breezy.hr/


## Requirements
Requests and PyYAML is necessary to run this code:

`pip install requests pyyaml`


## Usage

Before using the code, make sure to create an auth.yaml file and include your credentials:

```yaml
email: your@email.here
password: breezyPassword
```

Then you can import the BreezyAPI class and make your requests:

```python
# import BreezyAPI from breezy.py
from breezy import BreezyAPI

# create a BreezyAPI object
breezy = BreezyAPI()


# Upon instantiaton, the breezy object will automatically call the /signin
# endpoint and obtain a token, if it fails to do it will raise an exception.
print(breezy.token)  # will print the generated token

# you will now be able to communicate with the API

# for example, we can get the companies' ids, which will be required for most
# of Breezy's API calls
companies = breezy.call(
    "companies" 
)

```
