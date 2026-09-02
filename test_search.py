from hospital_tools import search_hospital_information

print('Running hospital search test...')
try:
    result = search_hospital_information.invoke({"query": "What are the payment methods?"})
    print('Search result:')
    print(result)
except Exception as e:
    print('ERROR during search:', e)
