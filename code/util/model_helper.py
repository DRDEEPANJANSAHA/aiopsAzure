"""
model_helper.py
"""
from azureml.core import Run
from azureml.core import Workspace
from azureml.core.model import Model as AMLModel


def get_current_workspace() -> Workspace:
    """
    Retrieves and returns the latest model from the workspace
    by its name and tag. Will not work when ran locally.

    Parameters:
    None

    Return:
    The current workspace.
    """
    run = Run.get_context(allow_offline=False)
    experiment = run.experiment
    return experiment.workspace


def _get_model_by_tag(
    model_name: str,
    tag_name: str,
    tag_value: str,
    aml_workspace: Workspace = None
) -> AMLModel:
    """
    Retrieves and returns the latest model from the workspace
    by its name and tag.

    Parameters:
    aml_workspace (Workspace): aml.core Workspace that the model lives.
    model_name (str): name of the model we are looking for
    tag (str): the tag value the model was registered under.

    Return:
    A single aml model from the workspace that matches the name and tag.
    """
    # Validate params. cannot be None.
    if model_name is None:
        raise ValueError("model_name[:str] is required")
    if tag_name is None:
        raise ValueError("tag_name[:str] is required")
    if tag_value is None:
        raise ValueError("tag[:str] is required")
    if aml_workspace is None:
        aml_workspace = get_current_workspace()

    # get model by tag.
    model_list = AMLModel.list(
        aml_workspace, name=model_name,
        tags=[[tag_name, tag_value]], latest=True
    )

    # latest should only return 1 model, but if it does, then maybe
    # internal code was accidentally changed or the source code has changed.
    should_not_happen = ("THIS SHOULD NOT HAPPEN: found more than one model "
                         "for the latest with {{tag_name: {tag_name},"
                         "tag_value: {tag_value}. "
                         "Models found: {model_list}}}")\
        .format(tag_name=tag_name, tag_value=tag_value,
                model_list=model_list)
    if len(model_list) > 1:
        raise ValueError(should_not_happen)

    return model_list


def get_model_by_tag(
    model_name: str,
    tag_name: str,
    tag_value: str,
    aml_workspace: Workspace = None
) -> AMLModel:
    """
    Wrapper function for get_model_by_tag that throws an error if model is none
    """
    model_list = _get_model_by_tag(
        model_name, tag_name, tag_value, aml_workspace)

    if model_list:
        return model_list[0]

    no_model_found = ("No Model found with {{tag_name: {tag_name} ,"
                      "tag_value: {tag_value}.}}")\
        .format(tag_name=tag_name, tag_value=tag_value)

    raise Exception(no_model_found)
