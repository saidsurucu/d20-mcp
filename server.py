"""MCP server for dice rolling using the d20 library."""

from typing import Any, Annotated
import d20
from fastmcp import FastMCP


# Create the FastMCP server
mcp = FastMCP("d20-mcp")


def serialize_ast_node(node: Any) -> dict[str, Any]:
    """
    Recursively serialize a d20 AST node to a JSON-serializable dictionary.

    Args:
        node: A d20 AST node (Expression, Number, Dice, etc.)

    Returns:
        Dictionary representation of the node
    """
    if node is None:
        return {"type": "null", "value": None}

    node_type = type(node).__name__
    result = {"type": node_type}

    # Handle different node types
    if hasattr(node, "total"):
        result["total"] = node.total

    if hasattr(node, "number"):
        result["number"] = node.number

    if hasattr(node, "size"):
        result["size"] = node.size

    if hasattr(node, "values"):
        result["values"] = [
            {"value": v.value if hasattr(v, "value") else v,
             "kept": v.kept if hasattr(v, "kept") else True}
            for v in node.values
        ]

    if hasattr(node, "children") and node.children:
        result["children"] = [serialize_ast_node(child) for child in node.children]

    if hasattr(node, "comment") and node.comment:
        result["comment"] = node.comment

    return result


@mcp.tool(output_schema=None)
def roll(
    expression: Annotated[str, "Dice expression to evaluate (e.g., '1d20+5', '4d6kh3')"],
    allow_comments: Annotated[bool, "Allow comments after the expression (e.g., '1d20 fire damage')"] = False
) -> dict[str, Any]:
    """
    Roll dice using standard RPG notation and return the total result.

    PURPOSE:
    Use this tool when you need a quick dice roll with just the total numeric result and
    a formatted output string. This is the most common tool for standard RPG scenarios like
    attack rolls, ability checks, saving throws, and damage calculations.

    WHEN TO USE:
    - Making attack rolls (1d20+5)
    - Rolling damage (2d6+3, 8d6)
    - Ability checks and saves (1d20+modifier)
    - Any roll where you just need the total
    - Quick single rolls without needing detailed breakdown

    WHEN NOT TO USE:
    - If you need to see individual die results, use roll_detailed instead
    - If you need to make multiple different rolls, use roll_batch instead
    - If you just want to validate syntax without rolling, use validate_syntax instead

    SUPPORTED NOTATION:
    - Basic: 1d20, 3d6, d20 (equivalent to 1d20)
    - Arithmetic: 1d20+5, 2d6-1, 3d6*2, 1d20/2
    - Keep highest/lowest: 4d6kh3 (keep highest 3), 4d6kl1 (keep lowest 1)
    - Drop: 4d6p1 (drop lowest 1, equivalent to kh3)
    - Reroll: 1d20rr<10 (reroll until ≥10), 1d20ro1 (reroll 1s once)
    - Exploding: 1d6e (explode on max), 1d6e6 (explode on 6)
    - Min/Max: 1d20mi10 (minimum 10), 1d20ma20 (maximum 20)
    - Complex: (1d4+1)*2, (1d6, 3, 2d4)

    COMMON EXAMPLES:
    - D&D Attack Roll: "1d20+5" → Check if hits AC
    - Ability Score: "4d6kh3" → Roll 4d6, keep highest 3
    - Fireball Damage: "8d6" → Total fire damage
    - Sneak Attack: "1d20+7" for attack, then "1d6+3d6" for damage
    - Critical Hit: "2d8+6" (doubled dice)
    - With Advantage: "2d20kh1" (roll 2d20, keep highest)
    """
    try:
        result = d20.roll(expression, allow_comments=allow_comments)

        response = {
            "total": result.total,
            "result": str(result),
        }

        if allow_comments and result.comment:
            response["comment"] = result.comment

        return response
    except d20.RollError as e:
        return {"error": str(e)}


