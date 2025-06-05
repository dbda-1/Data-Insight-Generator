# Data Insight Generator

Data Insight Generator is a powerful and user-friendly web application designed to simplify the process of data analysis and visualization. Built with FastAPI and enhanced by Google Gemini’s advanced generative AI, this tool enables users—whether beginners or experts—to upload their structured data files, extract meaningful insights, and create dynamic visualizations effortlessly through natural language queries.

---

## Description

Analyzing data and generating insightful visualizations often requires coding expertise and manual effort. Data Insight Generator bridges this gap by combining robust backend data processing with cutting-edge AI-driven code generation. Users can upload files in popular formats like CSV, Excel, and structured TXT, which the system parses and converts into clean, analyzable datasets. By leveraging Google Gemini’s generative capabilities, the app transforms simple natural language instructions into executable Python plotting code—enabling fast, customizable, and accurate visualizations without needing to write code manually.

---

## Key Features

- **Multi-format File Upload & Parsing:** Seamlessly upload `.csv`, `.xls`, `.xlsx`, and structured `.txt` files. The system intelligently reads and extracts structured data, ready for analysis.

- **Automatic Data Structuring:** Text files with data are parsed to extract meaningful columns, enabling flexible data inputs beyond traditional tabular formats.

- **Interactive Data Preview:** View a snapshot of your uploaded data directly through the API to verify contents before generating visualizations.

- **Natural Language Plotting Queries:** Describe the type of chart or analysis you want in plain English (e.g., “Plot the monthly sales trend”) and get automated Python plotting code generated.

- **AI-Powered Python Code Generation:** Uses Google Gemini’s generative AI model to convert user queries into clean, ready-to-execute Python code for matplotlib/seaborn.

- **Dynamic Plot Rendering:** Execute the AI-generated code safely within the app and return the resulting visualization image for immediate user feedback.

- **Extensible & Modular:** Designed for easy addition of new data types, visualization styles, or AI models to accommodate evolving needs.

- **Robust Error Handling:** Captures and returns detailed error tracebacks if AI-generated code fails, helping users troubleshoot quickly.

- **Web-based UI with FastAPI & Jinja2:** A simple and clean front-end to upload files, enter queries, and view results, enhancing accessibility and usability.

---

## Additional Possible Features (for future releases)

- **Support for More File Formats:** PDF tables, JSON, XML, and database connections.

- **Advanced NLP Interpretation:** Better understanding of complex multi-step analysis requests.

- **Interactive Plot Customization:** Allow users to tweak plot styles, colors, and parameters dynamically.

- **User Authentication & Profiles:** Save past uploads and plots for registered users.

- **Export Options:** Download generated plots in various formats (PNG, SVG, PDF).

- **Integration with Dashboards:** Embed generated plots into interactive dashboards for reporting.

- **Cloud Storage Support:** Save uploaded files and results securely on cloud platforms.

---

## Why Use Data Insight Generator?

- **No Coding Required:** Generate complex plots using simple English instructions.

- **Faster Data Exploration:** Quickly visualize and understand datasets without manual scripting.

- **Leverages State-of-the-Art AI:** Google Gemini ensures the plotting code is relevant and efficient.

- **Flexible & Scalable:** Suitable for data analysts, researchers, students, and business users.

## Installation & Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/data-insight-generator.git
   cd data-insight-generator
