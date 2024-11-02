# A CS2 demo (.dem) file manager for vod watchers

## Core app functions:
1. Lets user extract the contents of a zipped file and copy them directly to csgo folder
2. Lets user rename the .dem files before exporting them.
3. Lets user delete .dem files from the csgo folder.

## Prerequisites:
Get [Winrar](https://www.win-rar.com/start.html?&L=0) 

## Installation:

- **Assuming you have Python and Git installed.**

    - ### Development
        - **Clone the repository**:
        ```bash
        git clone git@github.com:garrythewarlord/IDTCopy.git
        ```

        - **Create a virtual environment**:
            - Navigate to the project root:
            ```bash
            cd /path/to/project/root
            ```
            - Create the virtual environment:
            ```bash
            python3 -m venv venv
            ```

        - **Activate the virtual environment**:
            - **Windows**:
            ```bash
            venv\Scripts\activate
            ```
            - **Linux**:
            ```bash
            source venv/bin/activate
            ```

        - **Install dependencies**:
            * Navigate to the project root and run:
                ```bash
                pip install -r requirements.txt
                ```
        
        - **Replace .env variable paths**:
            * Navigate to .env file
            * Replace CSGO_PATH and UNRAR_PATH with values that point to csgo folder and unrar.exe on your system:
            ```
            CSGO_PATH="C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo"
            UNRAR_PATH="C:\Program Files\WinRAR\UnRAR.exe"
            ```


        - **Run the application**:
            * Open `app.py` in VS Code and run the Python file.


    - ### Executable
        - **Download the executable file**:
        [Link](https://www.test.com)

        - **Set up environmental variables**
            * Create a file extension .env inside the folder where .exe is located
            * Edit .env file and copy-paste variables below and replace their values with corresponding paths on your system:
            ```
            CSGO_PATH="C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo"
            UNRAR_PATH="C:\Program Files\WinRAR\UnRAR.exe"
            ```
            * Save the .env file and run the executable.


## Screenshots
![alt text](<Screenshot 2024-10-25 012245-1.png>)
\
![alt text](<Screenshot 2024-10-25 215129.png>)
