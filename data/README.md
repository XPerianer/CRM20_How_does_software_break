The four datasets presented can be generated with the following calls to Mutester:

```
python -m mutester repos/flask repos/flask/venv/ 1 2094 -j 40 -v  --filename flask_full_with_context
python -m mutester repos/jinja repos/flask/venv/ 1 4959 -v -j 40 --filename jinja_full_with_context
python -m mutester repos/docopt repos/docopt/venv/ 1 447 -j 10 --filename docopt_full_with_context -v
python -m mutester repos/httpie repos/httpie/venv/ 1 1814 -v  --filename httpie_full_with_context -j 20
```
Notice: the first path has no backslash after it, while the second one has (for the virtual environment). This is a [bug](https://github.com/XPerianer/CRM2020/issues/4)

Do not wonder, I reused the virtual environment of flask for the jinja calls as well, as their dependencies are very similar.

Important to generate own datasets with mutester is to install a virtual environment that has all necessary dependencies installed, and also a slightly modified version of mutester.

You can find details in this [Dockerfile](https://github.com/XPerianer/CRM2020/blob/master/Dockerfile) from the other repo. That contains the calls needed to generate the flask dataset. Besides slight differences in installing the test dependencies, the other projects work the same.
