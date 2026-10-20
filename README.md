# Expense Tracker

A second-year final project (Sep – Nov 2023): two merchandise shops and an expense tracker that share one XML data file. Buying something in either shop records the purchase, and the tracker shows every purchase with search, filters, sorting, and editing.

Built with Python, Flask, XML, HTML, CSS, and Bootstrap.

## How it fits together

| App | File | Port | What it does |
|-----|------|------|--------------|
| Expense tracker | `fetch.py` | 5000 | Lists all purchases; filter by expense type, shop, or date; search products; sort by date; edit and delete records |
| Hoyo Shop | `hoyofetch.py` | 5002 | Genshin Impact merchandise shop |
| League Shop | `leaguefetch.py` | 5003 | League of Legends merchandise shop |

All three read and write `userdata.xml`, which ships with sample purchases.

## Running it

Requires Python 3.10 or newer.

```powershell
pip install -r requirements.txt
```

Start each app in its own terminal:

```powershell
python fetch.py        # http://127.0.0.1:5000  (expense tracker)
python hoyofetch.py    # http://127.0.0.1:5002  (Hoyo Shop)
python leaguefetch.py  # http://127.0.0.1:5003  (League Shop)
```

Buy something in one of the shops, then refresh the expense tracker to see the purchase.

## Project structure

```
fetch.py, hoyofetch.py, leaguefetch.py   Flask apps
userdata.xml                             shared purchase data
templates/                               page templates (tracker, shops, error page)
static/                                  Bootstrap, CSS, and product images
```

## Notes

This is a student project kept for reference. Product names and images are from Genshin Impact (HoYoverse) and League of Legends (Riot Games) merchandise and belong to their respective owners.
