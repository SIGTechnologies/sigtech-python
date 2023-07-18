![SigTech SDK Banner](https://8647283.fs1.hubspotusercontent-na1.net/hubfs/8647283/Python%20SDK_github_856x268-1.png "SigTech SDK Banner")

&nbsp;

<p align="center" id="dummy">
    <a href="https://discord.gg/XcVJDYV4k7">
        <img src="https://img.shields.io/badge/CHAT-DISCORD-blue?style=for-the-badge&logo=discord&labelColor=rgb(55,55,55)&color=blueviolet">
    </a>
    <a href="https://learn.sigtech.com/reference/">
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
[license-url]: https://github.com/SIGTechnologies/sigtech-python/blob/master/LICENSE
[repo_wiki_url]: https://www.learn.sigtech.com
[repo_wiki_img]: https://img.shields.io/badge/docs-wiki_page-blue?style=for-the-badge&logo=none


# SigTech Python SDK
The SigTech Python SDK is designed to simplify the usage of the SigTech API for backtesting investment strategies by providing a higher-level, object-oriented method of interfacing with our API. With this SDK, you can easily test and view the performance of historical strategies.

#### Key Features
- Provides a higher-level object-based interface for convenient interaction with the SigTech API.
- Simplifies the creation of advanced trading strategies by providing methods which simulate rolling future strategies, basket strategies, and more.
- Interfaces with SigTech's collection of historical performance data facilitating accurate backtesting. Explore the [SigTech API data catalog](https://sigtechapi.streamlit.app/) to see the library of instruments available.


## Installation

```sh 
pip install sigtech
```

### Requirements
- Python 3.6+

## Getting started with SigTech Python SDK
### Authentication
>Note! \
>We are currently performing closed beta testing. Sign up to our [waitlist](https://get.sigtech.com/join-the-api-waitlist) to be notified of the public release and for a chance to use all API functionality for free as one of our beta users! When we're ready to welcome you, we'll send an email with instructions for creating your SigTech account.

1. Create a SigTech account following the instructions in your welcome email.
1. Generate an API key using our [dashboard](https://dashboard.sigtech.com/api). 
1. Secure your API key and save it as a global environment variable by following our instructions [here](https://learn.sigtech.com/docs/auth).

### Creating your first strategy
Our SDK provides convenient wrappers for boilerplate functions that are required to interact with our API. Copy the following code into your IDE and run it to quickly create, backtest and view the performance of a custom rolling futures strategy.

>**Note!**\
>The example below will only work if you have saved your API key as the global environment variable `SIGTECH_API_KEY`.

```python
# Import the SigTech API
import sigtech.api as sig

# Initialize your session
sig.init()

# Create a Rolling Future Strategy
es_future = sig.RollingFutureStrategy(
    currency="USD",
    start_date="2020-01-04",
    contract_code="ES", 
    contract_sector="INDEX",
    rolling_rule="front",  
    front_offset="-6:-4", 
)

# Retrieve the strategy history
print(es_future.history())
```
## Next steps
1. Learn more about the parameters used in the above strategy and how you can tailor them for you own use by reading the documentation for our [Rolling futures strategy](https://learn.sigtech.com/reference/api_post_strategy_rolling_futures_strategies_futures_rolling_post-1) endpoint.
1. See how our Python SDK can help you quickly create and backtest more complex, real-world trading strategies by folowing the detailed walkthroughs in the [Examples](https://github.com/SIGTechnologies/sigtech-python/tree/master/examples) folder.

>**Tip!**\
>If you require more low level access to the API, our SDK also offers a **Client based** method of interaction. See [Client based interaction](https://github.com/SIGTechnologies/sigtech-python/blob/master/docs/client_based_interaction.md) for more information.

## Logging
Logs down to the `debug` log level are available for all API requests. They can be accessed using the Python `logging` library. 
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```
For more information, please refer to the `logging` library's [documentation](https://docs.python.org/3/library/logging.html). See [Logging in Python](https://realpython.com/python-logging/) for a useful summary of the `logging` library's capabilities.

## API Documentation
For detailed information about the SigTech API, please refer to our official [API user guide](https://learn.sigtech.com/docs) and our interactive [API reference guide](https://learn.sigtech.com/reference). 


## Contributing to the SigTech Python SDK

We appreciate and encourage your contributions to the SigTech Python SDK! If you are enjoying the SDK, please show your support by starring this repository and sharing it on social media channels. 

To contribute an example, provide feedback, report a bug or otherwise bring an issue to our attention regarding this project, please follow the steps outlined in the [Contribution guidelines](https://github.com/SIGTechnologies/sigtech-python/blob/master/CONTRIBUTING.md). 

Please remember that all contributors are expected to behave appropriately and abide by our [Code of conduct](https://github.com/SIGTechnologies/sigtech-python/blob/master/CODE_OF_CONDUCT.md).

## Support
If you encounter any issues or have any questions regarding our API or SDK, you can reach out to us via our [Discord channel](https://discord.gg/XcVJDYV4k7) or [Twitter](https://twitter.com/sigtechltd/).

## License
The SigTech Python SDK is released under the [MIT License](https://github.com/SIGTechnologies/sigtech-python/blob/master/LICENSE).
