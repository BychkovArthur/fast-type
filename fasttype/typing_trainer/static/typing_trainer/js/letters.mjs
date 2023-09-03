const letterECheck = (currentSymbol, correctSymbol) => {
    return (currentSymbol === 'е' && correctSymbol === 'ё') || (currentSymbol === 'ё' && correctSymbol === 'е') ||
    (currentSymbol === 'Е' && correctSymbol === 'Ё') || (currentSymbol === 'Ё' && correctSymbol === 'Е');
}

const CRLFChecker = (currentSymbol, correctSymbol) => {
    return currentSymbol === 'Enter' && correctSymbol.charCodeAt(0) === 10;
}

const additionalChecks = (currentSymbol, correctSymbol) => {
    return CRLFChecker(currentSymbol, correctSymbol) || letterECheck(currentSymbol, correctSymbol);
}

const tabCheck = (textToType, currentSymbol, currentIndex) => {
    if (
        currentSymbol === 'Tab' &&
        textToType[currentIndex] === ' ' &&
        textToType[currentIndex + 1] === ' ' &&
        textToType[currentIndex + 2] === ' ' &&
        textToType[currentIndex + 3] === ' '
    ) {
        return true
    }
}

const VALID_LETTERS_LIST = [' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '"', '\'', '/', '\\', '<',
    '>',
    '.',
    ',', '[', ']', '|', '{', '}', '#', '№', '@', '$', ';', '%', ':', '^', '&', '?', '*', '(', ')', '-', '_', '=',
    '+', 'й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х', 'ъ', 'э', 'ж', 'д', 'л', 'о', 'р', 'п', 'а', 'в',
    'ы', 'ф', 'я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю', 'Й', 'Ц', 'У', 'К', 'Е', 'Н', 'Г', 'Ш', 'Щ', 'З', 'Х',
    'Ъ', 'Э', 'Ж', 'Д', 'Л', 'О', 'Р', 'П', 'А', 'В', 'Ы', 'Ф', 'Я', 'Ч', 'С', 'М', 'И', 'Т', 'Ь', 'Б', 'Ю', 'q',
    'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'l', 'k', 'j', 'h', 'g', 'f', 'd', 's', 'a', 'z', 'x', 'c', 'v',
    'b', 'n', 'm', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'L', 'K', 'J', 'H', 'G', 'F', 'D', 'S', 'A',
    'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Backspace', 'ё', 'Ё', 'Enter', 'Tab',
    ]
const VALID_LETTERS = new Set()
VALID_LETTERS_LIST.forEach(elem => VALID_LETTERS.add(elem))



export { additionalChecks, tabCheck, VALID_LETTERS }