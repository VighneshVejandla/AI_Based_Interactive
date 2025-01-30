# backend/ai_analyzer.py

import openai  # Assuming you're using OpenAI's GPT model

class AIAnalyzer:
    def __init__(self, api_key):
        """
        Initialize the AI Analyzer with an API key for the language model.
        """
        openai.api_key = api_key

    def analyze_financial_data(self, financial_data, question):
        """
        Analyze financial data and answer a specific question using the AI model.
        
        :param financial_data: The financial data in text or structured format.
        :param question: The question to be answered.
        :return: The AI-generated answer.
        """
        try:
            # Combine the financial data and the question into a prompt
            prompt = f"Financial Data:\n{financial_data}\n\nQuestion: {question}\nAnswer:"
            
            # Call the OpenAI API to generate an answer
            response = openai.Completion.create(
                engine="text-davinci-003",  # Use an appropriate model
                prompt=prompt,
                max_tokens=150,  # Limit the response length
                temperature=0.7,  # Control the creativity of the response
            )
            
            # Extract and return the answer
            answer = response.choices[0].text.strip()
            return answer
        except Exception as e:
            print(f"Error in AI analysis: {e}")
            return None