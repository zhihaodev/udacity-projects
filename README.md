# Item Catalog

This is a web application that provides a list of items within a variety of categories and integrate third party user registration and authentication. CRUD operations are supported for authenticated users.

## Usage

- Install [virtualenv](https://virtualenv.pypa.io/en/latest/): `pip install virtualenv`.

- Create and activate the Python virtual environment: 
`virtualenv venv`
`source venv/bin/activate`.

- Install all required modules: `pip install -r requirements.txt`.

- Regenerate the database: `python manage.py db upgrade`.

- Run the web server: `python manage.py runserver`.

- Open http://localhost:5000/ to check out the item catalog website.


## License

Code released under [the MIT license](https://github.com/zhihaodev/item-catalog/blob/master/LICENSE).
