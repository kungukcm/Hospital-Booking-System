#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import sys

url = 'http://localhost:8000/chat'
headers = {'Content-Type': 'application/json'}

tests = [
    ('Habari', 'Swahili greeting'),
    ('What are the working hours?', 'Hospital hours query'),
    ('Who is the CEO of KUTRRH?', 'CEO query'),
    ('What payment methods are available?', 'Payment methods'),
]

print('=== COMPREHENSIVE SYSTEM TEST ===\n', file=sys.stderr, flush=True)

for message, description in tests:
    print(f'Test: {description}', file=sys.stderr)
    print(f'User: {message}', file=sys.stderr)
    
    payload = {'message': message}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            assistant_msg = result['conversation_history'][-1]['content']
            # Truncate if too long
            preview = assistant_msg[:100] if len(assistant_msg) > 100 else assistant_msg
            print(f'Assistant: {preview}...', file=sys.stderr)
        else:
            print(f'ERROR: Status {response.status_code}', file=sys.stderr)
    except Exception as e:
        print(f'ERROR: {str(e)}', file=sys.stderr)
    
    print('', file=sys.stderr)

print('\nAll tests completed', file=sys.stderr)
