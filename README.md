<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://8647283.fs1.hubspotusercontent-na1.net/hubfs/8647283/New%20SigTech%20Brand%20Assets/Logos%20and%20Favicons/st-logo-white-on-dark.png", style="margin-bottom:3cm">
  <img alt="Shows SigTech logo for light/dark mode." src="https://8647283.fs1.hubspotusercontent-na1.net/hubfs/8647283/New%20SigTech%20Brand%20Assets/Logos%20and%20Favicons/st-logo-black-on-white.png",style="margin-bottom:3cm">
</picture>

&nbsp;


<p align="center" id="dummy">
    <a href="https://discord.gg/XcVJDYV4k7">
        <img src="https://img.shields.io/badge/CHAT-DISCORD-blue?style=for-the-badge&logo=discord&labelColor=rgb(55,55,55)&color=blueviolet">
    </a>
    <a href="https://learn.sigtech.com">
        <img src="https://img.shields.io/badge/Docs-API_REFERENCE-1338be?&style=for-the-badge&logo=wiki&link=https://learn.sigtech.com/reference" alt="Docs" />
    </a>
     <a href="https://twitter.com/sigtechltd/">
        <img src="https://img.shields.io/badge/follow-%40sigtechltd-1DA1F2?logo=twitter&style=for-the-badge" />
    </a>
<p>
<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

</div>

[contributors-shield]: https://img.shields.io/github/contributors/SIGTechnologies/sigtech-python.svg?style=for-the-badge
[contributors-url]: https://github.com/SIGTechnologies/sigtech-python/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/SIGTechnologies/sigtech-python.svg?style=for-the-badge
[forks-url]: https://github.com/SIGTechnologies/sigtech-python/network/members
[stars-shield]: https://img.shields.io/github/stars/SIGTechnologies/sigtech-python.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/SIGTechnologies/sigtech-python
[issues-shield]: https://img.shields.io/github/issues/SIGTechnologies/sigtech-python.svg?style=for-the-badge
[issues-url]: https://github.com/SIGTechnologies/sigtech-python/issues
[license-shield]: https://img.shields.io/github/license/SIGTechnologies/sigtech-python.svg?style=for-the-badge
[license-url]: https://github.com/SIGTechnologies/sigtech-python/blob/master/LICENSE.txt
[repo_wiki_url]: https://www.learn.sigtech.com
[repo_wiki_img]: https://img.shields.io/badge/docs-wiki_page-blue?style=for-the-badge&logo=none


# SigTech Python SDK
The SigTech Python SDK is designed to simplify the usage of the SigTech API for backtesting investment strategies by providing a higher-level, object-oriented method of interfacing with the API. With this SDK, you can easily test and view the performance of historical strategies.

#### Key Features
- Provides a higher-level object-based interface for convenient interaction with the SigTech API.
- Simplifies the creation of advanced trading strategies by providing methods which simulate rolling future strategies, basket strategies, and more.
- Interfaces with SigTech's collection of historical performance data, enabling accurate backtesting and performance metrics for analysis and visualization.

## Installation
1. Clone the `sigtech-python` [repository](https://github.com/SIGTechnologies/sigtech-python).
1. Open a terminal window and change directory to the folder which contains the the cloned `sigtech-python` repository.
1. Run the following command in your terminal:
```sh
python setup.py install
```

### Requirements
-   Python 3.6+

## Authentication
1. Create a [SigTech API account](https://dashboard.sigtech.com).
1. Generate an API key using our [dashboard](https://dashboard.sigtech.com/api). 
1. Copy the API key.
1. Set the environment variable `'SIGTECH_API_KEY'` to your API key.
    - To set the environment variable globally for your operating system, you need to set it outside of the Python script using system-specific methods. See our detailed instructions (for both Windows and MacOS/Linux users) here - [Create an Environment Variable for your SigTech API key]((https://github.com/SIGTechnologies/sigtech-python/blob/master/CONTRIBUTION.md)).
    - To set the environment variable for a particular Python environment, use the following commands at the top of your python file:
        ```python
        import os
        os.environ['SIGTECH_API_KEY'] = <YOUR_API_KEY>
        ```


## Getting started
Our SDK provides convenient wrappers for boilerplate functions that are required to interact with our API. Copy the following code to quickly create, backtest and view the performance of a custom rolling futures strategy.

>**Tip!**\
>You must complete the `Authentication` steps before trying this. 

### Create a rolling futures strategy.
```python
# Import the SigTech API and datetime python libraries
import sigtech.api as sig
import datetime as dtm

# Initialize your session
sig.init()

# Create a Rolling Future Strategy
es_future = sig.RollingFutureStrategy(
    currency='USD',
    start_date=dtm.date(2020, 1, 4),
    contract_code='ES', 
    contract_sector='INDEX',
    rolling_rule='front',  
    front_offset='-6:-4', 
    )

# Retrieve the strategy history
print(es_future.history())
```
To learn more about the parameters used in the above strategy and how you can tailor them for you own use, please refer to [API Reference - Rolling futures strategy](https://learn.sigtech.com/reference/api_post_strategy_rolling_futures_strategies_futures_rolling_post-1.).

To see how SigTech Python SDK can help you quickly create and backtest more complex, real-world trading strategies refer to the [Examples](https://github.com/SIGTechnologies/sigtech-python/tree/master/examples) folder.

>**Tip!**\
>If you require more low level access to the API, our SDK also offers a **Client based** method of interaction. See [Client based interaction]() for more information.

## Logging
Logs down to the `debug` log level are available for all API requests. They can be accessed using the python `logging` library. 
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```
For more information, please refer to the `logging` library's [documentation](https://docs.python.org/3/library/logging.html). See [Logging in Python](https://realpython.com/python-logging/) for a useful summary of the `logging` library's capabilities.

## API Documentation
For detailed information about the SigTech API, including usage guidelines and a detailed API reference, please refer to our official [API user guide](https://learn.sigtech.com/docs) and [API reference guide](https://learn.sigtech.com/reference). 

If you have any questions or feedback regarding our documentation, please raise an issue on our [Documentation forum](https://learn.sigtech.com/discuss).

## Contributing to the SigTech Python SDK

We appreciate and encourage your contributions to the SigTech Python SDK! If you are enjoying the SDK, please show your support by starring this repository and sharing it on social media channels. 

To contribute an example, provide feedback, report a bug or otherwise bring an issue to our attention regarding this project, please follow the steps outlined in the [Contribution guidelines](https://github.com/SIGTechnologies/sigtech-python/blob/master/CONTRIBUTION.md). 

Please remember that all contributors are expected to behave appropriately and abide by our [Code of conduct](https://github.com/SIGTechnologies/sigtech-python/blob/master/CODE_OF_CONDUCT.md).

## Support
If you encounter any issues or have any questions regarding our API or SDK, you can reach out to us via our [Discord channel](https://discord.gg/XcVJDYV4k7).

## License
The SigTech Python SDK is released under the [MIT License](https://www.google.com).
