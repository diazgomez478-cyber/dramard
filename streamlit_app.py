# En streamlit_app.py
def get_ia_fuerte(prompt):
    for _ in range(5): # 5 intentos, no 1
        try:
            seed = random.randint(1,9999999)
            url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt+', dominican, cinematic, photorealistic 8k')}?width=512&height=512&seed={seed}&nologo=true&model=flux"
            r = requests.get(url, timeout=100, headers={"User-Agent":"Mozilla/5.0"})
            if r.status_code==200 and len(r.content)>10000:
                return Image.open(io.BytesIO(r.content)).convert("RGB").resize((1280,720))
        except: time.sleep(2)
    return None # Si falla, no pongas paisaje, intenta de nuevo

# Y usa estos prompts exactos:
prompts = [
    "dominican female judge black robe courtroom angry serious",
    "dominican mother crying happy hugging two children in dominican courtroom, flag dominicana",
    "dominican rich man furious throwing dollars money champagne luxury vip nightclub"
]
