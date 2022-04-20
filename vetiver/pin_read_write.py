import pydantic
import pins
import warnings
import json

from .vetiver_model import VetiverModel
from .meta import vetiver_meta
from .write_fastapi import _choose_version

def vetiver_pin_write(board: pins.BaseBoard, model: VetiverModel, versioned: bool=True):
    """
    Write pin including VetiverModel
    
    Parameters
    ----------
    board: pins.BaseBoard
        Location for pin to be saved
    model: vetiver.VetiverModel
        VetiverModel to be written to board
    versioned: bool
        Whether or not the pin should be versioned
    """
    if not board.allow_pickle_read:
        raise NotImplementedError # must be pickle-able

    board.pin_write(
        model.model,
        name = model.model_name,
        type = "joblib",
        description = model.description,
        metadata = {"required_pkgs": model.metadata.get("required_pkgs"),
                    "save_ptype": model.save_ptype,
                    "ptype": None if model.ptype == None else model.ptype().json()},
        versioned=versioned
    )

    # to do: Model card

    # message = """
    # Create a Model Card for your published model.
    # Model Cards provide a framework for transparent, responsible reporting.
    # Use the vetiver `.Rmd` template as a place to start."""

    # warnings.warn(message=message)


def vetiver_pin_read(board: pins.BaseBoard, name: str, version: str = None) -> VetiverModel:
    """
    Read pin and populate VetiverModel
    
    Parameters
    ----------
    board: pins.BaseBoard
        Board where pin is held
    name: string
        Name of pin
    versioned: bool
        Whether or not the pin should be versioned

    Returns
    --------
    vetiver.VetiverModel
    
    """
    version = version if version is not None else _choose_version(board.pin_versions(name))

    model = board.pin_read(name, version)
    meta = board.pin_meta(name)

    v = VetiverModel(model = model,
        model_name = name,
        description = meta.description,
        metadata = vetiver_meta(user = meta.user,
             version = version,
             url = meta.user.get("url"), # None all the time, besides Connect
             required_pkgs = meta.user.get("required_pkgs")
        ),
        save_ptype=meta.user.get("save_ptype"),
        ptype_data = json.loads(meta.user.get("ptype")) if meta.user.get("ptype") else None,
        versioned = True
        )
    
    return v