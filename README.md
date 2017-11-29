# codeguidelines

This program - Python script, that can prevent `commit` or `push` code with wrong guidelines. This scripts can be put in `.git/hooks`

## What checks are supported?
It is supported:
* Checking trailing spaces
* Prevent of using:
    1. try/catch
    2. typedef
    3. using namespace
    4. dynamic_cast

## How to use?
At first, you should choose, when a check is called.

`pre-push` - called before `git push`

`pre-commit` - called before `git commit`

When you choose variant of gitHook, or you choose two variants, you should copy `codeguidelines.py` and `pre-push` or `pre-commit` into `.git/hooks`

For ex. make `pre-push` gitHook:
```bash
cp codeguidelines.py ../.git/hooks/codeguidelines.py
cp pre-push ../.git/hooks/pre-push
```

If something went wrong, you can contact with me on email:
 
nedostoev.ka@phystech.edu

inedostoev@gmail.com`

