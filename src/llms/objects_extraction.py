import ast

from transformers.modeling_utils import PreTrainedModel
from transformers.tokenization_utils_fast import PreTrainedTokenizerFast
import torch

from src.llms.prompts import SPOT_OBJECTS_CHAT_TEMPLATE


def get_key_objects(
    tokenizer: PreTrainedTokenizerFast,
    model: PreTrainedModel,
    message: str,
    **model_params: dict,
) -> dict[str, str | list[tuple[str, list[str | None]]]]:
    """
    Extracts key objects and additional prompts from a response generated by a large language model.

    Args:
        tokenizer (PreTrainedTokenizerFast): The tokenizer used to encode and decode text.
        model (PreTrainedModel): The large language model that generated the response.
        message (str): The message that was used to prompt the model.
        **model_params (dict): Additional parameters to be passed to the model's generate() function.

    Returns:
        dict[str, str | list[tuple[str, list[str | None]]]]: A dictionary containing:
            * objects (list[tuple[str, list[str | None]]]): A list of tuples where the first
                element is the object name and the second element is a list of attributes or None
                if not available.
            * bg_prompt (str): The background prompt extracted from the response.
            * neg_prompt (str): The negation prompt extracted from the response (empty string if
                not present).
    """
    prompt = tokenizer.apply_chat_template(
        message, tokenize=False, add_generation_prompt=True
    )
    input_ids = tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt")
    generated_ids = model.generate(
        input_ids=input_ids.to(model.device),
        **model_params,
    )
    response = tokenizer.decode(generated_ids[0])
    response = response[len(prompt) :].replace("<eos>", "")

    # Extracting key objects
    key_objects_part = response.split("Objects:")[1]
    start_index = key_objects_part.index("[")
    end_index = key_objects_part.rindex("]") + 1
    objects_str = key_objects_part[start_index:end_index]

    # Converting string to list
    parsed_objects = ast.literal_eval(objects_str)

    # Extracting additional negative prompt
    bg_prompt = response.split("Background:")[1].split("\n")[0].strip()
    negative_prompt = response.split("Negation:")[1].split("\n")[0].strip()
    negative_prompt = negative_prompt if negative_prompt != "None" else ""

    parsed_result = {
        "objects": parsed_objects,
        "bg_prompt": bg_prompt,
        "neg_prompt": negative_prompt,
    }
    return parsed_result


def spot_objects(
    tokenizer: PreTrainedTokenizerFast,
    model: PreTrainedModel,
    prompt: str,
    **model_params: dict,
) -> dict[str, str | list[tuple[str, list[str | None]]]]:
    """
    This function identifies objects mentioned in a given prompt using a pre-trained
    tokenizer and model.

    Args:
        tokenizer (PreTrainedTokenizerFast): The tokenizer to use for processing the text.
        model (PreTrainedModel): The pre-trained model used for object detection.
        prompt (str): The user prompt containing the text to analyze for objects.
        **model_params (dict): Additional parameters to pass to the pre-trained model.

    Returns:
        dict[str, str | list[tuple[str, list[str | None]]]]: A dictionary containing:
            * objects (list[tuple[str, list[str | None]]]): A list of tuples where the first
                element is the object name and the second element is a list of attributes or None
                if not available.
            * bg_prompt (str): The background prompt extracted from the response.
            * neg_prompt (str): The negation prompt extracted from the response (empty string if
                not present).
    """
    question = {"role": "user", "content": f"User Prompt: {prompt}"}
    message = [*SPOT_OBJECTS_CHAT_TEMPLATE, question]
    result = get_key_objects(tokenizer, model, message, **model_params)
    return result
