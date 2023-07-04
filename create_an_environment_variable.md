# Create an environment variable for your API key
An environment variable is a variable that is set on your operating system, rather than within your application. It consists of a name and a value. We **strongly** recommend that you set the name of the variable name as `SIGTECH_API_KEY`. Setting this environment variable enables you to commit and share your code without the risk of exposing your API key.

## Windows
### Option 1: Set your environment variable via the command prompt
1. Open a command prompt window.
1. Run the following in the command prompt, replacing `<yourkey>` with your API key:
    ```
    setx SIGTECH_API_KEY “<yourkey>”
    ```
1. Close your command prompt window.
1. Open a new command prompt window and validate that the environment variable has been set by running the command:
    ```
    echo %SIGTECH_API_KEY%
    ```

### Option 2: Set your environment variable using the control panel
1. Select `Start` and then type "environment variable" into the search box.
1. Select `Edit environment variables for your account`.
1. Select `Environment Variables…`.
1. Select `New…` under your existing user variables.
1. Define your new variable:
    1. In `Variable name`, enter `SIGTECH_API_KEY`. 
    1. In `Variable value`, enter your API key.

## MacOS/Linux
### Option 1: Set your environment variable using zsh
1. Open a terminal window.
1. Run the following command in your terminal, replacing `yourkey` with your API key. 
    ```curl
    echo "export SIGTECH_API_KEY='yourkey'" >> ~/.zshrc
    ```
1.  Update the shell with the new variable by running the following command:
    ```curl
    source ~/.zshrc
    ``` 
1. Confirm that you have set your environment variable by running the following command. The value of your API key will be the resulting output.
    ```curl
    echo $SIGTECH_API_KEY
    ```

### Option 2: Set your environment variable using bash
Follow the directions above replacing `.zshrc` with `.bash_profile`.