import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import anthropic
import json
import requests

# Create your views here.
def test_view(request):
    return JsonResponse({'message': 'Hello, world!'})


@csrf_exempt
def ask_view(request):

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=api_key)

    if request.method == 'POST':
        data = json.loads(request.body)
        phrase = data.get('phrase')
        if phrase:

            # Make the API call here and store the result
            api_endpoint = "http://127.0.0.1:8000/api/v1/product/list/"
            api_response = requests.get(api_endpoint)
            api_result = api_response.json()

            # Combine the phrase and the API result
            combined_content = f"product list: {api_result} \n\n{phrase}"

            message = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                temperature=0.1,
                system="you are a professional fashion curator, and you are helping a customer find the perfect outfit for a special event. The customer is looking for a dress that is elegant and sophisticated, but also modern and unique. The customer is open to trying new styles and colors, and is looking for something that will make a statement. contained in the product list are available clothing materials on the database, look through the list and suggest a dress that you think would be perfect for the customer. Return the names, product IDs and the image URLS of the products and a brief description of why you think it would be a good choice.",
                messages=[
                    {"role": "user", "content": combined_content}
                ]
            )
            return JsonResponse({'response': message.content[0].text})
        else:
            return JsonResponse({'error': 'No phrase provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)