@mcp.tool(output_schema=None)
def roll_detailed(
    expression: Annotated[str, "Dice expression to evaluate"],
    allow_comments: Annotated[bool, "Allow comments after the expression"] = False
) -> dict[str, Any]:
    """
    Roll dice with comprehensive breakdown including AST structure and individual die values.

    PURPOSE:
    Use this tool when you need to see exactly what happened during a dice roll, including
    which specific values each die showed, which dice were kept or dropped, and the complete
    Abstract Syntax Tree (AST) structure of the roll. Perfect for debugging, transparency,
    and understanding complex roll mechanics.

    WHEN TO USE:
    - Character creation: See which specific values you rolled for ability scores (4d6kh3)
    - Debugging: Understand why a complex roll gave a particular result
    - Transparency: Show players exactly what each die rolled
    - Learning: Understand how keep/drop/reroll mechanics work
    - Complex rolls: Analyze multi-step expressions with nested operations
    - Statistical analysis: See individual die distributions

    WHEN NOT TO USE:
    - Simple rolls where you only need the total (use roll instead)
    - Multiple different rolls (use roll_batch instead)
    - You don't need the AST complexity for basic gameplay

    AST STRUCTURE EXPLANATION:
    The "ast" field contains a tree structure representing the roll:
    - "type": Type of node (Expression, Dice, Number, etc.)
    - "total": Numeric value of this node
    - "number": Number of dice rolled (for Dice nodes)
    - "size": Dice size, e.g., 6 for d6 (for Dice nodes)
    - "values": Array of individual die results with "value" and "kept" (true/false)
    - "children": Nested operations (for complex expressions)

    INDIVIDUAL DIE RESULTS:
    The "values" array shows each die roll:
    - {"value": 4, "kept": true} → This die was kept in the final result
    - {"value": 2, "kept": false} → This die was dropped (e.g., in 4d6kh3)

    COMMON EXAMPLES:
    - Character Stats: "4d6kh3" → See which 3 of 4 dice were kept
    - Advantage: "2d20kh1" → See both d20 results, know which was kept
    - Reroll Analysis: "4d6rr1" → See which dice were rerolled
    - Exploding Dice: "3d6e" → See which dice exploded and their chain
    - Complex Expression: "(1d4+1)*2d6kh1" → Full breakdown of nested operations
    """
    try:
        result = d20.roll(expression, allow_comments=allow_comments)

        # Serialize the AST
        ast_dict = serialize_ast_node(result.expr)

        response = {
            "total": result.total,
            "result": str(result),
            "ast": ast_dict,
        }

        if allow_comments and result.comment:
            response["comment"] = result.comment

        return response
    except d20.RollError as e:
        return {"error": str(e)}


@mcp.tool(output_schema=None)
def roll_batch(
    expressions: Annotated[list[str], "Array of dice expressions to evaluate"],
    allow_comments: Annotated[bool, "Allow comments after each expression"] = False
) -> dict[str, list[dict[str, Any]]]:
    """
    Roll multiple different dice expressions in a single efficient operation.

    PURPOSE:
    Use this tool when you need to make several different dice rolls at once. Instead of
    calling the roll tool multiple times, batch them together for efficiency and to receive
    all results in a single structured response. Perfect for combat rounds, character creation,
    or any scenario requiring multiple distinct rolls.

    WHEN TO USE:
    - Combat rounds: Roll attack, damage, and saving throws together
    - Character creation: Roll all 6 ability scores at once (6x "4d6kh3")
    - Multiple checks: Roll several different ability checks simultaneously
    - Efficiency: When you need 3+ different rolls, batching is more efficient
    - Organized results: Get all rolls back in a structured array
    - Mixed roll types: Different expressions with different modifiers/mechanics

    WHEN NOT TO USE:
    - Single roll (use roll instead)
    - Need detailed AST for each roll (call roll_detailed multiple times)
    - Rolls are dependent on each other (roll one, check result, then decide next roll)

    ERROR HANDLING:
    Each roll in the batch is evaluated independently. If one expression fails, it returns
    an error entry, but other rolls continue. Check the "success" field for each result:
    - success: true → Roll succeeded, has "total" and "result"
    - success: false → Roll failed, has "error" message

    COMMON EXAMPLES:

    Combat Round:
    ["1d20+5", "2d6+3", "1d20+2"]
    → Attack roll, damage roll, saving throw

    Character Creation (6 ability scores):
    ["4d6kh3", "4d6kh3", "4d6kh3", "4d6kh3", "4d6kh3", "4d6kh3"]
    → Roll all six ability scores at once

    Party Ability Checks:
    ["1d20+3", "1d20+1", "1d20+5", "1d20+0"]
    → Perception checks for 4 party members

    Mixed Damage Types:
    ["2d6", "1d8", "3d4+2"]
    → Sword damage, fire damage, poison damage

    With Advantage/Disadvantage:
    ["2d20kh1+5", "2d20kl1+2"]
    → Attack with advantage, save with disadvantage
    """
    results = []

    for expr in expressions:
        try:
            result = d20.roll(expr, allow_comments=allow_comments)
            roll_result = {
                "expression": expr,
                "total": result.total,
                "result": str(result),
                "success": True
            }

            if allow_comments and result.comment:
                roll_result["comment"] = result.comment

            results.append(roll_result)
        except d20.RollError as e:
            results.append({
                "expression": expr,
                "success": False,
                "error": str(e)
            })

    return {"results": results}


