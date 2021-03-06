from luigi import LocalTarget
import luigi
from luigi.task import flatten
from hashlib import sha256
import os

# path issues with sphinx and the relative paths for running as a module, as intended when I wrote them
abs_path = os.path.dirname(__file__)


def get_salted_version(task: luigi.Task) -> str:
    """
    Rough edit of Prof. Gorlin's implementation from here: https://github.com/gorlins/salted/blob/master/salted_demo.py.
    """
    salt = ""
    # sorting the requirements as suggested to increase salt stability
    for req in sorted(flatten(task.requires())):
        salt += get_salted_version(req)

    salt += task.__class__.__name__ + task.__version__
    salt += "".join(
        [
            "{}={}".format(param_name, repr(task.param_kwargs[param_name]))
            for param_name, param in sorted(task.get_params())
            if not param_name in ["lower", "upper"]
        ]
    )
    return sha256(salt.encode()).hexdigest()[:10]
