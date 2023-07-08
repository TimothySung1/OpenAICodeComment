import openai
import time

openai.api_key = "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"

WAIT_TIME = 60 # wait time per request in seconds (3 reqs / min is fastest)

request_times = []

# create individual requests for methods
def get_function_docstrings(function_code):
    # print("get_function_docstrings()")
    # check if 3 requests made
    if len(request_times) == 3:
        # wait for WAIT_TIME seconds after the first request was made
        while time.time() < request_times[0] + WAIT_TIME:
            time.sleep(1)
        
        # remove first request from request_times, add current time
        request_times.pop(0)

    request_times.append(int(time.time()))
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": '''Output format: 
"""[Summary]

:param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
:type [ParamName]: [ParamType](, optional)
...
:raises [ErrorType]: [ErrorDescription]
...
:return: [ReturnDescription]
:rtype: [ReturnType]
"""
'''},
            {"role": "user", "content": "Only output python docstrings for the following function.\n" + function_code}
        ]
    )

    response = completion["choices"][0]["message"]["content"]
    # print(response)
    return response
