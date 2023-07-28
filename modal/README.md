# setup
```
pip install -r requirements.txt
modal token new
```


# [hello-world](https://modal.com/docs/guide/ex/hello_world)
```bash
# run locally
modal run hello_world/main.py
```

# [stable-diffusion](https://modal.com/docs/guide/ex/stable_diffusion_cli)
```bash
# add huggingface secret on modal page https://modal.com/secrets from 
# https://huggingface.co/settings/tokens

# run locally
modal run stable_diffusion/main.py --prompt cat --samples 2 --steps 50 --batch-size 1
# deploy
modal deploy stable_diffusion.main
# call deployed function
python stable_diffusion/call.py
```

# custom template
