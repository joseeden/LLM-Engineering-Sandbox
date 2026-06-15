
# WhatsApp Integration for AI Workflows

## Overview

This project extends the [AI Content Publishing Workflow](https://github.com/joseeden/llm-engineering-sandbox/blob/master/building-ai-workflows/10-ai-content-publishing-pipeline/README.md) by adding WhatsApp notifications.

The original workflow generates:

- A blog post
- A thumbnail image
- A LinkedIn post

This version performs the same AI content workflow and then sends a WhatsApp message when the workflow completes.

The WhatsApp message contains a summary of the generated outputs, which makes it easier to monitor workflow execution from a mobile device.

This project uses the [Meta WhatsApp Cloud API.](https://developers.facebook.com/documentation/business-messaging/whatsapp/get-started)

## Scope

This project demonstrates how to send WhatsApp notifications from an AI workflow using the WhatsApp Cloud API.

Included:

- WhatsApp Cloud API setup
- Sending WhatsApp messages from Python
- Workflow completion notifications
- Custom text message examples

Not Included:

- Receiving WhatsApp messages
- Triggering workflows from WhatsApp
- Human-in-the-loop approvals
- Interactive buttons
- Webhook processing
- Production message templates
- Production WhatsApp Business setup

Some topics are intentionally excluded to keep the example focused on outbound workflow notifications.

## Workflow

The workflow processes content in multiple steps.

1. Load a blog post outline
2. Load example blog posts
3. Generate a blog post using an LLM
4. Evaluate the generated article
5. Improve the article if needed
6. Generate a thumbnail image
7. Generate a LinkedIn post
8. Save all outputs to local files
9. Send a WhatsApp notification

Each step has a single responsibility, which makes the workflow easier to understand and maintain.

<!-- ## Architecture

```text
Outline
    │
    ▼
Generate Blog Post
    │
    ▼
Evaluate Article
    │
    ▼
Improve Article
    │
    ▼
Generate Thumbnail
    │
    ▼
Generate LinkedIn Post
    │
    ▼
Save Outputs
    │
    ▼
Send WhatsApp Notification
``` -->

## Project Structure

```text
whatsapp-integration-for-ai-workflows/
│
├── linkedin-post-examples
│   ├── cloud-computing.txt
│   └── devops.txt
│
├── outlines
│   ├── outline-cloud-computing.txt
│   ├── outline-marathon.txt
│   └── outline-ruby.txt
│
├── posts-examples
│   ├── cybersecurity-basics.mdx
│   ├── iot-edge-monitoring.md
│   └── running-consistency.mdx
│
├── prompts
│   ├── article_developer_prompt.txt
│   ├── article_improvement_prompt.txt
│   ├── article_user_prompt.txt
│   ├── evaluation_developer_prompt.txt
│   ├── evaluation_user_prompt.txt
│   ├── linkedin_developer_prompt.txt
│   ├── linkedin_user_prompt.txt
│   └── thumbnail_prompt.txt
│
├── posts-to-publish/
├── thumbnails/
├── linkedin-posts/
│
├── test-whatsapp-template.py
├── test-whatsapp-text.py
│
├── pyproject.toml
├── main.py
└── README.md
```

## Important Notes

### WhatsApp Restrictions

WhatsApp integration is more strict than Slack.

Slack webhooks can usually send any message immediately.

WhatsApp has more rules because it is a messaging platform tied to real phone numbers.

For testing, Meta provides:

- A temporary access token
- A test WhatsApp business phone number
- A phone number ID
- A way to add your own WhatsApp number as a test recipient

For production, you usually need:

- A Meta Business account
- A WhatsApp Business Account
- A real business phone number
- A permanent access token
- Approved message templates for business-initiated messages

### Costs Considerations

The WhatsApp Cloud API can be **tested for free** using Meta's developer setup.

However, production WhatsApp Business Platform messages are billed per delivered message.

Pricing depends on:

- Recipient country
- Message category
- Whether the message is marketing, utility, authentication, or service

For this project, use the free developer test setup first.

## Prerequisites

WhatsApp setup:

- [A Meta account](https://developers.meta.com/horizon/sign-up/)
- [A WhatsApp account on your personal phone](https://faq.whatsapp.com/441163784889902)
<!-- - A test recipient phone number -->

Environment setup: 

- [Python 3.11+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [An OpenAI account](https://platform.openai.com/login)
- [OpenAI API credentials](https://platform.openai.com/account/api-keys)

## WhatsApp Cloud API Setup

1. Create or Sign In to a Meta Account

    Go to:

    ```text
    https://developers.facebook.com/
    ```

    Sign in using your Facebook or Meta account.

    If you do not have one, create a Meta account first.

2. Go to Meta Developer Apps

    ```text
    https://developers.facebook.com/apps/
    ```

    Click **Create App**

    <div class='img-center'>

    ![](/img/docs/Screenshot2026-06-15093538.png)

    </div>

3. Create a Meta App

    Provide an app name and contact email.

    ```text
    Testing - AI Content Workflow
    ```

    Click **Next.**

    <div class='img-center'>

    ![](/img/docs/Screenshot2026-06-15093816.png)

    </div>

    Choose the use case that supports business messaging, then click **Next.**

    <div class='img-center'>

    ![](/img/docs/Screenshot2026-06-15095433.png)

    </div>

4. Create a business portfolio 

    You may get asked for a business portfolio. You can choose an existing one or create a new one. In my case, I just created a new one.

    <div class='img-center'>

    ![](/img/docs/Screenshot2026-06-15095356.png)

    </div>

    If you created a new business portfolio, you will need to provide the following:

    - Business portfolioname
    - First name
    - Last name
    - Business email

    After that, you might get asked to perform some verifications, such as:

    **Edit:** These are optional. You can usually skip them for testing purposes.

    - Adding trusted domains 
    - Removing users without passkeys

5. Select the business portfolio 

    Back in the app creation flow, select the business portfolio you just created. 

    <div class='img-center'>

    ![](/img/docs/Screenshot2026-06-15095316.png)

    </div>

6. Review the App and Create it. 

    You can skip the **Requirements** section for now.

    Review the app details and click **Create App.**


7. Add WhatsApp to the Meta App

    Inside the Meta app dashboard, click **Customize the Connect...**:

    <div class='img-center'>

    ![](/img/docs/Screenshot2026-06-15100621.png)

    </div>

    Confirm the business portfolio if asked, then **Continue.**

    You should now see a WhatsApp Business Platform banner in the app dashboard.

    <div class='img-center'>

    ![](/img/docs/Screenshot2026-06-15100844.png)

    </div>


8. Open WhatsApp API Setup

    In the left sidebar, go to **API Setup**

    This page contains the important test credentials.

    You should see:

    - Phone number ID
    - WhatsApp Business Account ID
    - Test phone number

    <div class='img-center'>

    ![](/img/docs/Screenshot2026-06-15101333.png)

    </div>


9. Generate the Access Token

    > You may be prompted to choose the WhatrsApp account you want the Meta app to have access to. Choose the account you just created.

    Create the temporary token and copy it.

    This will be useful later for sending the test message (and actual message for the script)

10. Add Your Personal WhatsApp Number as a Test Recipient

    > If you haven't done yet, [register a WhatsApp account](https://faq.whatsapp.com/441163784889902) on your personal phone.

    In the API Setup page,  add your personal WhatsApp number as a test recipient.

    - Use international format without the plus sign.

    - Meta will send a verification code to your WhatsApp.

    - Enter the verification code in the Meta Developer Portal.

    After this, your number becomes an allowed test recipient.

    <div class='img-center'>

    ![](/img/docs/Screenshot2026-06-15101653.png)

    </div>


11. Send Meta's Built-In Test Message

    Before writing any Python code, test using Meta's built-in form.

    In step 2, click **Send message**.

    - You should receive a WhatsApp message from the Meta test business number.

    - Do not continue until this works.

    **EDIT:** The bearer token should be automatically filled in if you generated the token in the previous step. If not, copy the temporary access token and paste it in the form.

    <div class='img-center'>

    ![](/img/docs/Screenshot2026-06-15101853.png)

    </div>

12. Confirm the WhatsApp message is received

    Check your WhatsApp.

    You should receive a message similar to:

    ```text
    Hello world! Welcome and Congratulations...
    ```


13. Copy the Required WhatsApp Values

    From the WhatsApp API Setup page, copy these values:

    - Temporary access token
    - Phone number ID
    - Recipient phone number

    You will use these later in `.env`.

## Environment Setup

1. Clone the repository

    ```bash
    git clone https://github.com/joseeden/llm-engineering-sandbox

    cd project-llm-engineering-sandbox/building-ai-workflows/21-whatsapp-integration-for-ai-workflows
    ```

2. Copy the environment file

    Create a `.env` file from the provided example:

    ```bash
    cp .env.example .env
    ```

3. Configure environment variables

    Open `.env` and update the values.

    **NOTE:** NEVER commit your real API keys to source control.

    ```env
    OPENAI_API_KEY=your_openai_key_here
    OPENAI_BASE_URL="https://api.openai.com/v1"

    MODEL_NAME=gpt-4.1-mini
    IMAGE_MODEL_NAME=gpt-image-1

    # WhatsApp Integration Configuration
    WHATSAPP_ACCESS_TOKEN="your_meta_access_token_here"
    WHATSAPP_PHONE_NUMBER_ID="your_phone_number_id_here"
    WHATSAPP_TO_NUMBER="your_recipient_number_here"
    WHATSAPP_API_VERSION="v25.0"
    ```

    Do not include the `+` symbol in the phone number. Use the international format without the plus sign.

    Example:

    ```env
    WHATSAPP_TO_NUMBER=6591234567
    ```

    **Note 1:** The OpenAI SDK automatically appends the correct endpoint paths based on the method being called, so the base URL should just be this.

    **Note 2:** You can use other models that support image generation,such as `gpt-4.1` or `gpt-5-nano`, but `gpt-4.1-mini` is a good option for testing since it is cheaper and still supports image generation. 

    See [Pricing: Image generation models](https://developers.openai.com/api/docs/pricing?tab=models#image-tokens) 

4. Install UV 

    Linux / macOS

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    Verify installation:

    ```bash
    uv --version
    ```


5. Install Dependencies

    From the project directory, run:

    ```bash
    uv sync
    ```

    This will:

    1. Create a virtual environment if needed
    2. Install all project dependencies
    3. Use the versions locked in `uv.lock`


### Image Generation Requirements

The thumbnail generation step uses OpenAI's image generation API.

To use image generation models such as `gpt-image-1`, your OpenAI organization must be verified.

Without verification, image generation requests may fail even if text generation works correctly.

Before running the thumbnail generation step:

1. Open the OpenAI Platform
2. Navigate to Organization Settings
3. Complete the verification process
4. Confirm that image generation is enabled for your account

<div class='img-center'>

![](/img/docs/Screenshot2026-06-15004842.png)

</div>


### Prompts

The workflow stores prompts in the `prompts/` directory.

The prompts define the behavior for each AI step:

- Article generation
- Article evaluation
- Article improvement
- Thumbnail generation
- LinkedIn post generation

The prompts are externalized to keep the Python code clean and make prompt changes easier to manage.

```bash
├── prompts
│   ├── article_developer_prompt.txt
│   ├── article_improvement_prompt.txt
│   ├── article_user_prompt.txt
│   ├── evaluation_developer_prompt.txt
│   ├── evaluation_user_prompt.txt
│   ├── linkedin_developer_prompt.txt
│   ├── linkedin_user_prompt.txt
│   └── thumbnail_prompt.txt
```

### Example Posts

The `posts-examples/` directory contains previous blog posts.

These are used as writing style references for the article generation and improvement steps.

The model should follow the tone, structure, and formatting style of the examples, but it should not copy their content.

```bash
├── posts-examples
│   ├── cybersecurity-basics.mdx
│   ├── iot-edge-monitoring.md
│   └── running-consistency.mdx 
```

### LinkedIn Post Examples

The `linkedin-post-examples/` directory contains sample LinkedIn posts.

These examples help the model generate a LinkedIn post in a similar writing style.

```bash
├── linkedin-post-examples
│   ├── cloud-computing.txt
│   └── devops.txt
```

### Outlines 

The `outlines/` directory contains blog post outlines. 

These are basically the "topics" that you want to generate content for. 

Currently the workflow takes a single outline as input, but you could modify it to process multiple outlines in a batch if you want.

You can use the sample outlines, but you can also create your own.

```bash
outlines/
├── outline-cloud-computing.txt
├── outline-marathon.txt
└── outline-ruby.txt
```

### Outputs

The workflow saves generated outputs into separate folders.

```text
posts-to-publish/

thumbnails/

linkedin-posts/
```

The blog post is saved as Markdown.

The thumbnail is saved as a JPEG image.

The LinkedIn post is saved as a text file.


## Test WhatsApp Using a Template Message

Before adding the workflow, create a `test-whatsapp-template.py` file to test the WhatsApp integration separately.

```bash
uv run python test-whatsapp-template.py
```

Expected result:

```text
WhatsApp template message sent successfully.
```

You should receive a WhatsApp message using Meta's default `hello_world` template.

**Note:** You can send custom text messages for testing, but you usually need to message the Meta test business number first to open a 24-hour service window. For production, you need approved message templates. 

Meta says Cloud API errors can be synchronous in the API response or asynchronous through webhooks, so delivery problems may not always appear in the immediate API response. See [Error codes.](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes?utm_source=chatgpt.com)

## Test WhatsApp Using a Custom Text Message

<!-- ## Open a 24-Hour Customer Service Window -->

To send custom text messages, send a message from your personal WhatsApp account to the Meta test business number first.

Example message:

```text
Hello
```

This opens a customer service window.

After that, your app can send free-form text messages to your WhatsApp number for testing.

To test this, run the `test-whatsapp-custom-text.py` script:

```bash
uv run python test-whatsapp-custom-text.py
```

Expected result:

```text
Sending message: Hello there from the other side! I was triggered from the test script

WhatsApp text message sent successfully.
```

You should receive:

```text
Hello there from the other side! I was triggered from the test script
```

**EDIT:** You can also pass the message during execution:

```bash
uv run python test-whatsapp-custom-text.py --message "Hello again. I was sent from the terminal this time!"
```




## Run the Application

Run the full workflow:

```bash
uv run python main.py outlines/outline-ruby.txt
```

(You can choose the other available outlines, or you can create your own.)

## Skipping Steps 

**Run Without Thumbnail:** Image generation costs money and may require account verification. To skip thumbnail generation:

```bash
uv run python main.py outlines/outline-ruby.txt --skip-thumbnail
```

To skip LinkedIn post generation:

```bash
uv run python main.py outlines/outline-ruby.txt --skip-linkedin
```

To skip WhatsApp notification: 

```bash
uv run python main.py outlines/outline-ruby.txt --skip-whatsapp
```

To skip both thumbnail and LinkedIn post generation:

```bash
uv run python main.py outlines/outline-ruby.txt --skip-thumbnail --skip-linkedin
```

## Validation

After running the workflow, verify the local output folders.

Example:

```text
linkedin-posts/
└── 15062026-why-ruby-remains-a-great-language-for-learning-software-development-01.txt

posts-to-publish/
└── 15062026-why-ruby-remains-a-great-language-for-learning-software-development-01.md

thumbnails
└── 15062026-why-ruby-remains-a-great-language-for-learning-software-development-01.jpeg

```

Then check WhatsApp.

You should receive a message similar to:

```text
AI content workflow completed.

Title: Why Running Local AI Models Is Useful for Developers
Needs improvement: False
Feedback: The article is clear and complete.

Article: 15062026-why-running-local-ai-models-is-useful-for-developers-01.md
Thumbnail: 15062026-why-running-local-ai-models-is-useful-for-developers-01.jpeg
LinkedIn post: 15062026-why-running-local-ai-models-is-useful-for-developers-01.txt
```

If the files are generated and the WhatsApp message appears, the integration is working correctly.

## Common Issues

### Error: Missing Environment Variables

If you see:

```text
Missing required environment variables
```

Check your `.env` file.

Make sure these values are present:

```env
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=
WHATSAPP_TO_NUMBER=
```

### Error: Access Token Expired

The temporary access token from Meta expires.

Go back to Meta Developer Portal ➜ Your App ➜ WhatsApp ➜ API Setup

Copy a new temporary access token.

For long-term use, create a permanent access token using a Meta system user.

### Error: Recipient Not Allowed

For test mode, your recipient number must be added and verified in the WhatsApp API Setup page.

Add your WhatsApp number again and complete the verification step.

### Error: Cannot Send Custom Text Message

Send a message from your personal WhatsApp account to the Meta test business number first.

Example:

```text
Hello
```

Then run the text message test again.

### Error: Image Generation Failed

Thumbnail generation requires OpenAI image generation access.

Run without thumbnail:

```bash
uv run python main.py outlines/sample-outline.txt --skip-thumbnail
```

## Production Notes

For production usage, do not rely on the temporary access token.

Use:

- A Meta Business account
- A WhatsApp Business Account
- A real business phone number
- A permanent access token
- Approved message templates

For workflow notifications, the best production approach is usually a WhatsApp utility template.

Example template idea:

```text
Your AI workflow has completed.

Title: {{1}}
Article: {{2}}
LinkedIn post: {{3}}
```

This allows your application to send workflow notifications even when the user has not recently messaged the WhatsApp business number.

