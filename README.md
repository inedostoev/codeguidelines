# codeguidelines

This program - Python script, that can prevent `commit` or `push` code with wrong guidelines. This scripts can be put in `.git/hooks`

## What checks are supported?
It is supported:
* Checking trailing spaces
* Prevent of using:
    1. pre C++11: `typedef`
    2. exceptions: `try`, `catch`
    3. `using namespace ...`
    4. RTTI: `dynamic_cast`, `typeid`

## How to use?
At first, you should choose, when a check is called.

`pre-push` - called before `git push`
`pre-commit` - called before `git commit`

When you choose variant of gitHook, or you choose both variants, add the repository as submodule and configure hooks:
```bash
git submodule add ...
git config core.hooksPath hooks
```

If something went wrong, you can contact with me on email:
 
nedostoev.ka@phystech.edu

inedostoev@gmail.com

