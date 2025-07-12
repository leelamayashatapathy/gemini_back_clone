import os
import requests
from django.conf import settings

def get_gemini_response(prompt):
    api_key = getattr(settings, 'GEMINI_API_KEY', os.getenv('GEMINI_API_KEY', ''))
    
    # Use the correct Gemini API endpoint
    url = 'https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent'
    
    headers = {
        'Content-Type': 'application/json',
    }
    
    data = {
        'contents': [
            {
                'parts': [
                    {
                        'text': prompt
                    }
                ]
            }
        ],
        'generationConfig': {
            'temperature': 0.7,
            'topK': 40,
            'topP': 0.95,
            'maxOutputTokens': 1024,
        }
    }
    
    params = {'key': api_key}
    
    try:
        response = requests.post(url, headers=headers, params=params, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        # Extract the response text
        if 'candidates' in result and len(result['candidates']) > 0:
            candidate = result['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                parts = candidate['content']['parts']
                if len(parts) > 0 and 'text' in parts[0]:
                    return parts[0]['text']
        
        # Fallback if the structure is different
        return result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'No response generated')
        
    except requests.exceptions.RequestException as e:
        return f"[Gemini API Error] {str(e)}"
    except Exception as e:
        return f"[Gemini API Error] {str(e)}" 