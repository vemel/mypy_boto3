"""
Jinja2 renderer and black formatter.
"""
from pathlib import Path
from typing import Optional

try:
    import black
except ModuleNotFoundError:
    pass

from mypy_boto3_builder.constants import TEMPLATES_PATH
from mypy_boto3_builder.enums.service_name import ServiceName
from mypy_boto3_builder.structures.module_record import ModuleRecord
from mypy_boto3_builder.jinja_manager import JinjaManager

BLACK_INSTALLED = "black" in locals()


def blackify(content: str, file_path: Path, fast: bool = True) -> str:
    """
    Format `content` with `black` if `file_path` is `*.py` or `*.pyi`.

    On error writes invalid `content` to `file_path` to check for errors.

    Arguments:
        content -- Python code to format.
        file_path -- Target file path.
        fast -- Whether to skip AST post-check.

    Returns:
        Formatted python code.

    Raises:
        ValueError -- If `content` is not a valid Python code.
    """
    if not BLACK_INSTALLED:
        return content

    if file_path.suffix not in (".py", ".pyi"):
        return content

    file_mode = black.FileMode(is_pyi=file_path.suffix == ".pyi")
    try:
        content = black.format_file_contents(content, fast=fast, mode=file_mode)
    except black.NothingChanged:
        pass
    except IndentationError as e:
        file_path.write_text(content)
        raise ValueError(f"Cannot parse {file_path}: {e}")
    except black.InvalidInput as e:
        file_path.write_text(content)
        raise ValueError(f"Cannot parse {file_path}: {e}")

    return content


def render_jinja2_template(
    template_path: Path,
    module: Optional[ModuleRecord] = None,
    service_name: Optional[ServiceName] = None,
) -> str:
    """
    Render Jinja2 template to a string.

    Arguments:
        template_path -- Relative path to template in `TEMPLATES_PATH`
        module -- Module record.
        service_name -- ServiceName instance.

    Returns:
        A rendered template.
    """
    template_full_path = TEMPLATES_PATH / template_path
    if not template_full_path.exists():
        raise ValueError(f"Template {template_path} not found")

    template = JinjaManager.get_environment().get_template(template_path.as_posix())
    return template.render(module=module, service_name=service_name,)
