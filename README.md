# MedAgent: Dr. Adrin Virtual Assistant

Welcome to the Dr. Adrin Virtual Assistant project! This repository contains the code and resources needed to set up and run a virtual assistant designed to assist doctors by managing patient interactions, providing emergency guidance, and handling various administrative tasks.

## Table of Contents

- [Project Overview](#project-overview)
- [Setup Instructions](#setup-instructions)
- [How It Works](#how-it-works)
- [Requirements](#requirements)
- [Running the Project](#running-the-project)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The Dr. Adrin Virtual Assistant is an AI-powered assistant tailored for healthcare professionals. It efficiently manages patient communications, assesses emergencies, and offers immediate assistance. The assistant leverages advanced natural language processing (NLP) techniques, utilizing tools like LangChain and Qdrant for intelligent interaction and quick information retrieval.

## Setup Instructions

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.10 or higher
- Git

### Cloning the Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/inamdarmihir/dr_adrin_virtual_assistant.git
cd dr_adrin_virtual_assistant
```

### Installing Dependencies

To install the required Python packages, run the following command:

```bash
pip install -r requirements.txt
```

This command will install all the necessary dependencies listed in the `requirements.txt` file.

## How It Works

The virtual assistant is built to handle a wide range of scenarios that doctors encounter daily. It is designed with the following core functionalities:

- **Emergency Detection**: The assistant can detect emergency situations based on patient inputs and provide appropriate next steps.
- **Information Retrieval**: It uses a vector database to quickly retrieve and provide relevant medical information.
- **Location Handling**: The assistant can manage user location data to offer accurate directions and estimated arrival times.
- **Patient Interaction**: It interacts with patients to confirm emergencies, leave messages, or provide further assistance based on the user's needs.

The system is designed for robustness, with capabilities to handle various edge cases and concurrent user interactions through asynchronous programming.

## Requirements

The project relies on several key Python packages:

- `langchain==0.0.316`
- `langchain-community==0.0.8`
- `langchain_openai`
- `langchain_core`
- `google-search-results==2.4.2`
- `qdrant_client`

These dependencies ensure that the virtual assistant can handle complex tasks efficiently.

## Running the Project

Once the dependencies are installed, you can start the virtual assistant by running the Jupyter notebook provided in the repository. Follow these steps:

1. Launch Jupyter Notebook in your terminal:

   ```bash
   jupyter notebook
   ```

2. Open the `Untitled30.ipynb` notebook.
3. Follow the instructions in the notebook to start the assistant.

## Troubleshooting

If you encounter any issues while setting up or running the project, consider the following steps:

- **Dependency Issues**: Ensure all required packages are installed correctly by reviewing the `requirements.txt` file.
- **Python Version**: Make sure you are using Python 3.10 or higher.
- **Runtime Errors**: Check the Jupyter notebook for any specific error messages and follow the suggestions provided.

For further assistance, feel free to open an issue on the GitHub repository.

## Contributing

Contributions to the Dr. Adrin Virtual Assistant project are welcome! If you have any improvements or suggestions, please submit a pull request or open an issue on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Thank you for using the Dr. Adrin Virtual Assistant! We hope it enhances your workflow and improves patient care.
