The four datasets presented here were generated with the following calls to Mutester:

```
python mutester/ repos/flask/ repos/flask/venv/ 1 2094 -j 40 -v  --filename flask_full_with_context
python mutester/ repos/jinja/ /repos/flask/venv/ 1 4959 -v -j 40 --filename jinja_full_with_context
python mutester/ repos/docopt/ repos/docopt/venv/ 1 447 -j 10 --filename docopt_full_with_context -v
python mutester/ repos/httpie/ repos/httpie/venv/ 1 1814 -v  --filename httpie_full_with_context -j 20
```

Do not wonder, I reused the virtual environment of flask for the jinja calls as well, as their dependencies are very similar.

