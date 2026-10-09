Autonomous Texi Project

Self-driving taxi algorithm developed and tested in the Quanser Interactive Labs (QLabs) simulation.

SETUP:
    Prereqs
    -Registered in Quanser Portal
    -Have Python 3.13 installed

Linux (Ubuntu/Debian)

1. Install the Quanser Python API (system-wide, once)

    bash
    wget --no-cache https://repo.quanser.com/debian/release/config/configure_repo.sh
    chmod u+x configure_repo.sh
    ./configure_repo.sh
    rm -f ./configure_repo.sh
    sudo apt update
    sudo apt install python3-quanser-apis

    Also install QLabs itself from the Linux tab on Quanser’s Getting Started page. I couldn’t confirm those commands.

2. Make a projects folder, clone, and create the venv

    Note: Don't need to create the folder given here if there's a specific place you want to put it
    
    bash
    mkdir -p ~/Projects
    cd ~/Projects
    git clone https://github.com/cullenowens/Quanser-Autonomous-Driving-Project.git
    cd <repo-folder>
    python3 -m venv --system-site-packages .venv
    source .venv/bin/activate
    python -c "import quanser.common, quanser.communications; print('ok')"

    --system-site-packages is required here so the venv can see the apt-installed Quanser packages.

3. Install the QLabs libraries

    bash
    curl -L -o install.py https://raw.githubusercontent.com/quanser/Quanser_Interactive_Labs_Resources/main/install.py
    python install.py

    Now close the terminal and open a new one, so the environment variables load.

4. Install dependencies and test

    bash
    cd ~/Projects/<repo-folder>
    source .venv/bin/activate
    python -m pip install -r requirements.txt
    python scripts/test_connection.py

    Open QLabs and load a workspace before running the test.


Windows (PowerShell)

1. Install the Quanser software (manual installers, once)

    Download and run both from Quanser’s Getting Started page or the Portal, keeping the default options: Quanser SDK for Windows and Quanser Interactive Labs. Then open a new PowerShell window so it picks up the QSDK_DIR variable the SDK installer sets.

2. Make a projects folder, clone, create the venv, and install the wheels

    Note: Don't need to create the folder given here if there's a specific place you want to put it

    powershell
    mkdir -Force $HOME\Projects
    cd $HOME\Projects
    git clone https://github.com/cullenowens/Quanser-Autonomous-Driving-Project.git
    cd <repo-folder>
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    $wheels = Get-ChildItem (Join-Path $env:QSDK_DIR "python") -Filter *.whl | ForEach-Object FullName
    python -m pip install --upgrade pip
    python -m pip install --upgrade $wheels
    python -c "import quanser.common, quanser.communications; print('ok')"

    If PowerShell blocks the activate script, run Set-ExecutionPolicy -Scope CurrentUser RemoteSigned once and retry.

3. Install the QLabs libraries

    powershell
    curl.exe -L -o install.py https://raw.githubusercontent.com/quanser/Quanser_Interactive_Labs_Resources/main/install.py
    python install.py

    Now close PowerShell and open a new one. Restart Windows if the variables still don’t show up.

4. Install dependencies and test

    powershell
    cd $HOME\Projects\<repo-folder>
    .venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt
    python scripts/test_connection.py

    Open QLabs and load a workspace before running the test.

    On Windows, keep the projects folder under your user folder (like C:\Users\you\Projects), not Desktop or Documents. Those are often synced by OneDrive, which can choke on the thousands of files in a venv.

Following steps 1-4:
    Install dependencies:
        python -m pip install -r requirements.txt
    Test the connection
        Open QLabs, log in, and load a workspace first. The script connects to the running app, so it fails if QLabs isn't open.
        python scripts/test_connection.py
        You should see Connected to QLabs: True.
