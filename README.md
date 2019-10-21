# pyIUDX - Python SDK for IUDX.

## Installation
```
pip install pyIUDX
```

## Usage

### Catalogue
```python
from pyIUDX import Catalogue 
cat = Catalogue()
print(cat.connectToCat("https://catalogue.iudx.org.in", "443", "1"))  # IP/ Domain, Port, Version 
print(cat.getItemCount())
print(cat.getAllItems())
print(cat.getResourceItem("rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/pscdcl/aqm-bosch-climo/Pune Railway Station_28"))

```

### Auth 
```python
from pyIUDX import Auth 
auth = Auth("auth.iudx.org.in","my-certificate.pem", "my-private-key.pem")
access_token = auth.get_token(
	[
		{"resource-id": "rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/pscdcl/aqm-bosch-climo/Pune-Railway-Station-1"},
		{"resource-id": "rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/pscdcl/aqm-bosch-climo/Pune-Railway-Station-2"},
		{"resource-id": "rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/pscdcl/aqm-bosch-climo/Pune-Railway-Station-3"},
		{"resource-id": "rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/pscdcl/aqm-bosch-climo/Pune-Railway-Station-4"},
		{"resource-id": "rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/pscdcl/aqm-bosch-climo/Pune-Railway-Station-5"}
	]
)
print(access_token)
```

## PyPI
[https://pypi.org/project/pyIUDX/](https://pypi.org/project/pyIUDX/)

## Authors
* Mukunth A
* [Jishnu P](https://jishnujayakumar.github.io)
* Arun Babu
* Rakshit Ramesh
