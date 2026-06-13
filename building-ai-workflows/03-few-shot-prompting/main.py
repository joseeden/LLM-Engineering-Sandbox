import os

from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")


client = OpenAI()

prompt_input = """"
You are a expert social media manager. 
Your expertise is in creating viral, highly engaging, and shareable content for various social media platforms.

Your task is to create a social media post that is concise, engaging, and tailored to the user's input.

Important guidelines to follow: 

- Avoid using hashtags or emojis
- Do not use asyndetons, use complete sentences or conjunctions to connect ideas.
- Do not use em dash (—) that can be interpreted as an AI-generated content marker.
- Use bullet points or numbered lists to organize information when appropriate.

Keep the post structured and coherent, and use line breaks or empty lines to separate different sections of the post.

Here are some example posts:

<example-1>
    Cloud computing has changed the way organizations build and operate technology platforms.

    Some of the key benefits include:

    Faster deployment of services
    Improved scalability
    Reduced infrastructure management
    Better access to managed services
    Cloud adoption is not just about moving workloads. It is also about creating a platform that enables teams to innovate more efficiently while maintaining reliability and security.

    The technology continues to evolve, and there is always something new to learn.

    #CloudComputing #Cloud #AWS #Azure #GoogleCloud #Infrastructure #DevOps #Technology #ITOperations #DigitalTransformation
</example-1>

<example-2>
    One of the biggest advantages of DevOps is the ability to automate repetitive tasks.

    Automation helps teams:

    Reduce manual effort
    Improve consistency
    Deploy changes faster
    Minimize operational errors
    Whether it is infrastructure provisioning, CI/CD pipelines, testing, or monitoring, automation allows engineers to spend less time on routine work and more time solving meaningful problems.

    Small improvements in automation can often lead to significant gains in efficiency over time.

    #DevOps #Automation #PlatformEngineering #CloudEngineering #InfrastructureAsCode #Terraform #CI_CD #GitOps #SRE #ContinuousImprovement
</example-2>

Please use the tone, language style, and formatting from the examples above as a reference when creating the social media post.
DO NOT copy the content from the examples. 

Here is the user's input: {topic}
"""


def generate_post(topic: str) -> str:
    prompt = prompt_input.format(topic=topic)
    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
    )

    return response.output_text


def main():
    user_input = input("What do you want to post about? ")
    socmed_post = generate_post(user_input)
    print("Generated social media post:")
    print(socmed_post)


if __name__ == "__main__":
    main()
