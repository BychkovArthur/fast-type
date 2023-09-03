import { getWPM } from "./time.mjs"
const switchTextToResult = (timeStart, timeTotal, correctlyTypedSymbols, wrongSymbolsTyped) => {
    const textToTypeDiv = document.getElementById('text-to-type-div')
    const resultDiv = document.getElementById('result-div')
    const resultTdWPM = document.getElementById('result-td-wpm')
    const resultTdTime = document.getElementById('result-td-time')
    const resultTdAcc = document.getElementById('result-td-acc')
    const resultTdMiss = document.getElementById('result-td-miss')

    textToTypeDiv.style.display = 'none'
    resultDiv.style.display = 'block'

    getWPM(timeStart, correctlyTypedSymbols, resultTdWPM)
    resultTdTime.textContent = timeTotal
    if ((1 - (wrongSymbolsTyped / correctlyTypedSymbols.count)) * 100 < 0) {
        resultTdAcc.textContent = '0%'
    } else {
        resultTdAcc.textContent = new String(((1 - (wrongSymbolsTyped / correctlyTypedSymbols.count)) * 100).toFixed(2)) + '%'
    }
    resultTdMiss.textContent = wrongSymbolsTyped
}

export default switchTextToResult