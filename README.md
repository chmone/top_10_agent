# Top 10 Agent 🏆

An intelligent AI agent system built with Google's ADK (Agent Development Kit) that searches for and evaluates the best products/services in any category, returning the top 5 recommendations with expert judgment and reasoning.

## 🎯 Overview

The Top 10 Agent aggregates expert opinions from multiple "top 10" lists across the web, analyzes consensus picks, and provides you with the ACTUAL top 5 products based on comprehensive research - not algorithmic scoring, but genuine expert evaluation.

## ✨ Features

- **Multi-Agent Architecture**: Orchestrator, Search Specialist, and Analyzer agents working together
- **Local Artifact Storage**: Saves search results and analyses locally for reuse
- **Session State Management**: Tracks searches, enforces limits, and maintains session context
- **Expert Consensus Analysis**: Identifies products that appear across multiple credible sources
- **Source Credibility Evaluation**: Weights recommendations by source quality (Tier 1/2/3)
- **Smart Search Limits**: Maximum 5 searches per session to ensure focused, quality results

## 🏗️ Architecture

### Agent System

```
┌─────────────────────────────────────┐
│       Top 10 Orchestrator           │
│   (Coordinates & Makes Judgments)   │
└────────────┬───────────┬────────────┘
             │           │
    ┌────────▼────┐ ┌───▼──────────┐
    │   Search    │ │   Analyzer   │
    │ Specialist  │ │    Agent     │
    └─────────────┘ └──────────────┘
```

- **Root Agent** (`agent.py`): Orchestrates the search, delegates to specialists, makes final top 5 selection
- **Search Agent** (`agents/search_agent.py`): Finds top 10 lists from credible review sites
- **Analyzer Agent** (`agents/analyzer_agent.py`): Deep analysis to identify consensus picks and evaluate sources

### State & Storage

- **Session Callbacks** (`callbacks.py`): Tracks search count, artifacts saved, session ID
- **Local Artifacts** (`tools/artifact_tools.py`): Saves research to `agent/artifacts/` folder
- **Memory System**: Uses ADK's memory tools for caching within sessions

## 📦 Installation

### Prerequisites

- Python 3.8+
- Google ADK
- API keys for Google services (set in `.env`)

### Setup

```bash
# Clone the repository
git clone https://github.com/chmone/top_10_agent.git
cd top_10_agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install google-adk
pip install python-dotenv

# Create .env file with your API keys
echo "GOOGLE_API_KEY=your_key_here" > .env
```

## 🚀 Usage

### Running the Agent

```bash
# Interactive chat interface
cd agent
adk chat agent.py

# Web interface
adk web
# Navigate to http://localhost:5000
```

### Example Queries

- "What are the best wireless headphones?"
- "Find me the top 5 budget laptops for students"
- "What are the best coffee makers under $200?"

### How It Works

1. **You ask** about a product category
2. **Agent checks** memory and artifacts for previous research
3. **Search specialist** finds top 10 lists from credible sources (max 5 searches)
4. **Analyzer** identifies consensus picks across multiple lists
5. **Orchestrator** makes expert judgment on the actual top 5
6. **Results saved** as artifacts for future reference

## 📁 Project Structure

```
top_10_agent/
├── agent/
│   ├── agent.py              # Root orchestrator agent
│   ├── callbacks.py          # Session state management
│   ├── agents/
│   │   ├── search_agent.py   # Search specialist
│   │   └── analyzer_agent.py # List analyzer
│   ├── tools/
│   │   └── artifact_tools.py # Local artifact storage
│   └── artifacts/            # Local storage (git-ignored)
├── docs/
│   └── implementation_plan.md # Original planning docs
├── repos/                    # Reference materials
└── CLAUDE.md                # AI assistant guidelines
```

## 🔧 Configuration

### Models Used
- **Orchestrator**: `gemini-2.0-flash-exp`
- **Search Agent**: `gemini-2.0-flash-exp`
- **Analyzer**: `gemini-2.0-flash-exp`

### Limits & Constraints
- **Max searches per session**: 5
- **Max results per search**: 10
- **Artifact storage**: Local JSON files in `agent/artifacts/`

## 🧠 Key Concepts

### Source Credibility Tiers

- **Tier 1** (Highest): Professional review sites with testing labs (Wirecutter, Consumer Reports, RTings)
- **Tier 2** (Good): Tech publications, established blogs with hands-on reviews
- **Tier 3** (Moderate): General blogs, affiliate sites without clear methodology

### Consensus Analysis

The agent identifies products that appear across multiple credible sources, weighing recommendations by:
- Source credibility
- Testing methodology
- Recency of reviews
- Consistency across sources

## 🛠️ Development

### Running Tests

```bash
# Interactive testing
adk web
```

## 🔍 Artifacts

Research data is saved locally in JSON format:

```json
{
  "category": "wireless headphones",
  "type": "search_results",
  "timestamp": "2024-01-15T10:30:00",
  "data": {
    // Search results or analysis data
  }
}
```

Artifacts are stored in `agent/artifacts/` and can be:
- `search_results`: Raw search data
- `analysis`: Processed consensus analysis
- `recommendations`: Final top 5 selections
