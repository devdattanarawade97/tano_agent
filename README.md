

**Tano Swarm Agent**
================

**Table of Contents**
-----------------

1. [Introduction](#introduction)
2. [Setup](#setup)
3. [Running the Server](#running-the-server)
4. [Agents](#agents)
	* [Text Agent](#text-agent)
	* [Image Agent](#image-agent)
	* [Docs Agent](#docs-agent)
5. [API Documentation](#api-documentation)
	* [Introduction](#api-introduction)
	* [API Endpoints](#api-endpoints)
		+ [Text Agent](#text-agent-endpoint)
		+ [Image Agent](#image-agent-endpoint)
		+ [Docs Agent](#docs-agent-endpoint)
	* [API Parameters](#api-parameters)
	* [API Response Codes](#api-response-codes)
	* [API Authentication](#api-authentication)
	* [API Rate Limiting](#api-rate-limiting)

**Introduction**
---------------

This repository contains a chatbot agent system built with FastAPI and OpenAI's GPT-3. The system supports three types of agents: text, image, and docs.

**Setup**
--------

To run the code, you'll need to set up your environment. First, create a `.env` file in the root directory and add your OpenAI API key:

```bash
OPENAI_API_KEY=your_api_key
COHERE_API_KEY=your_cohere_api_key
GEMINI_API_KEY=your_gemini_api_key
```

Then, install the required dependencies:

```bash
pip install -r requirements.txt
```

**Running the Server**
---------------------

To run the server, use the following command:

```bash
uvicorn main:app --reload
```

This will start the server on `http://localhost:8000`.

**Agents**
---------

The system supports three types of agents: text, image, and docs. Each agent has its own endpoint for making queries.

### Text Agent

The text agent is the main agent for answering user queries. It can handle queries related to text, and if the user mentions 'gemini' or 'cohere', it will transfer the conversation to the Gemini Agent or Real Info Agent respectively.

#### Endpoint

To make a query to the text agent, send a POST request to `/text-query` with a JSON payload containing the user message:

```json
{
  "user_message": "your_message"
}
```

#### Example

To make a query to the text agent, send a POST request to `/text-query` with the following payload:

```json
{
  "user_message": "What is the capital of France?"
}
```

### Image Agent

The image agent is responsible for generating images based on user queries.

#### Endpoint

To make a query to the image agent, send a POST request to `/image-query` with a JSON payload containing the user message:

```json
{
  "user_message": "your_message"
}
```

#### Example

To make a query to the image agent, send a POST request to `/image-query` with the following payload:

```json
{
  "user_message": "Generate an image of a cat"
}
```

### Docs Agent

The docs agent is responsible for answering user queries based on relevant documents.

#### Endpoint

To make a query to the docs agent, send a POST request to `/docs-query` with a JSON payload containing the user query and relevant documents:

```json
{
  "user_query": "your_query",
  "relevant_docs": "your_docs"
}
```

#### Example

To make a query to the docs agent, send a POST request to `/docs-query` with the following payload:

```json
{
  "user_query": "What is the capital of France?",
  "relevant_docs": "The capital of France is Paris."
}
```

**API Documentation**
-------------------

### Introduction

This API documentation describes the endpoints and parameters for interacting with the tano_agent system. The system provides three types of agents: text, image, and docs, each with its own endpoint for making queries.

### API Endpoints

#### Text Agent

##### POST /text-query

* **Description**: Makes a query to the text agent.
* **Request Body**:
	+ `user_message` (string): The user's message or query.
* **Response**:
	+ `content` (string): The response from the text agent.
* **Example Request**:

```json
{
  "user_message": "What is the capital of France?"
}
```

* **Example Response**:

```json
{
  "content": "The capital of France is Paris."
}
```

#### Error Handling

* **400 Bad Request**: If the request body is missing or invalid.
* **500 Internal Server Error**: If there is an error



Here is the rest of the rewritten README.md file:

#### Image Agent

##### POST /image-query

* **Description**: Makes a query to the image agent.
* **Request Body**:
	+ `user_message` (string): The user's message or query.
* **Response**:
	+ `response` (string): The response from the image agent, including the generated image URL.
* **Example Request**:

```json
{
  "user_message": "Generate an image of a cat"
}
```

* **Example Response**:

```json
{
  "response": "https://example.com/image.jpg"
}
```

#### Error Handling

* **400 Bad Request**: If the request body is missing or invalid.
* **500 Internal Server Error**: If there is an error with the image agent.

#### Docs Agent

##### POST /docs-query

* **Description**: Makes a query to the docs agent.
* **Request Body**:
	+ `user_query` (string): The user's query.
	+ `relevant_docs` (string): The relevant documents for the query.
* **Response**:
	+ `content` (string): The response from the docs agent.
* **Example Request**:

```json
{
  "user_query": "What is the capital of France?",
  "relevant_docs": "The capital of France is Paris."
}
```

* **Example Response**:

```json
{
  "content": "The capital of France is Paris."
}
```

#### Error Handling

* **400 Bad Request**: If the request body is missing or invalid.
* **500 Internal Server Error**: If there is an error with the docs agent.

### API Parameters

* `user_message`: The user's message or query.
* `user_query`: The user's query.
* `relevant_docs`: The relevant documents for the query.

### API Response Codes

* **200 OK**: The request was successful.
* **400 Bad Request**: The request was invalid or missing required parameters.
* **500 Internal Server Error**: There was an error with the agent.

### API Authentication

* **None**: No authentication is required for this API.


### API Rate Limiting

* **None**: There is no rate limiting for this API.

