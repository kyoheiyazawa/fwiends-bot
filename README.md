Dependencies managed using `pipenv`, get it using `pip`:
```python
pip install --user pipenv
```

Install dependencies:
```python
pipenv install
```

Create config.py with Channel ID and token:
```python
channel = 'AA999999'
token = 'zzzz-0000000'
```

Build markov.json:
```bash
./setup.sh
```

Run the bot and generate html output:
```bash
./run.sh
```
