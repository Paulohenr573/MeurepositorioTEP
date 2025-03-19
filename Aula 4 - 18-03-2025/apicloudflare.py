import requests
import base64

# URL do Worker AI da Cloudflare
API_URL = "https://api.cloudflare.com/client/v4/accounts/4db4d75fec8840b8233b17c4da8dfb68/ai/run/@cf/black-forest-labs/flux-1-schnell"

# Substitua pela sua chave de API (se necessário)
HEADERS = {
    "Authorization": "Bearer TmXs-3zBuiZ3AovWnFe3KkG7KSrjrgdTreiVXgQA",
    "Content-Type": "application/json"
}

# Prompt para gerar a imagem
DATA = {
    "prompt": "A charming Shih Tzu, wearing a tiny pirate hat with a playful grin, joyfully runs across the deck of the Going Merry, the beloved ship of the Straw Hat Pirates. Her silky fur flows with every movement as she eagerly chases a group of fluttering butterflies that dance around the ship. The soft, golden light of the setting sun casts a warm glow on the ship's wooden deck, while the sparkling ocean stretches out beneath a vibrant, colorful sky. The butterflies, in shades of blue, yellow, and orange, flutter gracefully in the air, creating a magical atmosphere as the wind tousles her fur. The Going Merry, with its iconic figurehead and charming, weathered look, stands proudly in the background, adding to the adventure-filled scene. Her excitement is clear, with her tongue sticking out in pure joy and her eyes sparkling with happiness, as the ship sails onward toward new adventures, all captured in this picturesque, whimsical moment.",
    "width": 1024,
    "height": 1024,
    "num_inference_steps": 30
}

# Faz a requisição para gerar a imagem
response = requests.post(API_URL, json=DATA, headers=HEADERS)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    result = response.json()
    
    image_base64 = result["result"]["image"]
    
    if image_base64:
        # Converte Base64 para imagem
        try:
            with open("output.png", "wb") as img_file:
                img_file.write(base64.b64decode(image_base64))
            print("Imagem salva como output.png")
        except Exception as e:
            print(f"Erro ao decodificar a imagem: {e}")
else:
    print(f"Erro: {response.status_code}, {response.text}")
