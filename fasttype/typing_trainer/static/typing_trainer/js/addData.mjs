// Определяем функцию которая принимает в качестве параметров url и данные которые необходимо обработать:
const postData = async (url = '', data = {}) => {
    // Формируем запрос
    const response = await fetch(url, {
      // Метод, если не указывать, будет использоваться GET
      method: 'POST',
     // Заголовок запроса
      headers: {
        'Content-Type': 'application/json',
        "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
      },
      // Данные
      body: JSON.stringify(data)
    });
    return response.json(); 
}

export default postData