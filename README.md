# Financial Assistant

## Description
A Streamlit-based AI financial assistant application that interacts with various APIs to provide financial data and insights.
Retrieves data from alphavantage API and can create dashboards and visualizations following user instructions.


## Features
- Chat-based interface for financial queries
- Integration with multiple APIs for financial data
- Real-time message streaming


## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/yourproject.git
    ```
2. Navigate to the project directory:
    ```sh
    cd yourproject
    ```
3. Create and activate a virtual environment:
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```
4. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```


## Configuration
1. Obtain the necessary API keys and fill in the `.env.example` file:
    ```shell
    ANTHROPIC_API_KEY='YOUR_API_KEY'
    LANGCHAIN_API_KEY="YOUR_API_KEY"
    ALPHAVANTAGE_API_KEY='YOUR_API_KEY'
    PYTHONPATH='YOUR_PROJECT_ROOT_FULL_PATH'
    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
    LANGCHAIN_PROJECT="fin_assistant"
    ```
2. Rename `.env.example` to `.env`:
    ```sh
    mv .env.example .env
    ```


## Usage
1. Start the Streamlit UI:
    ```sh
    streamlit run main.py
    ```

2. Interact with the financial assistant through the chat interface. After the query is completed you should see new dashboard appear in 'generated_analytics' page.


## Contributing
1. Fork the repository.
2. Create a new branch:
    ```sh
    git checkout -b feature/your-feature
    ```
3. Make your changes and commit them:
    ```sh
    git commit -m 'Add some feature'
    ```
4. Push to the branch:
    ```sh
    git push origin feature/your-feature
    ```
5. Open a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
