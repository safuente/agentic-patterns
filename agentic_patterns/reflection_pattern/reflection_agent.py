from groq import Groq
from agentic_patterns.utils.completions import ChatHistory, build_prompt, create_completion
from dotenv import load_dotenv
load_dotenv()


BASE_GENERATION_SYSTEM_PROMPT = """
Your task is to try to generate better quality code following PEP8 standards and best practices in Python Language.
If the user provides critique, respond with a revised version of your previous attempt.
You must always output the revised content.
"""

BASE_REFLECTION_SYSTEM_PROMPT = """
You are a world-class senior Python developer and code reviewer with deep expertise in writing production-grade code.

Your task is to critically evaluate the Python code provided by the assistant. Consider the following aspects:

1. Correctness and logic
2. Code clarity and readability (code user-friendly)
3. Adherence to PEP8 standards
4. Efficient and pythonic use of language features
If the code is correct and no improvements are needed, respond with: `<OK>`.
Always be precise and avoid a big list of suggestions.
"""



class ReflectionAgent:
    """
    A class that implements a Reflection Agent, which generates responses and reflects
    on them using the LLM to iteratively improve the interaction. The agent first generates
    responses based on provided prompts and then try to improve them in a reflection step.

    Attributes:
        model (str): The model name used for generating and reflecting on responses.
        client (Groq): An instance of the Groq client to interact with the language model.
    """

    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        self.client = Groq()
        self.model = model

    def _request_completion(self, messages: list[dict]) -> str:
        """
        Sends a list of messages to the specified model using the Groq client and returns the generated response.

        Args:
            messages (list[dict]): A list of message objects representing the conversation history to send to the model.
        """
        response = create_completion(self.client, messages, self.model)
        return response
    
    def generate_response(self, generation_messages_history: list[dict] ) -> str:
        """
        Generates a response using the specified model and returns the generated response.

        Args:
            generation_messages_history (list[dict]): A list of message objects representing the conversation history to send to the model.
        """
        return self._request_completion(generation_messages_history)
    
    def reflect_response(self, reflection_messages_history: list[dict] ) -> str:
        """
        Reflects on a response using the specified model and returns the reflected response.
        """
        return self._request_completion(reflection_messages_history)
    
    def run(self, user_msg: str, generation_system_prompt: str = "", reflection_system_prompt: str="", n_iterations: int = 10) -> str:
        """
        Runs the reflection agent for a given number of iterations.
        """
        generation_system_prompt += BASE_GENERATION_SYSTEM_PROMPT
        reflection_system_prompt += BASE_REFLECTION_SYSTEM_PROMPT

        generation_history = ChatHistory(
            [
                build_prompt(content=generation_system_prompt, role="system"),
                build_prompt(content=user_msg, role="user"),
            ],
            total_length=3, fixed_first=True
        )


        reflection_history = ChatHistory(
            [build_prompt(content=reflection_system_prompt, role="system")],
            total_length=3, fixed_first=True
        )

        for step in range(n_iterations):


            # Generate the response
            generation = self.generate_response(generation_history)
            generation_history.update_chat_history(generation, "assistant")
            reflection_history.update_chat_history(generation, "user")

            # Reflect and critique the generation
            critique = self.reflect_response(reflection_history)
            print(critique)

            if "<OK>" in critique:
                # If no additional suggestions are made, stop the loop
                print(
                    f"\n\nStop Sequence found. Stopping the reflection loop with {step + 1 } iterations... \n\n",
                )
                break

            generation_history.update_chat_history(critique, "user")
            reflection_history.update_chat_history(critique, "assistant")

        return generation



agent = ReflectionAgent()
output = agent.run(
    user_msg="Write a function that iterates over a list of 100000 numbers and returns the sum of the numbers.",
    n_iterations=3,
)
print(output)
    

    
    
