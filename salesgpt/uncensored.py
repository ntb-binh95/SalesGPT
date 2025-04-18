from openai import OpenAI
from salesgpt.prompts import SALES_UNCENSORED_PROMPTS, SALES_UNCENSORED_INSTRUCT_PROMPTS

class UncensoredLLM:
    def __init__(self):
        # init the client but point it to TGI
        self.client = OpenAI(
            base_url="http://localhost:8080/v1",
            api_key="-"
        )
    
    def chat(self, input_message):
        chat_completion = self.client.chat.completions.create(
            model="tgi",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. You talk in polite manner" },
                {"role": "user", "content": input_message}
            ],
            stream=False
        )
        # iterate and print stream
        return chat_completion.choices[0].message.content

    def adjust(self, ai_log):
        text = ai_log["output"]
        conversation_history = ai_log["conversation_history"]
        print(ai_log)
        system_prompt = SALES_UNCENSORED_PROMPTS.format(
            salesperson_name=ai_log["salesperson_name"],
            salesperson_role=ai_log["salesperson_role"],
            company_name=ai_log["company_name"],
            company_business=ai_log["company_business"],
            company_values=ai_log["company_values"],
            conversation_purpose=ai_log["conversation_purpose"],
            conversation_type="chat"
        )
        print("SYSTEM PROMPT: ", system_prompt)
        chat_completion = self.client.chat.completions.create(
            model="tgi",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": SALES_UNCENSORED_INSTRUCT_PROMPTS.format(conversation_history=conversation_history, text=text)}
            ],
            stream=False
        )
        # iterate and print stream
        response = chat_completion.choices[0].message.content
        if response[0] == "\"" and response[-1] == "\"":
            response = response[1:-1]
        ai_log["output"] = response
        return ai_log

if __name__ == "__main__":
    llm = UncensoredLLM()
    print(llm.chat("What is Deep Learning?"))