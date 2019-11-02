# pyIUDX - Python SDK for IUDX.

## Installation
```
pip install pyIUDX
```

## Usage

### Catalogue
1. Load the catalogue module \
```
from pyIUDX.cat import cat 
self.catalogue = cat.Catalogue("https://catalogue.iudx.org.in/catalogue/v1")
```
2. Show how many items are in the catalogue
```
print(cat.getItemCount())
```
3. Print the catalogue item for one item
```
print(cat.getResourceItem("rbccps.org/aa9d66a000d94a78895de8d4c0b3a67f3450e531/pscdcl/aqm-bosch-climo/Pune Railway Station_28"))
```

### Resource servers


## PyPI
[https://pypi.org/project/pyIUDX/](https://pypi.org/project/pyIUDX/)

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
