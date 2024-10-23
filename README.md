
# 🌐 **OminiQuery** - AI-Powered Data Query Interface

OminiQuery is a user-friendly interface designed to simplify data retrieval from SQL and NoSQL databases using natural language. Powered by cutting-edge AI, it makes database interactions as easy as having a conversation. Explore your data, generate insights, and visualize results with a few simple inputs! 🚀

## ✨ **Features**

### 🗨️ **Easy-to-use User Interface**
- Interact with the database using natural language, making data retrieval effortless.
- Simply type your query as if you're chatting, and let OminiQuery handle the rest.

### 🗄️ **Support for SQL & NoSQL Databases**
- Compatible with various database types, ensuring smooth integration with your systems.

### 📊 **Auto Graph Generation**
- Automatically create visual data representations like charts and graphs for better analysis and insights.

### 📝 **View and Modify Queries**
- Review and edit the generated data-fetching queries before or after execution for greater control.

### 📚 **Displays Schema Along with the Chat**
- Get a real-time view of the database schema within the chat interface, helping you understand the structure and context of the data.

## 🛠️ **Tech Stack**

### **Backend** 🖥️
- **Python**: The core programming language.
- **Django & Flask**: Web frameworks for server-side operations.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM).
- **FAISS**: Facebook AI Similarity Search for efficient schema storage.
- **Firebase**: For real-time data management.
- **LLM (GPT-3.5)**: Language model for generating SQL queries.

### **Frontend** 🌐
- **HTML/CSS**: For structuring and styling web pages.
- **JavaScript**: Handles client-side interactions.
- **ECharts**: For dynamic data visualization.
- **Markdown-it**: Parses and renders Markdown content.

## 🧩 **Functionalities**

### 📋 **Database Configuration and Schema Retrieval**
- Configure a MySQL database connection via form submission or JSON.
- Retrieve and cache the schema of connected databases.

### 💬 **Chat Interface**
- A web-based chat interface for interacting with the database.
- Submit messages to generate SQL queries and fetch results seamlessly.

### 📈 **Data Visualization**
- Generate and display charts based on SQL query results in the chat interface.

### 💾 **Long-term Memory Storage**
- Efficiently store and retrieve table schemas using FAISS.

## 📂 **Project Structure**

### **Backend** 🛡️
- **`app.py`**:
  - `handle_form`: Processes form and JSON data for database configuration.
  - `get_schema_user`: Retrieves and returns the database schema.
  - `chat_response`: Handles chat interactions and query generation.
- **`faissStore.py`**:
  - `FaissStore.write`: Stores table schemas using FAISS.

### **Frontend** 🎨
- **`static/chat-interface.js`**: Manages form submissions and redirections.
- **`static/chat.js`**: Handles chat interactions and visual data representation.
- **`templates/ai-chat.html`**: HTML template for the chat interface.

## 🏆 **Specialties**

- **Interactive Chat Interface**: Effortlessly interact with databases and visualize results.
- **Efficient Schema Storage**: Quick schema retrieval with FAISS.
- **Dynamic Visualization**: Automatically generate charts from SQL results.
- **Flexible Data Input**: Form-based or JSON-based database configurations.
- **Support for SQL databases**: Supports Natural language queries for SQL databases

## 📈 **Flow Chart**

![{F1EC981E-0FBA-4F01-863C-AB95C69ECDF0}](https://github.com/user-attachments/assets/383129d4-8067-48da-a23a-25b15a877246)


## 📸 **Screen Shots**

![Pasted image (4)](https://github.com/user-attachments/assets/b4dfe7d1-3cc8-4447-a4b3-a5fbb33fb46f)
![Pasted image (3)](https://github.com/user-attachments/assets/a2efc90d-be11-452c-885b-3ce70ae5b1b1)
![Pasted image (2)](https://github.com/user-attachments/assets/299b8d56-8040-4aa5-93bc-2630870f73cf)
![Pasted image](https://github.com/user-attachments/assets/0aeb3470-fd9b-4218-b2ef-378d6261d44e)
![Pasted image (5)](https://github.com/user-attachments/assets/548f3985-c2b4-4b1c-8e71-0bb09d13c007)



## 🌟 **Get Started**

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/OminiQuery.git
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Server**:
   ```bash
   python app.py
   ```
4. **Access the Interface**:
   - Open your browser and navigate to `http://localhost:5000`.

📅 Happy Data Querying!!
