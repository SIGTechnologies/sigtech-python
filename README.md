![SigTech SDK Banner](https://sigtech.com/wp-content/uploads/2023/08/Python-SDK_github_856x268-1.png "SigTech SDK Banner")

&nbsp;

<p align="center" id="dummy">
    <a href="https://api.sigtech.com/docs">
        <img src="https://img.shields.io/badge/Docs-API_REFERENCE-1338be?&style=for-the-badge&logo=wiki&link=https://api.sigtech.com/docs" alt="Docs" />
    </a>
     <a href="https://twitter.com/sigtech_ai/">
        <img src="https://img.shields.io/badge/follow-%40sigtech_ai-1DA1F2?logo=twitter&style=for-the-badge" />
    </a>
</p>

<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
![Stargazers][stars-shield]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

</div>

[contributors-shield]: https://img.shields.io/github/contributors/SIGTechnologies/sigtech-python.svg?style=for-the-badge
[contributors-url]: https://github.com/SIGTechnologies/sigtech-python/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/SIGTechnologies/sigtech-python.svg?style=for-the-badge
[forks-url]: https://github.com/SIGTechnologies/sigtech-python/network/members
[stars-shield]: https://img.shields.io/github/stars/SIGTechnologies/sigtech-python.svg?style=for-the-badge
[issues-shield]: https://img.shields.io/github/issues/SIGTechnologies/sigtech-python.svg?style=for-the-badge
[issues-url]: https://github.com/SIGTechnologies/sigtech-python/issues
[license-shield]: https://img.shields.io/github/license/SIGTechnologies/sigtech-python.svg?style=for-the-badge
[license-url]: https://github.com/SIGTechnologies/sigtech-python/blob/master/LICENSE

# SigTech Python SDK

The SigTech Python SDK is designed to simplify the usage of the SigTech API for backtesting investment strategies by providing a higher-level, object-oriented method of interfacing with our API. With this SDK, you can easily test and view the performance of historical strategies.

#### Key Features

- Provides a higher-level object-based interface for convenient interaction with the SigTech API.
- Simplifies the creation of advanced trading strategies by providing methods which simulate rolling future strategies, basket strategies, and more.
- Interfaces with SigTech's historical market data facilitating accurate backtesting. Explore the [SigTech API data catalog](https://github.com/SIGTechnologies/sigtech-python/blob/master/docs/data.md) to see the list of instruments available.

## Installation

```sh
pip install sigtech
```

### Requirements

- Python 3.6+

## Getting started

### Authentication

1. Generate an API key using our [dashboard](https://dashboard.sigtech.com/api-keys).
1. Secure your API key and save it as a global environment variable by following our instructions [here](https://github.com/SIGTechnologies/sigtech-python/blob/master/docs/auth.md).

### Creating your first strategy

Our SDK provides convenient wrappers for boilerplate functions that are required to interact with our API. Copy the following code into your IDE and run it to quickly create, backtest, and view the performance of a custom rolling futures strategy.

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
    front_offset="-6,-5",
)

# Retrieve the strategy history
print(es_future.history())
```

## Next steps

1. Follow some of our [examples](https://github.com/SIGTechnologies/sigtech-python/tree/master/examples) to see how you can replicate and backtest more complex, real-world trading strategies.
1. Explore the full range of available instruments in the [API data catalog](https://github.com/SIGTechnologies/sigtech-python/blob/master/docs/data.md).
1. Explore the full range of endpoints in the [API reference](https://api.sigtech.com/docs). 




## Google Colab

We understand that getting started with backtesting and evaluating trading strategies can be a daunting task, especially for users new to financial data analysis and Python development. To make the process as seamless as possible, we've prepared a collection of real-world [examples](https://github.com/SIGTechnologies/sigtech-python/tree/master/examples) in Jupyter Notebook format (`.ipynb`). All you need to follow along is a SigTech API key.

## Logging

Logs down to the `debug` log level are available for all API requests. They can be accessed using the Python `logging` library.

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

For more information, please refer to the `logging` library's [documentation](https://docs.python.org/3/library/logging.html).


## Contributing

We appreciate and encourage your contributions to the SigTech Python SDK! If you are enjoying the SDK, please show your support by starring this repository and sharing it on social media channels.

To contribute an example, provide feedback, report a bug or otherwise bring an issue to our attention regarding this project, please follow the steps outlined in the [Contribution guidelines](https://github.com/SIGTechnologies/sigtech-python/blob/master/CONTRIBUTING.md).

Please remember that all contributors are expected to behave appropriately and abide by our [Code of conduct](https://github.com/SIGTechnologies/sigtech-python/blob/master/CODE_OF_CONDUCT.md).

## Security issues

If you believe you have discovered a security vulnerability in our repository please report it to us immediately following the instructions [here](https://github.com/SIGTechnologies/sigtech-python/blob/master/SECURITY.md).

>**Attention!**\
>Do not publicly disclose the vulnerability in a Github Issue or on a public forum such as X/Twitter.

## Support

If you encounter any issues or have any questions regarding our API or SDK, 
you can reach out to us via email at [support@sigtech.com](mailto:support@sigtech.com).

## License

The SigTech Python SDK is released under the [MIT License](https://github.com/SIGTechnologies/sigtech-python/blob/master/LICENSE).
