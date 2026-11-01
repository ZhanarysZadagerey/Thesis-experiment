

# Memory consistency experiment

Code and results of the experiment of masters thesis (Zhanarys Zadagerey, University of Pisa, 2026). 

## Check the results

No API key needed:

```
python3 summary.py
```

## To Run the experiment by yourself

You need Python 3 and an Anthropic API key. Each script overwrites its CSV file, so copy the original results first.

```
export ANTHROPIC_API_KEY="YOUR API KEY HERE"
python3 s1.py
```

Run `s2.py` - `s5.py` the same way. The model's answers vary, so new runs can give slightly different numbers.
