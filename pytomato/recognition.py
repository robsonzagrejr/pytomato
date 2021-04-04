"""Reconhecimento de Expressão

Recebe uma string e um dicionario, expressão e gramática,
do usuário e retorna se a expressão é válida ou não.
"S -> aS | aA \n A -> bA | b"
-> aab
"""
function isValidExpression(expression, dict, previousCharacter = null): boolean {
    if (isExpressionEmpty(expression, dict)) {
        return doesDictionaryAllowsEmptyExpression(dict);
    }

    if (expression.length == 1) {
        const possibleTerminalSymbolsList = getPossibleTerminalSymbols(dict);
        let isPreviousCharacterValid = false;
        let isCharacterValid = true;
        for (const possibleTerminalSymbols of possibleTerminalSymbolsList) { 
            const [possibleTerminalSymbol] = possibleTerminalSymbols;
            if (!previousCharacter) { // true
                if (character != possibleTerminalSymbol) { 
                    isCharacterValid = false;
                    continue;
                }

                return true
            }

            if (!isCharacterValid) {
                return false;
            }

            if (possibleTerminalSymbol == previousCharacter) {
                const [, targetCharacter] = possibleTerminalSymbols;
                return targetCharacter == character;
            }
        }

        return false;
    }

    const character = expression.shift() || null;
    if (!isValidExpression(character, dict, previousCharacter)) {
        return false;
    }

    return !character ? true : isValidExpression(expression, dict, previousCharacter);
}