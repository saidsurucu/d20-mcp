# 🎲 d20-mcp

> 🇹🇷 [Türkçe README için tıklayın / Click here for Turkish README](README.tr.md)

A powerful MCP (Model Context Protocol) server for dice rolling in RPG games. Built with [FastMCP](https://github.com/jlowin/fastmcp) and the [d20 library](https://github.com/avrae/d20), this server brings comprehensive dice mechanics to Claude and other MCP clients.

Perfect for D&D, Pathfinder, and any tabletop RPG that uses standard dice notation!

## ✨ Features

- **🎯 Simple Rolls**: Quick `1d20+5` expressions with instant results
- **📊 Detailed Analysis**: See every die roll with AST breakdown
- **⚡ Batch Rolling**: Roll multiple expressions efficiently
- **✅ Syntax Validation**: Check expressions before rolling
- **🎮 Advanced Mechanics**: Keep/drop, reroll, exploding dice, and more
- **🤖 LLM-Optimized**: Comprehensive tool descriptions for AI understanding

## 🚀 Quick Start

### Installation

The easiest way to use d20-mcp with Claude Desktop:

```bash
uvx --from git+https://github.com/saidsurucu/d20-mcp d20-mcp
```

### Claude Desktop Configuration

Add this to your `claude_desktop_config.json`:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "d20-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/saidsurucu/d20-mcp",
        "d20-mcp"
      ]
    }
  }
}
```

Restart Claude Desktop completely (Quit and reopen), then look for the 🔨 hammer icon!

## 🎮 Usage Examples

Once installed, try these prompts with Claude:

### Basic Rolling
```
Roll 1d20+5 for my attack
```

### Character Creation
```
Roll 6 sets of 4d6kh3 for ability scores
```

### Combat
```
Roll attack (1d20+7) and damage (2d8+4) for my greatsword
```

### With Advantage
```
Roll 2d20kh1+5 for my Perception check with advantage
```

### Complex Expressions
```
Roll (1d4+1)*2 for Magic Missile damage
```

## 🛠️ Available Tools

### `roll`
Quick dice rolls returning total and formatted result. Perfect for standard gameplay.

**Use for**: Attack rolls, ability checks, damage, saving throws

### `roll_detailed`
Comprehensive breakdown with AST structure showing individual die values and operations.

**Use for**: Character creation, debugging complex rolls, transparency

### `roll_batch`
Roll multiple different expressions in one operation.

**Use for**: Combat rounds, rolling all ability scores, party checks

### `validate_syntax`
Validate expressions without rolling (no randomness).

**Use for**: Testing complex expressions, user input validation

## 📝 Supported Dice Notation

### Basic
- `1d20` - Roll one 20-sided die
- `3d6` - Roll three 6-sided dice
- `d20` - Equivalent to 1d20

### Keep/Drop
- `4d6kh3` - Keep highest 3
- `4d6kl1` - Keep lowest 1
- `4d6p1` - Drop lowest 1

### Reroll
- `1d20rr<10` - Reroll until ≥10
- `1d20ro1` - Reroll 1s once

### Exploding Dice
- `1d6e` - Explode on max
- `1d6e6` - Explode on 6

### Min/Max
- `1d20mi10` - Minimum 10
- `1d20ma20` - Maximum 20

### Arithmetic
- `1d20+5` - Addition
- `2d6-1` - Subtraction
- `3d6*2` - Multiplication
- `(1d4+1)*2` - Parentheses

### Advanced
- `2d20kh1+5` - Advantage in D&D
- `2d20kl1+2` - Disadvantage
- `8d6 [fire]` - Annotated damage (with `allow_comments`)

## 🎯 Common RPG Use Cases

### D&D 5e Character Creation
```
Roll me 6 ability scores using 4d6 keep highest 3
```

### Attack with Advantage
```
I have advantage on this attack. Roll 2d20kh1+8
```

### Critical Hit
```
I crit! Roll 4d6+2d6+5 for my sneak attack damage
```

### Multiple Saves
```
Roll saves for 4 party members: 1d20+5, 1d20+2, 1d20+7, 1d20+3
```

## 🔧 Development

### Local Testing

```bash
# Clone the repository
git clone https://github.com/saidsurucu/d20-mcp.git
cd d20-mcp

# Run with uv
uv run server.py

# Or with Python directly (after installing dependencies)
python server.py
```

### Project Structure

```
d20-mcp/
├── server.py          # Main MCP server with 4 tools
├── pyproject.toml     # Project configuration
├── README.md          # English documentation
├── README.tr.md       # Turkish documentation
└── LICENSE            # MIT License
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Credits

Built with:
- **[d20](https://github.com/avrae/d20)** - Powerful dice rolling engine
- **[FastMCP](https://github.com/jlowin/fastmcp)** - FastMCP framework
- **[MCP](https://github.com/anthropics/mcp)** - Model Context Protocol

## 📚 Learn More

- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [FastMCP Documentation](https://gofastmcp.com)
- [d20 Library Documentation](https://github.com/avrae/d20)

---

Made with ❤️ for the TTRPG community
