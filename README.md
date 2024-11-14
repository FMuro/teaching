# What does this do?

This `python` package provides some CLI utilities to deal with my teaching admin:

- matching
- splitgrades
- fillgrades
- mailing
  

# Install

Run the following command in terminal:

```
pip install --upgrade git+https://github.com/FMuro/teaching.git#egg=teaching
```

Use this command to update the package too. 
Do you use `pipx`? This is typical if you have `python` installed on macOS through `homebrew`. Then the command to install is:

```
pipx install git+https://github.com/FMuro/teaching.git#egg=teaching
```

The command to update is:

```
pipx upgrade teaching
```


# Remove

```
pip uninstall teaching
```

If you installed it using `pipx`:

```
pipx uninstall teaching
```