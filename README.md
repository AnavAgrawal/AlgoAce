<!-- PROJECT LOGO -->
<br />
<div align="center">
  
<img src="https://th.bing.com/th/id/OIG3.4KSN22kFFkbCFQZm_C8y?w=1024&h=1024&rs=1&pid=ImgDetMain" width="150" />


  <h3 align="center">AlgoAce - The Competitive Programming Buddy</h3>

  <p align="center">
    An awesome LLM plugin for 
    <br />
    <a href="https://go.wetransfer.com/t-Ya9A1bGN37">View Demo</a>
    ·
    <a href="https://github.com/leabuende/mike-llm-slack-plugin/issues">Report Bug</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project is a Project management assistant, using Pathways LLM App to assess a Trello board's data in real time to answer questions and assist in task management.
Look at a few features we have incorporated now : 
[Mike Slack App Demo](https://youtu.be/Z0ckF6-YRYY)

<div align="center">
<img src="demo.gif" width="80%" />
</div>


### Built With

This project has been built in the context of Pathway's LLM Bootcamp. Big kudo's to them for their amazing course !
Here are all the tools I used :

* [Codeforces API](https://api.slack.com/)
* [Flask](https://flask.palletsprojects.com/en/3.0.x/)
* [Ngrok](https://ngrok.com/)
* [Pathway's LLM App](https://pathway.com/developers/showcases/llm-app-pathway)


<!-- GETTING STARTED -->

## Installation

### A. Run with Docker

### Prerequisites

Ensure you have Docker and docker compose both latest version installed on your system before proceeding. Docker compose  will be used to build and run the application in a containerized environment. For installation please refer the offcial documneation of docker [Docker Installation Guide](https://docs.docker.com/compose/install/linux/)

- **OpenAI API Key**:
    - Create an [OpenAI](https://openai.com/) account and generate a new API Key: 
    - To access the OpenAI API, you will need to create an API Key. You can do this by logging into the [OpenAI] (https://openai.com/product) website and navigating to the API Key management page.


### 1. Environment Setup

1. Create a `.env` file in the root directory of your project.
2. Add the following lines to the `.env` file, replacing `{YOUR_OPENAI_KEY}` with your actual OpenAI API key:

   ```env
    OPENAI_API_TOKEN={YOUR_OPENAI_KEY}
    HOST=0.0.0.0
    PORT=8080
    EMBEDDER_LOCATOR=text-embedding-ada-002
    EMBEDDING_DIMENSION=1536
    MODEL_LOCATOR=gpt-3.5-turbo
    MAX_TOKENS=400
    TEMPERATURE=0.2
   ```

This file will be used by Docker to set the environment variables inside the container.

### 2. Build and Run the Docker Image

With the environment variables set up, you can now build the Docker and run the image for the project.

- Open a terminal or command prompt.
- Navigate to the root directory of your project.
- Execute the following command to build and run the docker:

  ```sh
  docker compose up
  ```

This step compiles your application and its dependencies into a Docker image.


### 3. Access the Application

- Open your web browser.
- Navigate to `localhost:8501` to access the application.

You should see the application's interface if the setup was successful. This confirms that your Docker container is running and the application is accessible.

### 4. Troubleshooting

If you encounter any issues during the setup or execution process, please check the following:

- Ensure Docker is running on your system.
- Verify that the `.env` file contains the correct API key and settings.
- Make sure the Docker image was built successfully without errors.
- Check if the Docker container is running and the ports are correctly mapped.

For further assistance, consult the Docker documentation or seek help from Docker community forums.

### B. Run with Conda

### Prerequisites

Ensure you have Conda installed on your system before proceeding. Conda will be used to create an environment and run the application with all the required dependencies. If you don't have Conda installed, please follow the official [Conda Installation Guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

### Setting Up the Environment

1. Clone the project repository to your local machine.
    ```
    git clone https://github.com/AnavAgrawal/AlgoAce
    ```
2. Navigate to the project directory.
    ```
    cd AlgoAce
    ```

3. Set environment variables

    Create .env file in the root directory of the project, copy and paste the below config, and replace the {YOUR_OPENAI_KEY} configuration value with your key.

    ```env
    OPENAI_API_TOKEN={YOUR_OPENAI_KEY}
    HOST=0.0.0.0
    PORT=8080
    EMBEDDER_LOCATOR=text-embedding-ada-002
    EMBEDDING_DIMENSION=1536
    MODEL_LOCATOR=gpt-3.5-turbo
    MAX_TOKENS=400
    TEMPERATURE=0.2
   ```

4. Create a new Conda environment with the required dependencies:

    ```bash
    conda create --name myenv
    ```


5. Install dependencies
   ```
   pip install -r requirements.txt
   ```

6. Activate the newly created Conda environment:

    ```bash
    conda activate myenv
    ```
7. Run the supervisord command to start all the processes:

    ```bash
    supervisord
    ```
    - This starts the Backend Server, the Cronjob and the Streamlit UI Interface. 

8. Navigate to `localhost:8501` to access the Streamlit UI Inteface and use the application.


<!-- USAGE -->

## Usage

- **Select Learning Level:** Users can choose their learning level (Novice, Skilled, Expert) to customize the complexity of the content provided by AURA. This ensures that the learning experience is tailored to the user's current knowledge and skills. We can provide context to.
 - <img src="./assets/demo-2.gif" alt="demo 2" />

 - <img src="./assets/demo-3.gif" alt="demo 3" />
                
- **Upload Documents for In-depth Exploration:** Users have the option to upload PDFs or documents to AURA. This enhances its knowledge base, allowing AURA to draw from a broader range of resources when answering queries or providing educational content.

- **Engage with Queries:** Submit queries to AURA and receive personalized responses. AURA's AI-driven engine analyzes your questions to deliver precise and customized educational content, facilitating a more engaging learning experience.

- **Two Modes of Interaction:** 

    - **Basic Mode:** Offers quick answers and summaries for general queries, suitable for users seeking fast insights.
        

    - **Deep Dive Mode:** Provides detailed explanations and resources, ideal for users looking for an in-depth understanding of a topic.
- <img src="./assets/demo-4.gif" alt="demo 4" />

- **News API:** AURA calls the news API every 5 minutes of each hour using scheduler to update its knowledge base with the latest information and developments. This ensures that the educational content provided is current and relevant. You can refer to the code for more clarification
    ```bash
        ./aura/utils/news_api_connector.py
    ```

- **Enhancing AURA's Learning in Research:** Users can manually call the arXiv API to provide AURA with the latest research papers and articles. Files uploaded this way are automatically ingested into AURA's data pipeline, enriching its resource pool for advanced topics. Future updates to AURA will include automation of API calls for even greater ease of use. Example usage
    ```bash
        python ./utils/arxiv_connector.py  "deep learning"  --max_results 30




<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- CONTACT -->
## Contact

Anav Agrawal - anavagrawal2309@gmail.com




