# Hardware Store AI Assistant

A conversational AI assistant for hardware stores that can search for products across multiple UK hardware retailers (DIY.com, Screwfix, Toolstation, and Wickes). The assistant helps customers find the right tools and equipment for their DIY projects by providing product recommendations, detailed information, and price comparisons.

## Features

- **Product Search**: Search for products across multiple hardware retailers (DIY.com, Screwfix, Toolstation, and Wickes)
- **Product Details**: Retrieve detailed product information including specifications, prices, and promotions
- **Conversational Interface**: AI assistant that understands customer requirements and provides tailored recommendations
- **Price Comparison**: Compare prices across different retailers to find the best deals

## Project Structure

```
├── LICENSE                 # Unlicense (public domain)
├── pyproject.toml          # Project metadata and dependencies
├── scrapy.cfg              # Scrapy configuration
├── scripts/                # Utility scripts
│   ├── deploy.sh           # Script to deploy the MCP application
│   ├── setup.sh            # Script to set up dependencies
│   └── start.sh            # Script to start the development server
├── app/                    # Main application source code
│   ├── crawlers/           # Web crawlers for different retailers
│   │   ├── diy_dot_com_crawler/
│   │   ├── screwfix_crawler/
│   │   ├── toolstation_crawler/
│   │   └── wickes_crawler/
│   ├── main.py             # Demo script and FastAPI entry point
│   ├── mcp_server.py       # MCP server definition
│   └── stdio.py            # MCP stdio interface
```

## Requirements

- Python 3.12 or higher
- uv (Python package manager)

## Dependencies

- mcp[cli] 1.9.1 - Framework for AI assistant functionality
- beautifulsoup4 4.13.4 - Library for web scraping and parsing HTML
- crawlee[cli,parsel] 0.6.9+ - Web crawling/scraping framework

## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:neviaumi/uk-hardware-store-mcp.git
   cd uk-hardware-store-mcp
   ```

2. Install dependencies using the setup script:
   ```bash
   bash ./scripts/setup.sh
   ```

## Usage

### Starting the Development Server

Run the development server:
```bash
bash ./scripts/start.sh
```

This will start the MCP development server, which provides a web interface for interacting with the AI assistant.

### Deploying the Application

To deploy the application:
```bash
bash ./scripts/deploy.sh
```

### Using the Demo Script

The project includes a demo script that shows how to use the crawlers directly:

```bash
uv run app/main.py
```

This will search for "M6 coach screw table leg" on DIY.com and print the details of the first product found.

## License

This project is released into the public domain under the Unlicense. See the [LICENSE](LICENSE) file for details.
