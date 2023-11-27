// function summarize() {
//     const inputText = document.getElementById('inputText').value;

//     // You need to send this inputText to your server for summarization
//     // and update the #output element with the result.
//     // For simplicity, let's assume there's a fictional API endpoint.

//     // Replace 'YOUR_SUMMARIZATION_API_ENDPOINT' with your actual endpoint.
//     const apiUrl = 'YOUR_SUMMARIZATION_API_ENDPOINT';

//     fetch(apiUrl, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ text: inputText }),
//     })
//     .then(response => response.json())
//     .then(data => {
//         document.getElementById('output').innerText = data.summary;
//     })
//     .catch(error => {
//         console.error('Error:', error);
//     });
// }
// $.ajax({
//     url: '/submit_text', // replace with your Flask endpoint
//     type: 'GET', // or 'POST', depends on your needs
//     success: function(data) {
//         // 'data' is the response from your Flask server
//         // You can now use 'data' to update your webpage
//         console.log(data);
//     },
//     error: function(error) {
//         console.log(error);
//     }
// });