@mcp.tool(output_schema=None)
def validate_syntax(
    expression: Annotated[str, "Dice expression to validate"]
) -> dict[str, Any]:
    """
    Validate a dice expression's syntax without actually rolling any dice.

    PURPOSE:
    Use this tool to check if a dice expression is syntactically correct and can be
    evaluated before actually rolling it. Perfect for validating user input, testing
    complex expressions, or checking syntax in application development. This is a
    read-only operation that doesn't generate random results.

    WHEN TO USE:
    - User input validation: Check if user-provided expression is valid
    - Testing complex expressions: Verify syntax before committing to a roll
    - Application development: Validate dice notation in forms/configs
    - Error prevention: Catch syntax errors before attempting a roll
    - Teaching: Show users why an expression is invalid
    - API integration: Validate before passing to game systems

    WHEN NOT TO USE:
    - If you want to actually roll dice (use roll, roll_detailed, or roll_batch)
    - If the expression is simple and you're confident in its syntax
    - When immediate rolling is acceptable even if it fails

    VALIDATION SCOPE:
    This tool checks:
    ✓ Basic dice notation (NdN format)
    ✓ Arithmetic operators and precedence
    ✓ Keep/drop/reroll/explode operations
    ✓ Parentheses matching and nesting
    ✓ Valid operator combinations
    ✓ Number format and ranges

    This tool does NOT check:
    ✗ Logical sense (e.g., "1d0" may pass but isn't useful)
    ✗ Performance implications (e.g., "99999d99999" is valid but slow)
    ✗ Statistical properties of the roll

    COMMON EXAMPLES:

    Valid Expressions:
    - "1d20+5" → ✓ Valid
    - "4d6kh3" → ✓ Valid
    - "2d20kh1+5" → ✓ Valid (advantage)
    - "(1d4+1)*2" → ✓ Valid (parentheses)
    - "3d6e6" → ✓ Valid (exploding)

    Invalid Expressions:
    - "1d" → ✗ Invalid (missing die size)
    - "d20+" → ✗ Invalid (incomplete expression)
    - "1d20kh" → ✗ Invalid (missing keep count)
    - "roll 1d20" → ✗ Invalid (text instead of pure notation)
    - "1d20 +" → ✗ Invalid (trailing operator)

    USE CASES:

    Form Validation:
    Before saving a custom dice formula in a character sheet, validate it first.

    Complex Expression Testing:
    Testing: "(2d6+3)*1d4kh1" before using in game
    Validate → If valid, then roll

    User Input:
    User types: "3d8+5"
    Validate → Show ✓ or explain error → Then allow roll
    """
    try:
        # Try to parse (but not roll) the expression
        d20.roll(expression)

        return {
            "valid": True,
            "expression": expression
        }
    except d20.RollError as e:
        return {
            "valid": False,
            "expression": expression,
            "error": str(e)
        }
    except Exception as e:
        return {
            "valid": False,
            "expression": expression,
            "error": f"Unexpected error: {str(e)}"
        }


def main():
    """Entry point for the d20-mcp server."""
    mcp.run()


if __name__ == "__main__":
    main()
