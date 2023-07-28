import modal

f = modal.Function.lookup("stable-diffusion-cli", "StableDiffusion.run_inference")

result = f.call(prompt="cat", steps=50, batch_size=1)
print(len(result))
print(type(result[0]))

import ipdb; ipdb.set_trace()
