#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test Swahili booking flow with proper conversation history"""

import requests
import json

url = 'http://localhost:8000/chat'
headers = {'Content-Type': 'application/json'}

# Track conversation history
conversation_history = []

# Simulate booking flow in Swahili
booking_flow = [
    ('Habari, naomba kupanga miadi', 'Start booking in Swahili'),
    ('John Doe', 'Provide name'),
    ('12345', 'Provide patient ID'),
    ('+254701234567', 'Provide phone'),
    ('john@example.com', 'Provide email'),
]

print('=== SWAHILI BOOKING FLOW TEST (WITH CONVERSATION HISTORY) ===\n')

for user_input, description in booking_flow:
    print(f'{description}')
    print(f'User: {user_input}')
    
    # Build request with full conversation history
    payload = {
        'message': user_input,
        'conversation_history': conversation_history
    }
    
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        
        # Update conversation history with the full returned history
        conversation_history = result['conversation_history']
        
        # Get the assistant response
        assistant_msg = result['response']
        
        # Show preview
        preview = assistant_msg[:150] + '...' if len(assistant_msg) > 150 else assistant_msg
        print(f'Assistant: {preview}')
        
        # Check if response contains Swahili markers
        has_swahili = any(word in assistant_msg.lower() for word in [
            'tafadhali', 'jina', 'nambari', 'miadi', 'asante', 'taarifa', 
            'aina', 'tarehe', 'kupanga', 'kuendelea', 'taarifa'
        ])
        
        if has_swahili:
            print('✅ Response in SWAHILI')
        else:
            print('❌ Response in ENGLISH (should be Swahili)')
    else:
        print(f'Error: {response.status_code}')
    
    print()
