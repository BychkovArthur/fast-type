import hideElems from "./hideElems.mjs";
import switchTextToResult from "./switchWindows.mjs";
import postData from "./addData.mjs";
import {
    VALID_LETTERS,
    additionalChecks,
    tabCheck,
} from "./letters.mjs";
import {
    getWPM,
    updateTime
} from "./time.mjs";


const fontColor = `rgb(${document.getElementById("fontColor").textContent})`
const correctLetterColor = `rgb(${document.getElementById("correctLetterColor").textContent})`
const wrongLetterColor = `rgb(${document.getElementById("wrongLetterColor").textContent})`

let currentIndex = 0
let textToType = document.getElementById("text-to-type").textContent.replaceAll('\n', '\r\n');
let wordIndex = 0
let wrongLettersTyped = 0
const correctlyTypedSymbols = {
    count: 0
}

const currentWordParagraph = document.getElementById('current-word')
const correctlyTypedParagraph = document.getElementById('correctly-typed')
const percentDoneParagraph = document.getElementById('percent-done')
const timeParagraph = document.getElementById('time')
const WPMParagraph = document.getElementById('wpm')
const TEXT_LENGTH = textToType.length
let timeStart = 0;
let intervalIDTimer
let intervalIDWPM
let totalWrongLettersTyped = 0
let textComplete = 0


// Переменные для управлением количества отображаемых на экране строк
let previousStartYIndex = 0



const repeatCurrentText = () => {
    const textToTypeDiv = document.getElementById('text-to-type-div')
    const resultDiv = document.getElementById('result-div')
    textToTypeDiv.style.display = 'block'
    resultDiv.style.display = 'none'
    currentIndex = 0
    wordIndex = 0
    wrongLettersTyped = 0
    correctlyTypedSymbols.count = 0
    timeStart = 0
    totalWrongLettersTyped = 0
    textComplete = 0
    previousStartYIndex = 0
    currentWordParagraph.textContent = ''
    correctlyTypedParagraph.textContent = '0'
    percentDoneParagraph.textContent = '0'
    timeParagraph.textContent = '00:00'
    WPMParagraph.textContent = '0'

    const textLetters = document.getElementsByClassName('letter')
    const mainTextBrTags = document.querySelectorAll('.main-text>br')
    Array.from(textLetters).forEach( textLetter => {textLetter.style.cssText = ''})
    Array.from(mainTextBrTags).forEach( brTag => {brTag.style.cssText = ''})

}

const repeatCurrentTextButton = document.getElementById('repeat-current-text-button');
repeatCurrentTextButton.addEventListener('click', repeatCurrentText);


document.addEventListener("keyup", function (event) {
    // Текст успешно напечатан
    if (textComplete) {
        return
    }

    if (currentIndex === TEXT_LENGTH) {

        clearInterval(intervalIDWPM)
        clearInterval(intervalIDTimer)
        textComplete = 1

        switchTextToResult(timeStart, timeParagraph.textContent, correctlyTypedSymbols, totalWrongLettersTyped)

        const body = {
            'wpm': document.getElementById('result-td-wpm').textContent,
            'time': document.getElementById('result-td-time').textContent,
            'acc': document.getElementById('result-td-acc').textContent.slice(0, -1),
            'date': Date.now(),
            'author': document.getElementById('result-text-author').textContent,
            'text': document.getElementById('result-text').textContent,
            'category': document.getElementById('result-text-category').textContent,
        }
        const url = document.getElementById('add-stat-url').textContent

        postData(url, body)

        return
    }

    const currentSpanTag = document.getElementById(`letter${currentIndex}`)
    // Символ переноса коретки нужно скипать (у нее код 13, а так же, там пустой текст, т.к. я это заифал в шаблоне)
    if (currentSpanTag.textContent === '') {
        currentIndex++
        return
    }
});

// Отключаю навигацию по сайту, чтобы можно было печатать код
window.onkeydown = evt => {
    if (evt.key == 'Tab') {
        evt.preventDefault();
    }
}


