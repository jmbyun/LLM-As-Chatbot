import torch
from peft import PeftModel
from transformers import LlamaTokenizer, LlamaForCausalLM
from optimum.bettertransformer import BetterTransformer

def load_model(base, finetuned, multi_gpu, force_download_ckpt):
    tokenizer = LlamaTokenizer.from_pretrained(base)
    tokenizer.pad_token_id = 0
    tokenizer.padding_side = "left"

    if not multi_gpu:
        model = LlamaForCausalLM.from_pretrained(
            base,
            load_in_8bit=True,
            device_map="auto",
        )
        
        model = PeftModel.from_pretrained(
            model, 
            finetuned, 
            force_download=force_download_ckpt,
            device_map={'': 0}
        )

        # def wrapped_model(*args, **kwargs):
        #     print("## Model called!")
        #     print(args)
        #     print(kwargs)
        #     model(*args, **kwargs)

        # def wrapped_tokenizer(*args, **kwargs):
        #     print("## Model called!")
        #     print(args)
        #     print(kwargs)
        #     model(*args, **kwargs)
        # model = BetterTransformer.transform(model)
        return model, tokenizer
    else:
        model = LlamaForCausalLM.from_pretrained(
            base,
            torch_dtype=torch.float16,
            device_map="auto",
        )
        
        model = PeftModel.from_pretrained(
            model, 
            finetuned, 
            force_download=force_download_ckpt,
            torch_dtype=torch.float16
        )
        model.half()
        # model = BetterTransformer.transform(model)
        return model, tokenizer

