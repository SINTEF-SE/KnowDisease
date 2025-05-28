from transformers import AutoModelForCausalLM, AutoTokenizer
import outlines

def initialize_llm(deterministic=False):
    model_id = "hugging-quants/Meta-Llama-3.1-8B-Instruct-GPTQ-INT4"
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    
    model_kwargs = {
        "device_map": "cuda:0",
        "torch_dtype": "auto",
        "trust_remote_code": True
    }
    
    if "GPTQ" in model_id:
        try:
            from transformers import ExllamaConfig
            exllama_config = ExllamaConfig()
            exllama_config.max_input_len = 4096
            model_kwargs["exllama_config"] = exllama_config
        except ImportError:
            model_kwargs["max_memory"] = {0: "24GB"}
    
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        **model_kwargs
    )

    outlines_llm = outlines.models.Transformers(model=model, tokenizer=tokenizer)
    if deterministic:
        outlines_sampler = outlines.samplers.greedy()
    else:
        outlines_sampler = outlines.samplers.multinomial(top_p=0.9, temperature=0.4)

    return outlines_llm, outlines_sampler