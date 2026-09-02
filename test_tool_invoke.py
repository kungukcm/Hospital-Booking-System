import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import warnings
warnings.filterwarnings('ignore')

from hospital_tools import search_hospital_information

print(f'Tool type: {type(search_hospital_information).__name__}')
print(f'Has invoke: {hasattr(search_hospital_information, "invoke")}')
print(f'Has name: {hasattr(search_hospital_information, "name")}')
if hasattr(search_hospital_information, "name"):
    print(f'Tool name: {search_hospital_information.name}')

try:
    print("\nTesting tool invocation...")
    result = search_hospital_information.invoke({'query': 'What services does the hospital provide?'})
    print(f'SUCCESS: Got {len(result)} characters')
    print(f'\nResult:\n{result}')
except Exception as e:
    print(f'ERROR: {str(e)}')
    import traceback
    traceback.print_exc()
