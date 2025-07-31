import requests
import streamlit as st
import re
import json

# Country codes and phone number length rules (simplified for demo)
COUNTRY_CODES = [
    {"name": "India", "dial_code": "+91", "length": 10},
    {"name": "United States", "dial_code": "+1", "length": 10},
    {"name": "United Kingdom", "dial_code": "+44", "length": 10},
    {"name": "Australia", "dial_code": "+61", "length": 9},
    {"name": "Canada", "dial_code": "+1", "length": 10},
    {"name": "Germany", "dial_code": "+49", "length": 11},
    {"name": "France", "dial_code": "+33", "length": 9},
    {"name": "Singapore", "dial_code": "+65", "length": 8},
    {"name": "UAE", "dial_code": "+971", "length": 9},
    {"name": "China", "dial_code": "+86", "length": 11},
    # Add more as needed
]

# Placeholder for Groq API key (replace with your actual key)
GROQ_API_KEY = '#'
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

def ask_llm(prompt, context=None):
    """
    Send a prompt to the Groq LLM API and return the response.
    :param prompt: The prompt string to send.
    :param context: Optional context for the conversation.
    :return: LLM response as string.
    """
    try:
        # Prepare the messages for the API
        messages = []
        if context:
            messages.append({"role": "system", "content": context})
        messages.append({"role": "user", "content": prompt})
        
        # API request payload
        payload = {
            "model": "llama3-8b-8192",  # Using Llama model on Groq
            "messages": messages,
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Make API call
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            # Fallback response if API fails
            return f"Hello! I'm TalentScout, your AI hiring assistant. {prompt}"
            
    except Exception as e:
        # Fallback response for any errors
        return f"Hello! I'm TalentScout, your AI hiring assistant. {prompt}"

def validate_input(field, value, country_code=None):
    """
    Validate user input for a given field.
    :param field: The field name (e.g., 'email').
    :param value: The value to validate.
    :return: (is_valid, error_message)
    """
    if not value or value.strip() == "":
        return False, "This field cannot be empty."
    
    value = value.strip()
    
    if field == 'email':
        # Email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value):
            return False, "Please enter a valid email address."
        # Gmail-specific validation
        if value.lower().endswith('@gmail.com'):
            gmail_pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
            if not re.match(gmail_pattern, value):
                return False, "Please enter a valid Gmail address (e.g., example@gmail.com)."
    
    elif field == 'phone':
        # Phone validation with country code
        if not country_code:
            return False, "Please select a country code."
        # Find country info
        country = next((c for c in COUNTRY_CODES if c['dial_code'] == country_code), None)
        if not country:
            return False, "Invalid country code."
        # Remove non-digit chars except +
        phone_digits = re.sub(r'[^0-9]', '', value.replace(country_code, '', 1))
        # Check length
        if len(phone_digits) != country['length']:
            return False, f"Phone number should be {country['length']} digits for {country['name']}."
        # Basic phone pattern
        if not phone_digits.isdigit():
            return False, "Phone number should contain only digits."
    
    elif field == 'experience':
        # Experience validation
        try:
            exp = float(value)
            if exp < 0 or exp > 50:
                return False, "Please enter a reasonable number of years (0-50)."
        except ValueError:
            return False, "Please enter a valid number for years of experience."
    
    elif field == 'full_name':
        # Name validation
        if len(value) < 2:
            return False, "Name must be at least 2 characters long."
        if not re.match(r'^[a-zA-Z\s]+$', value):
            return False, "Name should only contain letters and spaces."
    
    elif field == 'tech_stack':
        # Tech stack validation
        if len(value) < 2:
            return False, "Please provide at least one technology."
    
    return True, ""

 