#  Beedy (API)

This is a API for Beedy powered by FastAPI.

Beedy is a LMS (Learning Management System).

This project is for SOA class in The UPP (Universidad Politécnica de Pénjamo)

This part contain all the information to execute the __*Backend*__

> 📺 [Frontend](#)

## Requirements

1. [Python 3](https://www.python.org/downloads/)
2. [Virtualenv](https://pypi.org/project/virtualenv/)
3. [MySQL](https://www.mysql.com/downloads/)

## How Configure?

1. Clone the repository
```bash
git clone https://github.com/Kike-H/beedy_api
```

2. Create a virtual environment
```bash
virtualenv .venv
```
3. Activate Virtualenv

> Linux/Unix 
```bash
source ./.venv/bin/activate
```
> Windows 

```bash
.\.venv\Scripts\activate.bat
```

4. Update pip
```
python -m pip install --upgrade pip   
```


5. Install all requirements

```bash
pip install -r requirements.txt
```

## How Run?

1. Go to src
```bash
cd src
```

2. Execute 
```bash
uvicorn app:app --reload
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
