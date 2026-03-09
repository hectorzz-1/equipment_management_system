# ⚽ Match Control Bot (MCB)

Match Control Bot (MCB) is a **Python CLI application** designed to manage football players and their match statistics.
The system stores players in a database, updates their statistics automatically from match reports using an AI agent, and allows ranking players based on different performance metrics.

The project combines:

- Database management
- AI-powered match report interpretation
- Player statistics tracking
- CLI interaction

---

# 📦 Features

### 1️⃣ Register Players

Add new players to the database with:

- Name
- Last name
- Shirt number

When a player is created, their statistics are automatically initialized with zero values.

---

### 2️⃣ Player Ranking

Generate rankings based on different statistical attributes.

Examples of attributes:

- goals
- assists
- matches
- minutes
- yellow_card
- red_card

The system sorts players based on the selected attribute.

---

### 3️⃣ AI Match Report Processing

The system integrates with **OpenAI** to process natural language match reports.

Example input:

```
Santiago Sanabria scored 2 goals and received a yellow card.
```

The AI agent:

1. Interprets the report
2. Extracts structured statistics
3. Updates the database automatically

---

### 4️⃣ Check Player Statistics

Display all players and their current statistics stored in the database.

Example output:

```
(PLAYER_ID) Santiago Sanabria - number:10
Statistics:
goals: 5
assists: 3
matches: 7
minutes: 540
yellow_card: 1
red_card: 0
```

---

# 🧠 AI Agent

The project includes an AI agent that converts **natural language match reports** into structured data.

The agent workflow:

1. User writes a match report
2. Report is sent to OpenAI
3. The agent validates and structures the data
4. Database statistics are updated

The AI configuration is stored in:

```
config_IA.json
```

---

# 🗄 Database Structure

The project manages two main tables:

### Players

| Field     | Description      |
| --------- | ---------------- |
| id        | Unique UUID      |
| name      | Player name      |
| last_name | Player last name |
| number    | Shirt number     |

---

### Statistics

| Field       | Description    |
| ----------- | -------------- |
| id_player   | Player UUID    |
| goals       | Goals scored   |
| assists     | Assists        |
| matches     | Matches played |
| minutes     | Minutes played |
| yellow_card | Yellow cards   |
| red_card    | Red cards      |

---

# 📂 Project Structure

```
project/
│
├── main.py
│
├── agent/
│   ├── initialize_IA.py
│   ├── actions_IA.py
│   └── valid_data_IA.py
│
├── db/
│   ├── initialize_db.py
│   ├── Table_players.py
│   ├── table_statistics.py
│   └── rankings.py
│
├── config_IA.json
├── .env
└── README.md
```

---

# ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/match-control-bot.git
cd match-control-bot
```

---

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Configure environment variables

Create a `.env` file in the root directory.

```
API_KEY_OPENAI=your_openai_api_key
```

---

# ▶️ Running the Project

Run the CLI application:

```bash
python main.py
```

You will see the following menu:

```
Actions:
register(1)
rank(2)
update(3)
check statistics(4)
```

---

# 🧪 Example Workflow

### Register a player

```
Action: 1
Player name: Santiago
Player last name: Sanabria
Number player: 10
```

---

### Process a match report

```
Action: 3

Please forward the report:
"Santiago Sanabria scored 2 goals and played 90 minutes"
```

The AI agent will extract the statistics and update the database.

---

# 🛠 Technologies Used

- **Python**
- **OpenAI API**
- **dotenv**
- **UUID**
- **JSON configuration**
- **Custom database abstraction layer**

---

# 🎯 Purpose of the Project

This project was built to explore:

- AI agents interacting with structured databases
- Natural language to structured data pipelines
- Python backend architecture
- Clean separation between database logic and AI logic

---
