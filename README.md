# A CS2 demo (.dem) file manager for vod watchers

## Core app functions:
1. Lets user extract the contents of a zipped file and copy them directly to csgo folder
2. Lets user rename the .dem files before exporting them.
3. Lets user delete .dem files from the csgo folder.

## Prerequisites:

Get [Winrar](https://www.win-rar.com/start.html?&L=0)

## Installation:

- ### Development
    - **Clone the repository**:
        ```bash
        git clone git@github.com:garrythewarlord/IDTCopy.git
        ```

    - **Create a virtual environment**:
        - Navigate to the project root of the cloned repository and create the virtual environment:
        ```bash
        python3 -m venv venv
        ```

    - **Activate the virtual environment**:
        ```bash
        venv\Scripts\activate
        ```

    - **Install dependencies**:
        ```bash
        pip install -r requirements.txt
        ```
    
    - **Replace .env variables**:
        * Navigate to .env file
        * Replace CSGO_PATH and UNRAR_PATH with corresponding abs paths on your system:
        ```
        CSGO_PATH="C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo"
        UNRAR_PATH="C:\Program Files\WinRAR\UnRAR.exe"
        ```


    - **Run the application**:
        * Open `app.py` in VS Code and run the Python file.


- ### Run Executable
    - **Download the executable file**:
    [Link](https://github.com/garrythewarlord/IDTCopy/releases/tag/v1.0)

    - **Set up environmental variables**
        * Create a file extension .env inside the folder where .exe is located
        * Edit .env file and copy-paste variables below and replace their values with corresponding paths on your system:
        ```
        CSGO_PATH="C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo"
        UNRAR_PATH="C:\Program Files\WinRAR\UnRAR.exe"
        ```
        * Save the .env file and run the executable.
    
    - **Project tree example** 

        IDTCopy \
        ├── IDTCopy.exe \
        ├── .env 


## Screenshots
![alt text](<Screenshot 2024-10-25 012245-1.png>)
\
![alt text](<Screenshot 2024-10-25 215129.png>)