document.addEventListener("keydown", function (event) {
    if (textComplete) {
        return
    }

    const currentSymbol = event.key
    const currentSpanTag = document.getElementById(`letter${currentIndex}`)
    const currentSpanColor = getComputedStyle(currentSpanTag).getPropertyValue("color")

    if ((!VALID_LETTERS.has(currentSymbol)) || (currentSymbol === 'Backspace' && currentIndex === wordIndex && currentSpanColor === fontColor)) {
        return
    }

    // Начало отсчета времени
    if (timeStart === 0) {
        timeStart = Date.now()
        intervalIDWPM = setInterval(getWPM, 500, timeStart, correctlyTypedSymbols, WPMParagraph)
        intervalIDTimer = setInterval(updateTime, 1000, timeStart, timeParagraph)
    }


    // Обработка стирания
    if (currentSymbol === 'Backspace') {
        currentWordParagraph.textContent = currentWordParagraph.textContent.slice(0, -1)

        if (wrongLettersTyped > 1) {
            wrongLettersTyped--
            return
        }

        if (currentSpanColor === fontColor) {

            currentIndex-- // Обновление индекса
            correctlyTypedSymbols.count-- // Обновление количества верно напечатанных, которые передаются КАК ССЫЛКА
            correctlyTypedParagraph.textContent = correctlyTypedSymbols.count // Обновление количества верно напечатаных
            percentDoneParagraph.textContent = (currentIndex / TEXT_LENGTH * 100).toFixed(2) // Обновление процента верно напечатаных


            const previousSpanTag = document.getElementById(`letter${currentIndex}`)
            previousSpanTag.style.cssText = `
                color: ${fontColor};
            `
        } else if (currentSpanColor === wrongLetterColor) {
            currentSpanTag.style.cssText = `
                color: ${fontColor};
            `
        }
        // Обработка ввода
    } else {

        // Замена пробела и переноса строки на более заментый символ
        if (currentSymbol === ' ') {
            currentWordParagraph.textContent += '·'
        } else if (currentSymbol === 'Enter') {
            currentWordParagraph.textContent += '↵'
        } else if (currentSymbol === 'Tab') {
            currentWordParagraph.textContent += '····'
        } else {
            currentWordParagraph.textContent += currentSymbol
        }

        const tabFlag = tabCheck(textToType, currentSymbol, currentIndex)

        if (currentSpanColor === fontColor) {

            if (currentSymbol === textToType[currentIndex] || additionalChecks(currentSymbol, textToType[currentIndex]) || tabFlag) {
                currentSpanTag.style.cssText = `
                    color: ${correctLetterColor};
                `

                // Каждый пробел таба я считаю за один символ. Т.е. весь таб = 4 символа, которые идут в общую статистику и WPM
                if (tabFlag) {
                    for (let i = 0; i < 3; i++) {
                        currentIndex++
                        correctlyTypedSymbols.count++
                        const currentSpanTag = document.getElementById(`letter${currentIndex}`)
                        currentSpanTag.style.cssText = `
                            color: ${correctLetterColor};
                        `
                    }
                }
                const yCoordBefore = document.getElementById(`letter${currentIndex}`).getBoundingClientRect().y // Запоминаем координату по y предыдущей буквы. Если у следующей буквы другая координата - надо стирать строку
                currentIndex++ // Обновление индекса
                correctlyTypedSymbols.count++ // Обновление количества верно напечатанных, которые передаются КАК ССЫЛКА
                correctlyTypedParagraph.textContent = correctlyTypedSymbols.count // Обновление количества верно напечатаных
                percentDoneParagraph.textContent = (currentIndex / TEXT_LENGTH * 100).toFixed(2) // Обновление процента верно напечатаных


                // Если текущий символ пробел, значит следующий символ - новое слово.
                // Обновляем индекс первой буквы нового слова, чтобы нельзя было стирать то, что ранее текущего слово (все до текущего слова - верный текст)
                // Так же, мне нужно обновить слово, которое отображается пользователю
                // Так же, здесь нужно обновлять перенос строки
                if (currentSymbol === ' ' || currentSymbol === 'Enter' || currentSymbol === 'Tab') {
                    wordIndex = currentIndex
                    currentWordParagraph.textContent = ''

                    const yCoordAfter = document.getElementById(`letter${currentIndex}`).getBoundingClientRect().y

                    if (yCoordBefore !== yCoordAfter) {
                        hideElems(previousStartYIndex, currentIndex, currentSymbol)
                        previousStartYIndex = currentIndex
                    }
                }
                // Если пользователь ошибся, перекрашиваем букву, заводим счетчик неправильных букв
            } else {
                currentSpanTag.style.cssText = `
                    color: ${wrongLetterColor};
                `
                wrongLettersTyped = 1
                if (currentSymbol === 'Tab') {
                    wrongLettersTyped = 4
                }
                console.log(wrongLettersTyped)
                totalWrongLettersTyped++
            }
            // Когда мы ввели вторую и более неправильную букву, увеличиваем счетчик (это происходит тогда, когда текущая буква красная)
        } else if (currentSpanColor === wrongLetterColor) {

            wrongLettersTyped++

            if (currentSymbol === 'Tab') {
                wrongLettersTyped += 3
            }
        }
    }
});