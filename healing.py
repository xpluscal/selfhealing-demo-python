from langchain.docstore.document import Document
from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import LLMChain
import os

import sys
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    PromptTemplate
)
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)

def main(build_output_file):
    with open(build_output_file, "r") as f:
        build_output = f.read()

    # Process the build_output as needed
    print(build_output)

    text = build_output

    human_message_prompt = HumanMessagePromptTemplate(
        prompt=PromptTemplate(
            template="Can you find the filename where this error comes from: {error}?  If you do, please reply with the filename only, if not please reply with no.",
            input_variables=["error"],
        )
    )

    chat_prompt_template = ChatPromptTemplate.from_messages([human_message_prompt])
    chat = ChatOpenAI(temperature=0)
    chain = LLMChain(llm=chat, prompt=chat_prompt_template)
    filename = chain.run(build_output);

    if filename == "no":
        print("No filename found")
        return
    
    print("Filename found: " + filename)

    # Read file
    with open(filename, "r") as f:
        file_text = f.read()

    # Process the file_text as needed
    print(file_text)

    human_message_prompt = HumanMessagePromptTemplate(
        prompt=PromptTemplate(
            template="The following file: {file} produces the following error: {error}. You're response can only include the fixed code or 'no' if you cannot fix the code.",
            input_variables=["file", "error"],
        )
    )

    chat_prompt_template = ChatPromptTemplate.from_messages([human_message_prompt])
    chat = ChatOpenAI(temperature=0)
    chain = LLMChain(llm=chat, prompt=chat_prompt_template)
    fixed_code = chain.run({'file':file_text, 'error': build_output});

    if fixed_code == "no":
        print("No fix found")
        return
    
    # Process the fixed_code as needed
    # detect ``` as end and start and get whats between
    print("Fix found: " + fixed_code)

    # Write file
    # with open(filename, "w") as f:
    #     f.write(fixed_code)


if __name__ == "__main__":
    build_output_file = sys.argv[1]
    main(build_output_file)