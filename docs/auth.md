# Authentication

After creating your API key we recommend saving it as a
global environment variable.

This has the following benefits:

- Prevents unauthorized access to your API key. By saving it as an environment variable, you can keep it separate from your codebase, reducing the risk of accidental exposure or leakage.
- It allows you to easily switch between different API keys or update them without modifying your code.
- When using our Python SDK, the command `sig.init()` will enable you to create a session linked to your API key.

## Setting your API key as a global environment variable

### Windows

**Option 1**: Set your environment variable via the command prompt

1. Open a command prompt window.
1. Run the following in the command prompt, replacing <yourkey> with your API key:

   ```powershell
   setx SIGTECH_API_KEY '<yourkey>'
   ```

1. Close your command prompt window.
1. Open a new command prompt window and validate that the environment variable has been set by running the command:

    ```powershell
    echo %SIGTECH_API_KEY%
    ```
   
**Option 2**: Set your environment variable using the control panel

1. Select `Start` and then type "environment variable" into the search box.
1. Select `Edit environment variables for your account`.
1. Select `Environment Variables…`.
1. Select `New…` under your existing user variables.
1. Define your new variable:
   1. In `Variable name`, enter `SIGTECH_API_KEY`.
   1. In `Variable value`, enter your API key.

### MacOS/Linux

**Option 1**: Set your environment variable using `zsh`

1. Open a terminal window.
1. Run the following command in your terminal, replacing your key with your API key.
   ```sh
   echo "export SIGTECH_API_KEY='yourkey'" >> ~/.zshrc
   ```
1. Update the shell with the new variable by running the following command:
   ```sh
   source ~/.zshrc
   ```
1. Confirm that you have set your environment variable by running the following command. The value of your API key will be the resulting output.
   ```sh
   echo $SIGTECH_API_KEY
   ```

**Option 2**: Set your environment variable using `bash`

1. Follow the directions above replacing `.zshrc` with `.bash_profile`.

## Check that it works

Check that this environment variable is set correctly by running the following command in your terminal or command prompt:

```python
import sigtech.api as sig
sig.init()
```
