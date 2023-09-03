const hideElems = (start, stop, currentSymbol) => {
    if (currentSymbol === 'Enter') {
        const br = document.getElementById(`br${stop - 1}`)
        br.style.display = 'none'
    }
    
    for (let i = start; i < stop; i ++) {
        const letter = document.getElementById(`letter${i}`)
        letter.style.display = 'none'
    }
}

export default hideElems