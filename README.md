# Survey Website: Do People Name Their Home Appliances?

A small Flask website built for my course paper on the onomasticon of household appliances (HSE University, 2022–2023). Respondents fill in a survey about whether they give names to their fridge, vacuum cleaner or kettle and which names they choose, and the site shows live statistics on the answers.

It used to run at mlemrr.pythonanywhere.com and is offline now.

## How it works

- **Pages**: home page, survey, thank-you page, statistics.
- **Survey**: one block about the respondent (all questions required) and one block about appliance names (the first two questions are required). Questions are stored in `questions.txt`.
- **Database** (SQLite, `instance/`): `user` (id, name, gender, age, region), `questions` (id, question), `answers` (user id and the answer to each question).
- **Front end**: Jinja templates in `templates/`, Bootstrap with custom CSS in `static/`.

More details (in Russian): `how_it_works.txt`.

## How to run

```bash
pip install flask flask-sqlalchemy
python hw5_result.py
```
