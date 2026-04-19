
![Test Output](https://github.com/cbonoz/kalshi-skill/blob/main/images/test_output.png)
## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the software.
kalshi-skill

# Kalshi Skill: Automated Market Analysis & Account Management

This project provides a Python-based skill for programmatically interacting with Kalshi prediction markets. It enables:

- Automated retrieval and analysis of Kalshi market data (including Bitcoin, S&P 500, and more)
- Portfolio and order management via the Kalshi API
- Custom business logic for identifying trading opportunities and market inefficiencies
- Integration with Openclaw for skill registration and orchestration

With this skill, users can build automated trading strategies, monitor market conditions, and manage their Kalshi accounts directly from code.
Openclaw Kalshi skill for programatically pulling markets and managing your account provided a read/write key.

This project uses <a href="https://docs.astral.sh/uv/">uv</a> for dependency management and runtime.


### Setup

.env
```
KALSHI_API_KEY_ID= # ex: api key id string
KALSHI_PRIVATE_KEY_PATH= # ex: personal.key (text file)
```

uv sync

uv run

### Registering with Openclaw

Prompt: `Can we register the skill kalshi-skill

### Additional links

pykalshi docs: https://github.com/ArshKA/pykalshi?tab=readme-ov-file#pykalshi
kalshi api docs: https://docs.kalshi.com/welcome


